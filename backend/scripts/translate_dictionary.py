#!/usr/bin/env python3
"""Translate the dictionary batches to English via an LLM API.

Bypasses the Claude Code weekly limit by using a direct API key (separate
billing). Resumable: skips batches whose .en.json already exists.

Prereqs:
  python3 scripts/make_en_batches.py      # creates data/en-batches/batch_*.json
Set ONE of:
  export ANTHROPIC_API_KEY=sk-ant-...      # uses anthropic (claude)
  export OPENAI_API_KEY=sk-...             # uses openai
Run:
  python3 scripts/translate_dictionary.py
Then:
  python3 scripts/assemble_en.py           # builds frontend/data.en.js

Only user-visible text is translated (term, definition, example, note,
category, aliases). ids are preserved. meta.json -> meta.en.json (field names).
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCHES = ROOT / "data" / "en-batches"

SYS = (
    "You translate Korean workplace-dictionary data into natural, professional "
    "English. You are given a JSON array of entries. Translate ONLY these text "
    "fields when present: term, definition, example, note, category, and each "
    "string in aliases. Keep the 'id' field EXACTLY unchanged. Keep only keys "
    "that were present. For English-loanword terms (CPC, 드롭->drop, 캡션->caption) "
    "use the real English word. Return ONLY a JSON array, same length and order, "
    "same keys, valid JSON, no commentary."
)


def _anthropic(text: str) -> str:
    import anthropic

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=os.environ.get("TRANSLATE_MODEL", "claude-opus-4-8"),
        max_tokens=16000,
        system=SYS,
        messages=[{"role": "user", "content": text}],
    )
    return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")


def _openai(text: str) -> str:
    from openai import OpenAI

    client = OpenAI()
    r = client.chat.completions.create(
        model=os.environ.get("TRANSLATE_MODEL", "gpt-4o"),
        messages=[{"role": "system", "content": SYS}, {"role": "user", "content": text}],
        response_format={"type": "json_object"},
    )
    return r.choices[0].message.content


def translator():
    if os.environ.get("ANTHROPIC_API_KEY"):
        return _anthropic
    if os.environ.get("OPENAI_API_KEY"):
        return _openai
    sys.exit("Set ANTHROPIC_API_KEY or OPENAI_API_KEY first.")


def extract_json_array(s: str):
    s = s.strip()
    i, j = s.find("["), s.rfind("]")
    if i == -1 or j == -1:
        raise ValueError("no JSON array in model output")
    return json.loads(s[i : j + 1])


def main():
    call = translator()
    srcs = sorted(BATCHES.glob("batch_*.json"))
    srcs = [p for p in srcs if not p.name.endswith(".en.json")]
    done = skipped = 0
    for src in srcs:
        out = src.with_suffix(".en.json")
        if out.exists():
            skipped += 1
            continue
        rows = json.loads(src.read_text(encoding="utf-8"))
        raw = call(json.dumps(rows, ensure_ascii=False))
        tr = extract_json_array(raw)
        if len(tr) != len(rows):
            print(f"! {src.name}: got {len(tr)} of {len(rows)} — retrying once")
            tr = extract_json_array(call(json.dumps(rows, ensure_ascii=False)))
        out.write_text(json.dumps(tr, ensure_ascii=False, indent=1), encoding="utf-8")
        done += 1
        print(f"  {src.name} -> {out.name} ({len(tr)})")

    # field names
    meta = BATCHES / "meta.json"
    meta_en = BATCHES / "meta.en.json"
    if meta.exists() and not meta_en.exists():
        m = json.loads(meta.read_text(encoding="utf-8"))
        raw = call(
            "Translate each Korean field name to concise English. Return ONLY a JSON "
            'object with the same keys. Input: ' + json.dumps(m["fields"], ensure_ascii=False)
        )
        s = raw[raw.find("{") : raw.rfind("}") + 1]
        meta_en.write_text(
            json.dumps({"fields": json.loads(s)}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print("  meta.json -> meta.en.json")

    print(json.dumps({"translated": done, "skipped_existing": skipped}))


if __name__ == "__main__":
    main()
