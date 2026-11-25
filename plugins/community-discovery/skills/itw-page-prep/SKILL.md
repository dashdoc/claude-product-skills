---
name: itw-page-prep
description: Prepare the Notion interview page for a booked Community discovery call (carrier/broker script or shipper script, chosen from the interviewee's profile) — contact, who they are, key numbers, Moderation/Planhat links, the interview guideline as ONE table with the questions to ask (core + the right module), the debrief rows, and a Notion AI Meeting Notes block ready to fire. Use when the PM says "prep the interview page", "create the page for the call with X", "itw-page-prep", "set up the Notion page for my 2:15", or right after itw-company-brief. Creates or fills a page after showing the plan. Pairs with itw-company-brief (before) and itw-process (after the call).
---

# itw-page-prep — Interview page ready to fire

Takes `BRIEF_DATA` from `itw-company-brief` (run it first if missing). Output: a Notion page in the **Interview DB** that needs nothing more from the PM than pressing record.

Gate (normal mode): show the plan (properties + page outline) and wait for OK before creating or editing. Dashdoc-facing text in English; the questions stay in the guideline's language (French; Spanish version for ES-based interviewees).

## Express mode (call starts in under ~15 min, or the PM says "quick", "I'm late", "5 min")

No plan gate. Two phases in the same run — don't stop between them:
1. **Skeleton first (do it immediately):** create the page with the full structure (TOC, Context headings, guideline table fetched live, debrief rows from the live Harvestr discoveries, `# Notes` + empty meeting block) and whatever is already known from the calendar event / email (title, date, interviewers, contact name). Unknown fields are marked `TODO`. Give the PM the page URL + the recording reminder **right away** (short message), so the PM can open it and press record.
2. **Then complete it in place** (edit the same page, never create a second one): contact card, company card, key numbers, `Data:` pre-fills, Planhat/Moderation links. Verify at the end (re-fetch: one table, one meeting block).
Final report lists **"Not checked"** (e.g. HubSpot, Harvestr history, Slack, Intercom, Moderation link, Planhat Phase) instead of silently skipping.

---

## Step 1 — Create or reuse the page

- Interview DB data source: `collection://524c887f-b4ac-45f8-a46b-60f94236e9bc` (🎙️ Interview).
- If the PM already made a blank page, **fetch it and fill it**; otherwise create it. Title pattern: `Community: <Name> de <Company>`.
- Properties: `Interviewer` (people — **the real interviewers**, they are not always the PM), `Date` and `Itw date` (the booking date), `Progress` (use an existing value of the DB — check the options; set "Itw processed" only later, in `itw-process`), `🧩 Sous-domaines` (Community discovery sub-domain page). Fill what you can, flag what you can't.
- Before replacing any existing text, check the comments on the page — rewriting can orphan threads. Surface them to the PM.

## Step 2 — Page outline (in this order)

1. `<table-of-contents />`
2. **# Context** — link to the Community discovery section, then **in this order** (layout the PM reworked by hand on a test page, 13 Nov 2026 — reproduce it):
   1. **Outreach** — one plain line: date of first email, when/for which slot they booked, the topic they typed (+ cancellation/reschedule if any).
   2. **Contact card** — a blue callout (👤), not bullets: `Name / Job title (HubSpot)`, email, phone, blank line, `Dashdoc role: …`, `Last login on Dashdoc: …`. Nothing else.
   3. **`## About: <company name as in HubSpot>`** — company name in the heading.
   4. **Company card** — a blue callout (🔗): `Dashdoc customer since <date> (company id <id>)`; then `Company type: <onboarding deal type, e.g. Broker | Commissionnaire>` and `Phase: <…>` (**Phase is a Planhat field** — not synced to HubSpot (HubSpot only has `health_score__planhat_`, `customer_segmentation__planhat_`, `planhat_url`, ARR), and the Planhat page needs a login, so read it from the Planhat page in the Browser pane only if the PM is signed in there, otherwise leave `Phase: TODO` and flag it; don't invent it); then one line `Moderation` + `Planhat` links.
   5. **Key numbers table** (rows as in the data brief; keep the window in the label when it isn't all-time).
   No "Who they are" bullet list, no HubSpot bullet, no deal list, no other-record note, no provenance or sources line.
3. **# Interview**
   - **Pick the script first (profile router).** From the data brief, label the interviewee 🚛 own fleet / 🔀 broker / 📦 shipper / 🧾 admin. 🚛 and 🔀 use the **carrier script**; 📦 uses the **shipper script** (Step 4 has both URLs). If the profile is unclear, say so and ask the PM once. If the contact is only 🧾 admin or exploitation, flag it at the top of the page ("respondent may not be the chartering/transport-buying person, ask for them or for a routing intro") instead of silently continuing.
   - Rules paragraph and the boxes of the chosen script, copied as on the guideline page: **"Known, don't re-ask"** callout and, for carriers, the **Vocabulary** callout (fill its 5 lines on what Dashdoc does with boards if known, else leave as on the guideline).
   - **ONE table** (Question | Réponse), section titles as grey title rows, questions under them, empty Réponse column.
     - **Carrier script v2 (35 min):** Intro, Who does what, Screen share (last real case), Bad event, Module, Reaction card, Closing. The Module block lists modules A to F (offer mechanics, trust and fraud, getting paid, money and budget, getting orders, quote and price): **keep only the 1 or 2 that fit the profile and the open hypotheses** and say which ones you kept and why in the plan/report; module D (money) only for an owner or DG; E only for a carrier without a sales team; F only for a broker answering quotes. Keep the Reaction card row with the card chosen for this interview (Matchmaker, Trust profile, Golden list / Blacklist or Past shippers), and ask the PM which idea to test if not obvious.
     - **Shipper script v2 (35 min):** Intro, Who does what, Routine flow, Spot (the last time), Carriers and bad events, Tools and money, Closing. No concept card in this round. Keep the whole table (no modules).
   - **Debrief rows in the same table**, under grey title rows. Fetch the live lists, never paste from memory:
     - Carrier: "Debrief: Community discoveries" = one row per **live level-2 discovery of the Harvestr Community component** (19 on 23 Nov 2026), then "Debrief: idea hypotheses" = one row per active idea (MM-, GL-, FS-, TP-, PS-) with its kill criterion, then profile and follow-up lines.
     - Shipper: one row per hypothesis S1 to S7 with its kill criterion (copy the debrief table of the shipper page, in the same single table), then the **landscape grid** (capability, tool today, who chose it, cost, satisfaction, verbatim; six rows) as a section of the same table, then the other debrief lines.
     - Both: direction ＋/－/±/∅ + intensity + verbatim in the answer column; profile; **data vs claim**; surprises or contradictions; open to a mock-up; recommended contacts; parking lot. Carrier adds "reaction to the card: kill criterion met?"; shipper adds "work done outside their tool".
   - No other table for the guideline or debrief (see the one-table rule below). If the shipper landscape grid cannot sit in the same table, keep it as the only exception and say so in the report.
4. **# Notes — meeting block**: the Notion AI Meeting Notes block, empty and ready to fire (see Step 3).
5. No "Raw" toggle in prep — `itw-process` adds it (with the single merged transcript) after the call.

**One-table rule:** the guideline + debrief live in one table. The key-numbers table stays a separate small table; ask the PM once if they want one table for the whole page.

## Content rules from the PM's review of a test page (13 Nov 2026)

**Cut (review comments: "not relevant", "don't care"):**
- Provenance/process notes on the page: "built from the id, not opened", "linked to the Dashdoc id through its … field", the "Sources:" line, "not flagged onboarding? in the scoring sheet". Keep the verification in your own report, not on the page.
- Deal detail beyond the first two items: no extra-licence / extra-entity deals, no amounts after the initial TMS deal.

**Keep (marked "important"):** the **onboarding** deal and its type (e.g. "Broker | Commissionnaire") — the customer's onboarding/segment says what kind of business they are. It is shown as `Company type: Broker | Commissionnaire` (the type taken from the onboarding deal name) in the company card, not as a deal.

**Put the data where the PM will use it:** in the **Réponse column**, next to the matching question, pre-fill the collected number in italics prefixed `Data:` so the PM can compare what is said to what we know at a glance during the call. Typical pre-fills: own vs chartering share, last-time subcontractor search (created in 30 days, fresh subcontractors and their share), last-time freight search (as shipper, fresh one-time shippers), "a partner also uses Dashdoc" (subscribed partners and share). Also pre-fill, so contradictions show up **during** the call (not only after): fleet size (Planhat trucks segment) next to the "profile" question, the chartered share, and distinct subcontractors + one-shot share next to the "how do you find carriers" question. The v2 scripts ask for it: the "Data:" rows are in the guideline itself (carrier: share of subcontracting in Who does what; shipper: orders per year, share subcontracted, number of carriers, orders arriving via the Transporeon connector, share of spot), and the interviewer asks "ça vous surprend ?" instead of asking for the figure. Fill them with the brief's numbers. For shippers, also pre-fill spot share ("sur 100 ordres, combien ?") when we have it. For carriers, if the data shows a subscribed partner, keep the conditional "dernière fois que ce sous-traitant était sur Dashdoc" row, otherwise delete it. Only where we have a real number; leave the rest empty. Keep the window in the row label when it isn't all-time (e.g. "last 6 months").

The separate key-numbers table stays (no objection raised).

## Step 3 — Meeting block

- Use `notion-create-meeting-note`: with `calendarEvent` set to the booked Calendar event (find it with the Notion Calendar tools) it creates/returns the note linked to the event; with `parent` = the interview page it appends the block to the page content. Prefer the calendar-linked variant so the transcript attaches to the event.
- Don't pass `content` unless asked: the block must be empty so the transcription fills it.
- **Verified on a test page (13 Nov 2026):** `notion-create-meeting-note` with `parent` = the interview page (no `content`, a plain title) appended exactly one empty `<meeting-notes>` block at the end of the page. Create the page first (ending on a `# Notes` heading), then call it. Still check by fetching that there is one block and no other recording block (two transcripts on one page is a bad practice we fixed by hand). Calendar-linking was not tested.
- Interviewers: read the calendar event's attendees and their responses — keep the accepted ones plus the PM, flag the pending ones. Resolve Notion people with `notion-get-users`, or copy the `user://` ids from a previous interview page; never guess an id.
- Dates: `date:Itw date:start` as `2026-11-13T16:30:00` + `is_datetime: 1` (Notion stores UTC, displays Paris).
- Consent: the first script row asks for recording consent and must be audible in the transcript; for a group call, add "everyone says their name" (a past group call had no speaker attribution).
- Reminder to put in the final message: record with the **Notion desktop app** (not a Chrome tab), with Screen & System Audio Recording permission, and do a 20-second level check at the start — a browser tab records the microphone only, so the interviewee is missing from the recording.

## Step 4 — Guideline source

- **Fetch the guideline page live** and adapt it; don't paste from memory — it evolves (rules, "Relance"/"Probe" rows, "If time" rows, modules). Two pages:
  - Carrier / broker: `🎙️ Community interview script (30 min), transporteur` (v2 of 23 Nov 2026, 35 min, core + modules + reaction card), `https://app.notion.com/p/4146d66c0b4a819187e2e5b6a4504470`. Spanish version in its toggle, for Spain-based interviewees (use it and keep the same module selection).
  - Shipper: `📦 Community interview script chargeur (35 min)`, `https://app.notion.com/p/4166d66c0b4a81c2b7aaf70fd08f9758`. Its Spanish version is not yet updated to v2 (translation pending): for a Spain-based shipper, say so and use the French questions or ask the PM.
- Don't copy the v1/v2 authoring callout (draft history) onto the interview page: replace the top callout with this interview's date, person, company and topic. Keep the related discovery names in section titles (not H-numbers, not S-numbers unless the page uses them).
- When the script versions on the pages change (title, minutes, sections), follow the pages, not this file.
- Optional pre-fill of the "Réponse" column from the brief ONLY for facts already known (e.g. "customer since …") — marked as pre-filled, otherwise leave empty.

## Step 5 — Optional Linear subtask (off by default)

If the PM wants it: a subtask under the Community discovery parent issue in Linear (`ITW <Name> (<Company>)`) with the Notion page link. Ask once per session; never create without OK.

## Step 6 — Verify and hand over

- Re-fetch the page: one table for the guideline, no leftover template text, meeting block present, links resolve.
- Return: page URL, what was filled, what is missing (Planhat, interview date, interviewers), the recording reminder, the open comments if any.
- If the PM keeps a work log, add one line with the link to the page.
