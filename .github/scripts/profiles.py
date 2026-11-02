"""Check digimon.json, or list what is still missing from it.

Usage: python profiles.py check   report mistakes that would break the file for others
       python profiles.py todo    list profiles to write and fields to fill in

A profile:
  {"folder": "agumon",
   "name": {"en": "Agumon", "zh": "亞古獸"},          zh is Traditional Chinese;
   "stage": {"en": "Rookie", "zh": "成長期"},         Simplified may be added as "zh_hans"
   "attribute": {"en": "Vaccine", "zh": "疫苗種"},
   "type": {"en": "Reptile", "zh": "爬蟲類型"},
   "evolves_from": ["koromon"], "evolves_to": ["greymon", "numemon[mistake]"],
   "description": {"en": "...", "zh": "..."},
   "source": "https://digimon.net/reference_en/detail.php?directory_name=agumon"}
"""
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
JSON = os.path.join(ROOT, "digimon.json")
BAKED = os.path.join(ROOT, "baked")

STAGES = {"Baby I": "幼年期Ⅰ", "Baby II": "幼年期Ⅱ", "Rookie": "成長期", "Champion": "成熟期",
          "Ultimate": "完全體", "Mega": "究極體", "Mega+": "究極體", "Armor": "裝甲體"}
TEXTS = ("name", "stage", "attribute", "type", "description")
TAGS = ("dark", "mistake", "warp", "armor", "mode")
FOLDER = re.compile(r"^[a-z0-9_-]+$")
# evolves_to: name, name[tag] or name(+partner); evolves_from may also be a+b (a fusion)
LINK = re.compile(r"^([a-z0-9_-]+)(?:\(\+([a-z0-9_+-]+)\))?(?:\[(\w+)\])?$")


def linked(tok, col):
    """The folders a link names, or None if it can't be read."""
    if col == "evolves_from" and "+" in tok and "(" not in tok:
        parts = tok.split("+")
        return parts if all(FOLDER.match(p) for p in parts) else None
    m = LINK.match(tok)
    if not m or (m.group(3) and m.group(3) not in TAGS):
        return None
    return [m.group(1)] + (m.group(2).split("+") if m.group(2) else [])


def problems(data):
    if not isinstance(data, list):
        return ["digimon.json must be a list of profiles"]
    out, folders = [], set()
    for i, e in enumerate(data):
        where = f"entry {i + 1}"
        if not isinstance(e, dict):
            out.append(f"{where}: not a profile ({{...}})")
            continue
        f = e.get("folder")
        if not isinstance(f, str) or not FOLDER.match(f):
            out.append(f'{where}: "folder" must be lower-case letters, digits, _ or -')
            continue
        where = f
        if f in folders:
            out.append(f"{f}: listed twice")
        folders.add(f)
        for k in TEXTS:
            v = e.get(k)
            if not isinstance(v, dict) or not all(isinstance(v.get(x, ""), str) for x in ("en", "zh", "zh_hans")):
                out.append(f'{where}: "{k}" must be {{"en": "...", "zh": "..."}}')
        if not (e.get("name") or {}).get("en"):
            out.append(f"{where}: needs an English name")
        st = (e.get("stage") or {}).get("en")
        if st not in STAGES:
            out.append(f"{where}: stage must be one of {', '.join(STAGES)}")
        if not isinstance(e.get("source") or "", str):
            out.append(f'{where}: "source" must be a link')
    for e in data:
        if not isinstance(e, dict) or e.get("folder") not in folders:
            continue
        for col in ("evolves_from", "evolves_to"):
            links = e.get(col)
            if not isinstance(links, list) or not all(isinstance(t, str) for t in links):
                out.append(f'{e["folder"]}: "{col}" must be a list of folders')
                continue
            for tok in links:
                names = linked(tok, col)
                if names is None:
                    out.append(f"{e['folder']}: can't read {tok!r} in {col} (tags: {', '.join(TAGS)})")
                for n in names or []:
                    if n not in folders:
                        out.append(f"{e['folder']}: {col} names {n!r}, which has no profile")
    return out


def todo(data):
    by = {e["folder"]: e for e in data}
    baked = sorted(os.listdir(BAKED)) if os.path.isdir(BAKED) else []
    # a version like agumon_adventure shares agumon's profile
    missing = [f for f in baked if f not in by and f.split("_")[0] not in by]
    print(f"Profiles to write ({len(missing)}): Digimon in baked/ with no profile")
    for f in missing:
        print(f"  {f}")
    gaps = []
    for e in data:
        f = e["folder"]
        st = e["stage"]
        for k in TEXTS:
            if k == "attribute" and st["en"].startswith("Baby"):
                continue  # Baby Digimon have no attribute
            for lang in ("en", "zh"):
                if not e[k].get(lang):
                    gaps.append(f"{f}: {k} ({lang}) is empty")
        if st["en"] in STAGES and st["zh"] and st["zh"] != STAGES[st["en"]]:
            gaps.append(f"{f}: stage {st['en']} is {STAGES[st['en']]} in Chinese, not {st['zh']}")
        if not e.get("source"):
            gaps.append(f"{f}: no source link")
    print(f"\nFields to fill in or check ({len(gaps)}):")
    for g in gaps:
        print(f"  {g}")


def main():
    if sys.argv[1:] not in (["check"], ["todo"]):
        sys.exit(__doc__)
    try:
        data = json.load(open(JSON, encoding="utf-8"))
    except ValueError as err:
        sys.exit(f"digimon.json is not valid JSON: {err}")
    found = problems(data)
    if sys.argv[1] == "check" or found:
        for p in found:
            print(p)
        if found:
            sys.exit(f"{len(found)} problem(s) in digimon.json")
        print(f"digimon.json: {len(data)} profiles, all fine")
        return
    todo(data)


if __name__ == "__main__":
    main()
