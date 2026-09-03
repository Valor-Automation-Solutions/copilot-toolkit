# -*- coding: utf-8 -*-
"""Validate Copilot skill folders against the four rules that actually break loading.

Usage:
    python validate.py [folder]

Checks each subfolder for:
  1. A file named exactly SKILL.md (case-sensitive; Windows will not tell you)
  2. name: in the frontmatter matching the folder name
  3. Frontmatter opened AND closed with ---
  4. UTF-8 without BOM, LF line endings

Exit code 0 if everything passes, 1 otherwise.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

SUPPORTED = {".md", ".txt", ".csv", ".json", ".xml", ".html", ".svg", ".py", ".js"}


# directories in this repo that are tooling, not skills
NOT_SKILLS = {"tests"}


def check(folder, name):
    path = os.path.join(folder, name)
    problems = []
    entries = os.listdir(path)

    # ".example" is Microsoft's documented way to park a skill without deleting
    # it: Copilot skips any folder whose name does not match its `name`.
    expected = name[:-len(".example")] if name.endswith(".example") else name

    # 1. exact filename — os.listdir preserves real case even on Windows
    if "SKILL.md" not in entries:
        near = [e for e in entries if e.lower() == "skill.md"]
        if near:
            problems.append(f'file is "{near[0]}", must be exactly "SKILL.md"')
        else:
            problems.append("no SKILL.md at all")
        return problems

    raw = open(os.path.join(path, "SKILL.md"), "rb").read()

    # 4. encoding and line endings
    if raw[:3] == b"\xef\xbb\xbf":
        problems.append("UTF-8 BOM present — strip it")
    if b"\r\n" in raw:
        problems.append("CRLF line endings — convert to LF")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        problems.append("not valid UTF-8")
        return problems

    # Normalise line endings before the structural checks, so a CRLF file
    # reports "CRLF" only — not a bogus "frontmatter" error on top of it.
    text = text.replace("\r\n", "\n")

    # 3. frontmatter
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        problems.append("frontmatter must open AND close with ---")
        return problems

    fm = m.group(1)

    # 2. name matches folder, and obeys the Agent Skills naming rules
    nm = re.search(r"^name:\s*(\S+)", fm, re.M)
    if not nm:
        problems.append("frontmatter has no name:")
    else:
        n = nm.group(1)
        if n != expected:
            problems.append(f'name "{n}" does not match folder "{expected}"')
        # agentskills.io/specification
        if len(n) > 64:
            problems.append(f"name is {len(n)} chars, spec limit is 64")
        if not re.fullmatch(r"[a-z0-9-]+", n):
            problems.append("name may only contain lowercase a-z, 0-9 and hyphens")
        if n.startswith("-") or n.endswith("-"):
            problems.append("name must not start or end with a hyphen")
        if "--" in n:
            problems.append("name must not contain consecutive hyphens")

    d = re.search(r"^description:\s*(\S.*)$", fm, re.M)
    if not d:
        problems.append("frontmatter has no description:")
    elif len(d.group(1)) > 1024:
        problems.append(f"description is {len(d.group(1))} chars, spec limit is 1024")

    return problems


def advisories(folder, name):
    """Non-fatal notes. These do not affect the exit code."""
    notes = []
    for e in os.listdir(os.path.join(folder, name)):
        ext = os.path.splitext(e)[1].lower()
        if ext and ext not in SUPPORTED:
            notes.append(f'"{e}" has an extension a skill folder does not support')
    return notes


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    names = sorted(
        d for d in os.listdir(folder)
        if os.path.isdir(os.path.join(folder, d))
        and not d.startswith(".")      # .git, .vscode
        and not d.startswith("__")     # __pycache__
        and d not in NOT_SKILLS
    )
    if not names:
        print("no skill folders found in", folder)
        return 1

    failed = 0
    for name in names:
        problems = check(folder, name)
        if problems:
            failed += 1
            print(f"FAIL  {name}")
            for p in problems:
                print(f"        - {p}")
        else:
            tag = "ok   " if not name.endswith(".example") else "off  "
            print(f"{tag} {name}" + ("   (parked: .example suffix)" if name.endswith(".example") else ""))
        for note in advisories(folder, name):
            print(f"        note: {note}")

    print()
    if failed:
        print(f"{failed} of {len(names)} skill(s) will not load correctly.")
        return 1
    print(f"All {len(names)} skill(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
