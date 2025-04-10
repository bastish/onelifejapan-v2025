import os
import re
from PIL import Image, ImageOps
from collections import defaultdict

# Define directories
dist_dir = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/dist'
assets_dir = os.path.join(dist_dir, 'assets')
output_file = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/_build_process/dist_image_resizing_changes.txt'
copy_log_file = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/_build_process/dist_image_resizing_copy_log.txt'

# Ensure assets directory exists
os.makedirs(assets_dir, exist_ok=True)

# Initialize the output files
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('Image resizing changes to be made:\n\n')

with open(copy_log_file, 'w', encoding='utf-8') as f:
    f.write('Image resizing copy log:\n\n')

# Dictionary to store images and their required sizes
images = defaultdict(lambda: {"sizes": set()})

# Function to process each image and height pair one at a time
def process_image_height_pair(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    #pattern = re.compile(r'(background-image:\s*url\(["\']?(/assets/[^"\'\)]+)["\']?\);.*?height:\s*(\d+px);)', re.DOTALL)
    
    pattern = re.compile(
        r'(background-image:\s*url\(["\']?(/assets/(?!blog/)[^"\'\s]+)["\']?\);.*?height:\s*(\d+px);)',
        re.DOTALL
    )
    matches = pattern.findall(content)

    for full_match, url, height_str in matches:
        height = int(height_str.replace('px', ''))
        if f'-{height}px' in url:
            continue  # Skip if the image URL already has the correct size suffix

        safe_relative_path = url.replace('/assets/', '').replace(' ', '_')
        new_url = f'/assets/{os.path.splitext(safe_relative_path)[0]}-{height}px.jpg'
        images[url]["sizes"].add(height)  # Track sizes

        # Replace only this specific instance
        updated_content = content.replace(full_match, full_match.replace(url, new_url), 1)
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        # Recursively process the next pair after updating the file
        process_image_height_pair(file_path)
        break

# Helper function to resize images
# def resize_image(img, height=None):
#     if height:
#         img = ImageOps.fit(img, (img.width * height // img.height, height), Image.ANTIALIAS)
#     return img
def resize_image(img, height=None):
    if height:
        new_size = (img.width * height // img.height, height)
        # Use Image.Resampling.LANCZOS instead of Image.ANTIALIAS
        img = ImageOps.fit(img, new_size, method=Image.Resampling.LANCZOS)
    return img


# Function to resize and save images
def resize_and_save_images():
    for url, data in images.items():
        relative_path = url.replace('/assets/', '')
        local_img_path = os.path.join(assets_dir, relative_path)
        
        if os.path.exists(local_img_path):
            for height in data["sizes"]:
                new_img_path = os.path.join(assets_dir, f'{os.path.splitext(relative_path)[0]}-{height}px.jpg')
                os.makedirs(os.path.dirname(new_img_path), exist_ok=True)
                
                if not os.path.exists(new_img_path):
                    with open(local_img_path, 'rb') as src_file:
                        img = Image.open(src_file)
                        img = resize_image(img, height=height)
                        img.save(new_img_path, optimize=True, quality=85)
                    
                    with open(copy_log_file, 'a', encoding='utf-8') as log_f:
                        log_f.write(f'Resized {local_img_path} to {new_img_path}\n')
        else:
            print(f'Failed to find {local_img_path} for resizing.')

# Process all HTML files in the dist directory to gather URLs and sizes
for root, dirs, files in os.walk(dist_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            print(f"processing {file_path}")
            process_image_height_pair(file_path)

# Resize and save images based on gathered information
resize_and_save_images()

print(f'Image resizing changes recorded in {output_file}.')
print(f'Image resizing operations recorded in {copy_log_file}.')
print('Images resized and paths updated.')
