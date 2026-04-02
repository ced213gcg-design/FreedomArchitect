#!/usr/bin/env python3
from pathlib import Path
import csv
import subprocess
from datetime import datetime
import sys

home = Path.home()
fa = home / "FreedomArchitect"
job_engine = fa / "11_Auto_Job_Finder"
app_engine = fa / "12_Auto_Application_Generator"
output_csv = job_engine / "output" / "jobs_ranked.csv"
app_output = app_engine / "output"
app_output.mkdir(parents=True, exist_ok=True)

ms_file = fa / "09_Mission_State_Dashboard" / "status" / "mission-state.env"
ex_file = fa / "10_Executive_Summary_Board" / "board" / "executive-state.env"
app_log = fa / "05_Application_Engine" / "logs" / "daily-application-log.md"

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def update_env_counter(path: Path, key: str, increment: int = 1):
    lines = path.read_text(encoding="utf-8").splitlines()
    new = []
    for line in lines:
        if line.startswith(f"{key}="):
            try:
                val = int(line.split("=",1)[1].strip().strip('"'))
                line = f"{key}={val + increment}"
            except Exception:
                pass
        new.append(line)
    path.write_text("\n".join(new), encoding="utf-8")

def update_env_text(path: Path, key: str, value: str):
    lines = path.read_text(encoding="utf-8").splitlines()
    new = []
    found = False
    for line in lines:
        if line.startswith(f"{key}="):
            line = f'{key}="{value}"'
            found = True
        new.append(line)
    if not found:
        new.append(f'{key}="{value}"')
    path.write_text("\n".join(new), encoding="utf-8")

# 1) Run job finder
finder = job_engine / "scripts" / "find_and_score_jobs.py"
if finder.exists():
    print("Running job finder...")
    res = run(["python3", str(finder)])
    print(res.stdout or res.stderr)
else:
    print("Job finder script not found.")
    sys.exit(1)

if not output_csv.exists():
    print("Ranked jobs CSV not found.")
    sys.exit(1)

# 2) Read top jobs
rows = []
with output_csv.open(encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get("score") and row.get("title"):
            rows.append(row)

if not rows:
    print("No jobs found.")
    sys.exit(1)

top = rows[:10]
print("\nTop Ranked Jobs:")
for i, r in enumerate(top, 1):
    print(f"{i}. [{r['score']}] {r['title']} | {r['company']} | {r['location']}")

# 3) Select a job
choice = input("\nSelect job number (1-10): ").strip()
if not choice.isdigit() or int(choice) < 1 or int(choice) > len(top):
    print("Invalid selection.")
    sys.exit(1)

job = top[int(choice)-1]
title = job["title"].replace("/", "").replace("\\", "").strip()
company = job["company"].replace("/", "").replace("\\", "").strip() or "UnknownCompany"

# 4) Generate application package
cover = f"""Hello,

I am applying for the {title} position at {company}.

My background is centered around cybersecurity operations, including SOC analysis, packet inspection, network defense, and system-level troubleshooting.

I have built hands-on lab environments that demonstrate real-world analyst workflows such as alert triage, traffic analysis, service exposure assessment, packet inspection, and defensive analysis.

My work is structured, evidence-based, and focused on defensive execution.

I would value the opportunity to contribute to your team and continue growing within your environment.

Best regards,
Cedrick Green
"""

resume = """- Conducted SOC-style alert investigations using structured workflows
- Performed packet analysis to identify suspicious traffic patterns
- Executed Nmap scans to assess network exposure and active services
- Built structured network defense and packet analysis labs
- Documented findings clearly with defensive recommendations
- Worked across Linux and Windows environments for operational support
"""

cover_file = app_output / f"{company}_{title}_cover.txt"
resume_file = app_output / f"{company}_{title}_resume.txt"
cover_file.write_text(cover, encoding="utf-8")
resume_file.write_text(resume, encoding="utf-8")

# 5) Log application event
now = datetime.now().strftime("%Y-%m-%d %H:%M")
with app_log.open("a", encoding="utf-8") as f:
    f.write(f"\n## AUTONOMOUS LOOP ENTRY\nTime: {now}\n")
    f.write(f"Company: {company}\nRole: {title}\n")
    f.write(f"Source: {job.get('source','')}\nLink: {job.get('link','')}\n")
    f.write("Action: Application package generated\n")

# 6) Update dashboards
update_env_counter(ms_file, "APPLICATIONS_SENT", 1)
update_env_counter(ex_file, "APPLICATION_COUNT", 1)
update_env_text(ms_file, "NEXT_ACTION", "Review generated application, submit, then send recruiter outreach")
update_env_text(ex_file, "NEXT_EXECUTIVE_MOVE", "Submit generated application and send recruiter outreach for selected role")

# 7) Commit and push
run(["git", "-C", str(fa), "add", "."])
commit = run(["git", "-C", str(fa), "commit", "-m", f"Autonomous loop: prepared application for {company} - {title}"])
print(commit.stdout or commit.stderr)
push = run(["git", "-C", str(fa), "push", "origin", "main"])
print(push.stdout or push.stderr)

print("\nGenerated Files:")
print(cover_file)
print(resume_file)
print("\nNext manual step: review these files, submit on the job site, then log recruiter outreach.")
