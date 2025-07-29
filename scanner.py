from modules import (
    port_scanner,
    banner_grabber,
    exploit_lookup,
    subdomain_enum,
    web_scanner,
    os_detector,
    report_gen
)
import os

import json

def run_full_scan(target):
    print("\n=== Python Vulnerability Scanner ===")
    print("Running full scan...\n")

    print("[1] Scanning open ports...")
    open_ports = port_scanner.scan_ports(target, 0, 1024)

    print("[2] Grabbing service banners...")
    banners = banner_grabber.grab_banners(target, open_ports)

    print("[3] Looking up known exploits...")
    exploits = exploit_lookup.lookup_exploits(banners)

    print("[4] Running web vulnerability scan...")
    web_vulns = web_scanner.scan_web_vulnerabilities(target)

    print("[5] Enumerating subdomains...")
    subdomains = subdomain_enum.enumerate_subdomains(target)

    print("[6] Detecting OS...")
    os_info =os_detector.detect_os("scanme.nmap.org") 

    



    print("[7] Generating report...")
    os.makedirs("reports", exist_ok=True)
    report_data = {
        "target": target,
        "open_ports": open_ports,
        "banners": banners,
        "exploits": exploits,
        "web_vulnerabilities": web_vulns,
        "subdomains": subdomains,
        "os":os_info
    }

    report_gen.generate_report(target, open_ports, banners, exploits, web_vulns, subdomains,os_info )
print("\n[✓] Scan complete. Report saved in 'reports/' folder.")

        




    
    
    # Pass to report generator

if __name__ == "__main__":
    target = input("Enter target IP or domain: ").strip()
    run_full_scan(target)
