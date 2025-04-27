import os
import shutil
from PIL import Image
import re

# -------------------------------
# Configuration
# -------------------------------
# Path to your manifest file – each line in the manifest is expected to be a file path such as:
# /assets/img/2024/media/routes/69/217/day-7-kumamoto-mt-aso-Google_Earth_View-medium.png

# Repository directories
abs_path = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025'
dist_dir = os.path.join(abs_path, 'dist')
manifest_file = os.path.join(abs_path, '_build_process', 'images_manifest.txt')
assets_dir = os.path.join(dist_dir, 'assets')
report_file = os.path.join(abs_path, '_build_process', 'optimization_report.txt')


# Optional parameters:
max_width = 700            # Maximum width for resizing images (if applicable)
jpeg_quality = 65          # Quality for JPEG optimization (0-100)
webp_quality = 80          # Quality setting for WebP conversion (0-100)
webp_method = 6            # Compression method for WebP (0=fastest, 6=slowest/best)

# Slider-specific conditions:
slider_max_height = 250    # Slider images in media/slider_images => 175 px height
special_slider_max_height = 193  # Images in top_sliders => 193 px height
chart_width = 620  # Images in top_sliders => 193 px height

# -------------------------------
# Helper Functions
# -------------------------------
def human_readable_size(num_bytes):
    """Return a human-readable file size string for num_bytes."""
    for unit in ['B','KB','MB','GB']:
        if num_bytes < 1024.0:
            return f"{num_bytes:.1f}{unit}" if unit != 'B' else f"{num_bytes}{unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f}TB"

def get_image_dimensions(filepath):
    """Return (width, height) of the image."""
    try:
        with Image.open(filepath) as img:
            return img.size  # (width, height)
    except Exception as e:
        print(f"Error reading image dimensions for {filepath}: {e}")
        return (None, None)

def insert_suffix(filename, suffix):
    """Insert a suffix before the file extension. 
       E.g., insert_suffix("foo.jpg", "-master") yields "foo-master.jpg"."""
    base, ext = os.path.splitext(filename)
    return f"{base}{suffix}{ext}"

# -------------------------------
# Main Processing Function
# -------------------------------
def process_manifest():
    if not os.path.exists(manifest_file):
        print(f"Manifest file not found: {manifest_file}")
        return

    # Open the report file for writing (overwrite each run)
    with open(report_file, 'w', encoding='utf-8') as rpt:
        rpt.write("Optimization Report\n")
        rpt.write("Format: [Master file: size, widthxheight, filepath] | [Optimized file: size, widthxheight, filepath]\n\n")
    
    # Process each file listed in the manifest.
    with open(manifest_file, 'r', encoding='utf-8') as mf:
        for line in mf:
            line = line.strip()
            if not line:
                continue
            # Each line should be something like:
            # /assets/img/2024/media/routes/.../filename.ext
            # Remove the leading /assets/ portion to create a relative path.
            if line.startswith("/assets/"):
                rel_path = line[len("/assets/"):]
            else:
                rel_path = line
            
            # Construct the full path to the master file in assets.
            master_path = os.path.join(assets_dir, rel_path)
            if not os.path.exists(master_path):
                print(f"Master file not found: {master_path}")
                continue
            
            # Create a backup copy (the "master" copy) with "-master" inserted before the extension.
            dir_name, filename = os.path.split(master_path)
            master_backup_filename = insert_suffix(filename, "-master")
            master_backup_path = os.path.join(dir_name, master_backup_filename)
            try:
                shutil.copy2(master_path, master_backup_path)
                print(f"Created master backup: {master_backup_path}")
            except Exception as e:
                print(f"Error creating master backup for {master_path}: {e}")
                continue
            
            # Get file sizes and dimensions for the master backup.
            master_size_bytes = os.path.getsize(master_backup_path)
            master_dimensions = get_image_dimensions(master_backup_path)
            master_info = f"{human_readable_size(master_size_bytes)}, {master_dimensions[0]}x{master_dimensions[1]}, {master_backup_path}"
            
            
            # --------------------------
            # Optimize the original file.
            # --------------------------

            # Determine if this image is a slider image.
            # Use the relative path in lowercase.
            rel_path_lower = rel_path.lower()
            height_limit = None
            width_limit = None
            # Set height limits for slider images.
            if "media/slider_images" in rel_path_lower:
                height_limit = slider_max_height  # e.g., 175 px
            elif "top_sliders" in rel_path_lower:
                height_limit = special_slider_max_height  # e.g., 193 px
            elif re.search(r'/routes/\d+/chart', rel_path_lower):
                width_limit = chart_width  # e.g., 620 px

            try:
                with Image.open(master_path) as img:
                    img_format = img.format  # "JPEG", "PNG", etc.
                    # First, if a height limit has been specified, enforce it.
                    if height_limit is not None:
                        if img.height > height_limit:
                            new_height = height_limit
                            new_width = int(img.width * new_height / img.height)
                            print(f"Resizing (height-limited) image {master_path} from {img.width}x{img.height} to {new_width}x{new_height}")
                            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    # Else, if a width limit is specified, enforce that.
                    elif width_limit is not None:
                        if img.width > width_limit:
                            new_width = width_limit
                            new_height = int(img.height * new_width / img.width)
                            print(f"Resizing (width-limited) image {master_path} from {img.width}x{img.height} to {new_width}x{new_height}")
                            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    else:
                        # Normal images: if the width exceeds max_width and aspect ratio is less than 5, resize.
                        aspect_ratio = img.width / img.height if img.height != 0 else 1
                        if img.width > max_width and aspect_ratio < 5:
                            new_width = max_width
                            new_height = int(new_width * img.height / img.width)
                            print(f"Resizing normal image {master_path} from {img.width}x{img.height} to {new_width}x{new_height}")
                            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Save the optimized image.
                    if img_format == 'JPEG':
                        img.save(master_path, format='JPEG', optimize=True, quality=jpeg_quality)
                    else:
                        img.save(master_path, format=img_format, optimize=True)
            except Exception as e:
                print(f"Error optimizing {master_path}: {e}")
                continue

            # Get info for the optimized file.
            optimized_size_bytes = os.path.getsize(master_path)
            optimized_dimensions = get_image_dimensions(master_path)
            optimized_info = f"{human_readable_size(optimized_size_bytes)}, {optimized_dimensions[0]}x{optimized_dimensions[1]}, {master_path}"

            # --------------------------
            # Convert the optimized file to WebP.
            # --------------------------
            webp_path = os.path.splitext(master_path)[0] + ".webp"
            try:
                with Image.open(master_path) as img:
                    # Optionally, you can resize here again if needed, but we assume the dimensions remain the same.
                    img.save(webp_path, format='WebP', quality=webp_quality, method=webp_method, optimize=True)
            except Exception as e:
                print(f"Error converting {master_path} to WebP: {e}")
                continue

            webp_size_bytes = os.path.getsize(webp_path)
            webp_dimensions = get_image_dimensions(webp_path)
            webp_info = f"{human_readable_size(webp_size_bytes)}, {webp_dimensions[0]}x{webp_dimensions[1]}, {webp_path}"

            # Write the optimization info to the report.
            with open(report_file, 'a', encoding='utf-8') as rpt:
                rpt.write(f"Master Backup: {master_info}\nOptimized: {optimized_info}\nWebP: {webp_info}\n\n")

            print(f"Processed {master_path}:")
            print(f"  Master Backup: {human_readable_size(master_size_bytes)}; {master_dimensions}")
            print(f"  Optimized: {human_readable_size(optimized_size_bytes)}; {optimized_dimensions}")
            print(f"  WebP: {human_readable_size(webp_size_bytes)}; {webp_dimensions}")

if __name__ == '__main__':
    process_manifest()
