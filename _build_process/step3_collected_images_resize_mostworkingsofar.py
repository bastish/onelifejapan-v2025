import os
import re
from PIL import Image, ImageOps
from collections import defaultdict

#############################################
# 1. Directory Definitions
#############################################
abs_path = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025'
dist_dir = os.path.join(abs_path, 'dist')
assets_dir = os.path.join(dist_dir, 'assets')
output_file = os.path.join(abs_path, '_build_process', 'dist_image_resizing_changes.txt')
copy_log_file = os.path.join(abs_path, '_build_process', 'dist_image_resizing_copy_log.txt')

os.makedirs(assets_dir, exist_ok=True)

#############################################
# 2. Initialize Log Files
#############################################
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('Image resizing changes to be made:\n\n')
with open(copy_log_file, 'w', encoding='utf-8') as f:
    f.write('Image resizing copy log:\n\n')

#############################################
# 3. Data Structure to Record Desired Dimensions
#############################################
# Each image URL (as found in HTML) maps to a set of recorded sizes.
images = defaultdict(lambda: {"sizes": set()})

#############################################
# 4. Regex Patterns to Identify Image References in HTML
#############################################
# (a) Background images in CSS; record the desired height.
pattern_bg = re.compile(
    r'background-image:\s*url\(["\']?(?P<url>/assets/(?!blog/)[^"\'\s]+)["\']?\).*?height:\s*(?P<height>\d+)(?:px)?\s*;',
    re.DOTALL | re.IGNORECASE
)

# (b) <img> tags. Note: We relax the width matching to accept an optional "px".
pattern_img = re.compile(
    r'<img\s+[^>]*?src=["\'](?P<url>/assets/(?!blog/)[^"\']+)["\'](?P<attrs>[^>]*?)>',
    re.IGNORECASE | re.DOTALL
)

#############################################
# 5. Utility Function: Update <img> Tag Attributes
#############################################
def update_img_tag(tag, new_src, new_width, new_height):
    """
    Update <img> tag by replacing:
      - The src attribute with new_src,
      - The width attribute to new_width (adds px if missing),
      - The height attribute to new_height (adds px if missing).
    """
    # Replace the src attribute.
    tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{new_src}"', tag)
    # Update or add the width attribute.
    if re.search(r'width=["\']\d+(?:px)?["\']', tag):
        tag = re.sub(r'width=["\']\d+(?:px)?["\']', f'width="{new_width}px"', tag)
    else:
        tag = tag.replace('>', f' width="{new_width}px">', 1)
    # Update or add the height attribute.
    if re.search(r'height=["\']\d+(?:px)?["\']', tag):
        tag = re.sub(r'height=["\']\d+(?:px)?["\']', f'height="{new_height}px"', tag)
    else:
        tag = tag.replace('>', f' height="{new_height}px">', 1)
    return tag

#############################################
# 6. HTML Processing: Recording Dimensions and Updating HTML
#############################################
def process_file(file_path):
    """
    Read an HTML file, record desired dimensions from:
      - CSS background-image rules (recorded as height), and
      - <img> tags (recorded as width if available, or determined from asset file).
    For <img> tags the tag is updated to use the new optimized image filename.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Skipping non-text file: {file_path}")
        return

    original_content = content
    # Normalize URLs if necessary.
    content = content.replace("//assets/", "/assets/")

    # (a) Process CSS background images.
    def bg_replacer(match):
        url = match.group('url')
        height = int(match.group('height'))
        images[url]["sizes"].add((height, "height"))
        log_line = f'{file_path} - Background image {url}: desired height = {height}px'
        print(log_line)
        with open(output_file, 'a', encoding='utf-8') as outf:
            outf.write(log_line + "\n")
        # Generate the new URL using the height.
        safe_relative_path = url.replace('/assets/', '').replace('%20', '_').replace(' ', '_')
        new_url = f'/assets/{os.path.splitext(safe_relative_path)[0]}-{height}px.jpg'
        # Replace the original URL with the new URL in the matched string.
        updated_bg = match.group(0).replace(url, new_url)
        return updated_bg
    content = pattern_bg.sub(bg_replacer, content)

    # (b) Process <img> tags.
    def img_replacer(match):
        full_tag = match.group(0)
        url = match.group('url')
        attrs = match.group('attrs')

        dimension = None
        dim_type = "width"  # Default to width
        
        # Step 1: Look for a width attribute (allowing optional "px").
        width_match = re.search(r'width=["\'](\d+)(?:px)?["\']', attrs)
        if width_match:
            dimension = int(width_match.group(1))
            print(f'Found explicit width for {url}: {dimension}px')
        else:
            # Step 2: Look for inline style with max-width.
            style_width_match = re.search(r'max-width:\s*(\d+)(?:px)?', attrs)
            if style_width_match:
                dimension = int(style_width_match.group(1))
                print(f'Found inline max-width for {url}: {dimension}px')

        # Step 3: If no width information, try opening the image to get its size.
        if dimension is None:
            local_img_path = os.path.join(assets_dir, url.replace('/assets/', ''))
            if os.path.exists(local_img_path):
                try:
                    with open(local_img_path, 'rb') as src_file:
                        img_obj = Image.open(src_file)
                        orig_w, _ = img_obj.size
                        dimension = 500 if orig_w > 500 else orig_w
                        print(f'No width in HTML for {url}; using default width: {dimension}px (orig: {orig_w}px)')
                except Exception as e:
                    print(f"Error opening {local_img_path}: {e}")
            else:
                print(f"Asset file not found for {url}.")
        
        # If still no dimension, skip tag update.
        if not dimension:
            print(f'No width found for <img> {url}. Leaving tag unchanged.')
            return full_tag

        # Record the dimension (we record as width for <img> tags).
        images[url]["sizes"].add((dimension, "width"))
        
        # Step 4: Compute the new optimized file URL.
        # Generate a safe relative path and then add the suffix '-{dimension}px'
        safe_relative_path = url.replace('/assets/', '').replace('%20', '_').replace(' ', '_')
        new_url = f'/assets/{os.path.splitext(safe_relative_path)[0]}-{dimension}px.jpg'
        
        # Step 5: Open the asset file to compute new height from aspect ratio.
        local_img_path = os.path.join(assets_dir, url.replace('/assets/', ''))
        new_height = 0
        if os.path.exists(local_img_path):
            try:
                with open(local_img_path, 'rb') as src_file:
                    img_obj = Image.open(src_file)
                    orig_w, orig_h = img_obj.size
                    new_height = round(orig_h * (dimension / orig_w))
                    print(f'{url}: original {orig_w}x{orig_h} -> new {dimension}x{new_height}')
            except Exception as e:
                print(f"Error reading {local_img_path}: {e}")
        else:
            print(f"Asset file for {url} not found. Setting height to 0.")

        log_line = (f'{file_path} - <img> {url}: width = {dimension}px, computed height = {new_height}px; '
                    f'new src: {new_url}')
        with open(output_file, 'a', encoding='utf-8') as outf:
            outf.write(log_line + "\n")
        print(log_line)

        # Step 6: Update the tag with new src, width, and height.
        new_tag = update_img_tag(full_tag, new_url, dimension, new_height)
        return new_tag

    content = pattern_img.sub(img_replacer, content)

    # Only write back if changes occurred.
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated HTML file: {file_path}")

#############################################
# 7. Image Resizing Functions
#############################################
def resize_image(img, *, height=None, width=None):
    """
    Resize an image while preserving aspect ratio.
    Supply either a target height or width.
    """
    if height:
        new_size = (img.width * height // img.height, height)
        return ImageOps.fit(img, new_size, method=Image.Resampling.LANCZOS)
    elif width:
        new_size = (width, img.height * width // img.width)
        return ImageOps.fit(img, new_size, method=Image.Resampling.LANCZOS)
    return img

def resize_and_save_images():
    """
    For every recorded image URL, open the asset, resize based on the recorded dimension (choosing
    the smallest value if multiple are recorded), and save the optimized file.
    """
    for url, data in images.items():
        # Build a safe file name portion.
        safe_relative_path = url.replace('/assets/', '').replace('%20', '_').replace(' ', '_')
        # Choose the smallest dimension if several exist.
        desired_dims = [dimension for (dimension, _) in data["sizes"]]
        if not desired_dims:
            print(f"No recorded dimension for {url}. Skipping.")
            continue
        target_dim = min(desired_dims)
        # Determine type; if any “height” match is recorded at this dimension, use height,
        # otherwise assume width.
        types = [typ for (dim, typ) in data["sizes"] if dim == target_dim]
        target_type = "height" if "height" in types else "width"

        new_img_path = os.path.join(assets_dir, f'{os.path.splitext(safe_relative_path)[0]}-{target_dim}px.jpg')
        print(f"Resizing {url}: target {target_type} = {target_dim}px => {new_img_path}")
        try:
            local_img_path = os.path.join(assets_dir, url.replace('/assets/', ''))
            with open(local_img_path, 'rb') as src_file:
                img = Image.open(src_file)
                if target_type == "height":
                    img = resize_image(img, height=target_dim)
                else:
                    img = resize_image(img, width=target_dim)
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    img = img.convert("RGB")
                img.save(new_img_path, optimize=True, quality=85)
            log_line = f"Resized {local_img_path} to {new_img_path} (using {target_type} = {target_dim}px)"
            with open(copy_log_file, 'a', encoding='utf-8') as log_f:
                log_f.write(log_line + "\n")
            print(log_line)
        except Exception as e:
            print(f"Error resizing image for {url}: {e}")

#############################################
# 8. Process HTML Files and Resize Images
#############################################
for root, dirs, files in os.walk(dist_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            print(f"Processing HTML file: {file_path}")
            process_file(file_path)

resize_and_save_images()

#############################################
# 9. Final Log Message
#############################################
print(f'\nChanges logged in {output_file}')
print(f'Resize operations logged in {copy_log_file}')
print('Processing complete: Images optimized and HTML updated.')
