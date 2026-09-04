import argparse, json
from ledger import verify_chain

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("ledger"); args=p.parse_args()
    result=verify_chain(args.ledger)
    print(json.dumps(result,indent=2)); raise SystemExit(0 if result["ok"] else 1)
