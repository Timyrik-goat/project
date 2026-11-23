from src.debug import DebugHelper
import json, os

def test_log_writes_file(tmp_path):
    lf = tmp_path / "test.log"
    dh = DebugHelper(str(lf), level=1)
    dh.log("hello")
    assert lf.read_text().strip().endswith("hello")

def test_dump_json():
    dh = DebugHelper("/dev/null")
    data = {"a": 1}
    dh.dump(data)

def test_trace_decorator():
    calls = []
    @DebugHelper().trace
    def add(x, y):
        return x + y
    assert add(2, 3) == 5
