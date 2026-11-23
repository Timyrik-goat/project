from datetime import datetime
from collections import Counter

def deal_statistics(deals: list[dict], since: str | None = None) -> dict:
    filtered = deals
    if since:
        filtered = [d for d in deals if d.get("created", "") >= since]
    stages = Counter(d["stage"] for d in filtered)
    total = sum(d.get("price", 0) for d in filtered if "price" in d)
    agents_load = Counter(d["agent_id"] for d in filtered)
    return {
        "total_deals": len(filtered),
        "by_stage": dict(stages),
        "total_value": total,
        "agents_load": dict(agents_load),
    }
