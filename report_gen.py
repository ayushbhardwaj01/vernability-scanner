from fpdf import FPDF
from datetime import datetime
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Vulnerability Scan Report", ln=True, align="C")
        self.ln(10)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"[+] {title}", ln=True)
        self.ln(2)

    def section_body(self, lines):
        self.set_font("Arial", "", 11)
        for line in lines:
            self.multi_cell(0, 8, f"- {line}")
        self.ln(5)

def generate_report(target, ports, banners, exploits, web_vulns, subdomains, os_info=None):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/report_{target.replace('.', '_')}_{now}.pdf"

    pdf = PDFReport()
    pdf.add_page()

    # Basic Target Info
    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 10, f"Target: {target}", ln=True)
    pdf.cell(0, 10, f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)

    # Sections
    pdf.section_title("Open Ports")
    pdf.section_body([f"Port {p}" for p in ports] if ports else ["None found"])

    pdf.section_title("Service Banners")
    pdf.section_body([f"Port {p}: {banners[p]}" for p in banners])

    pdf.section_title("Known Exploits")

    # Define filtered_exploits BEFORE using it
    filtered_exploits = {
        p: exploits[p]
        for p in exploits
        if "No public exploit found" not in exploits[p]
    }

    if filtered_exploits:
        pdf.section_body([f"Port {p}: {filtered_exploits[p]}" for p in filtered_exploits])
    else:
        pdf.section_body(["None detected"])



    pdf.section_title("Web Vulnerabilities")
    pdf.section_body(web_vulns if web_vulns else ["None detected"])

    pdf.section_title("Discovered Subdomains")
    pdf.section_body(subdomains if subdomains else ["None found"])

    if os_info:
        pdf.section_title("OS Detection")
        pdf.section_body([os_info])

    # Save PDF
    os.makedirs("reports", exist_ok=True)
    pdf.output(filename)
    print(f"[✓] PDF report saved: {filename}")
