"""Check or apply the sprite fixes listed in corrections.json.

Usage: python corrections.py check   report problems in the pending list
       python corrections.py apply   fix the sprites, then move each entry
                                     from "pending" to "applied"

An entry:
  {"file": "agumon/agumon_26.png", "rotate": 90, "flip": "horizontal",
   "crop": [left, top, right, bottom], "note": "...", "by": "github name"}
Only "file" is required. Steps run in order: rotate (clockwise), flip, crop.
Crop numbers are pixels to cut off each side, counted after rotate and flip.
"""
import datetime
import json
import os
import sys

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
JSON = os.path.join(ROOT, "corrections.json")
SPRITES = os.path.join(ROOT, "sprites")


def problems(e):
    out = []
    f = e.get("file")
    if not isinstance(f, str):
        return ['missing "file"']
    path = os.path.normpath(os.path.join(SPRITES, f))
    if not path.startswith(os.path.normpath(SPRITES) + os.sep) or not os.path.isfile(path):
        return [f"{f}: no such sprite"]
    if not any(k in e for k in ("rotate", "flip", "crop")):
        out.append(f"{f}: nothing to do (add rotate, flip or crop)")
    if "rotate" in e and e["rotate"] not in (90, 180, 270):
        out.append(f"{f}: rotate must be 90, 180 or 270")
    if "flip" in e and e["flip"] not in ("horizontal", "vertical"):
        out.append(f'{f}: flip must be "horizontal" or "vertical"')
    if "crop" in e:
        c = e["crop"]
        if not (isinstance(c, list) and len(c) == 4 and all(isinstance(n, int) and n >= 0 for n in c)):
            out.append(f"{f}: crop must be [left, top, right, bottom], whole numbers of pixels")
        else:
            w, h = turned(Image.open(path), e).size
            if c[0] + c[2] >= w or c[1] + c[3] >= h:
                out.append(f"{f}: crop removes the whole image ({w}x{h})")
    return out


def turned(im, e):
    if "rotate" in e:
        im = im.rotate(-e["rotate"], expand=True)
    if e.get("flip") == "horizontal":
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    elif e.get("flip") == "vertical":
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    return im


def main():
    data = json.load(open(JSON, encoding="utf-8"))
    pending = data.get("pending", [])
    errors = [p for e in pending for p in problems(e)]
    for p in errors:
        print("ERROR", p)
    if errors:
        sys.exit(1)
    if sys.argv[1:] == ["check"]:
        print(f"{len(pending)} pending correction(s) look fine")
        return
    today = datetime.date.today().isoformat()
    for e in pending:
        path = os.path.join(SPRITES, e["file"])
        im = turned(Image.open(path), e)
        if "crop" in e:
            l, t, r, b = e["crop"]
            im = im.crop((l, t, im.width - r, im.height - b))
        im.save(path)
        data.setdefault("applied", []).append({**e, "applied": today})
        print("fixed", e["file"])
    data["pending"] = []
    with open(JSON, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


if __name__ == "__main__":
    main()
