import os

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
                        new_entry = entry.rsplit('.', 1)[0] + '.webp'
                        # Replace all occurrences in the HTML content.
                        content = content.replace(entry, new_entry)
                
                # If changes were made, write back to the file.
                if content != original_content:
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated {html_path}")
                    
# -------------------------------
# MAIN EXECUTION
# -------------------------------
if __name__ == '__main__':
    manifest_entries = load_manifest(manifest_file)
    print("Manifest entries loaded:")
    for entry in manifest_entries:
        print(entry)
    update_html_for_webp(manifest_entries, dist_dir)
    print("HTML update for WebP completed.")
