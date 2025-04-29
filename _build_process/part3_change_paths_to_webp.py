import os
import time    
epoch_time = int(time.time())
# -------------------------------
# Configuration
# -------------------------------
# Path to your manifest file containing normalized image paths (one per line).
# For example, each line should look like: 
# /assets/img/2024/media/routes/69/217/thisimage.jpg
manifest_file = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/_build_process/images_manifest.txt'

# Root of your build where HTML files are stored.
dist_dir = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/dist'

# -------------------------------
# Helper Function: Load Manifest
# -------------------------------
def load_manifest(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as mf:
        # Return a list of lines (each a normalized asset path)
        return [line.strip() for line in mf if line.strip()]

# -------------------------------
# Function: Update HTML Files for WebP
# -------------------------------
def update_html_for_webp(manifest_entries, root_dir):
    """
    For every HTML file in root_dir, searches for each manifest entry (as a literal string)
    and replaces its extension (.jpg, .jpeg or .png) with .webp.
    """
    # Loop over all HTML files in the directory tree.
    for dirpath, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                html_path = os.path.join(dirpath, file)
                with open(html_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                original_content = content

                # For each manifest entry, do a simple literal replacement.
                for entry in manifest_entries:
                    # Only process entries ending with .jpg, .jpeg, or .png.
                    lower_entry = entry.lower()
                    if lower_entry.endswith('.jpg') or lower_entry.endswith('.jpeg') or lower_entry.endswith('.png'):
                        # Build the new entry by replacing the extension with .webp.
                        new_entry = entry.rsplit('.', 1)[0] + '.webp?v=' + str(epoch_time)
                        # Replace all occurrences in the HTML content.
                        content = content.replace(entry, new_entry)
                
                # If changes were made, write back to the file.
                if content != original_content:
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated {html_path}")
                    

import json

# -------------------------------
# Function: Update JSON Files for WebP
# -------------------------------
def update_json_for_webp(manifest_entries, json_files):
    """
    For each JSON file, searches for manifest entries and updates .jpg/.jpeg/.png paths to .webp.
    """
    for json_path in json_files:
        if not os.path.exists(json_path):
            print(f"JSON file not found: {json_path}")
            continue
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        original_data = json.dumps(data)  # serialize original to compare later

        # Helper to recursively update nested lists or strings
        def recursive_update(item):
            if isinstance(item, list):
                return [recursive_update(subitem) for subitem in item]
            if isinstance(item, str):
                for entry in manifest_entries:
                    lower_entry = entry.lower()
                    if lower_entry.endswith(('.jpg', '.jpeg', '.png', 'webp')) and entry in item:
                        item = item.replace(entry, entry.rsplit('.', 1)[0] + '.webp?v=' + str(epoch_time))
                return item
            return item

        updated_data = recursive_update(data)

        # Only save if changes were made
        if json.dumps(updated_data) != original_data:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2)
            print(f"Updated {json_path}")


# -------------------------------
# MAIN EXECUTION
# -------------------------------
if __name__ == '__main__':
    manifest_entries = load_manifest(manifest_file)
    print("Manifest entries loaded:")
    for entry in manifest_entries:
        print(entry)
    update_html_for_webp(manifest_entries, dist_dir)
    
    # NEW: Update your JSON files
    json_files_to_update = [
        '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/dist/data/card-images-pre-defined.json',
        '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/dist/data/card-image-paths.json'
    ]
    update_json_for_webp(manifest_entries, json_files_to_update)

    print("HTML and JSON update for WebP completed.")
