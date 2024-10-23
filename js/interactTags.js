<div id="tags">
    <button onclick="filterByTag('HTML')">HTML</button>
    <button onclick="filterByTag('beginner')">Beginner</button>
    <button onclick="filterByTag('tutorial')">Tutorial</button>
</div>
<div id="post-container"></div>

<script>
    async function filterByTag(tag) {
        const response = await fetch('tags.json');
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
</script>
