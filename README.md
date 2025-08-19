# Whitesecross - Advanced XSS Scanner

Whitesecross is a Python-based **Cross-Site Scripting (XSS) vulnerability scanner** designed for penetration testers, bug bounty hunters, and security researchers.  
It can crawl target websites, discover URLs and JavaScript files, inject custom payloads, and report potential XSS vulnerabilities.

---

## Features

- Deep website crawling to discover hidden pages, parameters, and JavaScript files  
- Multi-threaded scanning for faster results  
- Optionally scan subdomains of the target domain  
- Customizable payload injection to test XSS vulnerabilities  
- Headless browser support for DOM-based XSS detection  
- Generates a results file for reporting and analysis  

---

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/whiteseccybersecurity/Whitesecross.git
cd Whitesecross
```

### 𝟮. 𝗜𝗻𝘀𝘁𝗮𝗹𝗹 𝗿𝗲𝗾𝘂𝗶𝗿𝗲𝗱 𝗣𝘆𝘁𝗵𝗼𝗻 𝗽𝗮𝗰𝗸𝗮𝗴𝗲𝘀
```bash
pip install -r requirements.txt
```

### 3. Recommended: Python virtual environment
```bash
python3 -m venv whitesecross-env
source whitesecross-env/bin/activate
pip install -r requirements.txt
```

## Usage

### Run basic scan
```bash
python whitesecross.py -u http://target.com
```

### Save results to a file
```bash
python whitesecross.py -u http://target.com -o xss-results.txt
```

### Use multiple threads (default: 5)
```bash
python whitesecross.py -u http://target.com --threads 10
```

### Scan subdomains
```bash
python whitesecross.py -u http://target.com --subs
```

### Scan for DOM-based XSS (JS sinks)
```bash
python whitesecross.py -u http://target.com --sinks
```

### Use headless browser for DOM XSS
```bash
python whitesecross.py -u http://target.com --dom
```

### Display help menu
```bash
python whitesecross.py -h
```

## Examples

### Basic scan
```bash
python whitesecross.py -u http://testphp.vulnweb.com
```

### Scan and save results
```bash
python whitesecross.py -u http://testphp.vulnweb.com -o results.txt
```

### Scan with 10 threads
```bash
python whitesecross.py -u http://testphp.vulnweb.com --threads 10
```

### Scan subdomains and detect DOM XSS
```bash
python whitesecross.py -u http://example.com --subs --sinks --dom
```

## Adding Custom Payloads

1. Open `core/scanner.py`
2. Locate the `PAYLOADS` list
3. Add your own payloads. Example:

```python
PAYLOADS = [
    "<script>alert(1)</script>",
    "'\"><img src=x onerror=alert(1)>",
    "<svg onload=alert('XSS')>",
]
```

## How Whitesecross Works

1. **Crawling**: Discovers internal links and JS files
2. **Payload Injection**: Tests URLs with parameters for XSS
3. **DOM XSS Detection**: Uses headless browser if `--dom` is set
4. **Reporting**: Shows results in terminal and optionally saves them

## Notes

- Python 3 recommended; Python 2 partially supported
- Only test websites you own or have permission to test
- More threads = faster scanning but higher server load
- Activate virtual environment to avoid dependency conflicts
