import os
import sys
import re
import json
import html
from urllib.parse import unquote

# Insert the _build_process directory into sys.path so Python can find it.
project_root = os.path.dirname(os.path.abspath(__file__))
build_process_path = os.path.join(project_root, '_build_process')
sys.path.insert(0, build_process_path)

# Now import the reset function from part0_dist_refresh.py
from part0_dist_refresh import reset_dist
reset_dist(reset_flag=True)



from part1_edge_cases import process_links_json

# Define flag
ONLY_WRITE_CHANGES = False  # Set to False to actually perform the copy and update

#############################################
# Directory Definitions and Log File Setup
#############################################

# External assets library folder
original_assets_source_dir = '/Users/kevincameron/Documents/onelifejapan_static_2023/redesign/assets'

# Repository directories
abs_path = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025'
dist_dir = os.path.join(abs_path, 'dist')
assets_dir = os.path.join(dist_dir, 'assets')

# Log Files
output_file = os.path.join(abs_path, '_build_process', 'dist_changes.txt')
found_images_file = os.path.join(abs_path, '_build_process', 'dist_found_images.txt')
copy_log_file = os.path.join(abs_path, '_build_process', 'dist_copy_log.txt')
sliderimage_log_file = os.path.join(abs_path, '_build_process', 'sliderimage_log_file.txt')
manifest_file = os.path.join(abs_path, '_build_process', 'images_manifest.txt')
# Set to store image URLs collected from HTML files
image_urls = set()

# Ensure assets directory exists
os.makedirs(assets_dir, exist_ok=True)

# Initialize the output log files
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('Changes to be made:\n\n')
with open(found_images_file, 'w', encoding='utf-8') as f:
    f.write('Found image references:\n\n')
with open(copy_log_file, 'w', encoding='utf-8') as f:
    f.write('Copy log:\n\n')
with open(sliderimage_log_file, 'w', encoding='utf-8') as f:
    f.write('sliderimage_log_file log:\n\n')

#############################################
# FUNCTION: process_html_files
# Main Responsibility: Process all HTML files in the 'dist' directory by
#   - Removing absolute asset paths.
#   - Collecting all image URLs (those starting with /assets/).
#   - Overwriting the HTML files with the updated content.
#############################################
def process_html_files():
    global image_urls
    # Walk through all files in the dist directory
    for root, dirs, files in os.walk(dist_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    continue  # Skip non-text files

                print(f'Processing HTML file: {file_path}')

                # Remove absolute URLs such as "http://localhost:3020" and IP-based URLs
                content = content.replace('http://localhost:3020', '')
                content = re.sub(r'http://192\.168\.128\.\d+:\d+', '', content)
                content = content.replace("//assets/", "/assets/")
    
                # Find all standard asset URLs in the content.
                matches = re.findall(r'(/assets/[^"\'\s]+)', content)
                for match in matches:
                    # Skip matches that contain the encoded comma separator
                    if "&#34;,&#34;" in match or "," in match:
                        continue
                    # Simply collect the URL without further normalization.
                    image_urls.add(match)
                    # Log the found reference.
                    with open(found_images_file, 'a', encoding='utf-8') as out_f:
                        out_f.write(f'{file_path} - Found image reference {match}\n')
                    with open(output_file, 'a', encoding='utf-8') as out_f:
                        out_f.write(f'{file_path} - Updated image reference {match}\n')
                
                # **** Extra Edge-Case Processing ****
                # Call the edge-case function to extract additional URLs from data-linksjson attributes.
                extra_urls = process_links_json(content)
                for url in extra_urls:
                    image_urls.add(url)
                    with open(found_images_file, 'a', encoding='utf-8') as out_f:
                        out_f.write(f'{file_path} - (Edge Case) Found image reference {url}\n')
                    with open(output_file, 'a', encoding='utf-8') as out_f:
                        out_f.write(f'{file_path} - (Edge Case) Updated image reference {url}\n')
                # *************************************


                # Write the updated HTML content back to the file.
                if not ONLY_WRITE_CHANGES:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
    return image_urls

#############################################
# FUNCTION: copy_images
# Main Responsibility: Copy image files from the external assets library to the
#   dist/assets folder using the paths as referenced in the HTML.
#############################################
def copy_images(image_url_set):
    for img_url in image_url_set:
        # Get the relative path by removing the "/assets/" prefix.
        relative_path = img_url.replace('/assets/', '')
        new_img_path = os.path.join(assets_dir, relative_path)
        os.makedirs(os.path.dirname(new_img_path), exist_ok=True)

        # Decode URL to handle encoding issues.
        decoded_url = unquote(relative_path)
        local_img_path = os.path.join(original_assets_source_dir, decoded_url)
        safe_local_img_path = os.path.join(original_assets_source_dir, decoded_url.replace('%20', ' ').replace(' ', '_'))
        
        if os.path.exists(local_img_path):
            with open(local_img_path, 'rb') as src_file:
                with open(new_img_path, 'wb') as dst_file:
                    dst_file.write(src_file.read())
            with open(copy_log_file, 'a', encoding='utf-8') as log_f:
                log_f.write(f'Copied {local_img_path} to {new_img_path}\n')
        elif os.path.exists(safe_local_img_path):
            with open(safe_local_img_path, 'rb') as src_file:
                with open(new_img_path, 'wb') as dst_file:
                    dst_file.write(src_file.read())
            with open(copy_log_file, 'a', encoding='utf-8') as log_f:
                log_f.write(f'Copied {safe_local_img_path} to {new_img_path}\n')
        else:
            print(f'--')
            print(f'File not found: {local_img_path} or {safe_local_img_path}')
            print('')


#############################################
# FUNCTION: normalize_files_and_html
# Final Step: For any file paths that contain "%20", rename the file on disk in assets
# and update the HTML files to use the normalized (underscore) version.
#############################################
def normalize_files_and_html():
    # Get list of normalized files from manifest (or from the image_urls set)
    normalized_paths = [url for url in image_urls if "%20" in url]
    for norm_url in normalized_paths:
        print(f'---')
        print(f'norm_url {norm_url}')
        # Build the old path (as in the manifest and in HTML)
        old_path = f'{assets_dir}{norm_url}'
        old_path = old_path.replace('assets/assets', 'assets')
        # Create the normalized version: replace '%20' with '_'
        normalized_url = norm_url.replace('%20', '_')
        # print(f'norm_url:       {norm_url}')
        # print(f'normalized_url: {normalized_url}')

        #new_path = os.path.join(assets_dir, normalized_url)
        new_path = f'{assets_dir}{normalized_url}'
        new_path = new_path.replace('assets/assets', 'assets')
        if os.path.exists(old_path):
            # print(f'old_path {old_path}')
            # print(f'new_path {new_path}')
            os.rename(old_path, new_path)
            # print(f'Renamed file: {old_path} -> {new_path}')
            with open(copy_log_file, 'a', encoding='utf-8') as log_f:
                log_f.write(f'Renamed file: {old_path} -> {new_path}\n')
            # Now update each HTML file in dist that refers to norm_url,
            # replacing it with normalized_url.
            for root, dirs, files in os.walk(dist_dir):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if norm_url in content:
                            updated_content = content.replace(norm_url, normalized_url)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(updated_content)
                            print(f'Updated {file_path}: replaced {norm_url} with {normalized_url}')
        else:
            print(f'assets_dir: {assets_dir}')
            print(f'File to rename not found: {old_path}')


#############################################
# MAIN Execution Section
# Run the steps sequentially:
#   1. Process HTML files to update paths and collect image URLs.
#   2. Write a manifest file.
#   3. Copy images from the external library into the build's assets directory.
#   4. Normalize files and update HTML references (if any paths contain "%20").
#############################################
if __name__ == '__main__':
    # Step 1: Process HTML files – update references and collect image URLs.
    collected_image_urls = process_html_files()
    with open(manifest_file, 'w', encoding='utf-8') as mf:
        for url in collected_image_urls:
            normalized = url.replace('%20', '_').replace(' ', '_')
            mf.write(f'{normalized}\n')
        
    # Step 2: Copy images from the library into the dist/assets folder.
    copy_images(collected_image_urls)
    
    # Optionally log the final list of image URLs.
    with open(output_file, 'a', encoding='utf-8') as out_f:
        out_f.write('\nFinal list of image URLs:\n\n')
        for img_url in collected_image_urls:
            out_f.write(f'{img_url}\n')
    
    # Step 4: Normalize files (rename files on disk and update HTML) for paths with "%20".
    normalize_files_and_html()
    
    
    print(f'Changes recorded in {output_file}.')
    print(f'Found image references recorded in {found_images_file}.')
    print(f'Copy operations recorded in {copy_log_file}.')
