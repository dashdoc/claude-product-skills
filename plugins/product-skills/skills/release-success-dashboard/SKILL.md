---
name: release-success-dashboard
description: Build a pitch's success dashboard at release time (Metabase or Mixpanel, any product) — anchor on the roadmap card's success criteria, reuse an existing dashboard rather than creating a new one, find the feature's data + the customer-attribution path, pull a real baseline, then build trend cards for the team to attach. Use whenever Fabien says things like "build the success dashboard for [pitch]", "success dashboard FLO-xxx / COM-xxx", "track adoption for [pitch]", "set up the success metrics", "measure adoption of [feature]", or is working the DoD "Set up success dashboard" task. Always pull a real baseline before proposing metrics, reuse an existing dashboard where one fits, and confirm the card plan before creating anything.
---

# release-success-dashboard — Build a pitch's success dashboard

Turn a pitch's success criteria into a set of cards that track adoption after release. Works for **any product/area** (Flow, Community, Carbon, …) and in **either Metabase or Mixpanel**. Anchor on the roadmap card, reuse an existing dashboard, find the real data + attribution, pull a baseline, then build trend cards and hand a list for the team to attach.

## Usage

```
release-success-dashboard [pitch Notion roadmap card URL]
release-success-dashboard [FLO-xxx | COM-xxx]   # a DoD "Set up success dashboard" task, or any pitch issue
release-success-dashboard "[pitch name]"
```

Works from a roadmap card URL (best), a Linear issue, or a plain pitch name. If given a DoD task, find the parent release issue / project to identify the pitch, then locate its roadmap card.

---

## Known dashboards — reuse, don't multiply

**Fabien does not want to multiply dashboards.** A new pitch's metrics should almost always become a **new tab (or a few cards) on an existing product dashboard**, not a fresh dashboard. Check this list first; add to a matching one. Dashboard data is pushed **weekly/monthly into the Slack channel `#reporting-fabien`**, so keeping metrics on the shared boards (not personal collections) matters.

**Keep this list current** — when a new dashboard is genuinely created, add it here.

**Metabase**
- [3978 — Flow metrics](https://dashdoc.metabaseapp.com/dashboard/3978-flow-metrics?tab=1090-general) — Flow, per-pitch tabs (the default home for Flow pitch metrics)
- [1338 — Community network](https://dashdoc.metabaseapp.com/dashboard/1338-community-network?tab=397-quality) — Community, incl. Quality tab
- [4539 — Community repositories](https://dashdoc.metabaseapp.com/dashboard/4539-community-repositories?tab=1058-support) — Community, incl. Support tab
- [4374 — Community dedicated](https://dashdoc.metabaseapp.com/dashboard/4374-community-dedicated) — Community dedicated
- [2592 — Carbon footprint quality](https://dashdoc.metabaseapp.com/dashboard/2592-carbon-footprint-quality-dashboard) — Carbon footprint quality

**Mixpanel** (project 2584600)
- [Board 5697053](https://eu.mixpanel.com/project/2584600/view/3123880/app/boards#id=5697053) — Flow growth / bookings (referenced by Flow pitch cards)
- [Board 3356873](https://eu.mixpanel.com/project/2584600/view/3123880/app/boards#id=3356873)
- [Board 10195657](https://eu.mixpanel.com/project/2584600/view/3123880/app/boards#id=10195657)
- [Board 10839854](https://eu.mixpanel.com/project/2584600/view/3123880/app/boards#id=10839854)

*(Fill in Mixpanel board names as you identify them.)*

---

## Step 1 — Anchor on the success criteria (never invent metrics)

Fetch the pitch's **roadmap card** (Notion) and read its **Success criteria** section verbatim. Extract:
- The **adoption metric** — usually "N of [thing] with ≥X customers using it within N months of release".
- Any **growth metric** — often already pointed at a Mixpanel board (note the link).
- The **damage-control** line (guardrail metric).
- The **customer list** that motivated the pitch — the adoption target is usually "≥X customers **from that list**".

**Baseline discipline (hard rule):** never propose a metric or target without pulling its real baseline. A number without a baseline is noise.

If the card has no measurable success criteria, stop and flag it.

---

## Step 2 — Pick the tool + the dashboard to extend

**Metabase vs Mixpanel** — build where the metric naturally lives:
- **Metabase** — counts/states straight from production tables (rows created, distinct customers, configuration adopted). SQL/MBQL-modelled. Best when the truth is in the DB.
- **Mixpanel** — product **events** and funnels (feature used, step completion, activation, growth). Best when the metric is behavioural, or when the card explicitly references a Mixpanel board. Requires event instrumentation to exist.
Often it's a split: adoption counts in Metabase, growth/behaviour in Mixpanel — reuse the existing Mixpanel board for the latter rather than rebuilding it.

**Then pick the dashboard to extend** from the *Known dashboards* list above — match by product/area. Only create a new dashboard if none fits (and say so). Confirm the target dashboard/tab with Fabien.

Note: Metabase `search` returns **tables/metrics, not dashboards** — the registry above is your dashboard index, not search.

---

## Step 3 — Identify the source data + inspect its schema

**Metabase:** search for the feature's table, prefer the **BigQuery EU mirror** (database `BigQuery (Linear, Intercom, Notion, Github)`, schema `dashdoc_pg_public` — mirrors EU prod; most customers are EU). US = `Dashdoc US`; live EU pg = `Dashdoc Readonly`. Sample rows to learn columns — event timestamp, soft-delete (`deleted` → filter `IS NULL`), the actor, the FK to the owning object. Distinguish the new table from older look-alikes. Large results are saved to a file; parse with python.

**Mixpanel:** identify the event(s) that represent the adoption action (and confirm they're actually instrumented and firing — no events = no dashboard, flag it). Use the Mixpanel MCP query/board tools when connected.

---

## Step 4 — Attribute the signal to the customer

The adoption metric counts **customers** = the Dashdoc account that owns the feature usage (e.g. the site operator, the network owner), **not** the actor who performed the action (often a partner/carrier/other side).

Work out the join/segmentation from the event's object to the owning **company**, and validate it with a real query — a null/mismatched FK silently yields 0.

**Example (Flow):** `…slot_id → flow_flowslot.id`, then `flow_flowslot.zone_id → flow_flowzone.id → flow_flowzone.site_id → flow_flowsite.id → flow_flowsite.company_id`. Traps: `flow_flowslot.site_id` is always null (go via the zone); `flow_flowslot.company_id` is the **carrier**, not the customer; `flow_flowsite.slug` is a handy human label. See memory `reference_flow_metabase_attribution`. Other products have their own equivalent — find and verify it the same way.

MBQL join shape (Metabase MCP): each join is `{lib/type:"mbql/join", alias, conditions:[["=",{},<lhs>, <rhs with {"join-alias":…}>]], stages:[{source-table:[db,schema,table]}]}`; reference joined columns with `{"join-alias":"…"}`.

---

## Step 5 — Pull the real baseline

Before proposing anything, run the actual aggregates: total events, distinct customers (via the attribution) **vs the target**, distinct actors, first/last timestamps, per-customer breakdown. Exclude internal/test accounts; note pre-GA test data. This baseline is both the join sanity-check and the headline you report.

---

## Step 6 — Propose the card set + placement (confirm before building)

Recommend a **tab/cards on the chosen existing dashboard**. Present the plan and **wait for confirmation** — Fabien refines it. Typical set:
- **Adoption over time** (events per month) — trend.
- **Customers using it per month vs the ≥X target** — trend, via the attribution.
- **[Objects] with the feature per month** — depth trend.
- **By customer** — breakdown showing concentration + whether feedback-list customers adopted.

Map each card to a success criterion; flag anything reaching beyond the pitch so Fabien can scope it out.

---

## Step 7 — Apply Fabien's visualisation preferences

- **Trends over time beat scalars** — show the monthly series, not a single number.
- **Monthly granularity** is usually right.
- **Key the trend axis on a canonical date** (for Flow, the slot creation date, aligning with the existing board). Flag the cohort nuance: recent events on older objects land in the object's creation month.
- **The "within N months of release" window filter** keys off the **event date**, not the cohort/creation date. Add it once the **release date** is known (ConfigCat audit log if available, else the pitch's Linear "Released" date).

---

## Step 8 — Build the cards

**Metabase:** `construct_query` (MBQL) → validate with `execute_query` → `create_question` (display `line`/`row`/`scalar`), filter `deleted IS NULL`, clear name (`[Area] · [Pitch] — [metric]`) + description tying to the criterion, explicit `collection_id`.

**Mixpanel:** build the report/insight against the adoption event(s), segmented by the owning company, as a monthly trend; add to the target board.

---

## Step 9 — Hand off

**Metabase MCP can create questions and new dashboards, but cannot add a tab/card to an existing dashboard, nor read one.** So: create the questions, **give Fabien the list** (names + IDs + links) with instructions to add the tab and drop them in, and tell him to **move them from the personal collection to the shared dashboard collection** (so they surface in `#reporting-fabien`). Note any superseded questions to discard (the MCP can't delete them).

**Mixpanel:** if the MCP can write to the board, do so; otherwise hand the report definitions for Fabien to add.

---

## Step 10 — Report the success read

Close with the baseline headline: **where adoption stands vs the target**, concentration (is one customer most of it?), and **whether the feedback-list customers are adopting**. If below target or the early adopters aren't the requesters, call it out as a damage-control note. Note the date-filter follow-up, then offer to flip the DoD "Set up success dashboard" task to Done once the tab is attached.

---

## Constraints & gotchas

- **Metabase MCP:** `search` = tables/metrics only (no dashboards — use the registry above); no `get-dashboard`, no add-tab/add-card; `create_question` + `create_dashboard` only. Questions land in the personal collection → move to shared.
- **Mixpanel** (and other analytics) may be behind OAuth and absent in headless/cron runs — reference the board rather than assuming write access.
- Large tool results are written to a file — parse with python (`json.JSONDecoder().raw_decode` if there's trailing data).
- Don't rebuild a metric that already exists on a known board — extend it.

## Context

- **Success dashboard is a DoD release item** — anchors on the pitch's success criteria and closes the "Set up success dashboard" task.
- **Fabien is the approver** — confirm the card plan before creating; pull baselines before proposing targets; reuse dashboards, don't multiply them; metrics flow weekly/monthly into `#reporting-fabien`.
- **Reference:** Flow customer-attribution join → memory `reference_flow_metabase_attribution`. First built for **Attach Documents** (Jun 2026) — cards 30173–30175 + 30171 on the Flow metrics dashboard (#3978).
