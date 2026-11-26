---
name: itw-company-brief
description: Before a Community discovery interview, collect everything known about the interviewee and their company — who the contact is, what the company does, since when and how they use Dashdoc (Metabase numbers), prior Harvestr/Notion/Slack/Intercom history — and return a facts-only brief plus the structured data that itw-page-prep puts on the interview page. Use when the PM says "brief for my 2:15", "who is this company", "prep the interview with X", "collect what you know about the company", "company brief", "itw-company-brief", or when a booking for a Disco Community slot appears on the calendar. Read-only, writes nothing to Notion, Harvestr or Linear.
---

# itw-company-brief — Who am I about to talk to?

First of the pre-call steps (then `itw-page-prep`). Read-only. Deliverable: a brief in chat (skimmable, facts only) + a structured block `BRIEF_DATA` handed to `itw-page-prep`.

Language: brief in English, French quotes stay French. Facts only, no questions to ask (those come from the guideline).

---

## Step 1 — Identify the interview and the entity

1. **Booking** — start from Gmail, not Calendar: search `subject:"Disco Community"` (booking mail "Rendez-vous réservé: Disco Community (<Name>)" gives slot, Meet link, attendees = co-interviewers, **the company and topic the interviewee typed**, booking email). Calendar `search_events` (semantic) can return nothing for a company name — use `list_events` with a date range + `fullText` as a second check. Then **check for cancellation/decline** (`Refusé : Disco Community`, `Annulé`) and for a reschedule BEFORE doing any work — if the call is cancelled, stop and tell the PM (a call can be cancelled shortly before the slot, after the skill has started).
2. **Resolve the company by id, never by name.** `accounts_company` also holds address-book/partner rows (a company name can exist as several `invited` rows created by other customers; short names match longer ones). Order of sources for the id:
   - the target-list sheet (see `itw-target-list`) or a local export of it — has company id, score, `champion_*` contact, `onboarding?` flag, Moderation and Planhat links;
   - HubSpot company (domain / email domain);
   - if still ambiguous → ask the PM for the id.
3. If the contact isn't in the sheet (e.g. a group account with several entities), say so and list the candidate entities — don't pick one.

## Step 2 — Collect (in parallel, read-only)

| Source | What to pull | Note |
|---|---|---|
| Sheet / TSV | contact name, job, email, phone, scores, flags, Moderation + **Planhat link** | The Planhat link only exists as a `=HYPERLINK(...)` formula in the **local TSV** — the Drive text export drops link targets |
| HubSpot | company (domain, location, created date), contact job title, deals (name, amount, close date), last activity | Founding date: **verify in HubSpot** or on the company site — the script page has been wrong/unverified before |
| Notion | existing Interview DB entries for this company/contact; `Community discovery` pages | A prior interview changes the plan (follow-up vs first) |
| Harvestr | company + user, existing messages/feedbacks | Empty search proves nothing — try company, domain and contact name |
| Slack / Intercom | mentions, support tickets | Not searched in the first brief (gap) — do it |
| Gmail | outreach thread (date first email sent, reply/booking) | |
| Metabase | usage numbers, via the `dashdoc-data` skill | Load it BEFORE any query. Use native SQL if available |

### Metabase numbers (standard set)
Exclude deleted transports and templates, state the DB (BigQuery mirror 34 or masked 364), add the date.
- First / last transport; transports created; last 30 days
- Chartered out to subcontractors (count, % of created), distinct subcontractors
- Carrier vs shipper counts
- "Fresh" subcontractors (added ≤72h before first transport) count and share; "fresh" one-time shippers
- **Subcontractors already on Dashdoc** (for the Dashdoc↔Dashdoc flow discovery) — missing from the first brief, pull it
- Own fleet signal (transports as carrier): caveat that it may just be the chartering relationship
- Sanity checks per `dashdoc-data` step 6 (zero-result, ratios). Unexplained gaps → say so.

## Step 3 — Output

1. **Brief** (chat):
   - Who you talk to (name, role, booked how/when, topic they wrote)
   - Company table (name, location, activity, founded, size if known)
   - On Dashdoc (since when, deal, onboarding status, key numbers with source)
   - Prior history (Harvestr / Notion / Slack / Intercom / Gmail) — or "nothing found" per source
   - **Claims to check live**: any fact that data already contradicts or qualifies (e.g. a heavy-chartering profile with a high share of fresh subcontractors = one-shot sourcing, not a stable network). Phrase as data, not as a question.
   - Gaps: what you couldn't check and why.
2. **`BRIEF_DATA`** block for `itw-page-prep`: contact (name, job title, email(s), phone, last login, **booking email from the calendar invite, HubSpot contact id and HubSpot company id** — or `NOT IN HUBSPOT` — so the HubSpot note step doesn't redo the lookup; see [hubspot-interview-note](../shared-references/hubspot-interview-note.md)), company id, Moderation URL, Planhat URL (or `MISSING`), who-they-are bullets, key-numbers rows (label, value, source), interviewers, date/time, booking topic, language (FR/ES by country).

## Traps seen in earlier briefs
- **HubSpot entity mismatch:** a company can exist twice in HubSpot (a legacy record with no deals, and the real customer under a trade name and another domain), and the contact's email domain may differ from the customer record's. A domain or name search then lands on the wrong company — always resolve by `dashdoc_company_pk`, then associate deals/contacts from that record. A plain name query on DEAL also returns unrelated old deals. The Harvestr company usually carries the trade name.
- **Windows differ:** the sheet's score and "fresh" counts cover a fixed window (stated in the sheet, usually the last 6 months); Metabase counts are all-time. Say so next to the numbers.
- **Planhat link:** sheet exports and local files don't carry it, but **HubSpot does**. Search COMPANY with `dashdoc_company_pk = <Dashdoc company id>` and read `planhat_url` (also `planhat_id_v2`, `status_in_dashdoc`, city, employees). The id after `profile=Company.` identifies the company; the first path segment is probably a view id — use the PM's link if given, otherwise HubSpot's and say so. This lookup also resolves which HubSpot company is the customer, so start the HubSpot step with it before any name search. If the property is empty: `Planhat link: TODO`. (`accounts_company.hubspot_id` and `crm_data` can be NULL — the Dashdoc DB is not a shortcut.)
- **Standard SQL (BigQuery, `dashdoc_pg_public.shipments_transport`, `deleted IS NULL AND is_template = FALSE`):** filter `created_by_id|shipper_id|carrier_id = <id>`; chartered out = `created_by_id = <id> AND is_created_from_subcontracting`; subcontractors = distinct `carrier_id` of those; join `accounts_company` on `carrier_id` and group by `account_type` (`subscribed` vs `invited`) for "already on Dashdoc".

## Rules
- Facts only; state the source of every number.
- Moderation link: pattern `https://www.dashdoc.eu/moderation/companies/<id>/` — build it from the id and **open it once** to confirm it resolves.
- PII: a single company's contact is fine; never build lists across customers (org policy on exports).
- Don't send anything, don't write anywhere. If the PM keeps an inbox file (`inbox.md`), note actionable items there (e.g. missing Planhat link); otherwise put them in the report.
