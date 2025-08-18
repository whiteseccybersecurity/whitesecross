from __future__ import print_function
import requests
import re

from core.utils import log_info

JS_SINK_PATTERNS = [
    r'\.innerHTML',
    r'document\.write',
    r'eval\(',
    r'setTimeout\(',
    r'setInterval\(',
    r'location\.href',
    r'window\.location',
    r'\.outerHTML',
    r'\.insertAdjacentHTML',
]

def analyze_js_files(js_urls, proxy=None):
    warnings = []
    proxies = None
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy,
        }
    for js_url in js_urls:
        try:
            r = requests.get(js_url, timeout=10, proxies=proxies, verify=False)
            if r.status_code != 200:
                continue
            content = r.text
            for pattern in JS_SINK_PATTERNS:
                if re.search(pattern, content):
                    warnings.append('[JS Sink Warning] Pattern "%s" found in %s' % (pattern, js_url))
        except Exception as e:
            warnings.append('[!] Failed to fetch/analyze JS: %s (%s)' % (js_url, str(e)))
    return warnings
