from pathlib import Path
import re

base = Path.home() / "FreedomArchitect/12_Auto_Application_Generator"
output_dir = base / "output"
output_dir.mkdir(parents=True, exist_ok=True)

def clean(text):
    text = text.lower()
    text = re.sub(r"(salary|salaries|unknown|ref|\\(.*?\\))", "", text)
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")

job = input("Enter Job Title: ").strip()
company = input("Enter Company Name: ").strip()

job_clean = clean(job)
company_clean = clean(company)

cover = f"""Hello,

I am applying for the {job} position.

My background is centered around cybersecurity operations, including SOC analysis, packet inspection, network defense, and system-level troubleshooting.

I have built hands-on lab environments demonstrating real-world workflows: alert triage, traffic analysis, and threat investigation.

My work is structured, evidence-based, and focused on defensive execution.

Best regards,
Cedrick Green
"""

resume = """- Conducted SOC-style alert investigations
- Performed packet analysis on suspicious traffic
- Executed Nmap scans for network exposure
- Built structured cybersecurity lab environments
- Produced investigation reports with clear findings
"""

cover_file = output_dir / f"{company_clean}_{job_clean}_cover.txt"
resume_file = output_dir / f"{company_clean}_{job_clean}_resume.txt"

cover_file.write_text(cover)
resume_file.write_text(resume)

print(f"\nGenerated:\n{cover_file}\n{resume_file}")
