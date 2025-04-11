import os
import re
from PIL import Image, ImageOps
from collections import defaultdict

#############################################
# Directory Definitions
#############################################
abs_path = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025'
dist_dir = os.path.join(abs_path, 'dist')
assets_dir = os.path.join(dist_dir, 'assets')
output_file = os.path.join(abs_path, '_build_process', 'dist_image_resizing_changes.txt')
copy_log_file = os.path.join(abs_path, '_build_process', 'dist_image_resizing_copy_log.txt')

# Ensure assets directory exists
os.makedirs(assets_dir, exist_ok=True)

# Initialize the output files (overwrite any previous content)
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('Image resizing changes to be made:\n\n')
with open(copy_log_file, 'w', encoding='utf-8') as f:
    f.write('Image resizing copy log:\n\n')

# Dictionary to store images and their desired dimensions.
# For each image URL (as found in HTML) the "sizes" set holds tuples: (dimension, type)
# where type is "width" or "height". Later, if multiple dimensions are recorded for one image,
# we choose the minimum dimension (the most optimized, smallest version).
images = defaultdict(lambda: {"sizes": set()})

###############################################################################
# Regex Patterns
###############################################################################

# Pattern for CSS background-image references that include a height property.
# Example: background-image: url('/assets/...'); ... height: 400px;
pattern_bg = re.compile(
    r'background-image:\s*url\(["\']?(?P<url>/assets/(?!blog/)[^"\'\s]+)["\']?\);.*?height:\s*(?P<height>\d+)px;',
    re.DOTALL
)

# Pattern for <img> tags.
pattern_img = re.compile(
    r'<img\s+[^>]*?src=["\'](?P<url>/assets/(?!blog/)[^"\']+)["\'](?P<attrs>[^>]*?)>',
    re.IGNORECASE | re.DOTALL
)

###############################################################################
# File Processing Function (Reads HTML and records desired dimensions)
###############################################################################
def process_file(file_path):
    """
    Parse an HTML file to record (but not update) the desired dimensions for each image.
    This version does not modify the HTML because we want to work in-place with the original file names.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Skipping non-text file: {file_path}")
        return

    # Normalize any "//assets/" to "/assets/"
    content = content.replace("//assets/", "/assets/")

    ############################################
    # Process CSS background-image references
    # (We record the height as the desired dimension for this image.)
    ############################################
    def bg_replacer(match):
        url = match.group('url')
        height = int(match.group('height'))
        # Record the desired height for this image.
        images[url]["sizes"].add((height, "height"))
        log_line = f'{file_path} - For background image {url}, desired height: {height}px'
        print(log_line)
        with open(output_file, 'a', encoding='utf-8') as outf:
            outf.write(log_line + "\n")
        return match.group(0)  # No change to HTML

    content = pattern_bg.sub(bg_replacer, content)

    ############################################
    # Process <img> tags
    # (We record the width from a width attribute or max-width style.
    #  If no dimension is found but the URL contains "chart", default to 650px.)
    ############################################
    def img_replacer(match):
        url = match.group('url')
        attrs = match.group('attrs')

        dimension = None
        dim_type = None

        # Look for an explicit width attribute (e.g., width="620px")
        width_match = re.search(r'width=["\'](\d+)px["\']', attrs)
        if width_match:
            dimension = int(width_match.group(1))
            dim_type = "width"
            print(f'Explicit width for {url}: {dimension}px')
        else:
            # Look for an inline style with max-width (e.g., max-width: 400px)
            style_width_match = re.search(r'max-width:\s*(\d+)px', attrs)
            if style_width_match:
                dimension = int(style_width_match.group(1))
                dim_type = "width"
                print(f'max-width for {url}: {dimension}px')

        # If no dimension found and the URL contains "chart", use default width 650px.
        if dimension is None and "chart" in url:
            dimension = 650
            dim_type = "width"
            print(f'No dimension found for chart URL {url}, defaulting to width: {dimension}px')

        if dimension:
            images[url]["sizes"].add((dimension, dim_type))
            log_line = f'{file_path} - For <img> {url}, desired {dim_type}: {dimension}px'
            print(log_line)
            with open(output_file, 'a', encoding='utf-8') as outf:
                outf.write(log_line + "\n")
        else:
            print(f'No dimension found for <img> {url}')

        return match.group(0)  # No change to HTML

    content = pattern_img.sub(img_replacer, content)

    # (We are not writing back any changes to the HTML file.)
    print(f"Finished processing HTML: {file_path}")

###############################################################################
# Image Resizing Functions
###############################################################################
def resize_image(img, height=None, width=None):
    """Resize the image while preserving aspect ratio.
       If height is provided, resize to that height.
       If width is provided, resize to that width.
    """
    if height:
        new_size = (img.width * height // img.height, height)
        img = ImageOps.fit(img, new_size, method=Image.Resampling.LANCZOS)
    elif width:
        new_size = (width, img.height * width // img.width)
        img = ImageOps.fit(img, new_size, method=Image.Resampling.LANCZOS)
    return img

def resize_and_save_images():
    """
    For each image URL (from our images dict), choose the most optimal dimension
    (if multiple sizes are recorded, pick the smallest dimension) and resize the
    original asset file in place (overwrite it).
    """
    for url, data in images.items():
        relative_path = url.replace('/assets/', '')
        local_img_path = os.path.join(assets_dir, relative_path)
        if not os.path.exists(local_img_path):
            print(f'File not found for {url} at {local_img_path}')
            continue

        # If multiple sizes were recorded, choose the smallest numeric value.
        desired_dims = [dimension for (dimension, _) in data["sizes"]]
        if not desired_dims:
            print(f'No recorded size for {url}. Skipping.')
            continue

        target_dim = min(desired_dims)  # Pick the smallest dimension
        # We also need to know what type it is; if both width and height were recorded,
        # you could choose one based on your preference. Here we'll prioritize height if found.
        types = [typ for (dim, typ) in data["sizes"] if dim == target_dim]
        # If "height" is among the types, we'll use that; otherwise, use width.
        target_type = "height" if "height" in types else "width"

        print(f"Resizing {local_img_path}: target {target_type} = {target_dim}px")
        try:
            with open(local_img_path, 'rb') as src_file:
                img = Image.open(src_file)
                # Resize using the correct parameter.
                if target_type == "height":
                    img = resize_image(img, height=target_dim)
                else:
                    img = resize_image(img, width=target_dim)
                # Convert for JPEG if necessary.
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    img = img.convert("RGB")
                # Overwrite the original file.
                img.save(local_img_path, optimize=True, quality=85)
            log_line = f"Resized {local_img_path} in place (using {target_type}: {target_dim}px)"
            print(log_line)
            with open(copy_log_file, 'a', encoding='utf-8') as log_f:
                log_f.write(log_line + "\n")
        except Exception as e:
            print(f"Error resizing {local_img_path}: {e}")

###############################################################################
# Process All HTML Files and Then Resize Images
###############################################################################
for root, dirs, files in os.walk(dist_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            print(f"Processing {file_path}")
            process_file(file_path)

resize_and_save_images()

print(f'Image resizing changes recorded in {output_file}.')
print(f'Image resizing operations recorded in {copy_log_file}.')
print('Images resized and optimized in place.')
