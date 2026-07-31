---
name: release-changelog
description: Create the changelog entry for a released Dashdoc feature — classifies it as Fix/Quickwin/Feature/Launch, qualifies it (Communication Priority, Market, domain/team/roadmap/cycle, builders), then creates ONE row per change in the 🛎️ Changelog Notion database. The native Notion→Slack automation posts it to #changelog automatically. Accepts either a pitch Notion URL or a list of Linear issue IDs. Use whenever Fabien says things like "changelog for [pitch]", "release note for FLO-xxx", "write up what we just shipped", "changelog entry", "draft release note", "what should I post in #changelog", or any equivalent release-communication request. Confirm with Fabien before writing to Notion.
---

# release-changelog — Create the Changelog DB Entry

Given a pitch page or Linear ticket(s): classify the change, qualify it, draft the body, confirm with Fabien, then **create one row in the 🛎️ Changelog database**. Posting to `#changelog` is handled automatically by a native Notion→Slack automation on row creation — there is no manual Slack step.

> This skill implements the [Changelog overload PDR](https://app.notion.com/p/3996d66c0b4a8105ae93e6213d6ed0dc): one qualified row per shipped change is the single source of truth; distribution is driven off `Communication Priority`.

## Usage

```
release-changelog [pitch-notion-url]
release-changelog --linear [issue-id] [[issue-id]...]
```

**Examples:**
```
release-changelog https://www.notion.so/dashdoc/Zone-Management-abc123
release-changelog --linear FLO-203
release-changelog --linear FLO-412 FLO-415 FLO-418
```

---

## Where entries go

- **Database**: `🛎️ Changelog (aka Product release notes)` — `https://app.notion.com/p/17e6d66c0b4a804ca659eb53a60266a0`
- **Data source id (create parent)**: `4fc841cd-c4b5-4677-a76b-8469048890e7`
- **One row per shipped change** (not one page per cycle — the old per-cycle-page model is retired).
- After the row is created, the native automation posts a card to `#changelog` (`CANPU267R`) using the row's **Name + Type + Slack summary + link**. Do **not** post to Slack manually unless Fabien explicitly asks for a cross-post copy.

---

## Step 1 — Gather input

**If `--linear [ids]` was given:** fetch each issue and its comments in parallel:
- `mcp__linear__get_issue` — title, Problem, Solution, assignee, Linear URL, team, labels
- `mcp__linear__list_comments` — scan for video links (Tella, Loom), FAQ/Notion URLs, PR links

**If a Notion pitch URL was given:** `mcp__notion__notion-fetch` the page. Extract the Claim section (user value), linked Linear issues (fetch each + its comments in parallel), the roadmap card, and any feature-flag mention.

From comments across all issues, extract:
- **Video links** (`tella.tv/…`, `loom.com/…`) → embed inline in the body
- **FAQ / Notion page links** → `🔗 Further info`
- **PR links** → `🔗 Further info`

Also determine, asking Fabien if not explicit in context:
- **Is it behind a feature flag? Which one?** (needed for the callout and the activation date)
- **Who was the designer?** (needed for Builders — never leave Builders dev-only on a Feature/Launch)

If the input is too thin to classify or write, ask for more.

---

## Step 2 — Classify Type

| Type | When |
|------|------|
| **Fix** | Bug was broken, now repaired. No new functionality. |
| **Quickwin** | Small improvement or usability enhancement. |
| **Feature** | New capability or significant enhancement. New UI/workflow. |
| **Launch** | Major, transformative change. Old-vs-new comparison. |

Lean on the Linear label (`🐛` = Fix, `🍭` = Feature/Quickwin) and scope when unclear. Exact option values (must match): `Fix` / `Quickwin` / `Feature` / `Launch`.

---

## Step 3 — Qualify the entry (properties)

Resolve every property. **Rule: try to infer from context; if not explicit, ask Fabien to confirm.** Group all open questions into one message.

| Property | Value / how to resolve | Auto / Manual |
|---|---|---|
| **Name** (title) | The feature title (one change = one row) | auto-draft |
| **Type** | Step 2 | auto |
| **Communication Priority** | See heuristic below | **manual — always confirm** |
| **Market** | multi-select; default `All`; infer hints (e.g. SEPA→🇪🇸 Spain, US-only→🇺🇸 USA, shipper feature→🏭 Shippers) | **manual — confirm** |
| **🧩 Domains** | query the Sub-Domains DS `b0357249-a0b8-42e7-a311-5e47658adfaf` by name (from pitch domain / Linear team/label); resolves Product Line TMS/Flow via rollup | auto lookup; ask if ambiguous |
| **🫂 Team** | owning team → Teams DS `2b86d66c-0b4a-80c5-a4c5-000b37c9a1b5` (from the sub-domain's team or the Linear team) | auto lookup; ask if ambiguous |
| **🛡️ Linked to Roadmap** | the pitch / roadmap card from input → Roadmap DS `2336d66c-0b4a-806e-9203-000b7a8c4902` | auto |
| **Released during cycle** | current cycle → Cycles DS `2336d66c-0b4a-8028-b971-000b319ff0d0` (query for the active cycle) | auto; confirm |
| **Linked to Linear** | main issue URL | auto |
| **👷 Builders** | Linear assignees + PR authors + designer, as Notion `person`s | auto; ask for designer if missing |
| **Date of first activation** | production activation date. If FF-gated, this is when the flag was first enabled to real users → **ask Fabien** (ConfigCat audit logs are unreliable for this). If not FF-gated, propose the release/merge date or today. | **manual — confirm** |
| **Slack summary** | one sentence, English, what changed → benefit (see below) | auto-draft; confirm |

**Do not set `Betting`** — deprecated.

**Communication Priority heuristic** (propose, then confirm):
- `🌟 High (now to all Dashdockers)` — Launch, or a major Feature that everyone should know (revenue, big workflow change).
- `🙌 Medium (weekly to all)` — most Features and notable Quickwins.
- `🔍 Low (need to know basis)` — Fixes, small Quickwins, internal/CS-tooling changes.

**Slack summary format** (feeds the `#changelog` automation, which already adds Name + Type + link — so the summary just fills the "what is it" gap):
- One sentence, **English**, plain, no fluff. What the user can now do + the benefit.
- Optional single leading emoji.
- Example: `🗓️ Planners can now drag-and-drop activity notes on the Scheduler, with automatic resource reassignment at the depot.`

---

## Step 4 — Draft the body

Rules for all types:
- **Start with a core-value one-liner** stating the value, and whether this is a **partial** or **complete** release.
- **No `👷 Builders:` line** — Builders is a property now.
- If FF-gated, add a callout at the very top: a blue callout `⚠️ This feature is under FF \`featureFlagName\``.
- Tone: factual, short bullets. Emoji only in section headers.

### Fix / Quickwin — simple shape

```
[FF callout if any]
[Core-value one-liner — value + partial/complete]

### **The Problem:**
- [what was broken / painful]

### ✅ **The solution:**
[video embed if available]
- [what changed]

### 🔗 **Further info**
- [FAQ page]
- [Roadmap card / Linear URL]
```

### Feature / Launch — rich shape

```
[FF callout if any]
[Core-value one-liner — value + partial/complete]

📖 **User Story:** "As a [Role], I want to [Action], so that I can [Benefit]."

[video embed if available]

⚙️ **How it works:**
- [key change 1]
- [key change 2]

📖 **Common use cases:**
- [use case 1]

🎯 **Success Criteria:** (Launch only)
- [measurable outcome]

🔗 **Further info**
- [FAQ page]
- [Roadmap card / Pitch / Linear URL]
```

**Video embed**: render Tella/Loom URLs as a Notion video block on their own line: `<video src="https://..."></video>` (no curly braces, no blank lines around it). `file://` attachment videos and expiring S3 image URLs won't port — note to Fabien to add them manually.

---

## Step 5 — Present for confirmation

Show everything before writing:

```
## Changelog Entry — [Name]

**Properties**
- Type: …
- Communication Priority: …   ← confirm
- Market: …                   ← confirm
- Domains: … · Team: … · Roadmap: … · Cycle: …
- Linked to Linear: …
- Builders: …
- Date of first activation: … ← confirm (FF: `flagName` / not FF-gated)

**Slack summary:** …          ← confirm

---
[Full drafted body]
---

Create this row in the 🛎️ Changelog DB? (yes / edit / skip)
```

**Wait for confirmation.** `edit` → apply, re-show, wait again. `skip` → stop.

---

## Step 6 — Create the row

Use `mcp__notion__notion-create-pages` with `parent = { type: "data_source_id", data_source_id: "4fc841cd-c4b5-4677-a76b-8469048890e7" }`.

Property keys (exact, incl. emoji) and value formats:
- `"Name"`: title text
- `"Type"`: one of `Launch` / `Feature` / `Quickwin` / `Fix`
- `"Communication Priority"`: one of `🔍 Low (need to know basis)` / `🙌 Medium (weekly to all)` / `🌟 High (now to all Dashdockers)`
- `"Market"`: array from `🏭 Shippers` / `🇧🇪 Belgium` / `🇺🇸 USA` / `🇪🇸 Spain` / `🇫🇷 France` / `All`
- `"🧩 Domains"`, `"🫂 Team"`, `"🛡️ Linked to Roadmap"`, `"Released during cycle"`: arrays of related page URLs/IDs
- `"Linked to Linear"`: URL string
- `"👷 Builders"`: array of Notion user IDs
- `"date:Date of first activation:start"`: `YYYY-MM-DD`; plus `"date:Date of first activation:is_datetime"`: `0`
- `"Slack summary"`: the one-sentence summary

The body goes in `content` (Notion-flavored markdown, per Step 4).

---

## Step 7 — Report

```
✅ Created [Name](notion page url) in the 🛎️ Changelog DB.
The #changelog automation will post it (Name + Type + Slack summary + link).
```

Only produce a manual Slack copy if Fabien explicitly asks for a cross-post.

---

## Edge cases

- **Multiple issues, one feature**: one row; Name reflects the feature, not a ticket.
- **FF-gated**: capture the flag name (ask if unknown), add the callout, and treat activation date as the flag's first real enablement — confirm with Fabien.
- **Relation not resolvable** (no matching sub-domain/team/cycle, or ambiguous): ask Fabien rather than guessing.
- **Bug with no pitch**: Linear title + Problem is enough; skip the roadmap link if none.
- **Builder is free text / not a Linear user**: resolve via `/sync-team` or ask; don't leave a plain-text name in the person property.
- **No current cycle found**: ask Fabien which cycle to link.

---

## Context

- **PDR**: [Changelog overload](https://app.notion.com/p/3996d66c0b4a8105ae93e6213d6ed0dc) — read for the rationale and the distribution model (weekly/monthly digests are separate agents, not this skill).
- **All changelog content is in English** (per global rules), including the Slack summary.
- **Fabien's role**: approver. Always confirm the qualified row before creating it.
