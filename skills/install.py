# -*- coding: utf-8 -*-
"""Install skills from this repo into the right Copilot folder per app.

Usage:
    python install.py                 # show what would change, touch nothing
    python install.py --apply         # write
    python install.py --apply --prune # also remove installed skills not in the repo

Why a script: each skill belongs to a specific app folder, git rewrites the
line endings to CRLF on checkout, and a folder in the wrong place fails
silently. Hand-copying gets all three wrong eventually.

Routing comes from the APP marker in each skill's own SKILL.md — a comment
line reading:  <!-- app: excel -->  or  <!-- app: powerpoint -->
Skills with no marker default to powerpoint.
"""
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ONEDRIVE = os.environ.get("VALOR_ONEDRIVE") or os.path.expanduser(r"~\OneDrive - Valor")
COPILOT = os.path.join(ONEDRIVE, "מסמכים", "Copilot")

APPS = {
    "powerpoint": os.path.join(COPILOT, "Microsoft PowerPoint", "skills"),
    "excel": os.path.join(COPILOT, "Microsoft Excel", "skills"),
}

# skills we know belong to Excel; everything else defaults to PowerPoint
EXCEL_SKILLS = {"variance-analysis", "exec-email"}

NOT_SKILLS = {"tests"}


def app_of(name, text):
    m = re.search(r"<!--\s*app:\s*(\w+)\s*-->", text)
    if m and m.group(1).lower() in APPS:
        return m.group(1).lower()
    return "excel" if name in EXCEL_SKILLS else "powerpoint"


def repo_skills():
    out = {}
    for d in sorted(os.listdir(HERE)):
        p = os.path.join(HERE, d)
        if not os.path.isdir(p) or d.startswith((".", "__")) or d in NOT_SKILLS:
            continue
        if d.endswith(".example"):
            continue  # parked on purpose
        f = os.path.join(p, "SKILL.md")
        if not os.path.exists(f):
            continue
        text = open(f, encoding="utf-8").read()
        out[d] = (app_of(d, text), text.replace("\r\n", "\n"))
    return out


def main():
    apply = "--apply" in sys.argv
    prune = "--prune" in sys.argv

    missing = [a for a, p in APPS.items() if not os.path.isdir(os.path.dirname(p))]
    if missing:
        print("These app folders do not exist yet:")
        for a in missing:
            print(f"  {a}: {os.path.dirname(APPS[a])}")
        print("\nCreate each one from inside that app:")
        print("  Copilot pane -> ... -> Manage skills -> Custom skills -> Create OneDrive folder")
        print("Copilot picks the folder name itself. Do not create it by hand.\n")

    skills = repo_skills()
    changes = 0

    for name, (app, text) in skills.items():
        root = APPS[app]
        if not os.path.isdir(os.path.dirname(root)):
            print(f"  skip  {name:22} ({app} folder missing)")
            continue
        dest_dir = os.path.join(root, name)
        dest = os.path.join(dest_dir, "SKILL.md")
        current = None
        if os.path.exists(dest):
            current = open(dest, encoding="utf-8").read().replace("\r\n", "\n")
        if current == text:
            print(f"  same  {name:22} -> {app}")
            continue
        verb = "update" if current is not None else "add   "
        print(f"  {verb} {name:22} -> {app}")
        changes += 1
        if apply:
            os.makedirs(dest_dir, exist_ok=True)
            with open(dest, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)

    if prune:
        for app, root in APPS.items():
            if not os.path.isdir(root):
                continue
            for d in sorted(os.listdir(root)):
                p = os.path.join(root, d)
                if not os.path.isdir(p) or d.endswith(".example"):
                    continue
                if d in skills:
                    continue
                print(f"  remove {d:21} <- {app} (not in repo)")
                changes += 1
                if apply:
                    shutil.rmtree(p)

    print()
    if not apply:
        print(f"{changes} change(s) pending. Re-run with --apply to write.")
    else:
        print(f"{changes} change(s) written.")
        print("In each app: Copilot -> Manage skills -> Custom skills -> Refresh.")
        print("No need to restart the app.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
