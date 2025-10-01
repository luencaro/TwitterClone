(function() {
    document.addEventListener('DOMContentLoaded', function() {
        const cards = document.querySelectorAll('.js-post-card');
        if (!cards.length) {
            return;
        }

        const interactiveSelector = 'a, button, input, textarea, select, label, .btn, .like-button, .like-form';

        cards.forEach(function(card) {
            const url = card.dataset.href;
            if (!url) {
                return;
            }

            card.style.cursor = 'pointer';

            card.querySelectorAll('a, p, div, span, small, strong, form, svg, button, label').forEach(function(child) {
                if (!child.style.cursor || child.style.cursor === 'auto') {
                    child.style.cursor = 'pointer';
                }
            });

            const navigate = function(newTab) {
                if (newTab) {
                    window.open(url, '_blank', 'noopener');
                } else {
                    window.location.href = url;
                }
            };

            card.addEventListener('click', function(event) {
                if (event.defaultPrevented) {
                    return;
                }

                if (event.target.closest(interactiveSelector)) {
                    return;
                }

                const openInNewTab = event.ctrlKey || event.metaKey || event.button === 1;
                event.preventDefault();
                navigate(openInNewTab);
            });

            card.addEventListener('auxclick', function(event) {
                if (event.button !== 1) {
                    return;
                }

                if (event.target.closest(interactiveSelector)) {
                    return;
                }

                event.preventDefault();
                navigate(true);
            });

            card.addEventListener('keydown', function(event) {
                if (event.target !== card) {
                    return;
                }

                if (event.key === 'Enter' || event.key === ' ') {
                    if (event.key === ' ') {
                        event.preventDefault();
                    }

                    const openInNewTab = event.ctrlKey || event.metaKey;
                    navigate(openInNewTab);
                }
            });
        });
    });
})();
