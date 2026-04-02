#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import re

home = Path.home()
base = home / "FreedomArchitect" / "14_Auto_Recruiter_Outreach"
templates = base / "templates"
output = base / "output"
logs = base / "logs"

ms_file = home / "FreedomArchitect" / "09_Mission_State_Dashboard" / "status" / "mission-state.env"
ex_file = home / "FreedomArchitect" / "10_Executive_Summary_Board" / "board" / "executive-state.env"
app_log = home / "FreedomArchitect" / "05_Application_Engine" / "logs" / "daily-application-log.md"
recruiter_log = logs / "recruiter-outreach-log.md"

output.mkdir(parents=True, exist_ok=True)
logs.mkdir(parents=True, exist_ok=True)

def clean(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")

def update_counter(path: Path, key: str, increment: int = 1):
    lines = path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for line in lines:
        if line.startswith(f"{key}="):
            raw = line.split("=", 1)[1].strip().strip('"')
            try:
                val = int(raw)
                line = f"{key}={val + increment}"
            except Exception:
                pass
        new_lines.append(line)
    path.write_text("\n".join(new_lines), encoding="utf-8")

def update_text(path: Path, key: str, value: str):
    lines = path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    found = False
    for line in lines:
        if line.startswith(f"{key}="):
            line = f'{key}="{value}"'
            found = True
        new_lines.append(line)
    if not found:
        new_lines.append(f'{key}="{value}"')
    path.write_text("\n".join(new_lines), encoding="utf-8")

name = input("Enter Recruiter Name: ").strip() or "Recruiter"
company = input("Enter Company Name: ").strip() or "Company"
role = input("Enter Role Title: ").strip() or "Cybersecurity Role"
platform = input("Enter Platform (LinkedIn/Email/Other): ").strip() or "LinkedIn"

msg_tpl = (templates / "recruiter_message_template.txt").read_text(encoding="utf-8")
fol_tpl = (templates / "followup_template.txt").read_text(encoding="utf-8")

message = msg_tpl.replace("[NAME]", name).replace("[COMPANY]", company).replace("[ROLE]", role)
followup = fol_tpl.replace("[NAME]", name).replace("[COMPANY]", company).replace("[ROLE]", role)

slug = f"{clean(company)}_{clean(role)}"

msg_file = output / f"{slug}_recruiter_message.txt"
fol_file = output / f"{slug}_followup_message.txt"

msg_file.write_text(message, encoding="utf-8")
fol_file.write_text(followup, encoding="utf-8")

now = datetime.now().strftime("%Y-%m-%d %H:%M")

if not recruiter_log.exists():
    recruiter_log.write_text("# Recruiter Outreach Log\n", encoding="utf-8")

with recruiter_log.open("a", encoding="utf-8") as f:
    f.write(f"\n## {now}\n")
    f.write(f"Name: {name}\n")
    f.write(f"Company: {company}\n")
    f.write(f"Role: {role}\n")
    f.write(f"Platform: {platform}\n")
    f.write("Action: Outreach package generated\n")

with app_log.open("a", encoding="utf-8") as f:
    f.write(f"\n## RECRUITER OUTREACH ENTRY\n")
    f.write(f"Time: {now}\n")
    f.write(f"Recruiter: {name}\n")
    f.write(f"Company: {company}\n")
    f.write(f"Role: {role}\n")
    f.write(f"Platform: {platform}\n")
    f.write("Action: Recruiter message + follow-up generated\n")

update_counter(ms_file, "RECRUITER_MESSAGES", 1)
update_counter(ex_file, "RECRUITER_OUTREACH", 1)
update_text(ms_file, "NEXT_ACTION", "Send recruiter outreach, then continue applications and follow-ups")
update_text(ex_file, "NEXT_EXECUTIVE_MOVE", "Convert platform strength into recruiter conversations and interviews")

print("\nGenerated:")
print(msg_file)
print(fol_file)
print("\nLogged outreach and updated dashboard metrics.")
