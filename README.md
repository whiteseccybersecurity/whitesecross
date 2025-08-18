# Whitesecross – Advanced XSS Vulnerability Scanner

Whitesecross is an advanced XSS vulnerability scanner designed for security researchers and bug bounty hunters. It automates crawling of target websites, extracts JavaScript files and endpoints, and tests them against custom or built-in payloads. The tool is designed for flexibility, supporting proxy integration with BurpSuite, payload customization, and multi-threaded scanning.

---

## Features
- Automated crawling and endpoint discovery  
- Extraction of JavaScript files for deeper analysis  
- Custom payload injection for XSS testing  
- Proxy support for tools like BurpSuite  
- Multi-threaded crawling for faster results  
- Python 3 compatibility  
- Clear and structured logging  

---

## Installation

Clone the repository and install required dependencies:

```bash
git clone https://github.com/your-username/whitesecross.git
cd whitesecross
pip install -r requirements.txt
```

---

## Usage

### Basic Scan

```bash
python whitesecross.py -u https://example.com
```

This command crawls the target site, extracts links and JavaScript files, and tests discovered endpoints.

---

### Using a Proxy (BurpSuite)

If you want to intercept requests in BurpSuite or another proxy:

1. Open BurpSuite → Proxy tab → Set listener (default: 127.0.0.1:8080).  
2. Run Whitesecross with proxy option:

```bash
python whitesecross.py -u https://example.com --proxy http://127.0.0.1:8080
```

3. Requests from Whitesecross will now be routed through BurpSuite, allowing you to intercept, modify, and analyze them.

---

### Adding Custom Payloads

Payloads are stored in:

```
payloads/payloads.txt
```

To add your own:
1. Open the file in any text editor.  
2. Add each payload on a new line.  
3. Save the file and re-run the tool.  

Example custom payloads:
```
"><script>alert(1)</script>
<img src=x onerror=alert(2)>
```

---

### Multi-threaded Crawling

By default, the crawler runs with 5 threads. You can increase or decrease threads for speed:

```bash
python whitesecross.py -u https://example.com --threads 10
```

---

### Example Workflows

1. **Simple Scan**  
   ```bash
   python whitesecross.py -u https://target.com
   ```

2. **Scan With Proxy for BurpSuite**  
   ```bash
   python whitesecross.py -u https://target.com --proxy http://127.0.0.1:8080
   ```

3. **Custom Payload Scan**  
   Add payloads to `payloads/payloads.txt` and run the tool as normal.

---

## Output

- Crawled URLs  
- Extracted JavaScript files  
- Vulnerable parameters (if detected)  
- Console logs with status codes and error handling  

---

## Notes
- This tool is for **educational and authorized testing purposes only**.  
- Always get **legal permission** before testing any target.  
- Misuse of this tool is strictly discouraged.  
