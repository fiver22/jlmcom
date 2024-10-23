import os
import re
import json

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
                # Parse tags into a list
                if key == 'tags':
                    value = [v.strip() for v in value.strip('[]').replace('"', '').split(', ')]
                metadata[key] = value        
        return metadata
    return None

tags_dict = {}

# Traverse your directory for HTML files
for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            print(f"Processing file: {filepath}")
            with open(filepath, 'r') as f:
                content = f.read()
                metadata = extract_frontmatter(content)
                print(f"Extracted metadata: {metadata}")  # Print extracted metadata
                if metadata and 'tags' in metadata:
                    for tag in metadata['tags']:
                        tags_dict.setdefault(tag, []).append(file)

# Write the tags.json file
with open('tags.json', 'w') as json_file:
    json.dump(tags_dict, json_file, indent=4)

