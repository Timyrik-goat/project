from src.models import Object, Client, Deal, Status, DealStage

def test_object_creation():
    o = Object(address="X", price=1_000_000)
    assert o.status == Status.ACTIVE.value
    assert "id" in o.to_dict()

def test_client_from_dict():
    d = {"name": "Анна", "budget": 5_000_000, "requirements": {"min_area": 35}}
    c = Client.from_dict(d)
    assert c.budget == 5_000_000
    assert c.requirements["min_area"] == 35
