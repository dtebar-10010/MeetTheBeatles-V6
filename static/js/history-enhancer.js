document.addEventListener('DOMContentLoaded', function() {
    // Add a class to the body based on the current phase
    const phaseElements = document.querySelectorAll('.btn-primary.active');
    if (phaseElements.length > 0) {
        const phaseClass = phaseElements[0].classList[2]; // Gets the 'phase-XX' class
        document.body.classList.add(phaseClass);
    }

    // Format specific terms in the history text
    const historyEntries = document.querySelectorAll('.history-entry');

    if (historyEntries.length === 0) {
        // If no .history-entry elements found, try looking for other containers with text
        const possibleContainers = document.querySelectorAll('.history-container, .content-section, article, p');
        if (possibleContainers.length > 0) {
            console.log('Found alternative text containers:', possibleContainers.length);

            // Terms to highlight with specific classes
            const formatRules = [
                {pattern: /\b(The Beatles|Beatles)\b/g, className: 'band-name'},
                {pattern: /\b(John|Paul|George|Ringo|Lennon|McCartney|Harrison|Starr)\b/g, className: 'beatle-name'},
                {pattern: /\b(19\d{2}|20\d{2})\b/g, className: 'year'},
                {pattern: /["']([^"']+)["']/g, replace: '<span class="quote">"$1"</span>'},
                {pattern: /\b([A-Za-z\s]+Album|[A-Za-z\s]+LP|[A-Za-z\s]+EP|[A-Za-z\s]+Single)\b/g, className: 'album-name'}
            ];

            possibleContainers.forEach(container => {
                // Only process if it contains text about The Beatles
                if (container.textContent.includes('Beatles')) {
                    let content = container.innerHTML;

                    formatRules.forEach(rule => {
                        if (rule.replace) {
                            content = content.replace(rule.pattern, rule.replace);
                        } else {
                            content = content.replace(rule.pattern, `<span class="${rule.className}">$1</span>`);
                        }
                    });

                    container.innerHTML = content;
                }
            });
        }
    } else {
        console.log('Found history entries:', historyEntries.length);

        // Terms to highlight with specific classes
        const formatRules = [
            {pattern: /\b(The Beatles|Beatles)\b/g, className: 'band-name'},
            {pattern: /\b(John|Paul|George|Ringo|Lennon|McCartney|Harrison|Starr)\b/g, className: 'beatle-name'},
            {pattern: /\b(19\d{2}|20\d{2})\b/g, className: 'year'},
            {pattern: /["']([^"']+)["']/g, replace: '<span class="quote">"$1"</span>'},
            {pattern: /\b([A-Za-z\s]+Album|[A-Za-z\s]+LP|[A-Za-z\s]+EP|[A-Za-z\s]+Single)\b/g, className: 'album-name'}
        ];

        historyEntries.forEach(entry => {
            let content = entry.innerHTML;

            formatRules.forEach(rule => {
                if (rule.replace) {
                    content = content.replace(rule.pattern, rule.replace);
                } else {
                    content = content.replace(rule.pattern, `<span class="${rule.className}">$1</span>`);
                }
            });

            entry.innerHTML = content;
        });
    }
});
