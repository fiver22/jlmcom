reated and Merged a New Script:
        Developed a new Python script called blogManager.py to simplify the blog post creation process.
        Merged this script into the main branch after testing, ensuring it handles all necessary tasks without modifying unrelated files.

    Simplified Blog Workflow:
        Combined the functionality of genBlog.py and genTags.py into blogManager.py.
        Ensured the workflow is automated and avoids overwriting existing files.

    Retained Only the New Script:
        Merged only blogManager.py into main—discarded test files and avoided merging temporary changes like test posts and tag updates.

How to Generate a Blog Post with blogManager.py

To generate a new blog post, you use the blogManager.py script, which now handles:

    Creating the blog post file.
    Updating tags in the metadata section of the blog post.
    Updating tags.json to link the new post with its tags.

Example Command:

python3 blogManager.py --title "Your Blog Title Here" --tags "tag1, tag2, tag3" [--commit] [--debug]

    --title: Provide the title of the new blog post.
    --tags: Comma-separated list of tags for the new post.
    Optional Flags:
        --commit: Automates Git commit and push of the changes (e.g., add new blog post, update indices, etc.).
        --debug: Provides verbose output for debugging—useful if you need to trace what the script is doing step by step.

Workflow After Running the Script:

    Creates a New Blog Post File with a unique filename (e.g., YYYYMMDD.html).
    Updates Blog Indices (index.html and pages/blog/index.html) to include the new post.
    Adds Tags in the metadata of the new blog post and updates the central tags.json file to track these tags.

In Short:

    The new script (blogManager.py) allows you to generate, index, and manage tags for a blog post in one step.
    Run it with a title and tags, use --commit to push changes, and --debug to see details of the script execution.