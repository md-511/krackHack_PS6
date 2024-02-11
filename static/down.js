document.addEventListener("DOMContentLoaded", function() {
    const checkboxes = document.querySelectorAll('.sel_ip');
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                const row = this.closest('tr');
                const r_id = row.querySelector('td:nth-child(2)').textContent; 
                console.log("Selected Request ID:", r_id);
            }
        });
    });
});