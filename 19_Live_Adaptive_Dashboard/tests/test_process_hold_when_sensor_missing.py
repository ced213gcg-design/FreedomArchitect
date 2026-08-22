from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/'scripts'/'warroom'/'triggers'/'DET05_BLUE_PROCESS.sh'

def test_det05_holds_without_existing_process_sensor():
    text=SCRIPT.read_text(encoding='utf-8')
    assert 'HOLD_MISSING_SENSOR' in text
    assert 'auditctl -l' in text
    assert 'execve' in text
    assert 'apt-get install' not in text and 'yum install' not in text
