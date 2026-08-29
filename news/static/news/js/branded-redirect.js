(function () {
    'use strict';

    var cfg = {};
    try {
        var cfgEl = document.getElementById('redirect-config');
        if (cfgEl) cfg = JSON.parse(cfgEl.textContent || '{}');
    } catch (e) {
        cfg = {};
    }

    var dest = cfg.url || '/';
    var seconds = 2;
    var el = document.getElementById('countdown');
    var timer = setInterval(function () {
        seconds--;
        if (el) el.textContent = seconds;
        if (seconds <= 0) {
            clearInterval(timer);
            window.location.href = dest;
        }
    }, 1000);
})();
