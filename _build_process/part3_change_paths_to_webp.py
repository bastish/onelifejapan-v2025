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
def update_json_for_webp(manifest_entries, root_dir):
    """
    Walk root_dir for every .json (skipping any with " copy" in the name),
    then for each JSON:
      1) load it
      2) recursively replace any .jpg/.jpeg/.png entry with .webp?v=epoch_time
      3) write it back only if it changed
    """
    # 1) gather all JSON paths
    json_files = []
    for dirpath, _, files in os.walk(root_dir):
        for fname in files:
            if fname.lower().endswith('.json') and ' copy' not in fname:
                json_files.append(os.path.join(dirpath, fname))

    # 2) helper to recurse into lists, dicts, and strings
    def recursive_update(obj):
        if isinstance(obj, str):
            for entry in manifest_entries:
                # only originals ending in the image extensions
                if entry.lower().endswith(('.jpg', '.jpeg', '.png')) and entry in obj:
                    base = entry.rsplit('.', 1)[0]
                    obj = obj.replace(entry, f"{base}.webp?v={epoch_time}")
            return obj

        if isinstance(obj, list):
            return [recursive_update(item) for item in obj]

        if isinstance(obj, dict):
            return {k: recursive_update(v) for k, v in obj.items()}

        return obj  # leave numbers, booleans, etc. untouched

    # 3) process each file
    for path in json_files:
        print(f"# Process: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        updated = recursive_update(data)
        # compare by serialized form; keys/order won’t change in your replace
        if json.dumps(updated, ensure_ascii=False) != json.dumps(data, ensure_ascii=False):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(updated, f, ensure_ascii=False, indent=2)
            print(f"  ✅ Updated {os.path.basename(path)}")


# -------------------------------
# MAIN EXECUTION
# -------------------------------
if __name__ == '__main__':
    manifest_entries = load_manifest(manifest_file)
    print("Manifest entries loaded:")
    # for entry in manifest_entries:
    #     print(entry)
    update_html_for_webp(manifest_entries, dist_dir)
    
    # # NEW: Update your JSON files
    # json_files_to_update = [
    #     '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/dist/data/card-images-pre-defined.json',
    #     '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/dist/data/card-image-paths.json'
    # ]
    update_json_for_webp(manifest_entries, dist_dir)

    print("HTML and JSON update for WebP completed.")
