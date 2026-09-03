# -*- coding: utf-8 -*-
"""Fingerprint the RTL state of a .pptx, so a skill's claim can be checked against the file.

Usage:
    python rtl-fingerprint.py deck.pptx            # print the fingerprint
    python rtl-fingerprint.py before.json deck.pptx  # compare against a saved run

Why this exists: a skill reports on itself. "Fixed 14 paragraphs" is the skill's
own claim, not evidence. This reads the actual XML and counts what is really there.
"""
import json
import os
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")

HEB = re.compile(r"[֐-׿]")
SWALLOWED = re.compile(r"[0-9%](?=[֐-׿])|[֐-׿](?=[0-9])")


def fingerprint(path):
    z = zipfile.ZipFile(path)
    slides = sorted(
        (n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
        key=lambda n: int(re.search(r"\d+", n.split("/")[-1]).group()),
    )
    out = {"file": os.path.basename(path), "slides": len(slides), "per_slide": [],
           "totals": {"paragraphs": 0, "hebrew_paragraphs": 0, "rtl": 0,
                      "align_right": 0, "swallowed_spaces": 0}}

    for i, n in enumerate(slides, 1):
        xml = z.read(n).decode("utf-8")
        paras = re.findall(r"<a:p>.*?</a:p>", xml, re.S)
        rec = {"slide": i, "paragraphs": 0, "hebrew": 0, "rtl": 0, "algn_r": 0,
               "swallowed": [], "texts": []}
        for p in paras:
            runs = re.findall(r"<a:t>(.*?)</a:t>", p, re.S)
            text = "".join(runs).strip()
            if not text:
                continue
            rec["paragraphs"] += 1
            pPr = re.search(r"<a:pPr[^>]*/?>", p)
            attrs = pPr.group(0) if pPr else ""
            if HEB.search(text):
                rec["hebrew"] += 1
                if 'rtl="1"' in attrs:
                    rec["rtl"] += 1
                if 'algn="r"' in attrs:
                    rec["algn_r"] += 1
                for m in SWALLOWED.finditer(text):
                    frag = text[max(0, m.start() - 4):m.end() + 6]
                    rec["swallowed"].append(frag)
            rec["texts"].append(text)
        out["per_slide"].append(rec)
        out["totals"]["paragraphs"] += rec["paragraphs"]
        out["totals"]["hebrew_paragraphs"] += rec["hebrew"]
        out["totals"]["rtl"] += rec["rtl"]
        out["totals"]["align_right"] += rec["algn_r"]
        out["totals"]["swallowed_spaces"] += len(rec["swallowed"])
    return out


def show(fp):
    t = fp["totals"]
    print(f'{fp["file"]} — {fp["slides"]} slides')
    print(f'  paragraphs with text : {t["paragraphs"]}')
    print(f'  containing Hebrew    : {t["hebrew_paragraphs"]}')
    print(f'  with rtl="1"         : {t["rtl"]}')
    print(f'  with algn="r"        : {t["align_right"]}')
    print(f'  swallowed spaces     : {t["swallowed_spaces"]}')
    for s in fp["per_slide"]:
        if s["swallowed"]:
            print(f'    slide {s["slide"]}: {s["swallowed"]}')


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    if len(args) == 1:
        fp = fingerprint(args[0])
        show(fp)
        base = os.path.splitext(os.path.basename(args[0]))[0]
        dest = base + ".rtl-before.json"
        json.dump(fp, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nsaved baseline -> {dest}")
        return 0

    before = json.load(open(args[0], encoding="utf-8"))
    after = fingerprint(args[1])
    print("BEFORE / AFTER\n")
    changed = False
    for k in ("paragraphs", "hebrew_paragraphs", "rtl", "align_right", "swallowed_spaces"):
        b, a = before["totals"][k], after["totals"][k]
        mark = "" if a == b else "   <-- CHANGED"
        if a != b:
            changed = True
        print(f"  {k:22} {b:4} -> {a:4}{mark}")

    b_txt = [t for s in before["per_slide"] for t in s["texts"]]
    a_txt = [t for s in after["per_slide"] for t in s["texts"]]
    print(f"\n  text blocks            {len(b_txt):4} -> {len(a_txt):4}")
    edits = [(x, y) for x, y in zip(b_txt, a_txt) if x != y]
    if edits:
        changed = True
        print(f"  {len(edits)} text block(s) differ:")
        for x, y in edits[:15]:
            print(f"    - {x}\n    + {y}")
    else:
        print("  no text content changed")

    print("\nVERDICT:", "the file changed" if changed else "the file is byte-identical in every measured dimension")
    return 0


if __name__ == "__main__":
    sys.exit(main())
