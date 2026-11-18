---
name: itw-target-list
description: Build or extend the Community interview target list (the "Top relevant customers to talk about Community load board" Google Sheet) — score Dashdoc customers on load-board proxies from Metabase, add companies pushed by CS or colleagues, resolve the champion contact per company (first name, email, role, last login), flag bad contacts, and return the next wave ready to paste. Use when the PM says "find more interview targets", "next wave of companies", "extend the list", "who else should I interview", "itw-target-list", or when the sheet has no uncontacted rows left. Read-only on data; the sheet update is handed over as a paste-ready block.
---

# itw-target-list — Who should we interview next?

Step 1 of the Community interview workflow: list → emails (`itw-outreach-drafts`) → booking watch (`itw-followup-check`) → prep (`itw-company-brief`, `itw-page-prep`) → processing (`itw-process`).

Sheet: the Google Sheet titled "Top relevant customers to talk about Community load board" (tabs `Scoring` = method, `loadboard-scoring` = one row per company). Find it with Drive `search_files` on that title, or ask the PM for the link once. Method notes and queries are saved by this skill under `$ITW_OUTPUT_DIR` (default `./itw-notes/`).

Load the `dashdoc-data` skill BEFORE any query.

---

## Step 1 — What does the list already hold?

Read the sheet (Drive `read_file_content`). Columns: `id, Moderation, Planhat, name, country, customer_since, score, A_charter, B_shipper, C_freight, D_harvestr, A_fresh_subcontractors, A_fresh_share, B_fresh_carriers, C_fresh_oneoff_shippers, C_fresh_share, flag, champion_first_name, champion_last_name, champion_email, champion_phone, champion_poste (personas), champion_role, champion_last_login, First email shoot, Second email shoot`.

Report: rows total, rows with no `First email shoot`, rows contacted by whom (the PM, colleagues…), booked/done interviews (cross-check Notion Interview DB). **Never re-contact a company already contacted** — check by company id AND by contact email, and look at colleagues' rows ("<name> – 10/11", "contact call").

## Step 2 — Score (only if the uncontacted pool is thin)

The SQL **depends on who the target is**, so it is not stored in this skill: write it each time with the `dashdoc-data` skill. The method is the stable part:

1. **Name the target behaviour** in one line (e.g. "customers who probably use a load board").
2. **Pick 2–4 data proxies** that observe it in Dashdoc usage over a window (default last 182 days), subscribed customers only (`account_type = 'subscribed'`, no demo/dashdoc names), plus Harvestr when customers already said it. Say what each proxy catches and who is eligible (a minimum count).
3. **Score each proxy 0–100** among eligible companies, usually `70% percentile(count) + 30% percentile(share)`, then `score = 0.6 × best + 0.4 × second-best` so the top of the list is companies strong on two proxies.
4. **Validate on a company you know** (one that already told us the behaviour, e.g. in Harvestr) and sanity-check the counts per `dashdoc-data` step 6. Write down any unexplained gap.
5. **Flag** customers created less than a year ago (`onboarding?`): their counts may just be initial setup.
6. Save the results and the exact queries in `$ITW_OUTPUT_DIR` (dated file), not in the skill, and update the `Scoring` tab text of the sheet.

Example used for the first wave (load-board users, 6 Nov 2026, last 182 days; "fresh" = a partner added to the customer's address book at most 72 hours before the first transport with it): A charter to fresh subcontractors (≥5), B shipper orders to fresh carriers (≥3), C one-time orders from fresh shippers (≥10, private individuals excluded), D Harvestr load-board feedback (80 if ≥2025, 60 if older). Match Harvestr by company, never by name alone; check D rows by hand.

## Step 3 — Candidates beyond the score

- **Pushed by CS / colleagues** ("pushed by CS", "pushed by <colleague>"): add as manual rows with the pusher in the name, even without a score. Note when the contact is not the Dashdoc admin.
- **Not in the Dashdoc DB** (prospects, partners, contacts of group accounts): no id — flag `no id`, nothing from Metabase.

## Step 4 — Resolve the champion contact (per company, never in bulk)

For each company in the wave only (≤ ~20): the champion is the most recent active **Admin TMS** manager (`accounts_manager` not API user, `auth_user` active, latest `last_login`), with the persona list (`champion_poste`) from their roles. Get names/emails from the **unmasked** source (BigQuery 34 or PROD-EU); STAGING masked scrambles them. Cross-check with HubSpot contacts on the company found through `dashdoc_company_pk`.

Guardrails: org policy forbids broad customer/contact exports — only the wave's companies, no dump of the whole list, no emails across customers into chat beyond the wave. If a wave would exceed ~30 contacts, draft a message for `#hubspot-data-request` and stop.

Flags to raise per row before it goes to outreach:
- generic mailbox (`exploitation@`, `facturation@`, `compta@`, `contact@`, a shared gmail) → ask the PM or find a named contact in HubSpot
- placeholder or odd name (e.g. "Express", all caps, an email local-part as name)
- non-French country (ES, BE, NL) → language
- `onboarding?`
- already a Harvestr user with prior feedback (follow-up, not a cold email — the template says "Nous avons déjà échangé")

## Step 5 — Output

1. Table of the next wave: name, id, country, score, proxies, flags, contact.
2. A paste-ready block (TSV) of the new rows in the sheet's column order, plus the Moderation and Planhat links (Planhat: HubSpot `planhat_url` via `dashdoc_company_pk`).
3. What was skipped and why (already contacted, no contact, generic mailbox).

Do not write to the sheet unless the PM asks; the PM fills `First email shoot` after sending (`itw-outreach-drafts` hands over the exact values).
