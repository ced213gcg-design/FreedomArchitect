#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime

home = Path.home()
base = home / "FreedomArchitect" / "12_Auto_Application_Generator"

role = input("Enter Job Title: ").strip()
company = input("Enter Company Name: ").strip()

cover_template = (base / "templates" / "cover_letter_template.txt").read_text()
resume_template = (base / "templates" / "resume_bullets.txt").read_text()

cover = cover_template.replace("[ROLE]", role).replace("[COMPANY]", company)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

cover_file = base / "output" / f"{company}_{role}_cover.txt"
resume_file = base / "output" / f"{company}_{role}_resume.txt"
log_file = base / "logs" / "applications.md"

cover_file.write_text(cover)
resume_file.write_text(resume_template)

with log_file.open("a") as f:
    f.write(f"\n## {timestamp}\nCompany: {company}\nRole: {role}\nGenerated\n")

print("\nGenerated:")
print(cover_file)
print(resume_file)
