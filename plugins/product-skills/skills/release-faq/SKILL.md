---
name: release-faq
description: Update the Dashdoc internal FAQ in Notion from pitch content or Linear tickets — audit existing entries, plan creates/updates/removals, confirm, then implement. Accepts free-form text, --linear with issue IDs, or --linear-project with a project name. Use whenever Fabien says things like "update the FAQ", "FAQ for [pitch]", "check the FAQ against what shipped", "audit the FAQ", "add FAQ entries for FLO-xxx", "document this release in the FAQ", or any equivalent request involving the internal FAQ database. Always confirm the change plan with Fabien before editing Notion.
---

# release-faq — Update the Dashdoc Internal FAQ

Given pitch content or a list of Linear tickets, audit the FAQ in Notion, identify what needs to be created, updated, or removed, propose changes for confirmation, then implement them.

## Usage

```
release-faq "[pitch name or free-form description of changes]"
release-faq --linear [issue-id] [[issue-id]...]
release-faq --linear-project [project-name]
```

**Examples:**
```
release-faq "Zone Management — new feature allowing admins to define delivery zones per site"
release-faq --linear FLO-412 FLO-415 FLO-418
release-faq --linear-project "CRUD of signatories"
```

**Arguments:**
- Free-form text / pitch name → use as input directly
- `--linear [ids]` → fetch those Linear issues to extract feature details
- `--linear-project [name]` → search Linear for issues in that project and fetch them all

---

## FAQ location

- **Parent page**: `https://www.notion.so/dashdoc/46318bb1cffa412f87d76bf667f02fad`
- This page contains all FAQ sub-pages. Each sub-page is a thematic section of the FAQ.
- Structure within each page follows: `# Section` → `## Subsection` → `> ### Question` → answer content

---

## Step 1 — Gather input

**If `--linear [ids]` was given:**
Fetch each issue in parallel with `mcp__54d3c450-50e8-43e9-a5fd-211855d395e3__get_issue`. Extract title, description (Problem + Solution sections), and any relevant detail.

Also read the **QA Tests** section of each issue if present — the Result column is the ground truth for what actually shipped:
- `✅` — confirmed working; safe to document
- `❌` — broken or not implemented (linked bug issue); **do not document this behavior as working** in the FAQ
- `⚠️` note on a ✅ — nuance to capture (e.g., timing, edge case behavior); reflect it accurately in the FAQ entry
- `❓` — unverified; ask Fabien before documenting

The Solution section in Linear describes *intended* behavior. The QA Result column describes *actual* behavior. When they conflict, trust the QA results.

**If `--linear-project [name]` was given:**
Use `mcp__54d3c450-50e8-43e9-a5fd-211855d395e3__list_projects` to find the project, then `mcp__54d3c450-50e8-43e9-a5fd-211855d395e3__list_issues` with that project ID. Fetch each issue in parallel.

**If free-form text was given:**
Use it directly as the feature description.

If the input is ambiguous or too thin to identify FAQ implications, ask Fabien:
> "Can you share more detail about what changed? (e.g., new workflows, renamed concepts, removed features, changed permissions)"

---

## Step 2 — Audit the current FAQ

### 2a — Fetch the FAQ index

Fetch the parent FAQ page to get the list of sub-pages:
`mcp__64ac3cb2-924b-40b4-9f54-5c21553586f6__notion-fetch("https://www.notion.so/dashdoc/46318bb1cffa412f87d76bf667f02fad")`

List all child pages (FAQ sections).

### 2b — Identify relevant sections

From the input (pitch content / issue descriptions), extract:
- Key concepts, feature names, workflows, settings, roles, and permissions mentioned
- Potential user questions this change would trigger

Search for relevant FAQ pages:
- `mcp__64ac3cb2-924b-40b4-9f54-5c21553586f6__notion-search` with key terms from the input
- Also fetch any section pages whose titles clearly relate (e.g., "Permissions", "Zones", "Signatories")

Fetch each relevant page with `mcp__64ac3cb2-924b-40b4-9f54-5c21553586f6__notion-fetch`.

### 2c — Identify changes needed

For each relevant FAQ page and each new concept from the input, determine:

| Type | Criteria |
|------|----------|
| **Update** | Existing entry has outdated info, wrong workflow, or missing detail from the new feature |
| **Create** | No existing entry covers the question a user would naturally ask about this change |
| **Remove** | Existing entry describes a workflow that no longer exists or contradicts the new behavior |

Check for:
- Contradictions between current FAQ content and new input
- Knowledge gaps (questions the new feature raises that aren't answered)
- Outdated workflows or deprecated concepts
- Duplicate coverage across different sections

**When the issue has QA results**, additionally check:
- Does the FAQ describe behavior that QA marked ❌? → flag for removal or correction
- Do ⚠️ notes reveal nuances (timing, clamping, silent ignore) that the FAQ entry glosses over? → flag for update
- Does the Solution section describe a mechanism (e.g., migration tool, explicit error) that QA proved doesn't exist? → remove or correct any existing FAQ entries based on it

---

## Step 3 — Plan changes

Build a comprehensive change plan. For each change:

**For updates:** specify the page URL, section path (`# Section > ## Subsection > > ### Question`), what the current text says, and what it should say instead.

**For creations:** specify which page and subsection to place the entry in (or propose a new subsection), the question as a `> ### ...` heading, and the full answer content.

**For removals:** specify the page URL, section path, and clear justification.

If no FAQ page clearly fits a new entry, propose creating a new page or subsection — name it and explain where in the FAQ hierarchy it belongs.

---

## Step 4 — Present the plan for confirmation

Present the full plan before touching Notion:

```
## FAQ Update Plan — [Pitch / Feature Name]

### Summary
[2–3 sentence overview of what's changing and why]

---

### 📝 Updates ([N])

**1. [Page Title](Notion URL)**
Section: `# Section > ## Subsection > > ### Question title`

> **Current:** [existing answer, trimmed if long]

> **Proposed:** [new answer]

---

### ✅ New entries ([N])

**1. Placement:** [Page Title](URL) → `# Section > ## Subsection`
> ### [Question as it will appear]
[Full answer content]

---

### 🗑️ Removals ([N])

**1. [Page Title](URL)**
Section: `> ### Question title`
**Reason:** [why this entry is now obsolete or contradictory]

---

### Structure verification
All new entries are placed at the `> ### Question` level within a `## Subsection` — no nesting.

---
Proceed with these changes? (yes / edit first / skip)
```

**Wait for explicit confirmation before touching Notion.**
- `yes` → go to Step 5
- `edit first` → apply Fabien's corrections, re-show updated plan, wait again
- `skip` → stop, nothing written

---

## Step 5 — Implement approved changes

Implement in this order: updates first, then creations, then removals.

### Updates
For each update, use `mcp__64ac3cb2-924b-40b4-9f54-5c21553586f6__notion-update-page` to modify the relevant block(s) on the page. Preserve all surrounding content exactly — change only the identified entry.

### Creations
For new entries within an existing page, use `mcp__64ac3cb2-924b-40b4-9f54-5c21553586f6__notion-update-page` to append the new `> ### Question` block and its answer into the correct subsection.

For new pages (if proposed and approved), use `mcp__64ac3cb2-924b-40b4-9f54-5c21553586f6__notion-create-pages` with the FAQ parent page as parent, following the required structure format exactly.

### Removals
Use `mcp__64ac3cb2-924b-40b4-9f54-5c21553586f6__notion-update-page` to remove the identified blocks. If an entire subsection becomes empty after removal, remove the subsection heading too.

### Required FAQ structure format (always follow)

```
# Section Name
## Subsection Name
> ### Question as a question?
Answer text directly below, no extra formatting.
```

Rules:
- `> ### Questions` ONLY exist inside `## Subsections`
- Never nest FAQ entries inside other FAQ entries
- All entries within a subsection are at the same level
- No markdown headers (`####`, `#####`) inside answer content — use bold or bullet lists instead

---

## Step 6 — Deliver the summary

```
## FAQ Update Summary — [Feature Name]

✅ Created entries ([N]):
- [Question title](Direct Notion URL) — [brief description]

📝 Updated entries ([N]):
- [Question title](Direct Notion URL) — [what changed]

🗑️ Removed entries ([N]):
- [Question title] — [reason]

📊 Impact:
Total entries created: X
Total entries updated: X
Total entries removed: X
```

---

## Edge cases

- **No relevant FAQ sections found**: tell Fabien, propose which section to create the new entries in, ask for confirmation.
- **Ambiguous placement** (entry could fit multiple sections): show both options and ask Fabien to choose.
- **Input describes a removal or deprecation**: proactively flag all FAQ entries that reference the removed feature, not just the ones that are obviously wrong.
- **Multiple pitches / many tickets**: group changes by theme rather than by ticket — FAQ structure is topical, not ticket-by-ticket.
- **FAQ entry already up to date**: note it in the summary as "no change needed" and skip.

---

## Context

- **FAQ audience**: both humans (support, CS, customers) and agents answering questions — entries must be precise and self-contained.
- **Tone**: neutral, instructional, factual. No marketing language.
- **Fabien's role**: sole approver — always wait for explicit confirmation before writing.
- **Never deviate from the structure format** — agents parsing the FAQ depend on consistent heading levels.
- **Always capture and share Notion URLs** for every created or updated entry.
