from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/'scripts'/'warroom'/'triggers'/'DET04_BLUE_FIM.sh'

def test_det04_requires_confirmed_wazuh_monitored_writable_path():
    text=SCRIPT.read_text(encoding='utf-8')
    assert 'HOLD_MISSING_MONITORED_PATH' in text
    assert "root.iter('directories')" in text
    assert 'os.access(p,os.W_OK)' in text
    assert 'TEST_FILE="$MONITORED_PATH/' in text
    assert '/tmp/ccc' not in text
