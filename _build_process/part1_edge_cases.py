import re
import json
import html

def process_links_json(content):
    """
    Extract URLs from data-slider-images attributes by:
      - Unescaping HTML entities,
      - Parsing the JSON string,
      - Optionally cleaning the URL (e.g. removing the base URL).
    """
    # Match the attribute value
    pattern = re.compile(r'data-slider-images="([^"]+)"')
    extracted_urls = []
    
    matches = pattern.findall(content)
    for match in matches:
        try:
            # Unescape to convert &#34; to "
            unescaped = html.unescape(match)
            #print("Unescaped JSON string:", unescaped)
            # Load the JSON, which should result in a list
            url_list = json.loads(unescaped)
            # Process each URL in the list if needed
            for url in url_list:
                # Optionally, remove a base URL, e.g., http://localhost:3020
                if url.startswith("http://localhost:3020"):
                    url = url.replace("http://localhost:3020", "")
                extracted_urls.append(url)
        except Exception as e:
            print("Error processing data-slider-images:", e)
    return extracted_urls
