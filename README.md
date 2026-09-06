# Copilot toolkit — foundations workshop & AI leaders

Interactive tools and workshop materials from Valor Automation Solutions for
Microsoft 365 Copilot. Two audiences share one site; they are not the same track.

Live site: https://valor-automation-solutions.github.io/copilot-toolkit/

## Two audiences

| Audience | Entry | What it is |
| --- | --- | --- |
| **Participants — foundations (2 hours)** | `foundations/` and the top section of `index.html` | Hands-on workshop: capabilities → limits → shared demo per tool (Excel, Word, PowerPoint, Teams, Email + org search). Simple user language. Pricing / quotas / adoption are out of scope. |
| **AI leaders** | “למובילי AI” on `index.html` | Licensing portal, cost calculator, skill-to-studio, departmental demo kits, declarative agents, Office skills, and the adoption path in the prompt lab. |

The browser deck `tools/lecture-deck.html` is a **separate 60-minute client lecture**
(31 slides). It is **not** the foundations workshop deck.

## Foundations package (`foundations/`)

| Path | What it is |
| --- | --- |
| `Copilot-יסודות-מוכן-להנחיה.pptx` | 27-slide / 120-min facilitator deck — **not on the box yet** (pending machine reconnect). See `foundations/README.md`. |
| `הערות-דובר-מלאות.md` | Full speaker script aligned with Einat late decisions (minutes 61–69) |
| `התחל-כאן.md` | Prep checklist for meeting and workshop |
| `toolkit/` | Student practice files (synthetic demo data) |
| `README.md` | Package map and agenda rules |

## What else is here

| Path | Audience | What it is |
| --- | --- | --- |
| `tools/prompt-lab.html#session` | Foundations | Prompt library + 2-hour session structure |
| `tools/prompt-lab.html#path` | AI leaders | Adoption path (מסלול הטמעה) |
| `tools/training-simulator.html` | Foundations | Practice environment for participants |
| `tools/licensing-app.html` | AI leaders | Licensing portal |
| `tools/cost-calculator.html` | AI leaders | Provider cost comparison |
| `tools/skill-to-studio.html` | AI leaders | SKILL.md → Copilot Studio layers |
| `tools/lecture-deck.html` | Client lecture (separate) | 60-minute interactive lecture deck |
| `demo-kits/` | AI leaders | Finance, procurement, logistics, HR kits |
| `agents/` | AI leaders | M365 declarative agent Teams app ZIPs (one per dept) — **not** Copilot Studio solution exports; see `agents/README.md` |
| `skills/` | AI leaders | Seven PowerPoint / Excel skills + installer; practice guide `copilot-skills-practice.md`, bundle `skills/office-skills.zip`; `.nojekyll` fixes Pages 404s on `SKILL.md` |

Everything runs in the browser with no install. Interactive tool inputs stay in
the browser; some form details may use `localStorage`. The site index uses system
fonts (no Google Fonts). Demo data is synthetic and for training only.
