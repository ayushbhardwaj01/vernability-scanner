import requests
import re

def from_crtsh(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        r = requests.get(url, timeout=5)
        return list(set(
            entry['name_value'].replace('*.', '') for entry in r.json()
        ))
    except:
        return []

def from_threatcrowd(domain):
    try:
        r = requests.get(f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}", timeout=5)
        return r.json().get('subdomains', [])
    except:
        return []

def from_hackertarget(domain):
    try:
        r = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=5)
        return [line.split(',')[0] for line in r.text.splitlines()]
    except:
        return []

def from_dnsdumpster(domain):
    try:
        from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
        results = DNSDumpsterAPI().search(domain)
        return [entry['domain'] for entry in results['dns_records']['host']]
    except:
        return []

def enumerate_subdomains(domain):
    subs = set()
    subs.update(from_crtsh(domain))
    subs.update(from_threatcrowd(domain))
    subs.update(from_hackertarget(domain))
    subs.update(from_dnsdumpster(domain))
    return sorted(subs)
