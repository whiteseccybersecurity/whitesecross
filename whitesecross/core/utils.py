from __future__ import print_function
import sys
import os
import json
import time

try:
    import colorama
    colorama.init()
except ImportError:
    pass

COLOR_RESET = '\033[0m'
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_CYAN = '\033[96m'

def print_banner():
    banner = r'''

        .__    .__  __                                                         
__  _  _|  |__ |__|/  |_  ____   ______ ____   ___________  ____  ______ ______
\ \/ \/ /  |  \|  \   __\/ __ \ /  ___// __ \_/ ___\_  __ \/  _ \/  ___//  ___/
 \     /|   Y  \  ||  | \  ___/ \___ \\  ___/\  \___|  | \(  <_> )___ \ \___ \ 
  \/\_/ |___|  /__||__|  \___  >____  >\___  >\___  >__|   \____/____  >____  >
             \/              \/     \/     \/     \/                 \/     \/  Version 1
             youtube - https://www.youtube.com/@whiteseccybersecurity
'''
    print(COLOR_CYAN + banner + COLOR_RESET)

def log_info(message, color=COLOR_CYAN):
    print(color + message + COLOR_RESET)

def save_report(results, output_file, json_format=False):
    if not results:
        return
    dirname = os.path.dirname(output_file)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    try:
        if json_format:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
        else:
            with open(output_file, 'w') as f:
                for r in results:
                    f.write('URL: %s\n' % r['url'].encode('utf-8') if sys.version_info[0] < 3 else r['url'])
                    f.write('Parameter: %s\n' % r['parameter'])
                    f.write('Payload: %s\n' % r['payload'])
                    f.write('Type: %s\n' % r['type'])
                    f.write('Evidence: %s\n' % r['evidence'])
                    f.write('---\n')
        log_info('[*] Saved report to %s' % output_file)
    except Exception as e:
        log_info('[!] Failed to save report: %s' % str(e), COLOR_RED)

def safe_encode(s):
    try:
        return s.encode('utf-8')
    except:
        return s

def safe_decode(s):
    try:
        return s.decode('utf-8')
    except:
        return s
