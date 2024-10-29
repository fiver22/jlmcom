// scripts/blogPreviews.js
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".blog-link").forEach(link => {
        const url = link.getAttribute("href");
        fetch(url)
            .then(response => response.text())
            .then(data => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(data, 'text/html');
                const excerpt = doc.querySelector('p') ? doc.querySelector('p').innerText : 'No excerpt available.';
                const preview = document.createElement('p');
                preview.innerText = excerpt.substring(0, 100) + '...';
                preview.style.fontSize = "0.75rem"; 
                link.after(preview);
            })
            .catch(error => console.error('Error loading blog post:', error));
    });
});


