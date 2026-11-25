# Dashdoc product process — working reference

> ⚠️ **VOLATILE — last verified 2026-11-25.** The way the product team works is changing. The dedicated shaping week has been dropped, and some work (e.g. bootstrapping the Community product) runs out of cycle. Treat cadence statements as unconfirmed. When a skill depends on a date or ritual, check the Dashdoc calendar (`cycle-context.md`) and ask Fabien rather than relying on this page. Update the "last verified" date whenever someone confirms or corrects a section.

Canonical docs (more complete, may lag behind reality):
- [How do we do Product at Dashdoc](https://www.notion.so/dashdoc/How-do-we-do-Product-at-Dashdoc-2b68fe5e77164b5da0fc357263116556)
- [Definition of done for pitches](https://www.notion.so/dashdoc/Definition-of-done-for-pitches-1f56d66c0b4a809f8f6af155a3dee12d)
- [How to handle Quickwins](https://app.notion.com/p/dashdoc/How-to-handle-Quickwins-19f6d66c0b4a801d9906ccd6fe311ba3)
- [How to handle translations](https://app.notion.com/p/dashdoc/How-to-handle-translations-1186d66c0b4a801cbdfee192ec7d5bfc)
- [Harvestr guide](https://app.notion.com/p/dashdoc/How-to-collect-organize-and-analyze-user-feedbacks-with-Harvestr-1926d66c0b4a807fa1b5c7f62f57986d)
- [Functional domains](https://app.notion.com/p/dashdoc/Functional-domains-4f461e3682014f8f93e22591561ad58a) (domain → PM routing)

---

## 1. Cadence

Confirmed by Fabien on 2026-11-25 (may evolve):
- **6-week cycle + 2-week cooldown.** Betting table on the first Monday of the cooldown.
- **No dedicated shaping week anymore**, and no protected Thursday shaping slot. Shaping happens alongside the cycle; Thursday now holds the team weeklys.
- Fabien works partly **out of cycle** while bootstrapping the Community product.

Also known:
- Cycle and cooldown dates come from the all-day `Cycle N` / `Cooldown` events on the Dashdoc shared calendar (procedure in [`cycle-context.md`](cycle-context.md)). Linear opens cycles a week early, so don't use Linear dates.
- Designers' cycles have run about 2 weeks ahead of dev (they start when the cooldown starts).
- Work outside the cycle exists (new-product bootstrapping, quickwins).

## 2. Rituals and artifacts

| Ritual | What it produces |
|---|---|
| **Roadmap Review** (per impact team) | Vision, recently delivered pitches and their impact on metrics, short/mid-term priorities. Output: the list of roadmap cards to shape next. CS is synced beforehand on customer commitments. |
| **Shaping** (PM + dev + designer) | FOCUSED method (Frame → Observe → Claim → Unfold → Steal → Execute → … ). Frame is the roadmap card content itself. Output: a structured FigJam board + a short video (Tella) shared before the betting. Checklist: [Pitch shaping/building checklist](https://www.notion.so/dashdoc/Pitch-shaping-building-checklist-1d76d66c0b4a80d283b9dfc2bfa13b43). |
| **Betting table** | Decide per team what goes in the next cycle, based on what was shaped, cost and capacity. Everyone has watched the content beforehand. |
| **After betting** | The pitch is split into Linear tasks (`/create-pitch-tasks`), including the DoD release parent task. Risk analysis can happen before or after betting. |
| **During the cycle** | At least a weekly sync per pitch; progress shared as a **Linear project update**, pushed to the pitch's Slack channel and forwarded to `#pitch-updates`. |
| **Release** | DoD checklist (26 items) as a Linear parent task; FF in ConfigCat (created from the start); translations through Prismy; changelog entry; FAQ; Harvestr alignment; success dashboard. Orchestrated by `/release-pitch`. |

## 3. Vocabulary that changed

- **Roadmap card = pitch page.** There are no separate pitch pages any more. The roadmap card ([Product Roadmap DB](https://www.notion.so/2336d66c0b4a80a18a83c3a01afaf991)) is the single central piece pointing to every other resource (FigJam, Harvestr discovery, Linear project, changelog). A roadmap card "becomes a pitch" once it is bet on and its solution and appetite are decided.
- **Progress lives in Linear**, not Notion: one Linear team per impact team, one Linear project per pitch, tasks planned by Linear cycle.
- Cards to shape/deliver for a cycle are identified by the roadmap card **status** + **expected cycle** properties.

## 4. Customer signal

- Harvestr is the main insight store; structure rules in [`harvestr-structure.md`](harvestr-structure.md).
- Every inbound message lands unassigned in the inbox. Anyone in the product team dispatches it to the PM owning the domain. The PM links it to a discovery and weights it **1 = nice to have, 2 = must have, 3 = blocking**.
- Interviews: Notion Interview database (Notion AI meeting notes for transcripts). In-app surveys: Screeb.
- Continuous discovery (Teresa Torres) is the reference approach.

## 5. Bugs and quickwins

- **Zero-bug policy:** a team's open bug count must not grow week over week. If it ends the week higher, the team brings it back down. Bugs are triaged by Support Level 2, who confirm it is a bug, set the domain (→ responsible team) and move it to Todo. Bug dashboards live in Metabase.
- **Quickwins:** small feature requests with limited design needs, mostly from `#hello-product` (sales/CS short-term asks) or from Harvestr messages a PM judges better handled that way. Created in Linear Triage, prioritised by the PM, picked up by the team's devs when they have time; the dev owns it end to end (QA and communication included). Designers review the "Design needed" column during cooldown. No delivery commitment unless the quickwin is added to a cycle.

## 6. Slack conventions

- No internal email: everything is on Slack.
- `#team-<team>` = the team's internal channel. `#hello-<team>` = how others address that team. `#pitch-<name>` = one channel per pitch.
- `#team-product` hosts the daily standup thread; aliases `@pm` and `@designers`. `#hello-product` receives most product questions.

## 7. Tools

Notion (written structured info, keep pages in the Dashdoc workspace) · Linear (tickets, quickwins, pitches) · Harvestr (insights) · Figma / FigJam (mockups, shaping boards) · Tella (betting / roadmap videos) · ConfigCat (feature flags) · Prismy (translations, uses the glossary) · Metabase (data) · `ship.dashdoc.com` (small internal tools).

**Moderation = the backoffice.** Staff-only admin interface (company/transport/user search, connect to a company, demo accounts, merges). Staff answers about it go in the FAQ Moderation page. Environments: day-to-day on demo; staging for customer-like data (anonymised); be very careful on prod.

## 8. Glossary traps seen in sessions

Always use the official glossary (`/shaping-terminology`). Traps that already caused corrections:

| Wrong / internal | Use |
|---|---|
| geographic zones | **service zones** (as named in the product) |
| donneur d'ordre | **shipper** |
| ordre de transport / OT | **order** |
| "company" when it means an entity of a group | **entity** (group view is not a group) |
| UI separators/labels from the spec | the label **as shipped** (check the locale file) |
