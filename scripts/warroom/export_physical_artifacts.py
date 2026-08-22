#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BACK=ROOT/'19_Live_Adaptive_Dashboard'/'backend'
sys.path.insert(0,str(BACK))

from soc_adapter import SocAdapter
from soc_mission_adapter import five_missions
from soc_scenario_adapter import scenario_summary, sensor_inventory, bridge_status

OUT=ROOT/'artifacts'/'soc-live-five'


def write_json(path:Path,payload)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(payload,indent=2,default=str)+'\n',encoding='utf-8')


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def flatten_runs(summary:dict)->list[dict]:
    rows=[]
    for scenario in summary.get('scenarios',[]):
        for run in scenario.get('run_records',[]):
            if isinstance(run,dict): rows.append(run)
    rows.sort(key=lambda r:(str(r.get('scenario_id','')),str(r.get('trigger_time','')),str(r.get('run_id',''))))
    return rows


def report_text(gates:dict,summary:dict,sensors:dict,bridge:dict,soc:dict)->str:
    real=summary.get('real_scenario_count',0)
    pass_count=summary.get('pass_count',0)
    holds=[s['id'] for s in summary.get('scenarios',[]) if str(s.get('state','')).startswith('HOLD')]
    state='HOLD_WITH_DEFECTS'
    lines=[
        '# CCC SOC Physical Live Evidence Runtime Report','',
        '## FACT','',
        f"- Branch: `hotfix/ccc-soc-five-live-evidence-v1`",
        f"- Generated UTC: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Bridge mode: `{bridge.get('mode','FILE_FALLBACK')}`",
        f"- Current run: `{bridge.get('current_run') or 'UNKNOWN'}`",
        f"- SOC state: `{soc.get('state','UNKNOWN')}`",'',
        '## EVIDENCE','',
        f"- Control gates proven: `{gates.get('proven_count',0)} / 5`",
        f"- Detection scenarios with real evidence: `{real} / 5`",
        f"- Detection scenarios at 3/3 PASS: `{pass_count} / 5`",
        f"- Sensor inventory records: `{sensors.get('count',0)}`",'',
        '## VALUE','',
        '- Control Gates prove evidence transport and reconciliation readiness.',
        '- Detection Scenarios prove bounded observable behavior separately from infrastructure readiness.','',
        '## RISK','',
        f"- Holds: `{', '.join(holds) if holds else 'NONE_RECORDED'}`",
        '- Human visual review is not inferred by this exporter.',
        '- Physical acceptance remains subordinate to evidence, authorization, timestamp integrity and human review.','',
        '## ACTION','',
        f"- Next action: `{bridge.get('next_action') or 'RUN_DELL_ONE_DROP_OR_IMPORT_SANITIZED_FILE'}`",'',
        '## CONTROL GATES',''
    ]
    for g in gates.get('missions',[]): lines.append(f"- {g.get('id')} {g.get('name')}: `{g.get('state','UNKNOWN')}`")
    lines.extend(['','## DETECTION SCENARIOS',''])
    for s in summary.get('scenarios',[]): lines.append(f"- {s.get('id')} {s.get('name')}: `{s.get('state','UNKNOWN')}`; real runs `{s.get('runs_real',0)}/3`; evidence `{s.get('evidence_count',0)}`")
    lines.extend(['','## WHAT IS PROVEN','',f"- Machine-readable evidence present for `{real}` detection scenarios.",'','## WHAT IS NOT PROVEN','','- Human visual acceptance until explicitly reviewed.','- Any scenario without correlated real evidence.','- Production readiness, accreditation, or THRIVE.','','## STATE','',state,'',state,''])
    return '\n'.join(lines)


def export_once()->dict:
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'screenshots').mkdir(exist_ok=True)
    (OUT/'normalized').mkdir(exist_ok=True)
    (OUT/'report').mkdir(exist_ok=True)
    gates=five_missions()
    summary=scenario_summary()
    sensors=sensor_inventory()
    bridge=bridge_status()
    soc=SocAdapter().get_state()
    runs=flatten_runs(summary)
    write_json(OUT/'control-gates.json',gates)
    write_json(OUT/'scenario-summary.json',{k:v for k,v in summary.items() if k!='scenarios'}|{'scenarios':[{k:v for k,v in row.items() if k!='run_records'} for row in summary.get('scenarios',[])]})
    with (OUT/'scenario-runs.jsonl').open('w',encoding='utf-8') as f:
        for row in runs: f.write(json.dumps(row,default=str,separators=(',',':'))+'\n')
    write_json(OUT/'sensor-inventory.json',sensors)
    write_json(OUT/'normalized'/'bridge-state.json',bridge)
    write_json(OUT/'normalized'/'soc-state.json',soc)
    (OUT/'report'/'CCC_SOC_PHYSICAL_LIVE_EVIDENCE_REPORT.md').write_text(report_text(gates,summary,sensors,bridge,soc),encoding='utf-8')
    candidates=[p for p in OUT.rglob('*') if p.is_file() and p.name not in {'sha256sums.txt','evidence-index.json'}]
    hashes={str(p.relative_to(OUT)):sha256(p) for p in sorted(candidates)}
    write_json(OUT/'evidence-index.json',{'schema':'ccc.soc.evidence.index.v1','generated_at':datetime.now(timezone.utc).isoformat(),'files':[{'path':k,'sha256':v} for k,v in hashes.items()]})
    (OUT/'sha256sums.txt').write_text(''.join(f"{digest}  {path}\n" for path,digest in hashes.items()),encoding='ascii')
    return {'state':'VERIFY','real_scenarios':summary.get('real_scenario_count',0),'files':len(hashes)+2,'bridge_mode':bridge.get('mode','FILE_FALLBACK')}


def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--watch',action='store_true')
    parser.add_argument('--interval',type=float,default=2.0)
    args=parser.parse_args()
    result=export_once(); print(json.dumps(result))
    if not args.watch: return 0
    last=None
    bridge_path=Path(os.getenv('CCC_BRIDGE_PAYLOAD_PATH',ROOT/'runtime'/'soc'/'ccc-soc-bridge-payload.json'))
    while True:
        marker=(bridge_path.stat().st_mtime_ns,bridge_path.stat().st_size) if bridge_path.exists() else None
        if marker!=last:
            result=export_once(); print(json.dumps(result),flush=True); last=marker
        time.sleep(max(args.interval,0.5))

if __name__=='__main__': raise SystemExit(main())
