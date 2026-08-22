import argparse, json
from ledger import append_event

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("ledger")
    p.add_argument("event_json")
    args=p.parse_args()
    event=json.loads(open(args.event_json,encoding="utf-8").read())
    print(json.dumps(append_event(args.ledger,event),indent=2))
