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
                if key == 'tags':
                    value = [v.strip() for v in value.strip('[]').replace('"', '').split(',')]
                metadata[key] = value        
        return metadata
    return None

def main():
    # Ensure this is the correct root directory where your pages directory resides
    root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tags_dict = {}

    for root, dirs, files in os.walk(os.path.join(root_directory, 'pages')):
        for file in files:
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

    output_path = os.path.join(root_directory, 'tags.json')
    with open(output_path, 'w') as json_file:
        json.dump(tags_dict, json_file, indent=4)

    print("Done. Tags have been updated. Tags file written at:", output_path)

if __name__ == "__main__":
    main()

