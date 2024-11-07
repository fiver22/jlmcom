import argparse

# Argument Parser Setup
parser = argparse.ArgumentParser(description="Manage blog posts and tags for your website.")
parser.add_argument("--title", type=str, help="Title of the new blog post", required=True)
parser.add_argument("--tags", type=str, help="Comma-separated list of tags for the new post", required=False, default="")
parser.add_argument("--debug", action='store_true', help="Enable debugging output for troubleshooting")

args = parser.parse_args()

# Enable Debugging
debug = args.debug

# Extract title and tags from arguments
new_post_title = args.title
new_tags = args.tags.split(',') if args.tags else []


import os
from datetime import datetime

# Determine the base directory of the project dynamically, assuming the script is in the scripts folder
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the blog directory, relative to the project root for local use
# Use root-relative for the entire project structure
blog_dir = "/pages/blog"

# Construct the local file paths relative to the project root
local_blog_dir = blog_dir.lstrip("/")
template_path = os.path.join(project_root, local_blog_dir, "template_blog.html")
blog_index_path = os.path.join(project_root, local_blog_dir, "index.html")
root_index_path = os.path.join(project_root, "index.html")  # Adding path for the root index.html

# Step 1: Create a New Blog File
new_post_date = datetime.now().strftime("%Y%m%d")
new_post_title = args.title
new_post_filename = f"{new_post_date}.html"  # Change filename format to YYYYMMDD
new_post_path = os.path.join(project_root, local_blog_dir, new_post_filename)

# Check if the file already exists and generate a unique filename if necessary
counter = 1
while os.path.exists(new_post_path):
    new_post_filename = f"{new_post_date}_{counter}.html"
    new_post_path = os.path.join(project_root, local_blog_dir, new_post_filename)
    counter += 1

# Copy template_blog.html to new blog post file
try:
    with open(template_path, "r") as template_file:
        content = template_file.read()
except FileNotFoundError:
    print(f"Error: The template file '{template_path}' was not found.")
    exit(1)

# Replace placeholders with actual content
content = content.replace("YYYY-MM-DD", new_post_date).replace("<!-- Write your content here -->", new_post_title)

# Add Tags to the Blog Post Metadata before opening in vim for editing
if new_tags:
    tags_string = ", ".join([f'"{tag.strip()}"' for tag in new_tags])
    content = content.replace("--- tags: []", f"--- tags: [{tags_string}]")

# Write to the new blog post file
with open(new_post_path, "w") as new_post_file:
    new_post_file.write(content)

print(f"New blog post created: {new_post_filename}")

# Open the new blog post file in vim for editing


# Open the new blog post file in vim for editing
os.system(f"vim {new_post_path}")

# Re-read the edited blog post to capture any changes to the tags
with open(new_post_path, 'r') as post_file:
    content = post_file.read()

import json
import re

# Extract updated tags from the blog post metadata
updated_tags = []
tag_match = re.search(r'--- tags: \[(.*?)\]', content)
if tag_match:
    updated_tags = [tag.strip().strip('"') for tag in tag_match.group(1).split(',')]
    if debug:
        print(f"Debug: Updated tags extracted from the blog post: {updated_tags}")

# Update tags.json with the new tags and link to the post
tags_file_path = os.path.join(project_root, "tags.json")

try:
    # Load the existing tags from the tags.json file
    with open(tags_file_path, 'r') as tags_file:
        tags_data = json.load(tags_file)
    if debug:
        print(f"Debug: Loaded tags data from {tags_file_path} - {tags_data}")
except FileNotFoundError:
    tags_data = {}
    if debug:
        print(f"Debug: Tags file not found. Starting with an empty tags dictionary.")

# Update tags in the tags_data based on the final content after vim editing
# Add new tags or update existing ones
for tag in updated_tags:
    tag = tag.strip().lower()
    if tag in tags_data:
        if new_post_filename not in tags_data[tag]:
            tags_data[tag].append(new_post_filename)
    else:
        tags_data[tag] = [new_post_filename]

# Remove old tags that are no longer present in the updated tags
for tag in list(tags_data.keys()):
    if tag not in [t.strip().lower() for t in updated_tags]:
        if new_post_filename in tags_data[tag]:
            tags_data[tag].remove(new_post_filename)
        if not tags_data[tag]:
            del tags_data[tag]

# Write the updated tags back to tags.json
try:
    with open(tags_file_path, 'w') as tags_file:
        json.dump(tags_data, tags_file, indent=4)
    print(f"Tags updated in {tags_file_path}")
except Exception as e:
    print(f"Error: Failed to update tags in {tags_file_path} - {e}")

if debug:
    print(f"Debug: Final tags data to be written to {tags_file_path} - {tags_data}")

# Step 2: Update Blog Index Page in /pages/blog/index.html
try:
    with open(blog_index_path, "r") as index_file:
        index_content = index_file.readlines()
except FileNotFoundError:
    print(f"Error: The blog index file '{blog_index_path}' was not found.")
    exit(1)

# Add new blog link at the top of the list (assuming descending order)
# Use the root-relative path for the HTML link
new_entry = f'        <li><a href="{blog_dir}/{new_post_filename}">{new_post_date}: {new_post_title}</a></li>\n'

# Insert the new entry right after the opening <ul> tag in /pages/blog/index.html
for i, line in enumerate(index_content):
    if "<ul>" in line:
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
    root_index_content = None

if root_index_content:
    # Add new blog link at the top of the "Recent Posts" section using a marker comment
    # Use the root-relative path for the HTML link
    formatted_date = datetime.now().strftime("%Y-%m-%d")
    new_entry_root = f'            <article>\n                <h4><a class="blog-link" href="{blog_dir}/{new_post_filename}">{formatted_date}: {new_post_title}</a></h4>\n            </article>\n'

    # Look for a marker comment to identify where to insert new blog entries
    marker = "<!-- Add more blog links as new posts are created -->"
    marker_found = False
    for i, line in enumerate(root_index_content):
        if marker in line:
            root_index_content.insert(i + 1, new_entry_root)  # Insert right after the marker
            marker_found = True
            break

    if not marker_found:
        # If marker not found, add a warning and provide a fallback approach to insert at the top of the "Recent Posts" section
        print(f"Warning: Marker comment not found in /index.html. Adding entry at the top of the 'Recent Posts' section as fallback.")
        for i, line in enumerate(root_index_content):
            if "<section>" in line and "Recent Posts" in root_index_content[i + 1]:
                root_index_content.insert(i + 2, new_entry_root)
                break

    # Write the updated root index content back to file
    with open(root_index_path, "w") as root_index_file:
        root_index_file.writelines(root_index_content)
    print(f"Root index updated with new entry in /index.html: {new_post_title}")
else:
    print("Warning: Root index file could not be read. No changes made to root index.")


