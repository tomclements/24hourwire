/* 24HourWire shared front-end JavaScript.
 * Loaded on every page via base.html. All interactivity is wired through
 * delegated click handling on [data-action] elements (no inline handlers).
 */
(function () {
    'use strict';

    function esc(value) {
        return String(value == null ? '' : value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function getCookie(name) {
        const parts = ('; ' + document.cookie).split('; ' + name + '=');
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function readUI() {
        const el = document.getElementById('ui-config');
        if (!el) return {};
        try { return JSON.parse(el.textContent || '{}'); } catch (e) { return {}; }
    }

    const UI = readUI();
    const LANG = document.documentElement.getAttribute('data-lang') || 'en';
    const CSRF_TOKEN = getCookie('csrftoken') || '';

    /* ---------- Theme ---------- */
    function toggleTheme() {
        const html = document.documentElement;
        const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        try { localStorage.setItem('theme', next); } catch (e) {}
        updateThemeIcon(next);
    }

    function updateThemeIcon(theme) {
        const btn = document.querySelector('.theme-toggle');
        if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
    }

    function loadTheme() {
        let saved = 'light';
        try { saved = localStorage.getItem('theme') || 'light'; } catch (e) {}
        document.documentElement.setAttribute('data-theme', saved);
        updateThemeIcon(saved);
    }

    /* ---------- Cookie banner ---------- */
    function acceptCookies() {
        document.cookie = 'cookie_consent=accepted; max-age=31536000; path=/';
        const banner = document.getElementById('cookie-banner');
        if (banner) banner.style.display = 'none';
    }

    if (!getCookie('cookie_consent')) {
        const banner = document.getElementById('cookie-banner');
        if (banner) banner.style.display = 'block';
    }

    /* ---------- Language selector ---------- */
    const langSelect = document.getElementById('lang-select');
    if (langSelect) {
        langSelect.addEventListener('change', function () {
            const url = new URL(window.location);
            url.searchParams.set('lang', this.value);
            window.location.href = url.toString();
        });
    }

    /* ---------- Ongoing Coverage / Most Covered collapse ---------- */
    function toggleCoverage(sectionId) {
        const section = document.getElementById(sectionId);
        if (!section) return;
        const row = section.querySelector('.coverage-row');
        const btn = section.querySelector('.coverage-toggle');
        if (!row || !btn) return;
        const isCollapsed = row.classList.contains('coverage-collapsed');
        row.classList.toggle('coverage-collapsed', !isCollapsed);
        btn.textContent = isCollapsed ? '−' : '+';
        btn.setAttribute('aria-label', isCollapsed ? 'Collapse coverage' : 'Expand coverage');
        btn.setAttribute('aria-expanded', isCollapsed ? 'true' : 'false');
    }

    /* ---------- Category tabs ---------- */
    function setTabState(catId) {
        document.querySelectorAll('.tab').forEach(tab => {
            const active = tab.getAttribute('href') === '#' + catId;
            tab.classList.toggle('active', active);
            tab.setAttribute('aria-selected', active ? 'true' : 'false');
        });
    }

    function showCategory(catId) {
        document.querySelectorAll('.category-section').forEach(el => { el.style.display = 'none'; });
        const section = document.getElementById(catId);
        if (section) section.style.display = 'block';
        setTabState(catId);
        document.querySelectorAll('.coverage-row').forEach(row => row.classList.add('coverage-collapsed'));
        document.querySelectorAll('.coverage-toggle').forEach(btn => {
            btn.textContent = '+';
            btn.setAttribute('aria-label', 'Expand coverage');
            btn.setAttribute('aria-expanded', 'false');
        });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    /* ---------- Scroll tabs / filters ---------- */
    function scrollTabs(direction) {
        const container = document.querySelectorAll('.tabs-container')[1];
        if (!container) return;
        container.scrollBy({ left: direction === 'left' ? -300 : 300, behavior: 'smooth' });
    }

    function scrollFilters(direction) {
        const container = document.querySelectorAll('.tabs-container')[0];
        if (!container) return;
        container.scrollBy({ left: direction === 'left' ? -200 : 200, behavior: 'smooth' });
    }

    /* ---------- Load more ---------- */
    function addArticleSchema(article, story) {
        const schema = {
            '@context': 'https://schema.org',
            '@type': 'NewsArticle',
            headline: story.title,
            description: story.excerpt || story.title,
            url: story.url,
            author: { '@type': 'Organization', name: story.source },
            publisher: { '@type': 'NewsMediaOrganization', name: '24HourWire', url: 'https://24hourwire.news' }
        };
        if (story.image_url) schema.image = { '@type': 'ImageObject', url: story.image_url };
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(schema);
        article.appendChild(script);
    }

    async function loadMore(btn, category) {
        const section = btn.closest('.category-section');
        const grid = section.querySelector('.stories-grid');
        const loaded = parseInt(grid.dataset.loaded || '0', 10);
        const params = new URLSearchParams(window.location.search);
        const language = params.get('lang') || LANG;
        const sources = params.get('sources') || '';

        btn.disabled = true;
        btn.textContent = 'Loading...';

        try {
            const response = await fetch('/api/stories/?lang=' + encodeURIComponent(language) + '&category=' + encodeURIComponent(category) + '&offset=' + loaded + '&sources=' + encodeURIComponent(sources));
            const data = await response.json();

            if (data.stories && data.stories.length > 0) {
                const fragment = document.createDocumentFragment();
                const shownAsins = new Set();
                grid.querySelectorAll('.book-card[data-book-asin]').forEach(card => {
                    shownAsins.add(card.dataset.bookAsin);
                });

                let bookForInsertion = null;
                if (data.books && data.books.length > 0) {
                    for (const book of data.books) {
                        if (!shownAsins.has(book.asin)) { bookForInsertion = book; break; }
                    }
                }

                let pollInserted = false;

                data.stories.forEach((story, index) => {
                    const globalStoryNum = loaded + index + 1;

                    if (globalStoryNum === 24 && bookForInsertion) {
                        fragment.appendChild(createBookCard(bookForInsertion));
                        shownAsins.add(bookForInsertion.asin);
                        bookForInsertion = null;
                    }

                    if (index === 1 && data.poll && !pollInserted) {
                        fragment.appendChild(createPollCard(data.poll));
                        pollInserted = true;
                    }

                    const article = document.createElement('article');
                    article.className = 'story-card';
                    article.setAttribute('data-title', story.title.toLowerCase());
                    article.setAttribute('data-source', story.source.toLowerCase());
                    article.innerHTML = `
                        <div class="story-header">
                            <a href="${esc(story.url)}" target="_blank" rel="noopener" class="story-title">${esc(story.title)}</a>
                        </div>
                        ${story.image_url ? `<a href="${esc(story.url)}" target="_blank" rel="noopener" class="story-image-link"><img src="${esc(story.image_url)}" alt="${esc(story.title)}" class="story-image" loading="lazy" onerror="this.style.display='none'"></a>` : ''}
                        <div class="story-meta">
                            <span class="source-tag">${esc(story.source)}${story.is_paywalled ? '<span class="paywall-badge" title="Paywalled">$</span>' : ''}</span>
                            ${story.covered_by_count ? `<span class="covered-badge">${esc(story.covered_by_count)} sources</span>` : ''}
                            <span class="bias-badge ${esc(story.bias_class || '')}">${esc(story.bias_label)}</span>
                            <span class="time-badge">${esc(story.time_ago)}</span>
                        </div>
                        ${story.excerpt ? `<p class="story-excerpt">${esc(story.excerpt)}</p>` : ''}
                        <div class="story-actions">
                            <div class="story-links">
                                <a href="${esc(story.url)}" target="_blank" rel="noopener">Read full story &rarr;</a>
                                <a href="https://www.bing.com/news/search?q=${encodeURIComponent(story.search_terms || '')}" target="_blank" rel="noopener">Find more coverage</a>
                                <button class="different-angle-btn" data-action="different-angle" data-id="${esc(story.id)}" data-title="${esc(story.title)}" data-source="${esc(story.source)}" data-bias="${esc(story.bias_label)}" title="Different perspectives">Different Angle</button>
                            </div>
                            <button class="share-btn" data-action="share" data-title="${esc(story.title)}" data-source="${esc(story.source)}" data-token="${esc(story.share_token || '')}" title="Share"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg></button>
                        </div>
                    `;
                    addArticleSchema(article, story);
                    fragment.appendChild(article);
                });

                grid.appendChild(fragment);
                grid.dataset.loaded = loaded + data.stories.length;

                const countEl = document.getElementById('count-' + category);
                if (countEl) countEl.textContent = data.total + ' stories';

                const tabCountEl = document.getElementById('tab-count-' + category);
                if (tabCountEl) {
                    tabCountEl.textContent = data.total;
                    tabCountEl.dataset.total = data.total;
                }

                if (data.has_more) {
                    btn.textContent = 'Load more stories (' + (loaded + data.stories.length) + ' of ' + data.total + ' shown)';
                    btn.disabled = false;
                } else {
                    btn.style.display = 'none';
                }
            } else {
                btn.style.display = 'none';
            }
        } catch (err) {
            console.error('Failed to load more stories:', err);
            btn.textContent = 'Error loading stories. Try again.';
            btn.disabled = false;
        }
    }

    function createBookCard(book) {
        const article = document.createElement('article');
        article.className = 'book-card';
        article.setAttribute('data-book-asin', book.asin);
        const coverHtml = book.image_url
            ? `<img src="${esc(book.image_url)}" alt="${esc(book.title)}" class="book-cover" loading="lazy" onerror="this.style.display='none'">`
            : `<div class="book-cover" style="display: flex; align-items: center; justify-content: center; background: #f3f4f6; color: #9ca3af; font-size: 2rem;">📚</div>`;
        article.innerHTML = `
            <span class="book-badge">Recommended Read</span>
            ${coverHtml}
            <h3 class="book-title">${esc(book.title)}</h3>
            <p class="book-author">by ${esc(book.author)}</p>
            ${book.description ? `<p class="book-description">${esc(book.description.substring(0, 140))}${book.description.length > 140 ? '...' : ''}</p>` : ''}
            <a href="${esc(book.amazon_url)}" target="_blank" rel="noopener" class="book-link" data-action="book-click" data-asin="${esc(book.asin)}">View on Amazon &rarr;</a>
        `;
        return article;
    }

    function createPollCard(poll) {
        const article = document.createElement('article');
        article.className = 'poll-card-inline';
        article.setAttribute('data-poll-id', poll.id);
        const optionsHtml = poll.options.map((opt, idx) =>
            `<button class="poll-option-btn-inline" data-action="vote-poll" data-poll-id="${esc(poll.id)}" data-option="${idx}">${esc(opt)}</button>`
        ).join('');
        article.innerHTML = `
            <span class="poll-badge-inline">${esc(poll.poll_type)}</span>
            <h3 class="poll-question-inline">${esc(poll.question)}</h3>
            <div class="poll-options-inline" id="poll-options-${poll.id}">
                ${optionsHtml}
                <button class="poll-option-btn-inline" data-action="poll-results" data-poll-id="${esc(poll.id)}" style="background: transparent; border-style: dashed;">View results</button>
            </div>
            <div class="poll-results-inline" id="poll-results-${poll.id}" style="display: none;"></div>
            <a href="/poll/${esc(poll.id)}/" class="poll-view-full">View full poll &rarr;</a>
            <button class="poll-option-btn-inline" data-action="share-poll" data-poll-id="${esc(poll.id)}" style="background: transparent; border-style: dashed; margin-top: 8px; font-size: 0.8rem;">Share poll</button>
        `;
        return article;
    }

    /* ---------- Search ---------- */
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function (e) {
            const query = e.target.value.toLowerCase();
            const visibleSection = document.querySelector('.category-section:not([style*="none"])');
            if (!visibleSection) return;
            visibleSection.querySelectorAll('.story-card').forEach(card => {
                const title = card.getAttribute('data-title') || '';
                const source = card.getAttribute('data-source') || '';
                card.style.display = (title.includes(query) || source.includes(query)) ? 'flex' : 'none';
            });
        });
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && this.value.trim().length >= 2) {
                window.location.href = '/search/?q=' + encodeURIComponent(this.value.trim()) + '&lang=' + encodeURIComponent(LANG);
            }
        });
    }

    /* ---------- Share ---------- */
    function shareStory(title, source, token) {
        const wireUrl = 'https://24hourwire.news/go/' + token + '/';
        const shareText = 'via @24HourWire\n\n' + title + '\n\nSource: ' + source;
        if (navigator.share) {
            navigator.share({ title: 'via @24HourWire', text: shareText, url: wireUrl })
                .catch(() => openShareOverlay(title, source, wireUrl));
        } else {
            openShareOverlay(title, source, wireUrl);
        }
    }

    function openShareOverlay(title, source, wireUrl) {
        if (document.getElementById('share-overlay')) return;
        const overlay = document.createElement('div');
        overlay.id = 'share-overlay';
        overlay.innerHTML = `
            <div class="share-overlay-backdrop" data-action="close-overlay"></div>
            <div class="share-overlay-content">
                <div class="share-overlay-header">
                    <h3>${esc(UI.share_story_title || 'Share this story')}</h3>
                    <button class="close-overlay" data-action="close-overlay" aria-label="Close">&times;</button>
                </div>
                <div class="share-overlay-preview">
                    <p class="share-preview-source" style="color: var(--accent); font-weight: 600; margin-bottom: 8px;">via @24HourWire</p>
                    <p class="share-preview-text">${esc(title)}</p>
                    <p class="share-preview-source">Source: ${esc(source)}</p>
                </div>
                <div class="share-overlay-buttons">
                    <button class="share-option twitter" data-action="share-twitter" data-title="${esc(title)}" data-url="${esc(wireUrl)}">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                        <span>${esc(UI.share_on_x || 'Share on X')}</span>
                    </button>
                    <button class="share-option facebook" data-action="share-facebook" data-url="${esc(wireUrl)}">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                        <span>${esc(UI.share_facebook || 'Share on Facebook')}</span>
                    </button>
                    <button class="share-option linkedin" data-action="share-linkedin" data-url="${esc(wireUrl)}">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                        <span>${esc(UI.share_linkedin || 'Share on LinkedIn')}</span>
                    </button>
                    <button class="share-option copy" data-action="copy-share" data-title="${esc(title)}" data-url="${esc(wireUrl)}" data-source="${esc(source)}">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        <span>${esc(UI.copy_link || 'Copy link')}</span>
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
        document.body.style.overflow = 'hidden';
    }

    function closeShareOverlay() {
        const overlay = document.getElementById('share-overlay');
        if (overlay) {
            overlay.remove();
            document.body.style.overflow = '';
        }
    }

    function shareToTwitter(title, wireUrl) {
        const text = 'via @24HourWire\n\n' + title + '\n\n' + wireUrl;
        window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(text), '_blank', 'width=600,height=400,noopener');
        closeShareOverlay();
    }

    function shareToFacebook(wireUrl) {
        window.open('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(wireUrl), '_blank', 'width=600,height=400,noopener');
        closeShareOverlay();
    }

    function shareToLinkedIn(wireUrl) {
        window.open('https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(wireUrl), '_blank', 'width=600,height=400,noopener');
        closeShareOverlay();
    }

    function copyShareLink(title, wireUrl, source) {
        const text = title + '\n' + wireUrl + '\n\nSource: ' + source + ' | Curated by @24HourWire';
        navigator.clipboard.writeText(text).then(() => {
            const btn = document.querySelector('.share-option.copy');
            if (btn) {
                btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg><span>' + esc(UI.copied || 'Copied!') + '</span>';
            }
            setTimeout(closeShareOverlay, 1000);
        });
    }

    function trackBookClick(asin) {
        if (navigator.sendBeacon) {
            navigator.sendBeacon('/analytics/book-click/', JSON.stringify({ asin: asin, timestamp: Date.now() }));
        }
    }

    /* ---------- Bias filters ---------- */
    let selectedBiases = new Set(['all']);

    function toggleBiasFilter(bias) {
        if (bias === 'all') {
            window.location.href = '?sources=all';
            return;
        }
        selectedBiases.delete('all');
        if (selectedBiases.has(bias)) {
            selectedBiases.delete(bias);
        } else {
            selectedBiases.add(bias);
        }
        if (selectedBiases.size === 0) {
            window.location.href = '?sources=all';
            return;
        }
        updateBiasButtons();
        window.location.href = '?sources=' + Array.from(selectedBiases).join(',');
    }

    function updateBiasButtons() {
        document.querySelectorAll('.bias-pill').forEach(pill => {
            const bias = pill.getAttribute('data-bias');
            const active = selectedBiases.has(bias);
            pill.classList.toggle('active', active);
            pill.setAttribute('aria-pressed', active ? 'true' : 'false');
        });
    }

    function initBiasFilters() {
        const params = new URLSearchParams(window.location.search);
        const sources = params.get('sources');
        if (sources && sources !== 'all') {
            selectedBiases.clear();
            sources.split(',').forEach(bias => selectedBiases.add(bias.trim()));
        }
        updateBiasButtons();
        const label = document.getElementById('active-filters');
        if (label) {
            const names = {
                'left': 'Left',
                'left-center': 'Left-Center',
                'center': 'Center',
                'right-center': 'Right-Center',
                'right': 'Right'
            };
            label.textContent = selectedBiases.has('all')
                ? 'All Sources'
                : Array.from(selectedBiases).map(b => names[b] || b).join(', ');
        }
    }

    /* ---------- Different Angle ---------- */
    let currentDifferentAngleId = null;
    let currentRequestTimestamp = null;

    function showDifferentAngle(storyId, storyTitle, storySource, storyBias) {
        const modal = document.getElementById('different-angle-modal');
        const loading = document.getElementById('different-angle-loading');
        const list = document.getElementById('different-angle-list');
        const title = document.getElementById('different-angle-original-title');
        const source = document.getElementById('different-angle-original-source');
        if (!modal || !loading || !list || !title || !source) {
            alert('Error: Modal elements not found. Please refresh the page.');
            return;
        }
        const requestTimestamp = Date.now();
        currentDifferentAngleId = storyId;
        currentRequestTimestamp = requestTimestamp;

        modal.classList.add('active');
        loading.style.display = 'block';
        list.style.display = 'none';
        list.innerHTML = '';

        title.textContent = storyTitle;
        source.textContent = storySource + ' (' + storyBias + ')';

        fetch('/different-angle/' + storyId + '/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (currentDifferentAngleId !== storyId || currentRequestTimestamp !== requestTimestamp) return;
                loading.style.display = 'none';
                list.style.display = 'block';
                if (data.error) {
                    list.innerHTML = '<div class="no-different-angle">' + esc(data.error) + '</div>';
                    return;
                }
                if (data.related_stories && data.related_stories.length > 0) {
                    data.related_stories.forEach(story => {
                        const item = document.createElement('div');
                        item.className = 'different-angle-item';
                        item.innerHTML = `
                            <a href="${esc(story.url)}" target="_blank" rel="noopener">${esc(story.title)}</a>
                            <div class="different-angle-meta">
                                <span class="source-tag">${esc(story.source)}${story.is_paywalled ? '<span class="paywall-badge">$</span>' : ''}</span>
                                <span class="bias-badge" style="background: ${esc(story.bias_color)}20; color: ${esc(story.bias_color)};">${esc(story.bias_label)}</span>
                            </div>
                            ${story.excerpt ? `<p class="different-angle-excerpt">${esc(story.excerpt)}</p>` : ''}
                        `;
                        list.appendChild(item);
                    });
                } else {
                    list.innerHTML = '<div class="no-different-angle"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg><p>' + esc(UI.no_related_stories || 'No related stories found') + '</p></div>';
                }
            })
            .catch(error => {
                if (currentDifferentAngleId !== storyId || currentRequestTimestamp !== requestTimestamp) return;
                loading.style.display = 'none';
                list.style.display = 'block';
                list.innerHTML = '<div class="no-different-angle">' + esc(UI.error_loading || 'Error loading stories') + '</div>';
                console.error('Error:', error);
            });
    }

    function closeDifferentAngle() {
        const modal = document.getElementById('different-angle-modal');
        if (modal) modal.classList.remove('active');
        currentDifferentAngleId = null;
    }

    /* ---------- Inline poll voting ---------- */
    function voteInlinePoll(pollId, optionIndex, btn) {
        const container = btn.closest('.poll-card-inline');
        const buttons = container.querySelectorAll('.poll-option-btn-inline');
        buttons.forEach(b => b.disabled = true);

        fetch('/poll/' + pollId + '/vote/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': CSRF_TOKEN,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'option=' + optionIndex
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                showInlineResults(container, data.results);
            } else {
                alert(data.error || 'Error voting');
                buttons.forEach(b => b.disabled = false);
            }
        })
        .catch(() => {
            alert('Error voting. Please try again.');
            buttons.forEach(b => b.disabled = false);
        });
    }

    function showInlineResults(container, results) {
        const optionsDiv = container.querySelector('.poll-options-inline');
        const resultsDiv = container.querySelector('.poll-results-inline');
        if (optionsDiv) optionsDiv.style.display = 'none';
        if (resultsDiv) {
            let html = '';
            results.forEach(r => {
                html += `
                    <div class="poll-result-row">
                        <div class="poll-result-label">
                            <span>${esc(r.option)}</span>
                            <span>${esc(r.percentage)}%</span>
                        </div>
                        <div class="poll-result-bar-bg">
                            <div class="poll-result-bar-fill" style="width: ${parseFloat(r.percentage) || 0}%;"></div>
                        </div>
                    </div>
                `;
            });
            html += '<button class="poll-option-btn-inline" data-action="poll-options" data-poll-id="' + esc(container.dataset.pollId) + '" style="background: transparent; border-style: dashed; margin-top: 8px;">Back to voting</button>';
            resultsDiv.innerHTML = html;
            resultsDiv.style.display = 'flex';
        }
    }

    function showInlineResultsForPoll(pollId) {
        const container = document.querySelector('.poll-card-inline[data-poll-id="' + pollId + '"]');
        if (!container) return;
        const optionsDiv = container.querySelector('.poll-options-inline');
        const resultsDiv = container.querySelector('.poll-results-inline');
        if (optionsDiv) optionsDiv.style.display = 'none';
        if (resultsDiv) resultsDiv.style.display = 'flex';
    }

    function showInlineOptionsForPoll(pollId) {
        const container = document.querySelector('.poll-card-inline[data-poll-id="' + pollId + '"]');
        if (!container) return;
        const optionsDiv = container.querySelector('.poll-options-inline');
        const resultsDiv = container.querySelector('.poll-results-inline');
        if (optionsDiv) optionsDiv.style.display = 'flex';
        if (resultsDiv) resultsDiv.style.display = 'none';
        container.querySelectorAll('.poll-option-btn-inline').forEach(b => b.disabled = false);
    }

    /* ---------- Delegated click handling ---------- */
    function titleFromCard(el) {
        const card = el.closest('.story-card, .most-covered-card');
        const t = card ? card.querySelector('.story-title') : null;
        return t ? t.textContent : '';
    }

    document.addEventListener('click', function (e) {
        const el = e.target.closest('[data-action]');
        if (!el) return;
        const action = el.getAttribute('data-action');
        switch (action) {
            case 'theme-toggle': toggleTheme(); break;
            case 'bias-filter': toggleBiasFilter(el.getAttribute('data-bias')); break;
            case 'scroll-filters': scrollFilters(el.getAttribute('data-dir')); break;
            case 'scroll-tabs': scrollTabs(el.getAttribute('data-dir')); break;
            case 'show-category':
                e.preventDefault();
                showCategory(el.getAttribute('data-category'));
                break;
            case 'toggle-coverage': toggleCoverage(el.getAttribute('data-target')); break;
            case 'different-angle':
                showDifferentAngle(
                    parseInt(el.getAttribute('data-id'), 10) || 0,
                    el.getAttribute('data-title') || titleFromCard(el),
                    el.getAttribute('data-source') || '',
                    el.getAttribute('data-bias') || ''
                );
                break;
            case 'share':
                shareStory(
                    el.getAttribute('data-title') || titleFromCard(el),
                    el.getAttribute('data-source') || '',
                    el.getAttribute('data-token') || ''
                );
                break;
            case 'book-click': trackBookClick(el.getAttribute('data-asin')); break;
            case 'load-more': loadMore(el, el.getAttribute('data-category')); break;
            case 'vote-poll':
                voteInlinePoll(
                    parseInt(el.getAttribute('data-poll-id'), 10) || 0,
                    parseInt(el.getAttribute('data-option'), 10) || 0,
                    el
                );
                break;
            case 'poll-results': showInlineResultsForPoll(el.getAttribute('data-poll-id')); break;
            case 'poll-options': showInlineOptionsForPoll(el.getAttribute('data-poll-id')); break;
            case 'share-poll': {
                const card = el.closest('.poll-card-inline');
                const q = card && card.querySelector('.poll-question-inline')
                    ? card.querySelector('.poll-question-inline').textContent
                    : '24HourWire Poll';
                openShareOverlay(q, '24HourWire Poll', 'https://24hourwire.news/poll/' + el.getAttribute('data-poll-id') + '/');
                break;
            }
            case 'accept-cookies': acceptCookies(); break;
            case 'close-different-angle': closeDifferentAngle(); break;
            case 'close-overlay': closeShareOverlay(); break;
            case 'share-twitter': shareToTwitter(el.getAttribute('data-title'), el.getAttribute('data-url')); break;
            case 'share-facebook': shareToFacebook(el.getAttribute('data-url')); break;
            case 'share-linkedin': shareToLinkedIn(el.getAttribute('data-url')); break;
            case 'copy-share': copyShareLink(el.getAttribute('data-title'), el.getAttribute('data-url'), el.getAttribute('data-source')); break;
        }
    });

    /* ---------- Init ---------- */
    document.querySelectorAll('.category-section').forEach(el => { el.style.display = 'none'; });
    document.querySelectorAll('.tab').forEach(el => { el.classList.remove('active'); el.setAttribute('aria-selected', 'false'); });
    const firstSection = document.querySelector('.category-section');
    const firstTab = document.querySelector('.tab');
    if (firstSection) firstSection.style.display = 'block';
    if (firstTab) { firstTab.classList.add('active'); firstTab.setAttribute('aria-selected', 'true'); }

    initBiasFilters();
    loadTheme();

    const modal = document.getElementById('different-angle-modal');
    if (modal) {
        modal.addEventListener('click', function (e) {
            if (e.target === this) closeDifferentAngle();
        });
    }
})();