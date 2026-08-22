#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[3]
REGISTRY=ROOT/'config'/'soc-lab-targets.yaml'
def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--name',required=True); p.add_argument('--role',required=True); a=p.parse_args()
    cfg=yaml.safe_load(REGISTRY.read_text(encoding='utf-8'))
    matches=[t for t in cfg.get('targets',[]) if t.get('name')==a.name and t.get('role')==a.role]
    if len(matches)!=1:
        print('REJECTED_UNREGISTERED_LOCAL_HOST_OR_ROLE',file=sys.stderr); return 3
    print(a.name); return 0
if __name__=='__main__': raise SystemExit(main())
