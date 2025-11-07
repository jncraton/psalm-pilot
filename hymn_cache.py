from pathlib import Path
import json

hymns = sorted(
    str(p.as_posix())
    for p in Path("hymns").rglob("*")
    if p.is_file()
)

Path("hymns_list.json").write_text(json.dumps(hymns, indent=2), encoding="utf-8")