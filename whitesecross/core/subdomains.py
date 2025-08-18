from __future__ import print_function
import requests
import re

from core.utils import log_info, COLOR_YELLOW

def get_subdomains(domain):
    url = 'https://crt.sh/?q=%25.' + domain + '&output=json'
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            log_info('[!] Failed to fetch crt.sh data', COLOR_YELLOW)
            return []
        data = r.json()
        subdomains = set()
        for entry in data:
            name = entry.get('name_value', '')
            for sub in name.split('\n'):
                if sub.endswith(domain) and '*' not in sub:
                    subdomains.add(sub.strip())
        return list(subdomains)
    except Exception as e:
        log_info('[!] Exception during subdomain enumeration: %s' % str(e), COLOR_YELLOW)
        return []
