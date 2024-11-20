import os
from datetime import datetime

def create_blog_post(project_root, new_post_title, new_tags, debug):
    # Define the blog directory, relative to the project root for local use
    blog_dir = "/pages/blog"
    local_blog_dir = blog_dir.lstrip("/")
    template_path = os.path.join(project_root, local_blog_dir, "template_blog.html")
    
    # Determine new blog post path
    new_post_date = datetime.now().strftime("%Y%m%d")
    new_post_filename = f"{new_post_date}.html"
    new_post_path = os.path.join(project_root, local_blog_dir, new_post_filename)

    # Check if file exists
    counter = 1
    while os.path.exists(new_post_path):
        new_post_filename = f"{new_post_date}_{counter}.html"
        new_post_path = os.path.join(project_root, local_blog_dir, new_post_filename)
        counter += 1

    # Read template and replace placeholders
    try:
        with open(template_path, "r") as template_file:
            content = template_file.read()
    except FileNotFoundError:
        print(f"Error: The template file '{template_path}' was not found.")
        exit(1)

    content = content.replace("YYYY-MM-DD", new_post_date).replace("<!-- Write your content here -->", new_post_title)
    if new_tags:
        tags_string = ", ".join([f'"{tag.strip()}"' for tag in new_tags])
        content = content.replace("--- tags: []", f"--- tags: [{tags_string}]")

    # Write to the new blog post file
    with open(new_post_path, "w") as new_post_file:
        new_post_file.write(content)

    print(f"New blog post created: {new_post_filename}")

    # Open in vim for editing
    os.system(f"vim {new_post_path}")

    return new_post_path

