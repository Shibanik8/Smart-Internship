// Smart Internship Management System - Custom JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // 1. Bootstrap form validation hook
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // 2. Auto-fade alerts
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Check if bootstrap is loaded to close it smoothly
            if (typeof bootstrap !== 'undefined') {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                alert.style.display = 'none';
            }
        }, 5000);
    });

    // 3. Simple Client-Side Table Filter
    const searchInputs = document.querySelectorAll('.client-search');
    searchInputs.forEach(input => {
        const targetTableId = input.dataset.targetTable;
        const table = document.getElementById(targetTableId);
        
        if (table) {
            const rows = table.querySelectorAll('tbody tr');
            input.addEventListener('keyup', function (e) {
                const term = e.target.value.toLowerCase();
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(term)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        }
    });
});
