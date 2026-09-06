# -*- coding: utf-8 -*-
"""Build the three test files for the untested editing skills.

Each file carries deliberate traps that test the skill's NEGATIVE rules —
the "do not touch" clauses. Those are where a skill actually causes damage,
and they are the part a happy-path test never reaches.

Usage:
    python build_tests.py [output_dir]     # default: current directory
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.text import PP_ALIGN
import openpyxl


def rtl(p):
    pPr = p._p.get_or_add_pPr()
    pPr.set("rtl", "1")
    pPr.set("algn", "r")


def hebrew(frame, lines):
    frame.text = lines[0]
    for l in lines[1:]:
        frame.add_paragraph().text = l
    for p in frame.paragraphs:
        p.alignment = PP_ALIGN.RIGHT
        rtl(p)


# ────────────────────────────────────────────────────────────
# 1. slide-diet
# ────────────────────────────────────────────────────────────
def build_slide_diet(out):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # slide 1 — genuinely overloaded, 8 long lines. SHOULD be trimmed.
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = "סטטוס פרויקט רבעוני מפורט"
    hebrew(s.placeholders[1].text_frame, [
        "במהלך הרבעון השלישי השלמנו את כל אבני הדרך שהוגדרו בתחילת השנה למעט שתיים שנדחו לרבעון הבא",
        "צוות הפיתוח גדל משישה לתשעה מפתחים ונקלטו שני מהנדסי אמינות שעובדים על תשתית הניטור",
        "מערכת הניטור החדשה עלתה לאוויר בשלושה עשר באוגוסט ומאז זמן התגובה הממוצע ירד בשלושים אחוז",
        "התקבלו שלוש בקשות שינוי מהותיות מהלקוח הגדול שדורשות הערכה מחדש של לוחות הזמנים",
        "עלות התשתית החודשית עמדה על 47,300 שקלים לעומת תקציב מתוכנן של 41,000 שקלים",
        "שיעור התקלות בייצור ירד מארבע עשרה לשבע תקלות בחודש בעקבות שיפור תהליך הבדיקות",
        "נחתם הסכם עם ספק חדש לשירותי ענן שצפוי לחסוך כשנים עשר אחוזים בעלות השנתית",
        "אבי כהן עבד 210 שעות באוגוסט מול תקציב של 180 שעות ונדרשת החלטה על חלוקת עומס",
    ])

    # slide 2 — TRAP: contains a table. Skill must SKIP it.
    s = prs.slides.add_slide(prs.slide_layouts[5])
    s.shapes.title.text = "טבלת חריגות — אסור לגעת"
    rows, cols = 4, 3
    tbl = s.shapes.add_table(rows, cols, Inches(1), Inches(2), Inches(11), Inches(3)).table
    data = [["פרויקט", "תקציב", "בפועל"],
            ["דוחות רגולציה", "120", "152"],
            ["פיילוט DU", "80", "108"],
            ["אינטגרציית SAP", "60", "60"]]
    for r in range(rows):
        for c in range(cols):
            tbl.cell(r, c).text = data[r][c]

    # slide 3 — TRAP: contains a chart. Skill must SKIP it.
    s = prs.slides.add_slide(prs.slide_layouts[5])
    s.shapes.title.text = "גרף עומס — אסור לגעת"
    cd = CategoryChartData()
    cd.categories = ["ינואר", "פברואר", "מרץ"]
    cd.add_series("שעות", (120, 152, 108))
    s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                       Inches(1), Inches(2), Inches(8), Inches(4), cd)

    # slide 4 — TRAP: already compliant, 3 short lines. Must NOT be touched.
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = "שקף תקין"
    hebrew(s.placeholders[1].text_frame, [
        "שלוש שורות בלבד",
        "כל שורה קצרה",
        "אין מה לדלל כאן",
    ])

    # slide 5 — overloaded AND carries facts that must survive verbatim
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = "עובדות שחייבות לשרוד"
    hebrew(s.placeholders[1].text_frame, [
        "סך התקציב לשנה הוא 535 שעות והביצוע בפועל עמד על 567 שעות נכון לסוף אוגוסט 2026",
        "הפרויקטים שחרגו מעל עשרים אחוז הם 101 ו-103 ו-104 ונדרשת עבורם תוכנית קיבולת",
        "שירה ברק אחראית על מעקב ההטמעה ותאריך הבקרה הבא הוא 28.09.2026 בשעה עשר בבוקר",
        "מנהל הפרויקטים ביקש דוח מסכם עד סוף השבוע כולל פירוט לפי עובד ולפי לקוח",
        "העלות הממוצעת לשעת עבודה בפרויקטים האלה היא 285 שקלים לפני מעמ",
        "ההנהלה אישרה תוספת של שני מפתחים החל מהרבעון הרביעי בכפוף לעמידה ביעדים",
        "יש להעביר את המסקנות לוועדת ההיגוי לפני הישיבה הקרובה שנקבעה לתחילת החודש",
    ])

    p = os.path.join(out, "test-slide-diet.pptx")
    prs.save(p)
    return p


# ────────────────────────────────────────────────────────────
# 2. speaker-notes-he
# ────────────────────────────────────────────────────────────
def build_speaker_notes(out):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    content = [
        ("מה קרה ברבעון", ["הכנסות עלו ב-12%", "שלושה לקוחות חדשים"]),
        ("סיכונים", ["תלות בספק יחיד", "עיכוב באינטגרציה"]),
        ("תוכנית קיבולת", ["אבי כהן 210 שעות", "חריגה של 30 שעות"]),
        ("צעדים הבאים", ["לסגור תמחור", "לאשר תוכנית"]),
    ]

    # TRAP: every slide already has notes carrying a unique marker.
    # slide-diet parks removed text here, so overwriting loses facts.
    for i, (title, bullets) in enumerate(content, 1):
        s = prs.slides.add_slide(prs.slide_layouts[1])
        s.shapes.title.text = title
        hebrew(s.placeholders[1].text_frame, bullets)
        s.notes_slide.notes_text_frame.text = (
            f"MARKER-{i:02d} טקסט קיים שהועבר לכאן משקף עמוס. "
            f"עובדה שחייבת לשרוד: ערך ייחודי {i * 1111}."
        )

    p = os.path.join(out, "test-speaker-notes.pptx")
    prs.save(p)
    return p


# ────────────────────────────────────────────────────────────
# 3. variance-analysis  (two files: clean + malformed)
# ────────────────────────────────────────────────────────────
def build_variance(out):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "מעקב"
    ws.sheet_view.rightToLeft = True
    ws.append(["מזהה", "פרויקט", "עובד", "תקציב שעות", "שעות בפועל"])
    rows = [
        (101, "דוחות רגולציה", "אבי כהן", 120, 152),      # +26.7%  over
        (102, "דוחות רגולציה", "דנה לוי", 60, 72),        # +20.0%  boundary
        (103, "פיילוט DU", "אבי כהן", 80, 108),           # +35.0%  over
        (104, "פיילוט DU", "רועי כהן", 30, 38),           # +26.7%  over
        (105, "אינטגרציית SAP", "אבי כהן", 70, 60),       # under
        (106, "אינטגרציית SAP", "גלית שרון", 40, 38),     # under
        (107, "אוטומציה", "יוני אלון", 90, 85),           # under
        (108, "HR", "שירה ברק", 60, 54),                  # under
        (109, "בוט שירות", "עידן מזרחי", 75, 70),         # under
        (110, "עבודה לא מתוקצבת", "דנה לוי", 0, 44),      # TRAP: divide by zero
        (111, "בקשת שינוי", "רועי כהן", None, 17),        # TRAP: blank budget
    ]
    for r in rows:
        ws.append(list(r))
    clean = os.path.join(out, "test-variance.xlsx")
    wb.save(clean)

    # malformed: merged header spanning two rows. Skill must REFUSE.
    wb2 = openpyxl.Workbook()
    w2 = wb2.active
    w2.title = "מעקב"
    w2.sheet_view.rightToLeft = True
    w2["A1"] = "מעקב שעות — רבעון שלישי"
    w2.merge_cells("A1:E1")
    w2.append(["מזהה", "פרויקט", "עובד", "תקציב שעות", "שעות בפועל"])
    for r in rows[:5]:
        w2.append(list(r))
    w2.merge_cells("B4:B5")
    bad = os.path.join(out, "test-variance-malformed.xlsx")
    wb2.save(bad)
    return clean, bad


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    os.makedirs(out, exist_ok=True)
    a = build_slide_diet(out)
    b = build_speaker_notes(out)
    c, d = build_variance(out)
    for p in (a, b, c, d):
        print("built:", p)
    print("\nBaselines: run check_tests.py before running any skill.")


if __name__ == "__main__":
    main()
