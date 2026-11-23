from module_a import send
from module_b import process
from debug import DebugHelper

def integration_test():
    debug = DebugHelper("debug.log", level=2)
    debug.log("=== Интеграционный тест ===", 1)

    send("data/exchange.json", debug=debug)

    result = process("data/exchange.json", debug=debug)

    assert result["status"] == "ok", f"Ошибки: {result.get('details')}"
    assert result["stored"] == result["total"], \
        f"Загружено {result['stored']} из {result['total']}"

    debug.log(f"✅ Тест пройден: {result['stored']} объектов", 1)
    print(f"Передача успешна: {result['stored']} из {result['total']}")

if __name__ == "__main__":
    integration_test()
