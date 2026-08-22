from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib,json,subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts'/'infinity'


def git(args):
    try: return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    except Exception: return 'UNKNOWN'


def main():
    m=json.loads((ROOT/'20_CCC_Living_Organism'/'ccc.manifest.json').read_text())
    workers=json.loads(json.dumps(m.get('five_worker_constitution',{})))
    payload={
      'schema':'ccc.infinity.evidence.v1',
      'timestamp':datetime.now(timezone.utc).isoformat(),
      'branch':git(['branch','--show-current']),
      'commit':git(['rev-parse','HEAD']),
      'base_sha':(m.get('composition') or {}).get('base_sha'),
      'canonical_checkpoint':(m.get('composition') or {}).get('canonical_checkpoint'),
      'decision_triad_count':len((m.get('governance') or {}).get('decision_triad') or []),
      'evidence_sextet_count':len((m.get('governance') or {}).get('evidence_sextet') or []),
      'completion_nonet_count':len(m.get('completion_nonet') or []),
      'creator_alignment_count':len(m.get('creator_alignment') or []),
      'historical_completion_cycle_count':len((m.get('governance') or {}).get('completion_cycle') or []),
      'gamma_present':'GAMMA' in ((m.get('lifecycle_infinity') or {}).get('sequence') or []),
      'symbolic_cadence_telemetry_independent':(m.get('symbolic_cadence') or {}).get('telemetry_independent'),
      'five_worker_count':workers.get('exact_count'),
      'game_theory_authority':(m.get('game_theory_contract') or {}).get('authority'),
      'frozen_physical_candidate':(m.get('release') or {}).get('frozen_physical_candidate'),
      'state':'VERIFY',
      'validation':'MACHINE_CONTRACT_EXPORT_NOT_PHYSICAL_RUNTIME_PROOF'
    }
    OUT.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(payload,sort_keys=True,indent=2)+'\n'
    p=OUT/'infinity-evidence.json'; p.write_text(raw,encoding='utf-8')
    digest=hashlib.sha256(raw.encode()).hexdigest()
    (OUT/'sha256sums.txt').write_text(f'{digest}  infinity-evidence.json\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','artifact':str(p.relative_to(ROOT)),'sha256':digest},indent=2))
    return 0

if __name__=='__main__': raise SystemExit(main())
