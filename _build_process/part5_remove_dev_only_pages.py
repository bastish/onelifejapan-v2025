import xml.etree.ElementTree as ET
import os
import shutil

# -------------------------------
# Configuration
# -------------------------------
dist_dir = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/dist'
sitemap_path = os.path.join(dist_dir, 'sitemap-0.xml')

# -------------------------------
# Function: Process Dev-Only HTML Files
# -------------------------------
def get_dev_only_canonicals(dist_dir):
    """
    Walk through every HTML file in dist_dir.
    If the file contains <meta name="dev-only" content="true">,
    extract the canonical URL from <link rel="canonical" href="...">,
    delete the file, and return a list of canonical URLs.
    """
    from bs4 import BeautifulSoup  # Ensure you have BeautifulSoup installed (pip install beautifulsoup4)
    
    dev_canonicals = []
    for root, _, files in os.walk(dist_dir):
        for file in files:
            if file.endswith('.html'):
                html_path = os.path.join(root, file)
                with open(html_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                # Check for the dev-only meta tag.
                if soup.find('meta', attrs={'name': 'dev-only', 'content': 'true'}):
                    # Extract canonical URL.
                    canonical_tag = soup.find('link', rel='canonical')
                    if canonical_tag and canonical_tag.get('href'):
                        canonical_url = canonical_tag['href'].strip()
                        dev_canonicals.append(canonical_url)
                        print(f"Found dev-only page: {html_path}")
                        print(f"Canonical URL: {canonical_url}")
                    else:
                        print(f"Dev-only page {html_path} has no canonical link.")
                    # Delete the HTML file.
                    os.remove(html_path)
                    print(f"Deleted file: {html_path}")
    return dev_canonicals

# -------------------------------
# Function: Remove <url> Elements from Sitemap Tree
# -------------------------------
def remove_urls_from_sitemap(dev_canonicals, sitemap_path, paths_to_remove):
    """
    Parse the sitemap XML tree and remove any <url> elements
    whose <loc> text matches one of the dev-only canonical URLs.
    Write back the updated XML file.
    """
    try:
        # Parse the sitemap XML.
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        # Define namespace mapping: extract namespace from the <urlset> if available.
        ns = {}
        if root.tag.startswith("{"):
            uri, _, _ = root.tag[1:].partition("}")
            ns = {'sm': uri}  # Using prefix "sm" for sitemap namespace.
        
        # Choose proper tag names based on namespace.
        url_tag = 'url' if not ns else 'sm:url'
        loc_tag = 'loc' if not ns else 'sm:loc'
        
        # Find all <url> elements.
        urls_to_remove = []
        for url in root.findall(url_tag, ns):
            loc = url.find(loc_tag, ns)
            if loc is not None and loc.text:
                # Check if the canonical in <loc> matches one from our dev-only list.
                for dev_url in dev_canonicals:
                    if dev_url == loc.text.strip():
                        urls_to_remove.append(url)
                        print(f"Marking for removal: {loc.text.strip()}")
                        break
                
                # Additionally, remove URLs containing any of the paths in paths_to_remove.
                for path in paths_to_remove:
                    if path in loc.text.strip():
                        urls_to_remove.append(url)
                        print(f"Marking for removal (extra path): {loc.text.strip()}")
                        break


        # Remove the identified <url> elements.
        for url in urls_to_remove:
            root.remove(url)
        
        # Write the updated sitemap back to the file.
        tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
        print("Sitemap updated successfully.")
    except Exception as e:
        print(f"Error updating sitemap: {e}")


# -------------------------------
# Function: Remove /tools Directory
# -------------------------------
def remove_tools_directory(dist_dir):
    """
    Remove the /tools directory from the dist folder if it exists.
    """
    tools_dir = os.path.join(dist_dir, 'tools')
    if os.path.exists(tools_dir):
        shutil.rmtree(tools_dir)
        print(f"Removed /tools directory: {tools_dir}")
    else:
        print(f"/tools directory does not exist or was already removed.")

# -------------------------------
# MAIN EXECUTION
# -------------------------------
if __name__ == '__main__':
    # 1. Remove the /tools directory from the build.
    remove_tools_directory(dist_dir)

    # 2. Collect dev-only canonical URLs and delete the corresponding HTML files.
    dev_canonicals = get_dev_only_canonicals(dist_dir)
    print("")
    print("")
    if dev_canonicals:
        print("Dev-only canonical URLs found:")
        for url in dev_canonicals:
            print(url)
    else:
        print("No dev-only pages found.")

    extra_paths_to_remove = ['/route-accordian', '/highlight-points']

    # 3. Remove dev-only and /tools URLs from the sitemap.
    remove_urls_from_sitemap(dev_canonicals, sitemap_path, extra_paths_to_remove)

    print("")
    print("")
