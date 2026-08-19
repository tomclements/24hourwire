/* 24HourWire topic page JavaScript (extends app.js). */
(function () {
    'use strict';

    function filterTopicStories(filter, btn) {
        const grid = document.getElementById('topic-stories-grid');
        if (!grid) return;

        grid.querySelectorAll('.story-card').forEach(card => {
            const bias = card.getAttribute('data-bias') || '';
            card.style.display = (filter === 'all' || bias === filter) ? '' : 'none';
        });

        document.querySelectorAll('.topic-bias-filters .bias-filter-btn').forEach(b => {
            b.classList.remove('active');
            b.style.background = 'var(--bg-primary)';
            b.style.color = 'var(--text-primary)';
            b.style.borderColor = 'var(--border)';
            b.style.fontWeight = '400';
            b.setAttribute('aria-pressed', 'false');
        });

        btn.classList.add('active');
        btn.style.background = 'var(--accent)';
        btn.style.color = '#fff';
        btn.style.borderColor = 'var(--accent)';
        btn.style.fontWeight = '600';
        btn.setAttribute('aria-pressed', 'true');

        try { localStorage.setItem('topicBiasFilter', filter); } catch (e) {}
    }

    document.addEventListener('click', function (e) {
        const el = e.target.closest('[data-action="topic-filter"]');
        if (!el) return;
        filterTopicStories(el.getAttribute('data-filter'), el);
    });

    document.addEventListener('DOMContentLoaded', function () {
        try {
            const saved = localStorage.getItem('topicBiasFilter');
            if (saved && saved !== 'all') {
                const btn = document.querySelector('.topic-bias-filters .bias-filter-btn[data-filter="' + saved + '"]');
                if (btn) filterTopicStories(saved, btn);
            }
        } catch (e) {}
    });
})();