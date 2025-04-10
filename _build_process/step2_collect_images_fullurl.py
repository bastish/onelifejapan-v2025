import os
import re
import requests
from urllib.parse import unquote

# Define flag
ONLY_WRITE_CHANGES = False  # Set to False to actually perform the copy and update

# Define directories
dist_dir = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/dist'
assets_dir = os.path.join(dist_dir, 'assets')
project_assets_dir = 'assets'  # Directory where original assets are stored
image_urls = set()
output_file = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/_build_process/dist_changes.txt'
found_images_file = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/_build_process/dist_found_images.txt'
copy_log_file = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/_build_process/dist_copy_log.txt'
sliderimage_log_file = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/_build_process/dist_sliderimage_log_file.txt'


# Ensure assets directory exists
os.makedirs(assets_dir, exist_ok=True)

# Initialize the output files
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('Changes to be made:\n\n')

with open(found_images_file, 'w', encoding='utf-8') as f:
    f.write('Found image references:\n\n')

with open(copy_log_file, 'w', encoding='utf-8') as f:
    f.write('Copy log:\n\n')

## ADDED FOR THE 2021 LINKS
## ADDED FOR THE 2021 LINKS
## ADDED FOR THE 2021 LINKS
## ADDED FOR THE 2021 LINKS
## ADDED FOR THE 2021 LINKS
def replace_base_url_in_file(file_path, base_url="https://www.onelifejapan.com/2021/", replacement="/"):
    """
    Replaces occurrences of a specified base URL in a file with a new path or empty string.
    
    Args:
        file_path (str): Path to the file to process.
        base_url (str): The URL to be replaced.
        replacement (str): The replacement value (default is "/").
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return  # Skip non-text files
    
    # Replace all occurrences of the base URL
    updated_content = content.replace(base_url, replacement)
    
    # Write changes back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f'Updated file: {file_path}')


## ADDED FOR THE 2021 LINKS
## ADDED FOR THE 2021 LINKS
## ADDED FOR THE 2021 LINKS
## ADDED FOR THE 2021 LINKS
## ADDED FOR THE 2021 LINKS

# Helper function to add image URL
def add_image_url(url, file_path):
    image_urls.add(url)
    relative_path = url.replace('http://localhost:3020/assets/', '')
    safe_relative_path = relative_path.replace(' ', '_')  # Replace spaces with underscores
    with open(output_file, 'a', encoding='utf-8') as out_f:
        out_f.write(f'{file_path} - Replace {url} with /assets/{safe_relative_path}\n')
    with open(found_images_file, 'a', encoding='utf-8') as out_f:
        out_f.write(f'{file_path} - Found image reference {url}\n')
    if not ONLY_WRITE_CHANGES:
        copy_and_save_image(url, safe_relative_path)

# Function to copy image from project assets to dist/assets and handle renaming
def copy_and_save_image(url, safe_relative_path):
    local_img_path = os.path.join(project_assets_dir, url.replace('http://localhost:3020/assets/', ''))
    new_img_path = os.path.join(assets_dir, safe_relative_path)
    os.makedirs(os.path.dirname(new_img_path), exist_ok=True)
    if os.path.exists(local_img_path):
        with open(local_img_path, 'rb') as src_file:
            with open(new_img_path, 'wb') as dst_file:
                dst_file.write(src_file.read())
        with open(copy_log_file, 'a', encoding='utf-8') as log_f:
            log_f.write(f'Copied {local_img_path} to {new_img_path}\n')
    else:
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(new_img_path, 'wb') as img_file:
                img_file.write(response.content)
            with open(copy_log_file, 'a', encoding='utf-8') as log_f:
                log_f.write(f'Downloaded {url} to {new_img_path}\n')
        except requests.exceptions.RequestException as e:
            print(f'Failed to download {url}: {e}')

# Function to process all text files
def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return  # Skip non-text files

    print('')
    print(f'processing {file_path}')
    # Find all URLs in the content
    matches = re.findall(r'http://localhost:3020/assets/[^"\'\s]+', content)
    for match in matches:
        print(f'-- found {match}')
        match = unquote(match)  # Decode URL to handle any encoding issues
        add_image_url(match, file_path)
        if not ONLY_WRITE_CHANGES:
            safe_match = match.replace('http://localhost:3020/assets/', '/assets/').replace(' ', '_')
            content = content.replace(match, safe_match)
    
    # Find all relative URLs in the content
    matches_relative = re.findall(r'url\(["\']?(/assets/[^"\'\)]+)["\']?\)', content)
    for match in matches_relative:
        full_match = 'http://localhost:3020' + match  # Convert to full URL
        match = unquote(match)  # Decode URL to handle any encoding issues
        add_image_url(full_match, file_path)
        if not ONLY_WRITE_CHANGES:
            safe_match = match.replace('/assets/', '/assets/').replace(' ', '_')
            content = content.replace(match, safe_match)

    # Write updated content back to file
    if not ONLY_WRITE_CHANGES:
        with open(file_path, 'w', encoding='utf-8') as updated_f:
            updated_f.write(content)

# Process all files in the dist directory
for root, dirs, files in os.walk(dist_dir):
    for file in files:
        file_path = os.path.join(root, file)
        ## ADDED FOR THE 2021 LINKS
        replace_base_url_in_file(file_path)
        
        ## ORIGINAL
        process_file(file_path)

# Copy all collected images to dist/assets
for img_url in image_urls:
    relative_path = img_url.replace('http://localhost:3020/assets/', '')
    safe_relative_path = relative_path.replace(' ', '_')  # Replace spaces with underscores
    copy_and_save_image(img_url, safe_relative_path)

# Write the image URLs to be downloaded
with open(output_file, 'a', encoding='utf-8') as out_f:
    out_f.write('\nImages to be downloaded:\n\n')
    for img_url in image_urls:
        relative_path = img_url.replace('http://localhost:3020/assets/', '')
        safe_relative_path = relative_path.replace(' ', '_')  # Replace spaces with underscores
        out_f.write(f'{img_url} -> {os.path.join(assets_dir, safe_relative_path)}\n')

print(f'Changes recorded in {output_file}.')
print(f'Found image references recorded in {found_images_file}.')
print(f'Copy operations recorded in {copy_log_file}.')
if not ONLY_WRITE_CHANGES:
    print('Images copied and paths updated.')
