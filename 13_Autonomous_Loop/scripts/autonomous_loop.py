from pathlib import Path
import csv, subprocess, re
from datetime import datetime

def clean(text):
    text = text.lower()
    text = re.sub(r"(salary|salaries|unknown|ref|\\(.*?\\))", "", text)
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")

home = Path.home()
fa = home / "FreedomArchitect"
jobs_csv = fa / "11_Auto_Job_Finder/output/jobs_ranked.csv"
output_dir = fa / "12_Auto_Application_Generator/output"
log_file = fa / "05_Application_Engine/logs/daily-application-log.md"

output_dir.mkdir(parents=True, exist_ok=True)

subprocess.run(["python3", str(fa / "11_Auto_Job_Finder/scripts/find_and_score_jobs.py")])

rows = []
with open(jobs_csv) as f:
    reader = csv.DictReader(f)
    for r in reader:
        title = r.get("title","")
        if "salary" in title.lower():
            continue
        rows.append(r)

top = rows[:10]

print("\nTop Jobs:")
for i, r in enumerate(top,1):
    print(f"{i}. {r['title']} | {r['company']}")

choice = int(input("\nSelect job (1-10): "))
job = top[choice-1]

title = job["title"]
company = job["company"] or "company"

title_clean = clean(title)
company_clean = clean(company)

cover_file = output_dir / f"{company_clean}_{title_clean}_cover.txt"
resume_file = output_dir / f"{company_clean}_{title_clean}_resume.txt"

cover_file.write_text(f"Applying for {title} at {company}")
resume_file.write_text(f"Experience aligned to {title}")

with open(log_file,"a") as f:
    f.write(f"\n{datetime.now()} | {company} | {title}")

subprocess.run(["git","-C",str(fa),"add","."])
subprocess.run(["git","-C",str(fa),"commit","-m",f"auto apply {company_clean} {title_clean}"])
subprocess.run(["git","-C",str(fa),"push"])

print("\nDONE — CLEAN OUTPUT GENERATED")
