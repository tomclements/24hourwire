/* FOUC guard: apply saved theme before first paint. Load in HEAD without defer. */
(function () {
    try {
        var theme = localStorage.getItem('theme');
        if (theme) document.documentElement.setAttribute('data-theme', theme);
    } catch (e) {}

    /* Hide broken images without inline onerror (error does not bubble). */
    document.addEventListener('error', function (e) {
        var img = e.target;
        if (!img || img.tagName !== 'IMG') return;
        img.style.display = 'none';
        var parent = img.parentElement;
        if (!parent) return;
        var fallback = parent.querySelector('.book-cover-fallback');
        if (fallback) fallback.style.display = 'flex';
    }, true);
})();