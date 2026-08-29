(function () {
    'use strict';

    document.addEventListener('click', function (e) {
        var el = e.target.closest('[data-action="toggle-edit"]');
        if (!el) return;
        var pollId = el.getAttribute('data-poll-id');
        var form = document.getElementById('edit-form-' + pollId);
        if (form) form.classList.toggle('active');
    });

    var filterForm = document.querySelector('.filters form');
    if (filterForm) {
        filterForm.addEventListener('change', function () {
            filterForm.submit();
        });
    }
})();