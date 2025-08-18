from __future__ import print_function
import sys
import argparse
import os
import requests
import urllib3

# Disable SSL certificate warnings globally
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Python2/3 compatibility
try:
    input = raw_input
except NameError:
    pass

from core.utils import print_banner, log_info, save_report, COLOR_GREEN, COLOR_RED
from core.crawler import crawl_site
from core.subdomains import get_subdomains
from core.scanner import run_scanner
from core.js_analysis import analyze_js_files
from core.burp_export import export_to_burp_json


def main():
    print_banner()

    parser = argparse.ArgumentParser(description='Whitesecross - Advanced XSS Hunting Framework')
    parser.add_argument('-u', '--url', required=True, help='Target URL (e.g. https://example.com)')
    parser.add_argument('-o', '--output', default='scans/xss_report', help='Output file prefix (no extension)')
    parser.add_argument('--threads', type=int, default=5, help='Number of threads for crawling/scanning')
    parser.add_argument('--subs', action='store_true', help='Enumerate subdomains and scan them')
    parser.add_argument('--sinks', action='store_true', help='Perform static JS sink analysis')
    parser.add_argument('--dom', action='store_true', help='Enable DOM XSS scanning (requires Selenium)')
    parser.add_argument('--proxy', help='HTTP/HTTPS proxy (e.g. http://127.0.0.1:8080)')
    parser.add_argument('--payloads', help='Custom payloads file (one payload per line)')
    parser.add_argument('--append-payloads', action='store_true', help='Append custom payloads instead of override')
    parser.add_argument('--burp-export', help='Export results to Burp JSON format (provide file name)')
    args = parser.parse_args()

    if not args.url.startswith('http'):
        log_info('[!] Please provide full URL with http:// or https://', COLOR_RED)
        sys.exit(1)

    if not os.path.exists('scans'):
        os.mkdir('scans')

    # Subdomain enumeration if requested
    targets = [args.url.rstrip('/')]
    domain = args.url.split('//')[1].split('/')[0]
    if args.subs:
        log_info('[*] Enumerating subdomains for: %s' % domain)
        subdomains = get_subdomains(domain)
        if subdomains:
            log_info('[*] Found %d subdomains' % len(subdomains))
            for sd in subdomains:
                targets.append('http://' + sd)
        else:
            log_info('[!] No subdomains found or failed to enumerate.', COLOR_RED)

    all_results = []
    for target_url in targets:
        log_info('[*] Crawling target: %s' % target_url)
        try:
            urls, js_urls = crawl_site(target_url, args.threads, proxy=args.proxy)
        except Exception as e:
            log_info('[!] Crawling failed: %s' % str(e), COLOR_RED)
            continue

        log_info('[*] Found %d URLs and %d JS files' % (len(urls), len(js_urls)))

        if args.sinks and js_urls:
            log_info('[*] Performing static JS sink analysis...')
            sink_warnings = analyze_js_files(js_urls, proxy=args.proxy)
            for sw in sink_warnings:
                log_info(sw, COLOR_RED)

        log_info('[*] Running XSS scanner...')
        scan_results = run_scanner(urls, args.threads, proxy=args.proxy,
                                   payload_file=args.payloads,
                                   append_payloads=args.append_payloads,
                                   dom_scan=args.dom)

        all_results.extend(scan_results)

    if not all_results:
        log_info('[*] No vulnerabilities found.', COLOR_GREEN)
    else:
        log_info('[+] Total vulnerabilities found: %d' % len(all_results), COLOR_GREEN)

    # Save reports
    output_txt = args.output + '.txt'
    output_json = args.output + '.json'
    save_report(all_results, output_txt)
    save_report(all_results, output_json, json_format=True)
    log_info('[*] Reports saved: %s, %s' % (output_txt, output_json))

    # Burp export if requested
    if args.burp_export:
        export_to_burp_json(all_results, args.burp_export)
        log_info('[*] Burp JSON export saved: %s' % args.burp_export)


if __name__ == '__main__':
    main()
