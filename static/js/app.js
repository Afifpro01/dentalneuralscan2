document.addEventListener("DOMContentLoaded", function() {
    // Image preview functionality
    const fileInput = document.getElementById('dental-image-input');
    const previewContainer = document.getElementById('image-preview-container');
    const previewImage = document.getElementById('image-preview');
    const uploadBtn = document.getElementById('upload-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (fileInput.files && fileInput.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewContainer.classList.remove('d-none');
                    if (analyzeBtn) {
                        analyzeBtn.disabled = false;
                    }
                }
                
                reader.readAsDataURL(fileInput.files[0]);
            } else {
                previewContainer.classList.add('d-none');
                if (analyzeBtn) {
                    analyzeBtn.disabled = true;
                }
            }
        });
    }
    
    // Loading indicator for form submission
    const analysisForm = document.getElementById('analysis-form');
    if (analysisForm) {
        analysisForm.addEventListener('submit', function() {
            document.getElementById('loading-overlay').classList.remove('d-none');
        });
    }
    
    // Confidence meter animation on results page
    const confidenceMeter = document.getElementById('confidence-meter');
    if (confidenceMeter) {
        const confidenceValue = parseFloat(confidenceMeter.getAttribute('data-confidence'));
        setTimeout(() => {
            confidenceMeter.style.width = confidenceValue + '%';
        }, 300);
    }
    
    // Accordion functionality for education page
    const accordionButtons = document.querySelectorAll('.condition-accordion-button');
    if (accordionButtons.length > 0) {
        accordionButtons.forEach(button => {
            button.addEventListener('click', function() {
                const target = document.getElementById(this.getAttribute('data-target'));
                if (target) {
                    if (target.classList.contains('show')) {
                        target.classList.remove('show');
                        this.classList.remove('active');
                    } else {
                        target.classList.add('show');
                        this.classList.add('active');
                    }
                }
            });
        });
    }
});
