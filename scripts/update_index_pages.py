import os
from datetime import datetime

def update_index_pages(project_root, new_post_filename, new_post_title):
    # Define paths relative to the project root
    blog_index_path = os.path.join(project_root, "pages/blog/index.html")
    root_index_path = os.path.join(project_root, "index.html")

    # Step 1: Update Blog Index Page in /pages/blog/index.html
    try:
        with open(blog_index_path, "r") as index_file:
            index_content = index_file.readlines()
        print(f"[DEBUG] Loaded blog index content from: {blog_index_path}")
    except FileNotFoundError:
        print(f"Error: The blog index file '{blog_index_path}' was not found.")
        return

    # Add new blog link at the top of the list (assuming descending order)
    new_entry = f'        <li><a href="/pages/blog/{new_post_filename}">{new_post_title}</a></li>\n'

    # Insert the new entry right after the opening <ul> tag
    for i, line in enumerate(index_content):
        if "<ul>" in line:
            index_content.insert(i + 1, new_entry)
            print(f"[DEBUG] Inserted new entry into blog index at line {i + 1}")
            break

    # Write the updated index content back to file
    with open(blog_index_path, "w") as index_file:
        index_file.writelines(index_content)
    print(f"Blog index updated with new entry in {blog_index_path}: {new_post_title}")

    # Step 2: Update Root Index Page in /index.html
    try:
        with open(root_index_path, "r") as root_index_file:
            root_index_content = root_index_file.readlines()
        print(f"[DEBUG] Loaded root index content from: {root_index_path}")
    except FileNotFoundError:
        print(f"Error: The root index file '{root_index_path}' was not found.")
        return

    # Add a new blog link to the "Recent Posts" section
    formatted_date = datetime.now().strftime("%Y-%m-%d")
    new_entry_root = (
        f'            <article>\n'
        f'                <h4><a class="blog-link" href="/pages/blog/{new_post_filename}">'
        f'{formatted_date}: {new_post_title}</a></h4>\n'
        f'            </article>\n'
    )

    # Try to insert after marker comment or at the top of Recent Posts section as fallback
    marker = "<!-- Add more blog links as new posts are created -->"
    marker_found = False
    for i, line in enumerate(root_index_content):
        if marker in line:
            root_index_content.insert(i + 1, new_entry_root)  # Insert right after the marker
            print(f"[DEBUG] Marker found. Inserted new entry into root index at line {i + 1}")
            marker_found = True
            break

    if not marker_found:
        print(f"[DEBUG] Marker comment not found in root index.")
        # If the marker is not found, append the new entry near the top of the Recent Posts section
        for i, line in enumerate(root_index_content):
            if "<section>" in line and "Recent Posts" in root_index_content[i + 1]:
                root_index_content.insert(i + 2, new_entry_root)
                print(f"[DEBUG] Inserted new entry into Recent Posts section at line {i + 2}")
                break

    # Write the updated root index content back to file
    with open(root_index_path, "w") as root_index_file:
        root_index_file.writelines(root_index_content)
    print(f"Root index updated with new entry in {root_index_path}: {new_post_title}")


