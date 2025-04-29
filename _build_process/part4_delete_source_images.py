import os

# -------------------------------
# Configuration
# -------------------------------
# Path to your manifest file (each line is a normalized asset path)
# Example entries:
# /assets/img/2024/media/slider_images/slider-image-68.jpg
manifest_file = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/_build_process/images_manifest.txt'

# Root of your output (dist) directory where assets are stored.
dist_dir = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/dist'

# Assets folder inside dist
assets_dir = os.path.join(dist_dir, 'assets')

# -------------------------------
# Helper Functions
# -------------------------------
def load_manifest(manifest_path):
    """Return a list of non-empty lines from the manifest file."""
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def has_webp_version(file_path):
    """Return True if a WebP version for file_path exists (same name, with .webp extension)."""
    base, _ = os.path.splitext(file_path)
    webp_path = base + '.webp'
    return os.path.exists(webp_path)

def should_delete_file(file_path):
    """Return True if the file extension is .jpg, .jpeg, or .png."""
    ext = os.path.splitext(file_path)[1].lower()
    return ext in ['.jpg', '.jpeg', '.png']

def insert_suffix(filename, suffix):
    """Insert a suffix before the file extension.
       E.g., insert_suffix("foo.jpg", "-master") returns "foo-master.jpg"."""
    base, ext = os.path.splitext(filename)
    return f"{base}{suffix}{ext}"

# -------------------------------
# Main Deletion Routine
# -------------------------------
def delete_non_webp_files():
    manifest_entries = load_manifest(manifest_file)
    print("Processing manifest entries for deletion...")

    for entry in manifest_entries:
        # Remove the leading "/assets/" portion to get the relative path.
        if entry.startswith("/assets/"):
            rel_path = entry[len("/assets/"):]
        else:
            rel_path = entry

        # Construct the full path to the main file.
        main_path = os.path.join(assets_dir, rel_path)
        
        # Determine whether a corresponding .webp version exists for the main file.
        if has_webp_version(main_path):
            # Delete the original main file if it exists.
            if os.path.exists(main_path) and should_delete_file(main_path):
                try:
                    os.remove(main_path)
                    print(f"Deleted original: {main_path}")
                except Exception as e:
                    print(f"Error deleting {main_path}: {e}")
            else:
                print(f"Original file already deleted or not eligible: {main_path}")
            
            # Now, construct and delete the -master version.
            dir_name, filename = os.path.split(main_path)
            master_filename = insert_suffix(filename, "-master")
            master_path = os.path.join(dir_name, master_filename)
            if os.path.exists(master_path) and should_delete_file(master_path):
                try:
                    os.remove(master_path)
                    print(f"Deleted master backup: {master_path}")
                except Exception as e:
                    print(f"Error deleting {master_path}: {e}")
            else:
                print(f"Master backup not found or not eligible: {master_path}")
        else:
            print(f"Skipping deletion (no WebP found): {main_path}")
    
    print("Deletion process completed.")

if __name__ == '__main__':
    delete_non_webp_files()
