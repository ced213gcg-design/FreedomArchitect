from pathlib import Path

# --- Ensure directories exist ---
base = Path.home() / "FreedomArchitect/12_Auto_Application_Generator"
output_dir = base / "output"
templates_dir = base / "templates"

output_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)

# --- Input ---
job = input("Enter Job Title: ").strip()
company = input("Enter Company Name: ").strip()

# --- Clean inputs ---
job = job.replace("/", "").replace("\\", "")
company = company.replace("/", "").replace("\\", "")

# --- Templates ---
cover = f"""My background is centered around cybersecurity operations, including SOC analysis, packet inspection, network defense, and system-level troubleshooting.

I have built hands-on lab environments that demonstrate real-world analyst workflows such as alert triage, traffic analysis, and service exposure assessment.

My work is structured, evidence-based, and focused on defensive execution.

I would value the opportunity to contribute to your team and continue growing within your environment.

Best regards,
Cedrick Green
"""

resume = """- Conducted SOC-style alert investigations using structured workflows
- Performed packet analysis to identify suspicious traffic patterns
- Built network defense labs using Nmap and traffic inspection tools
- Developed investigation reports and documentation for simulated incidents
"""

# --- Write files ---
cover_file = output_dir / f"{company}_{job}_cover.txt"
resume_file = output_dir / f"{company}_{job}_resume.txt"

cover_file.write_text(cover)
resume_file.write_text(resume)

print("\nApplication Generated Successfully:")
print(f"Cover Letter: {cover_file}")
print(f"Resume Bullets: {resume_file}")
