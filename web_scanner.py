import requests

def scan_web_vulnerabilities(domain):
    vulns = []
    try:
        test_urls = [
            f"http://{domain}/?q=<script>alert(1)</script>",
            f"http://{domain}/?id=1' OR '1'='1"
        ]
        for url in test_urls:
            r = requests.get(url, timeout=3)
            if "<script>alert(1)</script>" in r.text:
                vulns.append(f"Possible XSS at {url}")
            if any(err in r.text.lower() for err in ["sql", "error", "syntax", "warning"]):
                vulns.append(f"Possible SQLi at {url}")
    except:
        vulns.append("Web scan failed or target not reachable")
    return vulns
