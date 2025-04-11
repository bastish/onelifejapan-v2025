import os
import re
import requests
import json
import html
from urllib.parse import unquote

# Define flag
ONLY_WRITE_CHANGES = False  # Set to False to actually perform the copy and update

#############################################
# 1. Directory Definitions
#############################################

# Get files from this external directory
original_assets_source_dir = '/Users/kevincameron/Documents/onelifejapan_static_2023/redesign/assets'

# this repositorry directories
abs_path = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025'
dist_dir = os.path.join(abs_path, 'dist')
assets_dir = os.path.join(dist_dir, 'assets')
# Log Files
output_file = os.path.join(abs_path, '_build_process', 'dist_changes.txt')
found_images_file =  os.path.join(abs_path, '_build_process', 'dist_found_images.txt')
copy_log_file = os.path.join(abs_path, '_build_process', 'dist_copy_log.txt')
sliderimage_log_file = os.path.join(abs_path, '_build_process', 'sliderimage_log_file.txt')

image_urls = set()


# Ensure assets directory exists
os.makedirs(assets_dir, exist_ok=True)

# Initialize the output files
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('Changes to be made:\n\n')

with open(found_images_file, 'w', encoding='utf-8') as f:
    f.write('Found image references:\n\n')

with open(copy_log_file, 'w', encoding='utf-8') as f:
    f.write('Copy log:\n\n')

with open(sliderimage_log_file, 'w', encoding='utf-8') as f:
    f.write('sliderimage_log_file log:\n\n')


# Helper function to add image URL
def add_image_url(url, file_path):
    image_urls.add(url)
    relative_path = url.replace('/assets/', '')
    safe_relative_path = relative_path.replace('%20', '_').replace(' ', '_')  # Replace spaces with underscores
    with open(output_file, 'a', encoding='utf-8') as out_f:
        out_f.write(f'{file_path} - Replace {url} with /assets/{safe_relative_path}\n')
    with open(found_images_file, 'a', encoding='utf-8') as out_f:
        out_f.write(f'{file_path} - Found image reference {url}\n')

# Function to copy image from project assets to dist/assets and handle renaming
def copy_and_save_image(url, safe_relative_path):
    if not url.startswith('/assets/'):
        #print(f"Skipping URL (not a relative asset): {url}")
        return

    # Skip if the URL seems to include multiple URLs (e.g. contains commas).
    if ',' in url:
        #print(f"Skipping multi-part URL: {url}")
        return
    if '/http://' in url:
        #print(f"Skipping /http://t URL: {url}")
        return

    # Decode URL to handle any encoding issues
    decoded_url = unquote(url.replace('/assets/', ''))
    local_img_path = os.path.join(original_assets_source_dir, decoded_url)
    safe_local_img_path = os.path.join(original_assets_source_dir, decoded_url.replace('%20', ' ').replace(' ', '_'))
    
    new_img_path = os.path.join(assets_dir, safe_relative_path)
    os.makedirs(os.path.dirname(new_img_path), exist_ok=True)
    
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
        print(f'File not found: {local_img_path} or {safe_local_img_path}')

# Function to process all text files
def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return  # Skip non-text files

    print('')
    print(f'processing {file_path}')
    
    # Find all relative URLs in the content
    matches = re.findall(r'(/assets/[^"\'\s]+)', content)
    for match in matches:
        decoded_match = unquote(match)  # Decode URL to handle any encoding issues
        safe_match = decoded_match.replace('%20', '_').replace(' ', '_')  # Make URL safe by replacing spaces and %20 with underscores
        add_image_url(match, file_path)
        if not ONLY_WRITE_CHANGES:
            content = content.replace(match, safe_match)

    # Process JSON attributes for data-slider-images
    def slider_replacer(m):
        attr_value = m.group(1)  # Get the attribute content
        # Unescape HTML entities so that &#34; becomes "
        decoded_value = html.unescape(attr_value)
        try:
            urls = json.loads(decoded_value)
        except Exception as e:
            print(f"Error parsing JSON in {file_path}: {e}")
            return m.group(0)  # Return the original attribute if parsing fails

        with open(sliderimage_log_file, 'a', encoding='utf-8') as out_f:
            out_f.write(f'{file_path} - Found attr_value reference {attr_value}\n')

        new_urls = []
        for url in urls:
            # Process each individual URL:
            safe_url = url.replace('%20', '_').replace(' ', '_')
            # Remove base references if present.
            safe_url = safe_url.replace('http://localhost:3020', '')
            safe_url = re.sub(r'http://192\.168\.128\.\d+:\d+', '', safe_url)
            new_urls.append(safe_url)

            with open(sliderimage_log_file, 'a', encoding='utf-8') as out_f:
                out_f.write(f'{file_path} - Found image reference {safe_url}\n')

            add_image_url(url, file_path)  # Log the original URL

        new_json = json.dumps(new_urls)
        # Escape new_json so it can be safely output as an HTML attribute value.
        new_attr = html.escape(new_json, quote=True)
        return f'data-slider-images="{new_attr}"'

    content = re.sub(r'data-slider-images="([^"]+)"', slider_replacer, content)
    content = content.replace("//assets/", "/assets/")
    # Remove localhost URL references
    content = content.replace('http://localhost:3020', '')
    content = re.sub(r'http://192\.168\.128\.\d+:\d+', '', content)

    # Write updated content back to file
    if not ONLY_WRITE_CHANGES:
        with open(file_path, 'w', encoding='utf-8') as updated_f:
            updated_f.write(content)

# Process all files in the dist directory
for root, dirs, files in os.walk(dist_dir):
    for file in files:
        file_path = os.path.join(root, file)
        process_file(file_path)

# Copy all collected images to dist/assets
for img_url in image_urls:
    relative_path = img_url.replace('/assets/', '')
    safe_relative_path = relative_path.replace('%20', '_').replace(' ', '_')  # Replace spaces with underscores
    copy_and_save_image(img_url, safe_relative_path)

# Write the image URLs to be downloaded
with open(output_file, 'a', encoding='utf-8') as out_f:
    out_f.write('\nImages to be downloaded:\n\n')
    for img_url in image_urls:
        relative_path = img_url.replace('/assets/', '')
        safe_relative_path = relative_path.replace('%20', '_').replace(' ', '_')  # Replace spaces with underscores
        out_f.write(f'{img_url} -> {os.path.join(assets_dir, safe_relative_path)}\n')

print(f'Changes recorded in {output_file}.')
print(f'Found image references recorded in {found_images_file}.')
print(f'Copy operations recorded in {copy_log_file}.')
if not ONLY_WRITE_CHANGES:
    print('Images copied and paths updated.')
