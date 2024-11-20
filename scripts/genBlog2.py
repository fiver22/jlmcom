import argparse
import os
from create_blog_post import create_blog_post
from manage_tags import manage_tags
from update_index_pages import update_index_pages

# Argument Parser Setup
# This is exactly as in the original `genBlog.py`
parser = argparse.ArgumentParser(description="Manage blog posts and tags for your website.")
parser.add_argument("--title", type=str, help="Title of the new blog post", required=True)
parser.add_argument("--tags", type=str, help="Comma-separated list of tags for the new post", required=False, default="")
parser.add_argument("--debug", action='store_true', help="Enable debugging output for troubleshooting")

args = parser.parse_args()

# Extract arguments - the same as the original
new_post_title = args.title
new_tags = args.tags.split(',') if args.tags else []
debug = args.debug

# Determine the base directory of the project dynamically
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Step 1: Create the new blog post (call to the split function)
new_post_path = create_blog_post(project_root, new_post_title, new_tags, debug)

# Step 2: Manage tags for the new blog post (call to the split function)
manage_tags(project_root, new_post_path, debug)

# Step 3: Update index pages (call to the split function)
new_post_filename = os.path.basename(new_post_path)
update_index_pages(project_root, new_post_filename, new_post_title)

print("Blog post creation completed successfully.")

