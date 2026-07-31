---
name: shaping-success
description: Rework or build the success criteria of a Dashdoc pitch during shaping — runs a state-of-the-art rubric, ladders the pitch into team vision + company OKRs, pulls REAL baselines from Metabase (never guesses numbers), then grills Fabien with prioritized questions before drafting a measurable Success criteria + Damage control block. Use whenever Fabien says things like "rework the success criteria", "build success criteria for [pitch]", "what are good success metrics for [card]", "define KPIs for this pitch", "success criteria for [pitch]", "are these metrics good", or any equivalent request tied to the metrics/success section of a shaping. Always pull baselines before proposing targets, and always grill before drafting.
---

# shaping-success — Build a Pitch's Success Criteria

Given a roadmap card (pitch), produce **measurable, strategy-linked success criteria**: run the rubric, ladder the pitch into the company strategy, pull real baselines from Metabase, grill Fabien on the open questions, then draft a `👍 Success criteria` + `💣 Damage control` block ready for the Notion card and the FigJam `FRAME > AMBITION` section.

This skill is the deep-dive companion to **shaping-start** (which drafts Frame/Observe/Claim). Use it when the metrics need real work, not a first pass.

---

## Core principle

> **Never invent numbers. Pull the baseline first, then set the target against reality.**

The single most valuable thing this skill does is ground targets in actual data. A target proposed without its baseline is noise. Always reach Metabase (or ask Fabien for the question IDs) before proposing any number.

---

## Context & resources

- **Roadmap DB**: `https://www.notion.so/2336d66c0b4a80a18a83c3a01afaf991` · data source `collection://2336d66c-0b4a-806e-9203-000b7a8c4902`
- **Company OKRs 2026**: `https://app.notion.com/p/2b26d66c0b4a800b97aad1d14cc8119d` — read the current period block (e.g. "May 1st – August 30th"), it carries the live KRs with `[bracketed]` themes
- **Team pages** (each holds the team vision + KPI dashboard links in 🎯 callouts):
  - Community: `https://app.notion.com/p/2b86d66c0b4a8062be52e2d0f75a5975`
  - The card's `Team` property points to the right team page — always fetch it.
- **Metabase connector**: tools `mcp__d0aae0b9-…__search`, `…__query`, `…__execute_query`
- **Fabien's KPI reporting**: Slack `#reporting-fabien` (`C07NUU1JD4M`) — extra KPI context (may be flaky; don't block on it)
- **Harvestr**: the card's `🌾 Harvestr discovery` — for the user value / persona behind the metric

---

## The rubric — what makes a success criterion good

Score every proposed criterion against this. Fabien's own working definition (linked to team vision/KPI, contributes to a global product KPI, easy to measure + actionable, easy to understand + explain) maps onto it:

| Principle | Test |
|---|---|
| **Outcome, not output** | Measures a behaviour/value change, not "we shipped X" |
| **Metric laddering** | feature metric → **team KPI** → **company OKR/KR**. No orphan metrics |
| **Leading + lagging pair** | one number readable *inside the cycle* (adoption/usage) + one that *proves value* (retention, NRR, churn-saved) |
| **Baseline → target → date** | "from X to Y by [when]". No baseline = not measurable |
| **Few & focused** | 1 primary north-star + 1–2 secondary. More dilutes |
| **Guardrail / counter-metric** | what must *not* degrade (cost, false positives, trust) |
| **Instrumentable pre-build** | measurable with Metabase/Mixpanel today? If not, the instrumentation *is* scope |
| **Easy to explain** | one sentence at the betting table |

---

## Step 1 — Fetch the pitch & its current criteria

Fetch the Notion card. Extract: `Name`, `Team`, `Status`, `🇺🇸 Desc`, `🌾 Harvestr discovery`, `🧩 Domains`, `Customer commitments`, `PM Owner`, and the **page body** — especially the existing `### Success criteria:` and `### 💣 Damage control` bullets. Note any Metabase links already embedded in the body (they're often the exact baseline source).

Read the current criteria critically against the rubric and note the gaps (missing baseline? output not outcome? orphan metric? no guardrail?).

## Step 2 — Map the strategy ladder (be honest)

This is where most pitches are sloppy. Determine **what this pitch actually ladders to** — don't force it:

1. Fetch the **team page** (`Team` property) → read the vision + the 3 guiding principles/tracks and their KPI dashboards.
2. Fetch **OKRs 2026** → current-period block → list the live KRs.
3. Decide the real parent. Common honest outcomes:
   - **Team-vision metric** — the pitch advances one of the team's tracks → use that track's KPI as the lagging parent.
   - **Key-account / customer commitment** — driven by a named customer (check `Customer commitments`) → ladders to the *business* KRs (e.g. NRR, key-account ARR), **not** a team-vision metric. Say so plainly.
   - **Standalone product KPI** — no clean team parent → flag it as an orphan Fabien must consciously own, and surface the tension rather than hiding it.
4. State the ladder in one sentence the betting table will accept.

> ⚠️ If the pitch doesn't map to the team's tracks, **name the tension** — don't shoehorn it. A commitment-driven pitch with a clean business ladder is better than a fake vision link.

## Step 3 — Pull the baselines from Metabase (do NOT guess)

**The connector exposes tables & metrics, not dashboard layouts.** You cannot enumerate a dashboard's cards. So:

- If the card body or Fabien gives a **dashboard URL**, ask for the specific **question IDs** (`…/question/XXXXX`) — or read them off the dashboard with Fabien's help.
- Once you have question IDs, run each: `mcp__d0aae0b9-…__query` with `{ source: { type: "card", id: <questionId> }, operations: [], continuation_token: null }`. The response includes `native_form.query` (the SQL — read it to understand exactly what the metric counts) and `rows`.
- For ad-hoc baselines, `…__search` for the table (e.g. `shipments_sharedactivity`, `bi_dim_activities`) then build a query, or use `…__execute_query` with SQL.

For each metric, capture: **current value, recent trend, and the precise definition** (from the SQL — e.g. "only activities with `eta_tracking` and a non-null eta"). Convert to the unit Fabien thinks in (per week vs per month vs % of eligible base) and compute the **denominator** so coverage/share metrics are honest.

> Lesson learned: a "coverage" metric is meaningless without its denominator. Always pull both the numerator (e.g. activities with an ETA) *and* the eligible total, and express the baseline as both an absolute and a %.

If Metabase is unreachable and Fabien can't supply IDs/numbers, proceed with **clearly-marked `[baseline TBD]` placeholders** — never fabricate.

## Step 4 — Grill Fabien (prioritized)

Ask in priority order. **A and B are load-bearing** — get those before the rest. Use `AskUserQuestion` for the crisp forks (north-star choice, target value, guardrail threshold); use prose for open ones. Keep it tight.

**A. The ladder** — Confirm the Step 2 finding. Is success framed as a team-vision metric, a key-account/commitment metric, or a standalone KPI Fabien owns? Be honest about which is real.

**B. The north-star** — What is the *one* number that, if it moves, means the pitch worked? If the pitch serves two audiences (e.g. all-customers vs one key account), allow **two tiers** rather than blending — a primary all-customer metric + a secondary commitment metric.

**C. Baseline reference** — For "sooner / better / more" criteria: *better than what baseline?* Pin the reference point. Flag any metric **not measurable today** → it's pending-instrumentation (see Step 5).

**D. Thresholds** — Separate distinct dimensions that get conflated (e.g. *coverage* ≠ *accuracy* ≠ *lead time*). Pin numeric thresholds for each (e.g. "precise = within ±15 min, great = ±5 min").

**E. Value proof (lagging)** — Beyond usage, what proves *value*? Often retention/commitment-met. Check whether the deeper behaviour (did users *act* on it?) is even measurable — if not, say so.

**F. Guardrails** — What must not degrade? Cost ceilings (e.g. external API costs), and the trust killer: a *wrong* output is worse than no output. Pin a counter-metric threshold.

**G. Scope of measurement** — Narrow (one key account, fast to prove) vs broad (all customers, slower)? Decides absolute vs relative-to-baseline targets.

## Step 5 — Classify the metrics

Sort every proposed criterion into:
- **Committed** — measurable today, has baseline + target. Goes under Success criteria.
- **Pending instrumentation** — the *right* metric but no signal exists yet (e.g. "lead time before detection"). Per Fabien's call, either keep under Success criteria clearly marked *(pending instrumentation)*, or move to Scope/Risks as a tech-explo deliverable. Default: ask which he prefers; keeping them signals intent honestly.
- **Guardrail / damage control** — counter-metrics.

> A metric you can't read yet is a *finding*, not a failure. Naming it honestly at the betting table beats a number you can't track.

## Step 6 — Draft the block

Produce a copy-paste-ready block matching the card's existing structure. Template:

```
### 👍 Success criteria

**🌍 Primary — [dimension] ([audience])** — [the core bet in a phrase]
- [Metric]: from **[baseline + unit]** ([% of base]) → **[target]**
- Source: [Metabase question link]

**🎯 [Accuracy / quality / trust]** — [why it matters; can double as guardrail]
- [Metric]: from **[baseline]** → **[target]** (good), **[stretch]** (great)
- Source: [Metabase question link]

**🚨 Secondary — [commitment / key-account outcome]** — ladders to [KR refs]
- [Metric]: from **[baseline]** → **[target]**
- [Qualitative criterion if relevant: commitment met / customer validation]

**🔭 Pending instrumentation** (intent stated; needs build to measure)
- [Metric] — no committed threshold until measurable
- Prerequisite: [what must be logged/built]

### 💣 Damage control
- **[What must not happen]**: [counter-metric + threshold] — [one-line why it's a trust killer]
- **[Cost] ceiling**: stay under **[€X / unit]** (confirm with [owner])
```

Rules:
- Every quantified criterion shows **baseline → target** and a **source link**.
- Mark every guardrail with its threshold.
- Keep each line one sentence; betting-table-readable.
- Leave genuinely-unknown numbers as `[TBD — confirm with X]`, never invented.

## Step 7 — Apply (ask first)

Ask Fabien how to apply (`AskUserQuestion`):
- **Notion card + FigJam** — replace the card's `### Success criteria:` / `### 💣 Damage control` body block, and reflect the metrics in the FigJam `FRAME > AMBITION` stickies (follow shaping-start Step 5 sticky placement/color rules verbatim — `section.appendChild`, copy peer fills, set x/y after append, run the verification gate).
- **Notion card only** — update the body block, leave FigJam.
- **Just the text** — output the block, Fabien pastes it.

Show the exact text before writing anything to Notion/FigJam.

---

## Edge cases

- **Metabase unreachable / no question IDs**: proceed with `[baseline TBD]` placeholders; never fabricate. Offer to revisit once IDs are available.
- **Pitch doesn't ladder to the team vision**: name the tension explicitly; ladder to business KRs or flag as orphan. Don't force a fake link.
- **Two audiences (e.g. one key account + all customers)**: write two tiers (primary + secondary), not a blended metric.
- **Conflated dimensions** (coverage vs accuracy vs lead-time): split them into separate criteria with their own thresholds.
- **Baseline already breaches the proposed guardrail** (e.g. avg error already > the threshold): reframe the guardrail as a *target to reach*, and say so.
- **Coverage metric without a denominator**: always pull the eligible total and express baseline as absolute + %.
- **Card is already `▶️ Betted` / `🚀 Released`**: confirm before rewriting criteria — they may be locked.
- **No Metabase signal exists for the ideal metric**: classify as pending-instrumentation and surface the instrumentation as scope.
