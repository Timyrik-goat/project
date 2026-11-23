import json
from pathlib import Path
from database import JSONStorage
from models import Object
from debug import DebugHelper

EXPECTED = {"id","address","type","area","rooms","price","status"}

def receive(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def validate(data: dict) -> list[str]:
    errors = []
    for i, obj in enumerate(data.get("objects", [])):
        missing = EXPECTED - set(obj.keys())
        if missing:
            errors.append(f"Объект {i}: отсутствуют поля {missing}")
        if obj.get("price", 0) <= 0:
            errors.append(f"Объект {i}: цена должна быть > 0")
    return errors

def store_objects(data: dict, storage: JSONStorage) -> int:
    count = 0
    for obj_dict in data["objects"]:
        if not any(o["id"] == obj_dict["id"] for o in storage.objects):
            storage.objects.append(obj_dict)
            count += 1
    return count

def process(filepath: str, debug: DebugHelper = None) -> dict:
    data = receive(filepath)
    errors = validate(data)
    if errors:
        if debug:
            debug.log(f"[module_b] Ошибки валидации: {errors}", 2)
        return {"status": "error", "details": errors}

    test_storage = JSONStorage("data_test.json")
    stored = store_objects(data, test_storage)
    test_storage.save()

    if debug:
        debug.log(f"[module_b] Загружено {stored} объектов в data_test.json", 1)
    return {"status": "ok", "total": len(data["objects"]), "stored": stored}
