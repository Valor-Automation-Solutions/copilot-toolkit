# דוח תבניות Workflows ו-Scheduled Prompts ב-Microsoft Teams

תאריך: 20.9.2026
היקף: 34 התבניות המוצעות בגלריה של Teams 365 (Copilot ואפליקציית Workflows)
עודכן בפורטל הרישוי: קבוצה חדשה במטריצת היכולות של licensing-app.html

## סיכום מנגנונים

בגלריה של Teams יש שלושה מנגנונים שונים מאחורי התבניות:

1. Scheduled Prompts של Microsoft 365 Copilot. פרומפט AI מחזורי שרץ נגד ה-Microsoft Graph בהרשאות המשתמש, והתוצאה מגיעה כהודעה בצ׳אט של Copilot ב-Teams וב-Outlook. מאז אוגוסט 2026 זו תכונת Connected Experiences רגילה (מופעלת כברירת מחדל), עם מגבלה של 10 פרומפטים פעילים למשתמש. הרצה מתבצעת בסביבת Power Platform ייעודית בשם Microsoft 365 שנוצרת אוטומטית בטננט, עם DLP קבועה מראש: רק Copilot actions, Teams ו-Outlook מורשים.
2. תבניות אירוע והודעה של אפליקציית Workflows (Power Automate seeded). זרימות דטרמיניסטיות של מחברי Standard, כלולות בזכויות Power Automate המובנות של כל מנוי M365 ארגוני (Business Standard ומעלה), ללא רישיון Copilot כלל.
3. תבניות AI מבוססות Agent Flows או מחברי Premium. דורשות Power Automate Premium (15 דולר למשתמש לחודש), AI Builder או Copilot Credits במודל החדש של Copilot Studio.

## רישוי בקצרה

| מנגנון | רישיון נדרש | מחיר |
|---|---|---|
| Scheduled Prompts (כל תבניות ה-Copilot) | Microsoft 365 Copilot | 30 דולר למשתמש לחודש |
| תבניות Workflows עם מחברי Standard | כלול במנוי M365 ארגוני | 0 |
| תבניות עם מחברי Premium (PagerDuty, HTTP יוצא) או פעולות AI | Power Automate Premium | 15 דולר למשתמש לחודש |
| Agent Flows שמופעלים על ידי סוכן (When an agent calls the flow) | כלול ב-M365 Copilot | 0 מעל הרישיון |
| Agent Flows עם טריגר עצמאי ב-Copilot Studio | Copilot Credits | 200 דולר ל-25,000 קרדיטים לחודש |

חשוב: אין תזמון פרומפטים ב-Copilot Chat החינמי ולא ב-Copilot Pro הפרטי. המנגנון ארגוני בלבד.

## קטגוריה א: תבניות Copilot מתוזמנות (דורשות M365 Copilot)

הגדרה: אפליקציית Copilot ב-Teams, לשונית Prompts או Workflows, בחירת תבנית, קביעת שעה ותדירות, שמירה. התשובה מגיעה בצ׳אט של Copilot.

| תבנית | מה עושה | מקורות נתונים |
|---|---|---|
| עזור לי להתכונן ליום שלי | תדריך בוקר: פגישות היום, מיילים דחופים, משימות, הודעות שלא נענו | Outlook, Exchange, Teams, To Do |
| תדרוך מותאם אישית על סדרי עדיפויות | רשימת עדיפויות מומלצת מהתקשורת האחרונה, אזכורים ומשימות פתוחות | Exchange, Teams, To Do |
| המשך טיפול בהודעה | תזכורת עקובה להודעת Teams במועד עתידי | Teams, Power Automate |
| סיכום יומי של כותרות חדשות | תמצית חדשות לפי נושאים שהוגדרו | Web grounding, SharePoint News |
| תזמן סיכום של הצ׳אטים או הערוצים | סיכום שיחות שלא נקראו בערוצים נבחרים | Teams |
| סקירה של נקודות מפתח מהפגישות האחרונות | תמצית משימות והחלטות מפגישות שהסתיימו | תמלילי פגישות, Intelligent Recap |
| סיכום תקשורת והדגשת פריטי פעולה | רשימה מרוכזת של דברים הדורשים טיפול, ממיילים, Teams וסיכומי פגישות | Exchange, Teams, Recap |
| עזור לי לסיים את היום ולהתכונן למחר | סיכום הישגים, משימות פתוחות ותצוגה מקדימה של מחר | Outlook, Exchange, Teams, To Do |
| סיכום שבועי של קבצים הקשורים לצוות | סיכום מסמכים חדשים או שהתעדכנו אצל הצוות בשבוע החולף | SharePoint, OneDrive |
| התכונן לפגישות שלי מחר | תדריך לכל פגישה של מחר: מיילים אחרונים, מסמכים, דיוני עבר | Outlook, Exchange, SharePoint, Teams |
| סיכום תקשורת בנושא | מקבץ תכתובות לפי מילת מפתח של פרויקט | Exchange, Teams, SharePoint |
| שלח הנחיה מתוזמנת ל-Copilot | פרומפט חופשי לחלוטין בתזמון קבוע, הבסיס לכל השאר | Microsoft Graph |
| תזמן מענה | שליחת תגובת Teams במועד עתידי | Teams, Power Automate |
| הצע מועד חלופי כאשר פגישת אחד על אחד נדחתה | בדיקת זמינות והצעת חלופות כשנדחה פגישת 1:1 | Outlook Free/Busy |

מגבלות משותפות: 10 פרומפטים פעילים למשתמש בכל התבניות יחד. סיכומי פגישות מותנים בהקלטה ותמלול מורשים. סיכום חדשות דורש אישור חיפוש רשת בטננט.

## קטגוריה ב: תבניות Workflows בזכויות M365 (ללא רישיון Copilot)

הגדרה: אפליקציית Workflows ב-Teams, חיפוש התבנית, אישור חיבורים, בחירת פרמטרים, Create flow.

| תבנית | טריגר | פעולה |
|---|---|---|
| הודע לערוץ כשמשימות Planner הושלמו | Planner: task completed | הודעה לערוץ |
| הודע לערוץ כאשר קובץ או פריטים ב-SharePoint משתנים | SharePoint: file modified | הודעה לערוץ |
| Notify a channel when new SharePoint files are added | SharePoint: file created | כרטיס לערוץ |
| הודע לערוץ כאשר פריט רשימה חדש נוסף ל-SharePoint | SharePoint: item created | הודעה לערוץ |
| Send an email when a list item is added or modified | SharePoint: item created or modified | שליחת מייל |
| העבר את הודעות הדואר האלקטרוני שלך לערוץ | Outlook: new email | פרסום בערוץ לפי מסנן |
| העבר פרסומים חדשים בערוץ ל-Outlook | Teams: channel message | שליחת מייל |
| פרסם הודעת ערוץ כאשר פורסם RSS חדש | RSS: feed item | הודעה לערוץ |
| שלח לערוץ התראות webhook | Teams webhook request | כרטיס אדפטיבי (מחליף את Incoming Webhooks שיצאו משימוש) |
| קבל הודעה כאשר מילה מפתח מוזכרת | Teams: channel message | התראה פרטית בצ׳אט או מייל |
| שלח לעצמך תזכורת | For a selected message | תזכורת עם קישור להודעה |
| הפוך תזכורות ועדכונים שבועיים לאוטומטיים בערוץ | Schedule: recurrence | הודעה חוזרת בערוץ |
| תזמן פגישה עם אנשים בצ׳אט או בערוץ | For a selected message | יצירת אירוע יומן |
| אני מאחר | לחיצה ידנית | הודעה למשתתפי הפגישה הקרובה |
| העברת הודעת Teams לערוץ | For a selected message | פרסום בערוץ יעד עם הערה |
| תזכורת לאשר הגעה לפגישות מתקרבות | Schedule: recurrence | תזכורת RSVP למי שלא אישר |
| Quickly get up to speed on the latest files | לפי דרישה או תזמון | טבלת קבצים שהתעדכנו |
| Review file approval and summarize latest requests | Schedule או Approvals | דוח אישורים ממתינים |
| הצע מועד חלופי כאשר פגישת 1:1 נדחתה | Outlook: declined event | הצעת מועדים חלופיים |

תנאים: אפליקציית Workflows מורשית במדיניות האפליקציות של Teams, DLP של Power Platform מאפשר את המחברים הרלוונטיים, וליוצר הזרימה יש הרשאות מתאימות באתר או ברשימה.

## קטגוריה ג: תבניות הדורשות רישיון נוסף

| תבנית | מה נדרש | סיבה |
|---|---|---|
| סכם את הקבצים האחרונים ובדוק אם חלה התקדמות | Power Automate Premium או AI Builder | פעולות סיכום AI (Create text with GPT) |
| צור ערוץ חדר מלחמה כאשר מופעל מקרה ב-PagerDuty | Power Automate Premium | מחבר PagerDuty הוא Premium |
| סיכום תקשורת והדגשת פריטי פעולה בגרסה מוגברת | לפי הרכיב שנבחר | AI Builder או Copilot Credits |

## המלצות אישיות לגיא

לפי אופי העבודה: יום עמוס בפגישות ולקוחות, תלות גבוהה במעקב אחר אנשים, והטננט של ואלור כסביבת הדגמה ללקוחות.

1. עזור לי להתכונן ליום שלי. התבנית הרלוונטית ביותר. תדריך בוקר אחד במקום פתיחת שלושה יישומים. דורש רישיון M365 Copilot.
2. התכונן לפגישות שלי מחר. תדרוך ערב לקראת יום הפגישות, כולל קשר למיילים ולמסמכים.
3. שלח הנחיה מתוזמנת ל-Copilot. התבנית הגמישה ביותר: כל פרומפט שימושי לך בתזמון קבוע. למשל סיכום שבועי של התקדמות מול יעדים.
4. קבל הודעה כאשר מילה מפתח מוזכרת. בחינם לחלוטין בזכויות M365. שווה הפעלה על הערוצים העמוסים.
5. שלח לערוץ התראות webhook. גם בחינם. מאפשר לחבר את GitHub וכלים חיצוניים לערוץ טכני.
6. לסביבת ההדגמות של ואלור: תבניות ההתראות של SharePoint ו-Planner הן חומר הדגמה מצוין בסדנאות, כי הן עובדות ללא רישיון Copilot ומראות ערך מיידי ללקוח.

איך מתחילים: Teams, אפליקציית Copilot, לשונית Prompts, בחירת התבנית, קביעת שעה קבועה, ושמירה. מאותו רגע התדריך מגיע לבד בצ׳אט של Copilot.

## מקורות רשמיים

- Manage Scheduled Prompts for Microsoft Copilot: https://learn.microsoft.com/en-us/microsoft-365/copilot/scheduled-prompts
- Schedule your most used Copilot prompts: https://support.microsoft.com/en-us/microsoft-365-copilot/schedule-your-most-used-copilot-prompts
- Power Automate licensing types and seeded rights: https://learn.microsoft.com/en-us/power-platform/admin/power-automate-licensing/types
- Get started with the Workflows app in Teams: https://support.microsoft.com/en-us/teams/apps-service/get-started-with-the-workflows-app-in-microsoft-teams
- Work with Workflows in Microsoft Teams: https://support.microsoft.com/en-us/office/work-with-workflows-in-microsoft-teams-9f195d88-5184-482f-8e50-983e20092403
- Microsoft 365 Copilot plans and pricing: https://www.microsoft.com/en-us/microsoft-365-copilot/pricing
- Copilot in Teams meetings: https://support.microsoft.com/en-us/office/get-started-with-copilot-in-microsoft-teams-meetings-3729c0e5-8e36-474d-862d-045a5ec36357
