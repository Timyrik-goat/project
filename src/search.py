from typing import Iterable


def filter_objects(objects: list[dict], **criteria) -> list[dict]:
    result = objects
    for key, val in criteria.items():
        if key.startswith("min_"):
            attr = key[4:]
            result = [o for o in result if o.get(attr, 0) >= val]
        elif key.startswith("max_"):
            attr = key[4:]
            result = [o for o in result if o.get(attr, 0) <= val]
        else:
            result = [o for o in result if o.get(key) == val]
    return result


def match_objects_for_client(client: dict, objects: list[dict]) -> list[dict]:
    req = client.get("requirements", {})
    return filter_objects(
        objects,
        status="active",
        price__lte=client.get("budget", float("inf")),
        **req
    )
