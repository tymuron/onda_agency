document.addEventListener('DOMContentLoaded', () => {
    console.log('Vastu Platform Loaded');

    // Add hover effects or simple interactions here if needed beyond CSS
    const checkboxes = document.querySelectorAll('.checkbox');
    checkboxes.forEach(box => {
        box.addEventListener('click', () => {
            box.classList.toggle('checked');
            // In a real app, this would update progress
            if(box.classList.contains('checked')) {
                box.style.backgroundColor = 'var(--primary-black)';
                box.style.borderColor = 'var(--primary-black)';
                // Add a checkmark icon or similar
            } else {
                box.style.backgroundColor = 'transparent';
                box.style.borderColor = 'var(--border-color)';
            }
        });
    });
});
