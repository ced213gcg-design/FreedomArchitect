from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]; src=ROOT/"artifacts"/"ccc-ci-summary.json"; out=ROOT/"artifacts"/"ccc-slack-summary.json"
d=json.loads(src.read_text())
text=(f"[CCC][TEST][{d['state']}]\nRepo: ced213gcg-design/FreedomArchitect\nCommit: {d.get('commit_sha')}\nRun: {d.get('run_id')}\nOrgan: release-train\nSummary: {d.get('tests_passed')}/{d.get('tests_total')} tests passed; {d.get('tests_failed')} failed\nPressure Loss: pending runtime evidence\nNext Action: review CI evidence\nEvidence Link: GitHub Actions artifact ccc-ci-summary")
out.write_text(json.dumps({"text":text})+"\n"); print(out)
