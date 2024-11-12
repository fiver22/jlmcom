document.addEventListener("DOMContentLoaded", async function() {
    try {
        console.log("Fetching tags.json...");
        const response = await fetch('/tags.json');
        if (!response.ok) {
            throw new Error(`Failed to fetch tags.json: ${response.statusText}`);
        }

        const tagMap = await response.json();
        console.log("Tags fetched successfully:", tagMap);

        const tagsContainer = document.getElementById('tags');
        if (!tagsContainer) {
            console.error("No element with ID 'tags' found in the DOM.");
            return;
        }

        // Check if we're on the tags.html page
        if (window.location.pathname.includes('/pages/tags.html')) {
            // Create a button for each tag that directly links to related posts
            for (const tag in tagMap) {
                console.log(`Creating button for tag: ${tag}`);
                const button = document.createElement('button');
                button.textContent = tag;
                button.onclick = () => displayPosts(tagMap, tag);
                tagsContainer.appendChild(button);
            }
        } else {
            // Original functionality (e.g., main page)
            for (const tag in tagMap) {
                console.log(`Creating button for tag: ${tag}`);
                const button = document.createElement('button');
                button.textContent = tag;
                button.onclick = () => filterByTag(tag);
                tagsContainer.appendChild(button);
            }
        }
        console.log("All tag buttons added successfully.");
    } catch (error) {
        console.error("Error during tags loading:", error);
    }
});

function displayPosts(tagMap, tag) {
    const relatedPosts = tagMap[tag] || [];
    const container = document.getElementById('post-container');
    container.innerHTML = '';

    relatedPosts.forEach(post => {
        console.log(`Adding post: ${post}`);
        const link = document.createElement('a');
        link.href = post;
        link.textContent = post.replace('.html', '');
        container.appendChild(link);
        container.appendChild(document.createElement('br')); // Add line break for readability
    });
}

