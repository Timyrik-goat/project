import argparse
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from debug import DebugHelper
from database import JSONStorage
from models import Object, Client, Deal, Status, DealStage
from search import filter_objects, match_objects_for_client
from reports import deal_statistics


def load_config():
    with open("config/config.json") as f:
        return json.load(f)

def cmd_object(args, db):
    if args.action == "add":
        obj = Object(
            address=args.address,
            type=args.type,
            area=float(args.area),
            rooms=int(args.rooms),
            price=float(args.price),
        )
        db.add_object(obj.to_dict())
        db.save()
        print(f"Object {obj.id} added")
    elif args.action == "list":
        for o in db.objects:
            print(o)
    elif args.action == "archive":
        updated = db.update_object(args.id, status=Status.ARCHIVED.value)
        if updated:
            db.save()
            print("Archived")
    elif args.action == "delete":
        db.delete_object(args.id)
        db.save()
        print("Deleted")

def cmd_client(args, db):
    if args.action == "add":
        client = Client(
            name=args.name,
            phone=args.phone,
            budget=float(args.budget),
            requirements=args.reqs or {},
        )
        db.add_client(client.to_dict())
        db.save()
        print(f"Client {client.id} added")
    elif args.action == "list":
        for c in db.clients:
            print(c)

def cmd_search(args, db):
    results = filter_objects(db.objects, **vars(args))
    print(f"Found {len(results)}")
    for o in results:
        print(o)

def cmd_match(args, db):
    client = next((c for c in db.clients if c["id"] == args.client_id), None)
    if not client:
        print("Client not found")
        return
    matches = match_objects_for_client(client, db.objects)
    print(f"Matches for {client['name']}: {len(matches)}")
    for o in matches:
        print(o)

def cmd_deal(args, db):
    if args.action == "create":
        deal = Deal(
            object_id=args.object_id,
            client_id=args.client_id,
            agent_id=args.agent_id,
            stage=DealStage.VIEW.value,
            created="2026-11-20",
        )
        db.add_deal(deal.to_dict())
        db.save()
        print(f"Deal {deal.id} created")
    elif args.action == "update":
        updated = db.update_deal(args.deal_id, stage=args.stage)
        if updated:
            db.save()
            print("Updated")

def cmd_report(args, db):
    stats = deal_statistics(db.deals, since=args.since)
    print(json.dumps(stats, indent=2, ensure_ascii=False))

def main():
    cfg = load_config()
    db = JSONStorage(cfg["data_file"])

    p = argparse.ArgumentParser("realtor")
    sub = p.add_subparsers(dest="command")

    obj_p = sub.add_parser("object")
    obj_p.add_argument("action", choices=["add", "list", "archive", "delete"])
    obj_p.add_argument("--id")
    obj_p.add_argument("--address")
    obj_p.add_argument("--type")
    obj_p.add_argument("--area")
    obj_p.add_argument("--rooms")
    obj_p.add_argument("--price")

    cli_p = sub.add_parser("client")
    cli_p.add_argument("action", choices=["add", "list"])
    cli_p.add_argument("--name")
    cli_p.add_argument("--phone")
    cli_p.add_argument("--budget")
    cli_p.add_argument("--reqs")

    srch_p = sub.add_parser("search")
    srch_p.add_argument("--status")
    srch_p.add_argument("--min_area")
    srch_p.add_argument("--max_price")

    match_p = sub.add_parser("match")
    match_p.add_argument("client_id")

    deal_p = sub.add_parser("deal")
    deal_p.add_argument("action", choices=["create", "update"])
    deal_p.add_argument("--deal_id")
    deal_p.add_argument("--object_id")
    deal_p.add_argument("--client_id")
    deal_p.add_argument("--agent_id")
    deal_p.add_argument("--stage")

    rep_p = sub.add_parser("report")
    rep_p.add_argument("--since")

    parser.add_argument("--debug", action="store_true", help="включить отладку")

    debug = None
    if args.debug:
        debug = DebugHelper("debug.log", level=3)
        debug.log("Отладка включена", 1)

      def _trace(func, *a, **kw):
          if debug:
              return debug.trace_call(func, *a, **kw)
          return func(*a, **kw)

    args = p.parse_args()
    if args.command == "object":
        cmd_object(args, db)
    elif args.command == "client":
        cmd_client(args, db)
    elif args.command == "search":
        kwargs = {k: (int(v) if k in ("min_area",) else float(v) if k in ("max_price",) else v)
                  for k, v in vars(args).items() if v is not None}
        print(json.dumps(filter_objects(db.objects, **kwargs), indent=2, ensure_ascii=False))
    elif args.command == "match":
        cmd_match(args, db)
    elif args.command == "deal":
        cmd_deal(args, db)
    elif args.command == "report":
        cmd_report(args, db)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
