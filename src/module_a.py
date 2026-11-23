import json
from datetime import datetime, timezone
from pathlib import Path
from database import JSONStorage
from models import Object


def collect_active_objects(storage: JSONStorage) -> list[dict]:
    return [o for o in storage.objects if o["status"] == "active"]

def build_package(storage: JSONStorage) -> dict:
    objs = collect_active_objects(storage)
    return {
        "version": "1.0",
        "source": "realtor_export",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "objects": objs,
    }

def send(filepath: str = "data/exchange.json", debug=None) -> None:
    storage = JSONStorage("data.json")
    package = build_package(storage)
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(package, f, indent=2, ensure_ascii=False)
    if debug:
        debug.log(f"[module_a] Экспортировано {len(package['objects'])} объектов → {filepath}", 1)
    print(f"[module_a] Данные записаны в {filepath}")
