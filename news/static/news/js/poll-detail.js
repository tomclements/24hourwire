(function () {
    'use strict';

    var cfg = {};
    try {
        var cfgEl = document.getElementById('poll-config');
        if (cfgEl) cfg = JSON.parse(cfgEl.textContent || '{}');
    } catch (e) {
        cfg = {};
    }

    var pollId = cfg.pollId;
    var pollQuestion = cfg.question || '';
    var csrfToken = cfg.csrfToken || '';

    function submitVote(optionIndex) {
        var buttons = document.querySelectorAll('.poll-option-btn');
        buttons.forEach(function (b) { b.disabled = true; });

        fetch('/poll/' + pollId + '/vote/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'option=' + optionIndex
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                showResults(data.results, data.vote_count);
            } else {
                alert(data.error || 'Error voting');
                buttons.forEach(function (b) { b.disabled = false; });
            }
        })
        .catch(function (err) {
            console.error(err);
            alert('Error voting. Please try again.');
            buttons.forEach(function (b) { b.disabled = false; });
        });
    }

    function showResults(results, voteCount) {
        var container = document.getElementById('poll-content');
        var html = '<div class="poll-results">';
        results.forEach(function (r) {
            html +=
                '<div class="result-row">' +
                    '<div class="result-label">' +
                        '<span>' + r.option + '</span>' +
                        '<span>' + r.percentage + '%</span>' +
                    '</div>' +
                    '<div class="result-bar-bg">' +
                        '<div class="result-bar-fill" style="width: ' + r.percentage + '%;"></div>' +
                    '</div>' +
                    '<div style="font-size: 0.8rem; color: var(--text-muted);">' +
                        r.count + ' vote' + (r.count === 1 ? '' : 's') +
                    '</div>' +
                '</div>';
        });
        html += '</div>';
        container.innerHTML = html;
        var voteCountEl = document.getElementById('vote-count');
        if (voteCountEl) {
            voteCountEl.textContent = voteCount + ' vote' + (voteCount === 1 ? '' : 's') + ' total';
        }
    }

    function sharePollFull() {
        var title = pollQuestion;
        var wireUrl = 'https://24hourwire.news/poll/' + pollId + '/';
        if (document.getElementById('share-overlay')) return;
        var overlay = document.createElement('div');
        overlay.id = 'share-overlay';
        overlay.innerHTML =
            '<div class="share-overlay-backdrop" data-action="close-overlay"></div>' +
            '<div class="share-overlay-content">' +
                '<div class="share-overlay-header">' +
                    '<h3>Share Poll</h3>' +
                    '<button class="close-overlay" data-action="close-overlay" aria-label="Close">&times;</button>' +
                '</div>' +
                '<div class="share-overlay-preview">' +
                    '<p class="share-preview-source" style="color: var(--accent); font-weight: 600; margin-bottom: 8px;">via @24HourWire</p>' +
                    '<p class="share-preview-text"></p>' +
                    '<p class="share-preview-source">24HourWire Community Poll</p>' +
                '</div>' +
                '<div class="share-overlay-buttons">' +
                    '<button class="share-option twitter" data-action="share-twitter">' +
                        '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>' +
                        '<span>Share on X</span>' +
                    '</button>' +
                    '<button class="share-option facebook" data-action="share-facebook">' +
                        '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>' +
                        '<span>Facebook</span>' +
                    '</button>' +
                    '<button class="share-option linkedin" data-action="share-linkedin">' +
                        '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>' +
                        '<span>LinkedIn</span>' +
                    '</button>' +
                    '<button class="share-option copy" data-action="copy-share">' +
                        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>' +
                        '<span>Copy link</span>' +
                    '</button>' +
                '</div>' +
            '</div>';
        document.body.appendChild(overlay);
        var preview = overlay.querySelector('.share-preview-text');
        if (preview) preview.textContent = title;
        overlay.querySelectorAll('[data-action="share-twitter"], [data-action="copy-share"]').forEach(function (n) {
            n.setAttribute('data-title', title);
            n.setAttribute('data-url', wireUrl);
        });
        overlay.querySelectorAll('[data-action="share-facebook"], [data-action="share-linkedin"]').forEach(function (n) {
            n.setAttribute('data-url', wireUrl);
        });
        document.body.style.overflow = 'hidden';
    }

    function closeShareOverlay() {
        var overlay = document.getElementById('share-overlay');
        if (overlay) {
            overlay.remove();
            document.body.style.overflow = '';
        }
    }

    function shareToTwitter(title, wireUrl) {
        var text = 'via @24HourWire\n\n' + title + '\n\n' + wireUrl;
        window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(text), '_blank', 'width=600,height=400');
        closeShareOverlay();
    }

    function shareToFacebook(wireUrl) {
        window.open('https://www.facebook.com/sharer/sharer.php?u=' + wireUrl, '_blank', 'width=600,height=400');
        closeShareOverlay();
    }

    function shareToLinkedIn(wireUrl) {
        window.open('https://www.linkedin.com/sharing/share-offsite/?url=' + wireUrl, '_blank', 'width=600,height=400');
        closeShareOverlay();
    }

    function copyShareLink(title, wireUrl) {
        var text = title + '\n' + wireUrl + '\n\n24HourWire Community Poll';
        function markCopied() {
            var btn = document.querySelector('.share-option.copy');
            if (btn) {
                btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg><span>Copied!</span>';
            }
            setTimeout(closeShareOverlay, 1000);
        }
        function fallbackCopy(value) {
            var textarea = document.createElement('textarea');
            textarea.value = value;
            textarea.style.position = 'fixed';
            textarea.style.left = '-9999px';
            document.body.appendChild(textarea);
            textarea.focus();
            textarea.select();
            try {
                document.execCommand('copy');
                markCopied();
            } catch (err) {
                console.error('Copy failed', err);
            }
            document.body.removeChild(textarea);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(markCopied).catch(function () { fallbackCopy(text); });
        } else {
            fallbackCopy(text);
        }
    }

    document.addEventListener('click', function (e) {
        var el = e.target.closest('[data-action]');
        if (!el) return;
        var action = el.getAttribute('data-action');
        if (action === 'submit-vote') {
            submitVote(parseInt(el.getAttribute('data-option'), 10) || 0);
        } else if (action === 'share-poll') {
            sharePollFull();
        } else if (action === 'close-overlay') {
            closeShareOverlay();
        } else if (action === 'share-twitter') {
            shareToTwitter(el.getAttribute('data-title') || pollQuestion, el.getAttribute('data-url') || '');
        } else if (action === 'share-facebook') {
            shareToFacebook(el.getAttribute('data-url') || '');
        } else if (action === 'share-linkedin') {
            shareToLinkedIn(el.getAttribute('data-url') || '');
        } else if (action === 'copy-share') {
            copyShareLink(el.getAttribute('data-title') || pollQuestion, el.getAttribute('data-url') || '');
        }
    });
})();
