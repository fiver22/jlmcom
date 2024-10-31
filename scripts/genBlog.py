import os
from datetime import datetime

# Determine the base directory of the project dynamically, assuming the script is in the scripts folder
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the blog directory, relative to the project root for local use
# Use root-relative for the entire project structure
blog_dir = "/pages/blog"

# Construct the local file paths relative to the project root
# Strip the leading slash to avoid confusion for local access
local_blog_dir = blog_dir.lstrip("/")
template_path = os.path.join(project_root, local_blog_dir, "template_blog.html")
blog_index_path = os.path.join(project_root, local_blog_dir, "index.html")
root_index_path = os.path.join(project_root, "index.html")  # Adding path for the root index.html

# Step 1: Create a New Blog File
new_post_date = datetime.now().strftime("%Y%m%d")
new_post_title = input("Enter the title for the new blog post: ")  # Prompt for the title of the new blog post
new_post_filename = f"{new_post_date}.html"
new_post_path = os.path.join(project_root, local_blog_dir, new_post_filename)

# Copy template_blog.html to new blog post file
try:
    with open(template_path, "r") as template_file:
        content = template_file.read()
except FileNotFoundError:
    print(f"Error: The template file '{template_path}' was not found.")
    exit(1)

# Replace placeholders with actual content
content = content.replace("YYYY-MM-DD", new_post_date).replace("<!-- Write your content here -->", new_post_title)

# Write to the new blog post file
with open(new_post_path, "w") as new_post_file:
    new_post_file.write(content)

print(f"New blog post created: {new_post_filename}")

# Step 2: Update Blog Index Page in /pages/blog/index.html
try:
    with open(blog_index_path, "r") as index_file:
        index_content = index_file.readlines()
except FileNotFoundError:
    print(f"Error: The blog index file '{blog_index_path}' was not found.")
    exit(1)

# Add new blog link in chronological order (assuming descending order)
# Use the root-relative path for the HTML link
new_entry = f'        <li><a href="{blog_dir}/{new_post_filename}">{new_post_title} - {new_post_date}</a></li>\n'

# Insert the new entry just after the marker comment in /pages/blog/index.html
for i, line in enumerate(index_content):
    if "<!-- Add more links here for each new blog post -->" in line:
        index_content.insert(i + 1, new_entry)
        break

# Write the updated index content back to file
with open(blog_index_path, "w") as index_file:
    index_file.writelines(index_content)

print(f"Blog index updated with new entry in /pages/blog/index.html: {new_post_title}")

# Step 3: Update Root Index Page in /index.html
try:
    with open(root_index_path, "r") as root_index_file:
        root_index_content = root_index_file.readlines()
except FileNotFoundError:
    print(f"Error: The root index file '{root_index_path}' was not found.")
    exit(1)

# Add new blog link in chronological order (assuming descending order)
# Use the root-relative path for the HTML link
new_entry_root = f'                <h3><a class="blog-link" href="{blog_dir}/{new_post_filename}">{new_post_date}: {new_post_title}</a></h3>\n'

# Insert the new entry just after the marker comment in /index.html
for i, line in enumerate(root_index_content):
    if "<!-- Add more blog links as new posts are created -->" in line:
        root_index_content.insert(i + 1, new_entry_root)
        break

# Write the updated root index content back to file
with open(root_index_path, "w") as root_index_file:
    root_index_file.writelines(root_index_content)

print(f"Root index updated with new entry in /index.html: {new_post_title}")

