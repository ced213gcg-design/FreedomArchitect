from pathlib import Path
from datetime import datetime,timezone
import json,os,subprocess,uuid,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]; out=ROOT/"artifacts"/"ccc-ci-summary.json"; out.parent.mkdir(parents=True,exist_ok=True)
report=ROOT/"artifacts"/"pytest-report.xml"; total=passed=failed=0; warnings=[]
if report.exists():
    tree=ET.parse(report); suite=tree.getroot()
    if suite.tag=="testsuites": suite=next(iter(suite),suite)
    total=int(suite.attrib.get("tests",0)); failed=int(suite.attrib.get("failures",0))+int(suite.attrib.get("errors",0)); skipped=int(suite.attrib.get("skipped",0)); passed=max(0,total-failed-skipped)
else: warnings.append("pytest_report_unavailable")
summary={"run_id":str(uuid.uuid4()),"commit_sha":os.getenv("CCC_COMMIT_SHA"),"branch":os.getenv("CCC_BRANCH"),"tests_total":total,"tests_passed":passed,"tests_failed":failed,"warnings":warnings,"security_findings":[],"state":"VERIFY" if failed==0 else "HOLD","timestamp":datetime.now(timezone.utc).isoformat()}
if not summary["commit_sha"]:
    try: summary["commit_sha"]=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    except Exception: summary["warnings"].append("commit_sha_unavailable")
if not summary["branch"]:
    summary["branch"]=os.getenv("GITHUB_HEAD_REF") or os.getenv("GITHUB_REF_NAME")
    if not summary["branch"]: summary["warnings"].append("branch_unavailable")
out.write_text(json.dumps(summary,indent=2)+"\n"); print(out)
