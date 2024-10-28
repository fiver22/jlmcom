document.addEventListener("DOMContentLoaded", async function() {
    // Fetch tags.json and create buttons dynamically
    const response = await fetch('/tags.json');
    const tagMap = await response.json();
    const tagsContainer = document.getElementById('tags');

    // Create a button for each tag
    for (const tag in tagMap) {
        const button = document.createElement('button');
        button.textContent = tag;
        button.onclick = () => filterByTag(tag);
        tagsContainer.appendChild(button);
    }
});

// Function to filter posts by selected tag
async function filterByTag(tag) {
    const response = await fetch('/tags.json');
    const tagMap = await response.json();
    const relatedPosts = tagMap[tag] || [];
    const container = document.getElementById('post-container');
    container.innerHTML = '';

    relatedPosts.forEach(post => {
        const link = document.createElement('a');
        link.href = post;
        link.textContent = post.replace('.html', '').replace('-', ' ');
        container.appendChild(link);
        container.appendChild(document.createElement('br'));
    });
}

