from src.search import filter_objects

def test_filter_by_price():
    objs = [{"id": "1", "price": 5000000, "status": "active"},
            {"id": "2", "price": 12000000, "status": "active"}]
    res = filter_objects(objs, max_price=8000000, status="active")
    assert len(res) == 1
    assert res[0]["id"] == "1"
