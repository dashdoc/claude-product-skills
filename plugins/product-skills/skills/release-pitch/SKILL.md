---
name: release-pitch
description: Run the whole release of a Dashdoc pitch or quickwin in one pass — build ONE fact sheet up front (cycle, feature flag + first-activation date, builders, designer, domain/team/priority/market, Linear project, roadmap card, Harvestr discovery), confirm it once, then chain release-faq → release-translations → release-harvestr → release-changelog → release-success-dashboard → roadmap card reconciliation, passing the facts so no sub-skill re-asks. Use whenever Fabien says things like "release [pitch]", "let's do the release of [pitch/FLO-xxx/QWN-xxx]", "run the release checklist", "do the DoD for [pitch]", "release tasks for [pitch]", "ship [pitch]: FAQ, changelog, Harvestr, dashboard", or when he starts chaining two or more release-* skills by hand. Each step still confirms before writing.
---

# release-pitch — One pass through the release of a pitch

The release of a pitch touches six artifacts. Fabien used to chain the `release-*` skills by hand and re-type the same answers (domain, team, priority, builders, activation date, reference example) at each step. This skill gathers those facts **once**, confirms them **once**, then runs each step with the facts already filled in.

Shared rules: [`notion-style.md`](../shared-references/notion-style.md), [`harvestr-structure.md`](../shared-references/harvestr-structure.md), [`product-process.md`](../shared-references/product-process.md).

## Usage

```
release-pitch [roadmap card URL | Linear project name/URL | main issue key]
release-pitch [...] --only faq,changelog      # run a subset of steps
release-pitch [...] --skip dashboard          # skip steps
```

Works for a full pitch (Linear project) or a quickwin (single QWN/FLO issue: steps default to faq + translations + changelog).

---

## Step 1 — Build the fact sheet (read-only, in parallel)

Resolve the pitch from the input, then gather:

| Fact | Where it comes from |
|---|---|
| **Roadmap card** | Product Roadmap DB (`https://www.notion.so/2336d66c0b4a80a18a83c3a01afaf991`); from the Linear project's links or by name search. |
| **Linear project + main issues** | `list_projects` / `list_issues(project=…)`. Keep 🧑‍💻 Dev stories, the 🚀 DoD release parent task, and their QA tables. Delivered set = issues completed since the previous release ticket closed (`completedAt`), not the card's scope list. |
| **Cycle** | Cycles DS `collection://2336d66c-0b4a-8028-b971-000b319ff0d0` for the active cycle, cross-checked with the Dashdoc calendar (`cycle-context.md`). If the work ran out of cycle, say so; don't force a cycle. |
| **Feature flag** | The DoD "Setup Feature Flag" task, the Linear issues and PR descriptions; then `ConfigCat` `get-setting` / `get-setting-values` for its current targeting. |
| **First activation date** | If FF-gated: propose the date the flag was first enabled for real users from ConfigCat audit logs (`list-auditlogs` filtered on the setting), and mark it **to confirm** (logs can be ambiguous: test companies, re-enables). If not gated: merge/deploy date of the last main PR. |
| **Builders** | Linear assignees + GitHub PR authors (`gh pr view <n> --repo dashdoc/dashdoc --json author` on every PR linked to the delivered issues) + the designer. |
| **Designer** | Card property or Figma file owner; else the designer referent of the team (`product-process.md` / TEAMS.yaml). Ask if still unknown. Never leave Builders dev-only on a Feature/Launch. |
| **Domain / Team** | Card's domain → Sub-Domains DS; team from the Linear team. |
| **Type / Communication Priority / Market** | Proposed with the heuristics of `release-changelog` Step 2–3. |
| **Entitlement gating** | Entitlements tracker lookup as in `release-changelog`. |
| **Harvestr discovery** | Card property `🌾 Harvestr discovery` + its sub-discoveries. |
| **Existing artifacts** | Existing changelog row for this card (don't create a duplicate), existing FAQ entries, existing success dashboard (see `release-success-dashboard` "Known dashboards"), demo video link (Tella) in Linear comments. |

## Step 2 — Confirm the fact sheet once

Show ONE compact table: fact, value, source, and a `to confirm` marker on anything inferred (priority, market, activation date, designer, gating). Add the step plan (which of the 6 steps will run, and which are already done and will be skipped).

> Fact sheet OK? Correct any line, then I run the steps.

Wait for the answer. From then on, **never re-ask a fact that is on the sheet**. If a sub-skill would normally ask it, pass the confirmed value.

## Step 3 — Run the steps in order

Each step follows its own skill, with the fact sheet as input. Each still shows its plan and waits for approval before writing (one approval per step, not per field).

| # | Step | Skill | Pass in | Notes |
|---|---|---|---|---|
| 1 | FAQ | `release-faq --linear-project` | project, delivered issues + QA results, feature name, FF | UI labels as shipped. |
| 2 | Translations | `release-translations` | delivered issue keys | Output the key list; Prismy tasks are created by the team, don't create them. |
| 3 | Harvestr | `release-harvestr` | card URL, main issue, sub-discoveries | Audit per sub-discovery. Uncovered feedbacks → decision from Fabien, and the FAQ "known limitation" option feeds back into step 1 if chosen. |
| 4 | Changelog | `release-changelog` | full fact sheet (all properties are already confirmed) | Then enrich the body like the reference pair (below). |
| 5 | Success dashboard | `release-success-dashboard` | card URL, success criteria, activation date | Real baseline only; extend an existing dashboard. |
| 6 | Roadmap card reconciliation | this skill | delivered set, QA deviations, step 3 + 5 results | See below. |

Run read-heavy prep for later steps in parallel while Fabien reviews an earlier step, but write in order.

### Reference pair for steps 4 and 6

The house pattern is the "Mobile app permissions for drivers" changelog entry ([page](https://app.notion.com/p/3c06d66c0b4a81799349ed7200302faa)) and its roadmap card "Admin > Protect the client base from drivers (mobile)" ([card](https://app.notion.com/p/2806d66c0b4a801eab58dfaea5b5dc84)). Fetch both and copy their shape.

**Changelog body, beyond what `release-changelog` produces:**
- `ℹ️ Good to know (and what it does *not* do yet)` — real limits and spec deviations, from the QA result columns and any follow-up pitch.
- `🗣️ For CS & Marketing` — **Say:** / **Say:** / **Don't promise:** (+ **Careful:** for operational traps).
- `🔗 Further info` — Help Center article, FAQ entries from step 1, main Linear issue, every PR grouped by theme.
- Don't touch the row properties after creation (the Notion→Slack automation would re-fire).

**Roadmap card reconciliation (step 6):**
- Keep Problem/Opportunity and Success criteria; add a `> ⚠️ **Post-release reconciliation (date)**` blockquote: which criteria are met, which aren't, why.
- `# 🧩 Solution` → `# 🧩 Solution (as delivered)`, past tense; `✅ Resolved:` on answered open questions; `⚠️` on spec deviations.
- Name cancelled / merged Linear stories explicitly.
- Close with a `Leftovers (date)` block routing every open issue (follow-up pitch, quickwin, backlog discovery).
- Resolve stale hedges ("time permitting") against what happened.
- Link the changelog row, FAQ entries and success dashboard on the card.
- If no baseline exists for a criterion, write it as an open action; never invent a number.

## Step 4 — Wrap up

One summary table: step, status (done / skipped / waiting on Fabien), link to the artifact. Then the remaining DoD items this skill does not cover (e.g. demo data, sales enablement, Help Center article, FF removal date) with their owner from the DoD task, so Fabien can tick or delegate them.

## Edge cases

- **Quickwin**: default steps faq + translations + changelog; card reconciliation only if a card exists.
- **Partial release** (FF on for a few customers): say "partial" in the changelog one-liner; activation date = first real customer; keep the Harvestr discovery In Progress.
- **A step was already done** (changelog row exists, FAQ already updated): audit it against the fact sheet instead of redoing it, and propose fixes only.
- **Another agent or session is working on the same Harvestr discovery**: don't start a second plan; run step 3 as read-only and report.
