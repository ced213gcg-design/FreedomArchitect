import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
GUARD=ROOT/'scripts'/'warroom'/'triggers'/'ccc_lab_guard.py'

def run(*args):
    return subprocess.run([sys.executable,str(GUARD),*args],capture_output=True,text=True)

def test_exact_registered_honey_target_is_allowed():
    r=run('--ip','10.69.69.30','--role','honeypot_target','--port','2222')
    assert r.returncode==0 and 'CCC-HONEY-TARGET' in r.stdout

def test_external_and_unregistered_in_range_targets_are_rejected():
    assert run('--ip','8.8.8.8','--role','honeypot_target').returncode!=0
    assert run('--ip','10.69.69.99','--role','honeypot_target').returncode!=0
