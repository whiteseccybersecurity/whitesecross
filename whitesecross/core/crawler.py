from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import threading

try:
    import queue  # Python 3
except ImportError:
    import Queue as queue  # Python 2

try:
    import urllib.parse as urlparse  # Python 3
except ImportError:
    import urlparse  # Python 2

from core.utils import log_info, COLOR_YELLOW, COLOR_RED


def is_internal_link(base_url, link):
    parsed_base = urlparse.urlparse(base_url)
    parsed_link = urlparse.urlparse(urlparse.urljoin(base_url, link))
    return parsed_base.netloc == parsed_link.netloc


def crawl_site(base_url, max_threads=5, proxy=None):
    urls_found = set()
    js_files = set()
    q = queue.Queue()
    q.put(base_url)
    urls_found.add(base_url)

    lock = threading.Lock()

    proxies = None
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy,
        }

    def worker():
        while True:
            try:
                url = q.get(timeout=5)
            except queue.Empty:
                break  # No more items → exit worker
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Whitesecross/2.0'
                }
                r = requests.get(url, headers=headers, proxies=proxies,
                                 timeout=10, verify=False)
                if r.status_code != 200:
                    continue

                soup = BeautifulSoup(r.text, 'html.parser')

                # Find all links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urlparse.urljoin(url, href)
                    if is_internal_link(base_url, full_url):
                        with lock:
                            if full_url not in urls_found:
                                urls_found.add(full_url)
                                q.put(full_url)

                # Find all JS file URLs
                for script in soup.find_all('script', src=True):
                    src = script['src']
                    full_js_url = urlparse.urljoin(url, src)
                    with lock:
                        js_files.add(full_js_url)

            except Exception as e:
                log_info('[!] Error crawling %s : %s' % (url, str(e)), COLOR_RED)
            finally:
                q.task_done()

    threads = []
    for _ in range(max_threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)

    q.join()

    return list(urls_found), list(js_files)
