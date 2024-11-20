import json
import re
import os

def manage_tags(project_root, new_post_path, debug=False):
    # Extract updated tags from the blog post metadata
    with open(new_post_path, 'r') as post_file:
        content = post_file.read()

    updated_tags = []
    tag_match = re.search(r'--- tags: \[(.*?)\]', content)
    if tag_match:
        updated_tags = [tag.strip().strip('"') for tag in tag_match.group(1).split(',')]
        if debug:
            print(f"[DEBUG] Updated tags extracted from the blog post: {updated_tags}")

    # Path to tags.json file
    tags_file_path = os.path.join(project_root, "tags.json")

    # Load existing tags data from tags.json
    try:
        with open(tags_file_path, 'r') as tags_file:
            tags_data = json.load(tags_file)
        if debug:
            print(f"[DEBUG] Loaded tags data from {tags_file_path} - {tags_data}")
    except FileNotFoundError:
        tags_data = {}
        if debug:
            print(f"[DEBUG] Tags file not found. Starting with an empty tags dictionary.")

    # Convert new_post_path to a root-relative path
    relative_post_path = os.path.relpath(new_post_path, project_root)
    relative_post_path = f"/{relative_post_path}"  # Ensure it starts with '/'

    # Update tags in tags_data
    for tag in updated_tags:
        tag = tag.strip().lower()

        # Add or update the tag in tags_data
        if tag in tags_data:
            if relative_post_path not in tags_data[tag]:
                tags_data[tag].append(relative_post_path)
        else:
            tags_data[tag] = [relative_post_path]

    # Remove old tags that are no longer present in the updated tags
    for tag in list(tags_data.keys()):
        if tag not in [t.strip().lower() for t in updated_tags]:
            if relative_post_path in tags_data[tag]:
                tags_data[tag].remove(relative_post_path)
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
        print(f"[DEBUG] Final tags data to be written to {tags_file_path} - {tags_data}")


