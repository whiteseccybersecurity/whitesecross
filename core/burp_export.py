from __future__ import print_function
import json

def export_to_burp_json(results, filename):
    items = []
    for r in results:
        item = {
            'type': 'issue',
            'name': 'XSS vulnerability',
            'host': r['url'],
            'parameter': r['parameter'],
            'payload': r['payload'],
            'type_of_xss': r['type'],
            'evidence': r['evidence'],
        }
        items.append(item)
    try:
        with open(filename, 'w') as f:
            json.dump(items, f, indent=4)
    except Exception as e:
        print('[!] Failed to export Burp JSON: %s' % str(e))
