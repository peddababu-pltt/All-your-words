#!/usr/bin/env python3
"""Split the dictionary into translation batches.

Reads backend/data/dictionary.json, writes compact per-entry source rows to
backend/data/en-batches/batch_NNN.json for translation into English. Only the
user-visible text fields are extracted; ids and structure are rebuilt later.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "dictionary.json"
OUT = ROOT / "data" / "en-batches"
OUT.mkdir(exist_ok=True)

BATCH = 120
FIELDS = ("term", "definition", "example", "note", "category")

data = json.loads(SRC.read_text(encoding="utf-8"))
entries = data["entries"]

rows = []
for e in entries:
    row = {"id": e["id"]}
    for f in FIELDS:
        v = e.get(f)
        if v:
            row[f] = v
    aliases = e.get("aliases") or []
    if aliases:
        row["aliases"] = aliases
    rows.append(row)

# also translate the 7 field names once (shared)
meta = {"fields": {f["id"]: f["name"] for f in data["fields"]}}
(OUT / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

n = 0
for i in range(0, len(rows), BATCH):
    chunk = rows[i : i + BATCH]
    (OUT / f"batch_{n:03d}.json").write_text(
        json.dumps(chunk, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    n += 1

print(json.dumps({"entries": len(rows), "batches": n, "batch_size": BATCH, "out": str(OUT)}))
