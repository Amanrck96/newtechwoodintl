import os
import re
import sys
import time
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Reconfigure stdout/stderr to use UTF-8 to prevent UnicodeEncodeError on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# Base configuration
BASE_URL = "https://www.newtechwoodintl.com"
DOMAIN = "www.newtechwoodintl.com"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONCURRENCY = 10
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# State variables
pages_to_crawl = set()
crawled_pages = set()
assets_to_download = set()
downloaded_assets = set()
failed_urls = set()

# Thread locks
state_lock = threading.Lock()
print_lock = threading.Lock()

def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

def clean_url(url, base_url=BASE_URL):
    if not url:
        return None
    url = url.strip()
    # Ignore protocol-less or non-http links
    if url.startswith(('mailto:', 'tel:', 'javascript:', '#', 'data:')):
        return None
    
    # Resolve relative URL
    resolved = urllib.parse.urljoin(base_url, url)
    parsed = urllib.parse.urlparse(resolved)
    
    # Check if the domain matches
    if parsed.netloc in (DOMAIN, 'newtechwoodintl.com', ''):
        # Normalize
        new_parts = list(parsed)
        new_parts[0] = 'https'
        new_parts[1] = DOMAIN
        return urllib.parse.urlunparse(new_parts)
    return None

def url_to_local_path(url):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    if path.startswith('/'):
        path = path[1:]
    
    path = path.strip()
    if not path:
        if parsed.query:
            safe_query = parsed.query.replace('=', '_').replace('&', '_').replace('/', '_')
            for char in ['<', '>', ':', '"', '|', '?', '*']:
                safe_query = safe_query.replace(char, '_')
            return f"query_{safe_query}/index.html"
        return "index.html"
    
    # Check if this is a directory/page (no extension)
    _, ext = os.path.splitext(path)
    if not ext:
        if not path.endswith('/'):
            path += '/'
        path += "index.html"
    else:
        path = urllib.parse.unquote(path)
        
    # Replace Windows-invalid chars
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    for char in invalid_chars:
        path = path.replace(char, '_')
        
    return path

def get_relative_path(from_path, to_path):
    from_dir = os.path.dirname(from_path)
    try:
        rel = os.path.relpath(to_path, from_dir)
        return rel.replace('\\', '/')
    except ValueError:
        return "/" + to_path.replace('\\', '/')

def download_url(url, retries=3):
    req = urllib.request.Request(url, headers=HEADERS)
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.read(), response.geturl()
        except Exception as e:
            if i == retries - 1:
                safe_print(f"Failed to download {url}: {e}")
                with state_lock:
                    failed_urls.add(url)
                return None, None
            time.sleep(1)
    return None, None

def parse_sitemaps():
    safe_print("Discovering URLs from sitemap...")
    root_sitemap = f"{BASE_URL}/wp-sitemap.xml"
    data, _ = download_url(root_sitemap)
    if not data:
        # Fallback to main sitemap.xml
        root_sitemap = f"{BASE_URL}/sitemap.xml"
        data, _ = download_url(root_sitemap)
        
    if not data:
        safe_print("No sitemaps found, starting crawl from homepage.")
        pages_to_crawl.add(f"{BASE_URL}/")
        return

    # Find sub-sitemaps
    urls = re.findall(r'<loc>(.*?)</loc>', data.decode('utf-8', errors='ignore'))
    sub_sitemaps = [u for u in urls if 'sitemap' in u]
    
    if not sub_sitemaps:
        # Root sitemap directly contains pages
        for u in urls:
            clean = clean_url(u)
            if clean:
                pages_to_crawl.add(clean)
    else:
        # Fetch each sub-sitemap
        for sm in sub_sitemaps:
            safe_print(f"Fetching sub-sitemap: {sm}")
            sm_data, _ = download_url(sm)
            if sm_data:
                sm_urls = re.findall(r'<loc>(.*?)</loc>', sm_data.decode('utf-8', errors='ignore'))
                for u in sm_urls:
                    clean = clean_url(u)
                    if clean:
                        pages_to_crawl.add(clean)
                        
    # Ensure home page is in crawl queue
    pages_to_crawl.add(f"{BASE_URL}/")
    safe_print(f"Found {len(pages_to_crawl)} unique pages from sitemaps.")

def process_html_content(html_content, page_url, page_local_path):
    # Extract script blocks to prevent regex modifications inside script tags
    script_pattern = re.compile(r'<script\b[^>]*>([\s\S]*?)</script>', re.IGNORECASE)
    scripts = []
    def script_extractor(match):
        scripts.append(match.group(0))
        return f"<!--SCRIPT_PLACEHOLDER_{len(scripts)-1}-->"
    
    html_content = script_pattern.sub(script_extractor, html_content)

    # 1. Rewrite url(...) in styles
    css_pattern = re.compile(r'url\s*\(\s*["\']?([^"\'\)]+)["\']?\s*\)', re.IGNORECASE)
    def css_replacer(match):
        value = match.group(1).strip()
        if value.startswith('data:'):
            return match.group(0)
        clean = clean_url(value, base_url=page_url)
        if clean:
            asset_local = url_to_local_path(clean)
            with state_lock:
                assets_to_download.add(clean)
            rel_path = get_relative_path(page_local_path, asset_local)
            return f"url('{rel_path}')"
        return match.group(0)
    
    html_content = css_pattern.sub(css_replacer, html_content)
    
    # 2. Rewrite HTML attributes
    attr_pattern = re.compile(r'(src|href|data-src|data-srcset|srcset|data-lazy-src|data-large_image)=["\']([^"\']*)["\']', re.IGNORECASE)
    def attr_replacer(match):
        attr = match.group(1)
        value = match.group(2).strip()
        
        if 'srcset' in attr.lower():
            parts = []
            for part in value.split(','):
                part = part.strip()
                if not part:
                    continue
                subparts = part.split(None, 1)
                img_url = subparts[0]
                descriptor = " " + subparts[1] if len(subparts) > 1 else ""
                
                clean = clean_url(img_url, base_url=page_url)
                if clean:
                    asset_local = url_to_local_path(clean)
                    with state_lock:
                        assets_to_download.add(clean)
                    rel_path = get_relative_path(page_local_path, asset_local)
                    parts.append(f"{rel_path}{descriptor}")
                else:
                    parts.append(part)
            return f'{attr}="{", ".join(parts)}"'
            
        clean = clean_url(value, base_url=page_url)
        if clean:
            parsed = urllib.parse.urlparse(clean)
            path = parsed.path.lower()
            asset_extensions = ('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.woff', '.woff2', '.ttf', '.otf', '.pdf', '.ico', '.webp', '.mp4', '.webm', '.xml', '.txt')
            is_page = not any(path.endswith(ext) for ext in asset_extensions)
            
            if is_page:
                page_local = url_to_local_path(clean)
                rel_path = get_relative_path(page_local_path, page_local)
                anchor = f"#{parsed.fragment}" if parsed.fragment else ""
                query = f"?{parsed.query}" if parsed.query else ""
                # Also add this page to crawl queue if not already crawled
                with state_lock:
                    if clean not in crawled_pages and clean not in pages_to_crawl:
                        pages_to_crawl.add(clean)
                return f'{attr}="{rel_path}{query}{anchor}"'
            else:
                asset_local = url_to_local_path(clean)
                with state_lock:
                    assets_to_download.add(clean)
                rel_path = get_relative_path(page_local_path, asset_local)
                return f'{attr}="{rel_path}"'
        return match.group(0)
        
    html_content = attr_pattern.sub(attr_replacer, html_content)

    # Restore script blocks
    for i, script in enumerate(scripts):
        html_content = html_content.replace(f"<!--SCRIPT_PLACEHOLDER_{i}-->", script)

    return html_content

def process_css_content(css_content, css_url, css_local_path):
    css_pattern = re.compile(r'url\s*\(\s*["\']?([^"\'\)]+)["\']?\s*\)', re.IGNORECASE)
    def css_replacer(match):
        value = match.group(1).strip()
        if value.startswith('data:'):
            return match.group(0)
        clean = clean_url(value, base_url=css_url)
        if clean:
            asset_local = url_to_local_path(clean)
            with state_lock:
                assets_to_download.add(clean)
            rel_path = get_relative_path(css_local_path, asset_local)
            return f"url('{rel_path}')"
        return match.group(0)
    
    return css_pattern.sub(css_replacer, css_content)

def save_file(local_path, content):
    abs_path = os.path.join(ROOT_DIR, local_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    
    mode = 'wb' if isinstance(content, bytes) else 'w'
    encoding = None if isinstance(content, bytes) else 'utf-8'
    
    try:
        with open(abs_path, mode, encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        safe_print(f"Error saving {local_path}: {e}")

def crawl_page_worker(url):
    data, final_url = download_url(url)
    if not data:
        return url, False
        
    local_path = url_to_local_path(final_url)
    safe_print(f"Crawling page: {url} -> {local_path} (Final: {final_url})")
    
    try:
        html_content = data.decode('utf-8', errors='ignore')
    except Exception as e:
        safe_print(f"Failed to decode page {url}: {e}")
        return url, False
        
    processed_html = process_html_content(html_content, final_url, local_path)
    save_file(local_path, processed_html)
    return url, True

def download_asset_worker(url):
    local_path = url_to_local_path(url)
    # Check if already exists to avoid re-download
    abs_path = os.path.join(ROOT_DIR, local_path)
    if os.path.exists(abs_path):
        return url, True
        
    safe_print(f"Downloading asset: {url} -> {local_path}")
    data, _ = download_url(url)
    if not data:
        return url, False
        
    # If the asset is a CSS file, we need to parse it for nested urls
    if url.lower().endswith('.css') or '.css?' in url.lower():
        try:
            css_content = data.decode('utf-8', errors='ignore')
            processed_css = process_css_content(css_content, url, local_path)
            save_file(local_path, processed_css)
        except Exception as e:
            safe_print(f"Failed to parse CSS asset {url}: {e}")
            save_file(local_path, data)
    else:
        save_file(local_path, data)
        
    return url, True

def main():
    start_time = time.time()
    
    # Phase 1: Sitemap discovery
    parse_sitemaps()
    
    # Phase 2: Page Crawl Loop
    safe_print("\n=== STARTING PAGE CRAWL ===")
    while True:
        # Get list of pages that need crawling
        with state_lock:
            remaining_pages = list(pages_to_crawl - crawled_pages)
            
        if not remaining_pages:
            break
            
        safe_print(f"Crawling batch of {len(remaining_pages)} discovered pages...")
        
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
            futures = {executor.submit(crawl_page_worker, url): url for url in remaining_pages}
            for future in as_completed(futures):
                url = futures[future]
                try:
                    url, success = future.result()
                    with state_lock:
                        crawled_pages.add(url)
                except Exception as e:
                    safe_print(f"Exception crawling {url}: {e}")
                    with state_lock:
                        crawled_pages.add(url)
                        failed_urls.add(url)
                        
    safe_print(f"Finished crawling pages. Total pages crawled: {len(crawled_pages)}")
    safe_print(f"Discovered {len(assets_to_download)} assets to download.")
    
    # Phase 3: Asset Download Loop (runs recursively in case CSS downloads discover more assets)
    safe_print("\n=== STARTING ASSET DOWNLOAD ===")
    while True:
        with state_lock:
            remaining_assets = list(assets_to_download - downloaded_assets)
            
        if not remaining_assets:
            break
            
        safe_print(f"Downloading batch of {len(remaining_assets)} assets...")
        
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
            futures = {executor.submit(download_asset_worker, url): url for url in remaining_assets}
            for future in as_completed(futures):
                url = futures[future]
                try:
                    url, success = future.result()
                    with state_lock:
                        downloaded_assets.add(url)
                        if not success:
                            failed_urls.add(url)
                except Exception as e:
                    safe_print(f"Exception downloading asset {url}: {e}")
                    with state_lock:
                        downloaded_assets.add(url)
                        failed_urls.add(url)

    # Save failed URLs list for review
    if failed_urls:
        save_file("failed_urls.txt", "\n".join(sorted(list(failed_urls))))
        safe_print(f"\nCompleted with {len(failed_urls)} failed downloads. Saved to failed_urls.txt")
    else:
        safe_print("\nCompleted with 0 failures!")
        
    end_time = time.time()
    duration = end_time - start_time
    safe_print(f"Total time elapsed: {duration:.2f} seconds")
    safe_print(f"Total pages saved: {len(crawled_pages)}")
    safe_print(f"Total assets saved: {len(downloaded_assets)}")

if __name__ == '__main__':
    main()
