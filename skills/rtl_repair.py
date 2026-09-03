# -*- coding: utf-8 -*-
"""Repair Hebrew right-to-left layout in a .pptx.

Usage:
    python rtl_repair.py deck.pptx              # writes deck.rtl-fixed.pptx
    python rtl_repair.py deck.pptx --in-place   # overwrites deck.pptx

Two passes, both measured against PowerPoint's own renderer on 2.9.2026:

  1. paragraph  - every paragraph containing Hebrew gets rtl="1" algn="r"
  2. runs       - each paragraph is re-split into runs by script, and each run
                  is tagged lang="he-IL" or lang="en-US"

Pass 2 is the one that matters and the one everyone skips. Without it, a space
between a Latin word and a Hebrew word renders on the wrong side of the word -
"CoPilot בתוך" displays as "CoPilotבתוך" in Slide Show even though the space is
present in the file. A non-breaking space fixes this only where the neighbour is
a digit; tagging the runs fixes every case, and needs no character substitution.

Idempotent: running it twice changes nothing the second time.
"""
import os
import re
import shutil
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
HEB = re.compile(r"[֐-׿]")
# a Latin word (possibly several) OR a stretch of anything else
CHUNK = re.compile(r"[A-Za-z][A-Za-z0-9'\-\.]*(?:\s+[A-Za-z][A-Za-z0-9'\-\.]*)*|[^A-Za-z]+")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def is_latin(s):
    return bool(re.match(r"^[A-Za-z]", s))


def fix_paragraph(p_xml, stats):
    texts = re.findall(r"<a:t>(.*?)</a:t>", p_xml, re.S)
    full = "".join(texts)
    if not HEB.search(full):
        return p_xml

    stats["hebrew_paragraphs"] += 1

    # --- pass 1: paragraph direction and alignment ---
    m = re.search(r"<a:pPr\b([^>]*?)(/?)>", p_xml)
    if m:
        attrs, selfclose = m.group(1), m.group(2)
        had = 'rtl="1"' in attrs and 'algn="r"' in attrs
        attrs = re.sub(r'\s*rtl="[^"]*"', "", attrs)
        attrs = re.sub(r'\s*algn="[^"]*"', "", attrs)
        new = f'<a:pPr{attrs} rtl="1" algn="r"{selfclose}>'
        p_xml = p_xml[:m.start()] + new + p_xml[m.end():]
        if not had:
            stats["aligned"] += 1
    else:
        p_xml = p_xml.replace("<a:p>", '<a:p><a:pPr rtl="1" algn="r"/>', 1)
        stats["aligned"] += 1

    # --- pass 2: one run per script, each tagged ---
    already = all(
        'lang="he-IL"' in r or 'lang="en-US"' in r
        for r in re.findall(r"<a:r>.*?</a:r>", p_xml, re.S)
    ) and re.search(r"<a:r>", p_xml)

    chunks = [c for c in CHUNK.findall(full) if c]
    if already and len(chunks) == len(re.findall(r"<a:r>", p_xml)):
        return p_xml

    # keep the first run's rPr as the style template
    first = re.search(r"<a:r>\s*(<a:rPr\b.*?(?:/>|</a:rPr>))", p_xml, re.S)
    tmpl = first.group(1) if first else "<a:rPr/>"
    tmpl = re.sub(r'\s*(alt)?[Ll]ang="[^"]*"', "", tmpl)

    runs = []
    for c in chunks:
        lang, alt = ("en-US", "he-IL") if is_latin(c) else ("he-IL", "en-US")
        rpr = tmpl
        if rpr.endswith("/>"):
            rpr = rpr[:-2] + f' lang="{lang}" altLang="{alt}"/>'
        else:
            rpr = rpr.replace("<a:rPr", f'<a:rPr lang="{lang}" altLang="{alt}"', 1)
        runs.append(f"<a:r>{rpr}<a:t>{esc(c)}</a:t></a:r>")
        stats["runs_tagged"] += 1

    # replace the run block, keep pPr and any trailing endParaRPr
    p_xml = re.sub(r"(<a:r>.*</a:r>)", "".join(runs), p_xml, count=1, flags=re.S)
    stats["paragraphs_resplit"] += 1
    return p_xml


def repair(src, dst):
    stats = {"slides": 0, "hebrew_paragraphs": 0, "aligned": 0,
             "paragraphs_resplit": 0, "runs_tagged": 0}
    zin = zipfile.ZipFile(src)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.match(r"ppt/slides/slide\d+\.xml$", item.filename):
                stats["slides"] += 1
                xml = data.decode("utf-8")
                out, last = [], 0
                for m in re.finditer(r"<a:p>.*?</a:p>", xml, re.S):
                    out.append(xml[last:m.start()])
                    out.append(fix_paragraph(m.group(0), stats))
                    last = m.end()
                out.append(xml[last:])
                data = "".join(out).encode("utf-8")
            zout.writestr(item, data)
    return stats


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    inplace = "--in-place" in sys.argv
    if not args:
        print(__doc__)
        return 2

    src = args[0]
    if not os.path.exists(src):
        print("no such file:", src)
        return 1

    base, ext = os.path.splitext(src)
    dst = base + ".rtl-fixed" + ext
    stats = repair(src, dst)

    print(f"slides scanned        : {stats['slides']}")
    print(f"Hebrew paragraphs     : {stats['hebrew_paragraphs']}")
    print(f"  set rtl + right     : {stats['aligned']}")
    print(f"  re-split into runs  : {stats['paragraphs_resplit']}")
    print(f"  runs tagged by lang : {stats['runs_tagged']}")

    if inplace:
        shutil.move(dst, src)
        print(f"\nwrote {src} (in place)")
    else:
        print(f"\nwrote {dst}")
    print("Open it in Slide Show and check a mixed Hebrew/English line.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
