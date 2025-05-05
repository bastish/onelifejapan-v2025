import re
import json
import html

def process_links_json(content):
    """
    Extract URLs from various edge-case attributes or inline CSS in one go.
    Just add new regexes to `patterns` as they arise.
    """
    # 1) Define all your edge-case patterns here.
    #    Group 1 should capture either a JSON list or a single URL.
    patterns = [
        # your existing data-slider-images attribute
        re.compile(r'data-slider-images="([^"]+)"'),
        # any other data-xxx-images you might add
        # re.compile(r'data-foo-images="([^"]+)"'),

        # CSS url(...) usage
        # matches url(some/path.png) or url('some/path.jpg') or url("some/path.jpeg")
        re.compile(r'url\(\s*["\']?([^)"\']+)["\']?\s*\)'),
    ]

    extracted_urls = []

    for pat in patterns:
        for match in pat.findall(content):
            # 2) If it looks like a JSON list, parse it
            if match.strip().startswith('['):
                try:
                    # turn &#34; into " before loading
                    url_list = json.loads(html.unescape(match))
                except json.JSONDecodeError:
                    continue
                for url in url_list:
                    cleaned = _clean_url(url)
                    extracted_urls.append(cleaned)

            # 3) Otherwise, treat it as a single URL
            else:
                cleaned = _clean_url(match)
                extracted_urls.append(cleaned)

    return extracted_urls


def _clean_url(url):
    """
    Shared cleanup logic for any URL:
    - strip a baseHost if present
    - return only the '/assets/…' substring
    """
    # remove your dev base if needed
    url = url.replace('http://localhost:3020', '')

    # if you only want the path from /assets onward:
    idx = url.find('/assets/')
    return url[idx:] if idx != -1 else url
