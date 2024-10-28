#!/usr/bin/env python3
import os
import re
import json

# Function to extract frontmatter metadata
def extract_frontmatter(content):
    match = re.search(r'<!--\s*---\s*(.*?)\s*---\s*-->', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        metadata = {}
        for line in frontmatter.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if key == 'tags':
                    value = [v.strip() for v in value.strip('[]').replace('"', '').split(',')]
                metadata[key] = value        
        return metadata
    return None

# Main function to iterate over HTML files and extract tags
def main():
    # Define root directory and initialize tags dictionary
    root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tags_dict = {}

    # Walk through the "pages" directory
    for root, dirs, files in os.walk(os.path.join(root_directory, 'pages')):
        for file in files:
            # Skip template_blog.html to prevent it from being processed
            if file == "template_blog.html":
                continue
            
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        metadata = extract_frontmatter(content)
                        if metadata and 'tags' in metadata:
                            for tag in metadata['tags']:
                                tags_dict.setdefault(tag, []).append(os.path.relpath(filepath, start=root_directory))
                        else:
                            print(f"No tags found in {file}")
                except Exception as e:
                    print(f"Error reading or processing {filepath}: {str(e)}")

    # Write collected tags to tags.json
    output_path = os.path.join(root_directory, 'tags.json')
    with open(output_path, 'w') as json_file:
        json.dump(tags_dict, json_file, indent=4)

    print("Done. Tags have been updated. Tags file written at:", output_path)

# Entry point for the script
if __name__ == "__main__":
    main()

