(function () {
    'use strict';

    var cfg = {};
    try {
        var cfgEl = document.getElementById('share-config');
        if (cfgEl) cfg = JSON.parse(cfgEl.textContent || '{}');
    } catch (e) {
        cfg = {};
    }

    var shareUrl = cfg.url || '';
    var shareTitle = cfg.title || '';
    var shareText = shareTitle + '\n\nCurated by @24HourWire';

    var seconds = 3;
    var countdownEl = document.getElementById('countdown');
    var timer = setInterval(function () {
        seconds--;
        if (countdownEl) countdownEl.textContent = seconds;
        if (seconds <= 0) clearInterval(timer);
    }, 1000);

    function shareToTwitter() {
        var url = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText) + '&url=' + encodeURIComponent(shareUrl);
        window.open(url, '_blank', 'width=600,height=400');
    }

    function shareToFacebook() {
        var url = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(shareUrl);
        window.open(url, '_blank', 'width=600,height=400');
    }

    function shareToLinkedIn() {
        var url = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(shareUrl);
        window.open(url, '_blank', 'width=600,height=400');
    }

    function copyLink() {
        var fullText = shareTitle + '\n' + shareUrl + '\n\nCurated by @24HourWire';
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(fullText).then(function () {
                alert('Link copied to clipboard!');
            });
        }
    }

    document.addEventListener('click', function (e) {
        var el = e.target.closest('[data-action]');
        if (!el) return;
        var action = el.getAttribute('data-action');
        if (action === 'share-twitter') shareToTwitter();
        else if (action === 'share-facebook') shareToFacebook();
        else if (action === 'share-linkedin') shareToLinkedIn();
        else if (action === 'copy-link') copyLink();
    });
})();
