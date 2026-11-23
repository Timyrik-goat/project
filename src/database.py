import json
from pathlib import Path


class JSONStorage:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._data: dict[str, list[dict]] = {
            "objects": [],
            "clients": [],
            "deals": [],
            "agents": [],
        }
        self.load()

    def load(self):
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                self._data = json.load(f)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    @property
    def objects(self) -> list[dict]:
        return self._data["objects"]

    def add_object(self, obj: dict) -> dict:
        self._data["objects"].append(obj)
        return obj

    def update_object(self, obj_id: str, **changes) -> dict | None:
        for obj in self._data["objects"]:
            if obj["id"] == obj_id:
                obj.update(changes)
                return obj
        return None

    def delete_object(self, obj_id: str) -> bool:
        self._data["objects"] = [o for o in self._data["objects"] if o["id"] != obj_id]
        return True

    @property
    def clients(self) -> list[dict]:
        return self._data["clients"]

    def add_client(self, client: dict) -> dict:
        self._data["clients"].append(client)
        return client

    @property
    def deals(self) -> list[dict]:
        return self._data["deals"]

    def add_deal(self, deal: dict) -> dict:
        self._data["deals"].append(deal)
        return deal

    def update_deal(self, deal_id: str, **changes) -> dict | None:
        for d in self._data["deals"]:
            if d["id"] == deal_id:
                d.update(changes)
                return d
        return None

    @property
    def agents(self) -> list[dict]:
        return self._data["agents"]

    def get_agent(self, agent_id: str) -> dict | None:
        return next((a for a in self._data["agents"] if a["id"] == agent_id), None)
