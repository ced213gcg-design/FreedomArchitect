from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HP=ROOT/'scripts'/'warroom'/'CCC_HP_SOC_WARROOM_ONE_DROP.sh'
DELL=ROOT/'scripts'/'warroom'/'CCC_DELL_SOC_WARROOM_ONE_DROP.ps1'

def test_hp_one_drop_has_hard_gates_and_no_secret_commit_path():
    text=HP.read_text(encoding='utf-8')
    for required in ['git stash push -u','git pull --ff-only','validate_ccc_repo.py','pytest -q','test_sphere.js','test_exception_constellation.js','test_soc_interaction_ui.js','test_soc_physical_evidence_ui.js','CCC_BRIDGE_TOKEN','FILE_FALLBACK','CCC_SOC_STATE_PATH','export_physical_artifacts.py','control-gates.json','scenario-summary.json','scenario-runs.jsonl','sensor-inventory.json','evidence-index.json','sha256sums.txt']:
        assert required in text
    assert 'git push' not in text

def test_dell_one_drop_requires_preflight_and_is_producer_only():
    text=DELL.read_text(encoding='utf-8')
    for required in ['#requires -Version 5.1','-PreflightOnly','ccc-soc-live-state.json','HMACSHA256','ccc-soc-bridge-payload.json','FILE_FALLBACK']:
        assert required in text
    assert 'New-PSSession' not in text and 'Enter-PSSession' not in text and 'Invoke-Command -ComputerName' not in text
