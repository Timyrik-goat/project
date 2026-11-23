import shutil, datetime, os

src = "data.json"

if os.path.exists(src):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(src, f"backup/data_{ts}.json")
    print("Backup created")
