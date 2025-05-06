document.addEventListener("DOMContentLoaded", function() {
    // Language toggle functionality
    const languageToggles = document.querySelectorAll('.language-toggle');
    
    if (languageToggles.length > 0) {
        languageToggles.forEach(toggle => {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                const language = this.getAttribute('data-language');
                window.location.href = `/set_language/${language}`;
            });
        });
    }
});
