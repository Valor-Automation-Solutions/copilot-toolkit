# תרגול והתקנת סקילים ל-Copilot · ואלור Toolkit

מדריך מעשי להתקנה ושימוש ב־7 הסקילים שבתיקיית [`skills/`](skills/).

> **למה קובץ זה קיים:** קישורי Pages ל־`*/SKILL.md` החזירו 404 כי GitHub Pages מריץ Jekyll כברירת מחדל. בריפו נוסף קובץ ריק [`.nojekyll`](.nojekyll) בשורש — אחרי פרסום מחדש, קבצי Markdown (כולל `SKILL.md`) אמורים להיחשף כקבצים סטטיים.

## הורדה מהירה

- **חבילה אחת:** [`skills/office-skills.zip`](skills/office-skills.zip) — כל תיקיות הסקילים + `install.py` + `validate.py` + כלי RTL + `README.md`
- **תיקיית המקור:** [`skills/`](skills/)
- **תיעוד מפורט:** [`skills/README.md`](skills/README.md)

## שבעת הסקילים

| סקיל | אפליקציה | תפקיד קצר |
| --- | --- | --- |
| `deck-review` | PowerPoint | ביקורת מצגת — מדווח בלי לשנות |
| `decision-slide` | PowerPoint | מוסיף שקף "מה אני מבקש להחליט" |
| `slide-diet` | PowerPoint | מדלל שקפים עמוסי טקסט |
| `speaker-notes-he` | PowerPoint | הערות דובר בעברית |
| `rtl-hebrew-repair` | PowerPoint | יישור RTL ותיקון רווחים בלועים |
| `variance-analysis` | **Excel** | תקציב מול ביצוע וחריגות |
| `exec-email` | **Excel** | טיוטת מייל להנהלה מתוך ממצאים |

## התקנה בפקודה אחת (מומלץ)

1. הורידו ופרקו את [`skills/office-skills.zip`](skills/office-skills.zip), או שיבטו את הריפו.
2. צרו פעם אחת את תיקיית הסקילים מתוך האפליקציה:
   - ב־PowerPoint / Excel: חלונית Copilot → `...` → `Manage skills` → `Custom skills` → `Create OneDrive folder`
3. מתוך תיקיית `skills/` (אחרי הפריקה):

```bash
python install.py                  # תצוגה מקדימה בלבד
python install.py --apply          # התקנה/עדכון
python install.py --apply --prune  # גם מחיקת סקילים ישנים שלא בריפו
```

4. בכל אפליקציה: `Manage skills` → `Custom skills` → **`Refresh`** (אין צורך לסגור את האפליקציה).
5. אימות: הקלידו `@` בחלונית Copilot — הסקיל אמור להופיע.

`install.py` מנתב אוטומטית: `variance-analysis` ו־`exec-email` → Excel; השאר → PowerPoint. ניתן לדרוס עם `<!-- app: excel -->` בתוך `SKILL.md`.

## התקנה ידנית (בלי Python)

1. צרו את תיקיית OneDrive מהאפליקציה (כמו למעלה).
2. העתיקו **את תיקיית הסקיל כולה** (לא רק את הקובץ) לתיקיית האפליקציה הנכונה:

```
OneDrive → Documents / מסמכים → Copilot → Microsoft PowerPoint → skills
OneDrive → Documents / מסמכים → Copilot → Microsoft Excel → skills
```

3. `Refresh` בחלונית Custom skills.

⚠️ סקיל של Excel שיושב בתיקייה של PowerPoint **לא ייטען ובלי הודעת שגיאה**.

## אימות מקומי

```bash
python validate.py
```

למדידת RTL אמיתית על קובץ מצגת (לא רק דיווח עצמי של הסקיל):

```bash
python rtl-fingerprint.py deck.pptx
python rtl_repair.py deck.pptx --in-place
```

## כללי פורמט שמפילים סקילים

1. שם הקובץ חייב להיות **`SKILL.md`** (רישיות חשובה לפרסר).
2. שם התיקייה זהה ל־`name` שב־front matter.
3. Front matter נפתח **וגם** נסגר ב־`---`.
4. UTF-8 בלי BOM, שורות LF (`install.py` ממיר CRLF→LF).

## הערת פרסום Pages

עדכוני GitHub Pages (כולל `.nojekyll` וחבילת ה־zip) **לא חיים** עד שמתבצע publish/deploy ל־`gh-pages` / Actions של האתר. בדיקה מקומית בלבד אומתה בסביבה זו.
