#!/usr/bin/env python3
"""Rebuild official-documents-md/README.md from state.jsonl.

Titles/published are taken from the front matter of the IT/EN Markdown files
themselves (which were written from index.jsonl), so the index never invents data.
Hold entries are excluded. Deduped by original_sha256 (last wins).
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))


def front_matter(path):
    fm = {}
    try:
        with open(os.path.join(BASE, path), encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return fm
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return fm
    for line in m.group(1).splitlines():
        mm = re.match(r"^(\w+):\s*(.*)$", line)
        if mm:
            key, val = mm.group(1), mm.group(2).strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1].replace('\\"', '"')
            fm[key] = val
    return fm


def main():
    entries = {}
    with open(os.path.join(BASE, "state.jsonl"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            entries[e["original_sha256"]] = e  # last wins

    done = [e for e in entries.values() if e.get("status") == "done"]

    rows = []
    for e in done:
        fm = front_matter(e["it_path"])
        fm_en = front_matter(e["en_path"])
        title_it = e.get("title_it") or fm.get("title_it") or "?"
        title_en = e.get("title_en") or fm_en.get("title_en") or "English"
        published = e.get("published") or fm.get("published") or "?"
        rows.append((published, title_it, title_en, e["it_path"], e["en_path"]))

    rows.sort(key=lambda r: (r[0], r[3]), reverse=True)

    lines = [
        "# Collesano — Official documents, unofficial English mirror",
        "",
        "This folder is an unofficial mirror of official documents published by the "
        "Comune di Collesano, converted to Markdown and machine-translated into English. "
        "The Italian originals published by the Comune di Collesano are the only legally valid texts.",
        "",
        "- `it/<year>/` — faithful Markdown conversion of each original, in Italian",
        "- `en/<year>/` — complete English translation of the Italian file",
        "- Each file's front matter records the source page, source file URL, the "
        "original's path and SHA-256, and how it was converted.",
        "",
        f"Documents indexed: {len(rows)}. Documents converted but awaiting a "
        "personal-data review are listed in `needs-review.md` and are not indexed here.",
        "",
        "| Published | Document (Italian) | English |",
        "|---|---|---|",
    ]
    for published, title_it, title_en, it_path, en_path in rows:
        ti = title_it.replace("|", "\\|")
        te = title_en.replace("|", "\\|")
        lines.append(f"| {published} | [{ti}]({it_path}) | [{te}]({en_path}) |")
    lines += [
        "",
        "_Every English file carries the notice that it is an unofficial machine "
        "translation and that the Italian original published by the Comune di "
        "Collesano is the only valid text._",
        "",
    ]

    with open(os.path.join(BASE, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"README.md rebuilt: {len(rows)} documents indexed")


if __name__ == "__main__":
    main()
