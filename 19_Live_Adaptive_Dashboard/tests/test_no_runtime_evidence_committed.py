import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def test_runtime_physical_evidence_paths_are_ignored_and_untracked():
    ignore=(ROOT/'.gitignore').read_text(encoding='utf-8')
    assert 'runtime/' in ignore and 'artifacts/' in ignore
    r=subprocess.run(['git','ls-files','runtime/soc/**','artifacts/soc-live-five/**'],cwd=ROOT,capture_output=True,text=True,check=True)
    assert r.stdout.strip()==''
