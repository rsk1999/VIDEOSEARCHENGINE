document.addEventListener("DOMContentLoaded", function() {
    // Example: Highlight selected videos
    const checkboxes = document.querySelectorAll('.form-check-input');
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            if(this.checked) {
                this.parentNode.style.backgroundColor = '#e8f0fe';
            } else {
                this.parentNode.style.backgroundColor = '#fff';
            }
        });
    });
});
