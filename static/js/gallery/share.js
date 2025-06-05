document.addEventListener('DOMContentLoaded', function() {
        const urlElement = document.querySelector('.share-url');
        if (urlElement) {
            urlElement.addEventListener('click', function() {
                const range = document.createRange();
                range.selectNode(urlElement);
                window.getSelection().removeAllRanges();
                window.getSelection().addRange(range);
                document.execCommand('copy');
                window.getSelection().removeAllRanges();
                
                const originalText = urlElement.textContent;
                urlElement.textContent = 'Copied!';
                setTimeout(() => {
                    urlElement.textContent = originalText;
                }, 2000);
            });
        }
    });