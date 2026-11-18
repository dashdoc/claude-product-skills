---
name: release-harvestr
description: Audit a Harvestr discovery at release time — check coverage of every validated feedback against QA results / FAQ / pitch scope, verify the discovery state and 🍫 title format, and alert on pending AI-suggested feedbacks. Takes a Notion roadmap card URL and optionally a main Linear issue. Use whenever Fabien says things like "audit Harvestr for [pitch]", "check coverage of [discovery]", "is this discovery ready to mark Released", "validate Harvestr feedbacks", "did we cover everything from Harvestr", or any equivalent request tied to validating that a shipped feature addresses the customer signal that motivated it.
---

# release-harvestr — Audit Harvestr Discovery at Release

Audit a Harvestr discovery against the roadmap card and what was shipped: check that every validated feedback is covered, verify discovery state and title format, and alert on pending suggested feedbacks.

## Usage

```
release-harvestr [notion-roadmap-card-url]
release-harvestr [notion-roadmap-card-url] --linear [main-issue-id]
```

**Examples:**
```
release-harvestr https://www.notion.so/dashdoc/Flow-Typed-custom-fields-2b96d66c0b4a80cca2eae6e7d9b04dcd
release-harvestr https://www.notion.so/dashdoc/Flow-Typed-custom-fields-2b96d66c0b4a80cca2eae6e7d9b04dcd --linear FLO-291
```

**Arguments:**
- `[notion-roadmap-card-url]` — URL of the Notion roadmap card (required)
- `--linear [issue-id]` — main Linear issue ID containing QA test results (optional; if omitted the skill attempts auto-detection, then falls back to the pitch Solution section)

---

## Step 1 — Fetch the roadmap card

`mcp__64ac3cb2-924b-40b4-9f54-5c21553586f6__notion-fetch([notion-roadmap-card-url])`

Extract:
- **Feature name**: the `Name` property (e.g., `Flow > Typed custom fields`)
- **Harvestr discovery URL**: the `🌾 Harvestr discovery` property
- **Pitch content**: the `# 💡 What is this about?` section — specifically the **What should be included in Scope** subsection and any explicit **out of scope** bullets
- **Canonical URL** of the roadmap card (for linking in the report)

**If `🌾 Harvestr discovery` is missing or empty**: stop and tell Fabien:
> "No Harvestr discovery linked in this roadmap card. Add the discovery URL to the `🌾 Harvestr discovery` property before running this audit."

**Extract the discovery ID** from the Harvestr URL — it is always the last path segment:
- `https://app.harvestr.io/components/0/list/_rBZEMdhX` → `_rBZEMdhX`
- `https://app.harvestr.io/components/0/[componentId]/[discoveryId]` → last segment

---

## Step 2 — Gather all data in parallel

Run all of the following simultaneously:

### A — Harvestr discovery details
`mcp__harvestr__list_harvestr_discoveries(ids=[discoveryId], include=["feedback_count"])`

Capture: title, state name, state type (`UNSTARTED` / `STARTED` / `FINISHED` / `CLOSED`), feedback count.

### B — Validated feedbacks
`mcp__harvestr__list_harvestr_feedback(discovery_ids=[discoveryId], source="validated", take=50, include=["customer"])`

Capture all validated feedback entries: content, customer name.

### C — Suggested feedbacks
`mcp__harvestr__list_harvestr_feedback(discovery_ids=[discoveryId], source="suggested", take=50, include=["customer"])`

Capture all AI-suggested (unvalidated) entries.

### D — Related Linear issues

**If `--linear [id]` was provided**: fetch directly with `mcp__54d3c450-50e8-43e9-a5fd-211855d395e3__get_issue([id])`.

**Otherwise**: attempt auto-detection with `mcp__54d3c450-50e8-43e9-a5fd-211855d395e3__list_issues(query=[feature name], label="🧑‍💻 Dev")` for the main user story issues, then the same call with `label="🚀 DoD"` for the DoD parent issue (`query` searches issue title + description). Fetch each found issue with `mcp__54d3c450-50e8-43e9-a5fd-211855d395e3__get_issue`.

If no Linear issues are found, proceed without Linear data — coverage will rely on the pitch Solution section and FAQ only. Note this limitation in the report.

### E — FAQ entries (supplementary)
`mcp__64ac3cb2-924b-40b4-9f54-5c21553586f6__notion-search([feature name keywords])` scoped to the FAQ parent page `https://www.notion.so/dashdoc/46318bb1cffa412f87d76bf667f02fad`.

Fetch any relevant FAQ pages found with `mcp__64ac3cb2-924b-40b4-9f54-5c21553586f6__notion-fetch`. These reflect what was officially documented as shipped behavior.

---

## Step 3 — Assess coverage for each validated feedback

For each validated feedback, determine coverage using the following priority order — stop at the first source that gives a clear verdict:

**Priority 1 — Linear QA Test results** (highest confidence, reflects what actually shipped)

Look in the `# QA Tests` table of Linear issues for tests addressing the same use case as the feedback. Read the `Result` column:
- `✅` → **Covered**
- `❌` → **Not covered** (broken or not implemented)
- `⚠️` on a `✅` → **Partially covered** — capture the nuance (e.g., clamping behavior, timing constraint)
- No matching test found → fall through to Priority 2

**Priority 2 — FAQ entries**

Does any FAQ entry directly address the need expressed in this feedback?
- Yes, with accurate content → **Covered** (link the FAQ entry)
- Yes, but with a known limitation noted → **Partially covered**
- Not found → fall through to Priority 3

**Priority 3 — Pitch Solution section** (lowest confidence — intended, not verified)

Does the "What should be included in Scope" section explicitly address this use case?
- Explicitly in scope → **Covered (intended)** — note that QA verification is missing
- Explicitly out of scope (❌ bullet) → **Not covered**
- Not mentioned → **Uncertain ❓**

**Coverage verdicts:**

| Verdict | Meaning |
|---------|---------|
| ✅ Covered | Confirmed by QA results, FAQ, or explicit scope |
| ❌ Not covered | Out of scope, QA-failed (❌), or explicitly excluded |
| ⚠️ Partially covered | Covered with a nuance, limitation, or caveat |
| ❓ Uncertain | Not traceable to any source — needs PM decision |

---

## Step 4 — Check discovery state

Compare `discoverystateType` against the expected release-time state:

| State type | Assessment |
|------------|------------|
| `UNSTARTED` | ❌ Discovery never started — ask PM to update to "In Progress" |
| `STARTED` | ⚠️ Valid minimum — ask PM: *"Has the feature been fully deployed and value confirmed with users? If yes, move the discovery to Released in Harvestr."* |
| `FINISHED` | ✅ Released — ask PM to confirm value was validated (not just shipped) |
| `CLOSED` | ✅ Acceptable |

The minimum acceptable state at release time is `STARTED`. Flag anything below that as a blocker.

---

## Step 5 — Check discovery title

Expected format: **`🍫 [Feature name]`**

Derive the expected title from the roadmap card `Name` property. Strip the team prefix if present (e.g., `Flow > Typed custom fields` → `Typed custom fields`). The discovery title should be `🍫 Typed custom fields`.

Checks:
- **Missing 🍫 prefix** → flag: suggest `🍫 [current title]`
- **Title doesn't match feature name** → flag: suggest `🍫 [expected name from roadmap card]`
- **Both issues** → flag both corrections together
- **Correct** → ✅

---

## Step 6 — Alert on suggested feedbacks

If there are any suggested (AI-tagged, unvalidated) feedbacks:

> ⚠️ **[N] AI-suggested feedbacks are pending categorization** on this discovery. You should review them in Harvestr before marking the discovery as Released — some may represent unaddressed customer needs.

List each with:
- Customer name
- First 120 characters of the feedback content

If none: "No pending suggested feedbacks — all feedback is validated."

---

## Step 7 — Deliver the audit report

```
## Harvestr Audit — [Feature Name]

Discovery: [🍫 Title](harvestr-url) · State: [state name]
Roadmap card: [Feature Name](notion-url)

---

### 📋 Feedback Coverage ([N validated])

| Customer | Feedback (summary) | Verdict | Notes |
|----------|--------------------|---------|-------|
| DAHER | Numeric-only input for pallet count | ✅ Covered | QA scenario A (✅) |
| HiperTrans SA | Character limit for DNI field | ❌ Not covered | Free-text char limits out of scope |
| DHL Meyzieu | Duplicate alert on container numbers | ✅ Covered | Unique value type |
| ...  | ... | ... | ... |

**Coverage: X/N covered · Y not covered · Z partially · W uncertain**

---

### 🔄 Discovery State

[✅/⚠️/❌] State: [state name]
[Message or confirmation question for Fabien]

---

### 🏷️ Title

[✅ Title is correct | ❌ Rename to: `🍫 [suggested title]`]

---

### ⚠️ Suggested feedbacks to categorize ([N])

[List or "None."]

---

### Actions needed

1. [Specific action if any — e.g., "Move discovery to Released", "Rename title", "Categorize N suggested feedbacks"]
...
[or "No action needed — discovery is clean."]
```

After presenting the report, for any **❌ Not covered** or **❓ Uncertain** feedbacks, ask Fabien:
> "How do you want to handle the uncovered feedbacks? Options:
> - Document as a known limitation in the FAQ
> - Hold the release until the gap is addressed
> - Confirm it's intentionally out of scope (no action)"

Wait for Fabien's decision before closing the audit.

---

## Edge cases

- **No validated feedbacks**: flag it — a discovery with zero customer signal is unusual; confirm it's intentional.
- **Multiple discoveries on one roadmap card**: run the audit on each one independently and present separate reports.
- **No Linear issues found and pitch Solution section is thin**: note that coverage assessment is limited; ask Fabien to provide a Linear issue ID or describe what shipped.
- **Feedback content is very short or ambiguous**: mark as ❓ and include the raw text so Fabien can judge.
- **Discovery title has 🍫 but wrong feature name**: flag the mismatch — correct the name while preserving the prefix.
- **State is FINISHED but feedbacks are ❌**: warn that the discovery may have been marked Released prematurely.

---

## Context

- **Harvestr discovery** = the insight/theme aggregating customer feedback for a feature; it tracks from "In Progress" → "Released" as the feature ships and delivers value
- **Validated feedbacks** = manually confirmed as relevant; these are the PM's commitments to customers — every one must be traceable to something that shipped
- **Suggested feedbacks** = AI-tagged; unverified; should be reviewed before marking Released
- **Coverage source priority**: QA results > FAQ > pitch Solution — earlier sources are more reliable because they reflect reality, not intent
- **Value validation**: "Released" state means the feature shipped AND customers confirmed value — don't mark Released based on deployment alone
- **🍫 prefix convention**: all Harvestr discoveries for shipped features use the 🍫 emoji prefix
- **Fabien's role**: sole decision-maker on uncovered feedbacks — always surface gaps and wait for explicit guidance
