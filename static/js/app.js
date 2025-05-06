document.addEventListener("DOMContentLoaded", function() {
    // Symptom form handling - ensure "None" checkboxes work correctly
    const noneCheckboxes = {
        'sensitivity-none': 'sensitivity[]',
        'symptom-none': 'additional_symptoms[]'
    };
    
    // Handle "None" checkbox exclusive selection
    Object.keys(noneCheckboxes).forEach(checkboxId => {
        const noneCheckbox = document.getElementById(checkboxId);
        if (noneCheckbox) {
            const checkboxName = noneCheckboxes[checkboxId];
            
            // When "None" is checked, uncheck all others in the group
            noneCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    const otherCheckboxes = document.querySelectorAll(`input[name="${checkboxName}"]:not(#${checkboxId})`);
                    otherCheckboxes.forEach(cb => {
                        cb.checked = false;
                    });
                }
            });
            
            // When any other checkbox in the group is checked, uncheck "None"
            const groupCheckboxes = document.querySelectorAll(`input[name="${checkboxName}"]:not(#${checkboxId})`);
            groupCheckboxes.forEach(cb => {
                cb.addEventListener('change', function() {
                    if (this.checked) {
                        noneCheckbox.checked = false;
                    }
                });
            });
        }
    });
    
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
