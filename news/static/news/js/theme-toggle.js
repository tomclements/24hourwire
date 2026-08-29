/* Theme toggle for standalone pages that do not load app.js. */
(function () {
    'use strict';

    function toggleTheme() {
        var html = document.documentElement;
        var current = html.getAttribute('data-theme');
        var next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        try { localStorage.setItem('theme', next); } catch (e) {}
        var btn = document.querySelector('.theme-toggle');
        if (!btn) return;
        var t = (btn.textContent || '').trim();
        if (t === '🌙' || t === '☀️') {
            btn.textContent = next === 'dark' ? '☀️' : '🌙';
        }
    }

    document.addEventListener('click', function (e) {
        var el = e.target.closest('[data-action="theme-toggle"]');
        if (!el) return;
        toggleTheme();
    });
})();
