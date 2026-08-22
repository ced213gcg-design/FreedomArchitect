#!/usr/bin/env python3
from __future__ import annotations
import argparse, ipaddress, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / 'config' / 'soc-lab-targets.yaml'

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('--ip', required=True)
    p.add_argument('--role', required=True)
    p.add_argument('--port', type=int)
    args=p.parse_args()
    cfg=yaml.safe_load(REGISTRY.read_text(encoding='utf-8'))
    network=ipaddress.ip_network(cfg['authoritative_range'])
    ip=ipaddress.ip_address(args.ip)
    if ip not in network:
        print('REJECTED_EXTERNAL_OR_NONLAB_TARGET', file=sys.stderr); return 2
    matches=[t for t in cfg.get('targets',[]) if t.get('range_ip')==args.ip and t.get('role')==args.role]
    if len(matches)!=1:
        print('REJECTED_UNREGISTERED_TARGET_OR_ROLE', file=sys.stderr); return 3
    if args.port is not None:
        allowed=[]
        for svc in matches[0].get('allowed_services',[]): allowed.extend(svc.get('ports',[]))
        if args.port not in allowed:
            print('REJECTED_PORT_NOT_ALLOWLISTED', file=sys.stderr); return 4
    print(matches[0]['name'])
    return 0
if __name__=='__main__': raise SystemExit(main())
