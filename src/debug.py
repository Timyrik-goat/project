import json
import functools
import inspect
from datetime import datetime
from typing import Any

class DebugHelper:
    def __init__(self, logfile: str = "debug.log", level: int = 1):
        self.logfile = logfile
        self.level = level
        self._indent = 0

    def log(self, msg: str, level: int = 1):
        if level > self.level:
            return
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"{'  '*self._indent}[{ts}] {msg}"
        print(line)
        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def dump(self, obj: Any, label: str = "DUMP", **kwargs):
        self.log(f"{label}:", 1)
        try:
            j = json.dumps(obj, indent=2, default=str, **kwargs)
            for line in j.splitlines():
                self.log(line, 1)
        except TypeError:
            import pprint
            self.log(pprint.pformat(obj), 1)

    def trace(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = func.__qualname__
            self._indent += 1
            self.log(f"CALL {name} args={args} kwargs={kwargs}", 3)
            try:
                result = func(*args, **kwargs)
                self.log(f"RETURN {name} -> {result!r}", 3)
                return result
            except Exception as e:
                self.log(f"EXCEPTION {name}: {e}", 3)
                raise
            finally:
                self._indent -= 1
        return wrapper

    def trace_call(self, func, *args, **kwargs):
        self._indent += 1
        self.log(f"CALL {func.__name__} {args} {kwargs}", 3)
        try:
            return func(*args, **kwargs)
        finally:
            self._indent -= 1
