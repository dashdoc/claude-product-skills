---
name: review-pitch-tasks
description: Walk through a Dashdoc pitch's user stories in Linear one at a time — showing each story's Problem → Solution (not QA) — so Fabien can check relevance and precision and refine them live. Applies full structural edits (rewrite, merge into parent/subtasks, cancel, retitle, relate/block) and keeps cross-references consistent. Use whenever Fabien says things like "let's review each task", "review the tasks in [project]", "walk me through the stories", "go through the pitch tasks one by one", "check each story is precise enough", or any equivalent request to iterate over an existing pitch/project's issues in Linear. Pulls shaping (Figma), Harvestr verbatims, and interview notes when they help or when asked. Not for creating a pitch from scratch — that's create-pitch-tasks.
---

# review-pitch-tasks — Review a pitch's user stories one by one

Iterate over the **user stories** of an existing Linear project (a pitch), one at a time, showing **Problem → Solution only**. Fabien reacts; you apply his edits live — including structural changes — and keep the project internally consistent. End with a structure recap.

This is the counterpart to `create-pitch-tasks` (which scaffolds a pitch). Here the tasks already exist and we refine them.

## Usage

```
review-pitch-tasks [project name or URL]
```

If no project is given, ask which one (or list the current/next-cycle Community + Flow projects to pick from).

## Conventions (Dashdoc)

- **Team IDs** — Flow: `80281c65-a634-4daa-bd9b-bdb3196005e6`, Community: `b5867e31-3cdf-4a62-9d7b-3bb5687637a0`.
- **Category labels** (workspace-level): `🧑‍💻 Dev` `3d01ab5d-c7a4-4218-b5b2-562d313fdc1f` · `💣 Risks` `31867eaa-3d8c-444f-a917-dd05acafd5a2` · `🚀 DoD` `30da14d5-7682-482c-9d32-514bd1fe85eb`.
- **Fabien** (assignee): `b339c0b8-91d7-4ac1-9964-42a293dd0577`.
- All Dashdoc artifacts in **English**. Use the glossary; watch FR→EN traps (donneur d'ordre → shipper, OT → order). `/shaping-terminology` if wording is in doubt.

---

## Step 1 — Resolve the project and pull its user stories

1. Resolve the project: `mcp__linear__list_projects(query=...)` (or the URL's slug). Confirm the match if ambiguous.
2. `mcp__linear__list_issues(project=<id>, includeArchived=false)` — pull all issues, then keep the **review set**:
   - **User stories only**: keep issues labelled `🧑‍💻 Dev` **and their subtasks**.
   - **Exclude** `💣 Risks` and `🚀 DoD` tasks, and any **Canceled** issue.
3. Fetch full descriptions as needed (`mcp__linear__get_issue`) so you can show Problem + Solution.

Order the review by logical grouping (e.g. connection flow → data/permissions → lifecycle → display), not by ID — mirror how the pitch hangs together. Nest subtasks under their parent.

## Step 2 — Present the agenda, then review one at a time

First, a compact grouped list of what you'll review (ID + title), so Fabien sees the shape.

Then go **one story at a time**. For each:

- Show **Problem** and **Solution** only — never the QA tables (he doesn't want them here). Keep it skimmable.
- End with: *"Relevant / precise, or adjust?"*
- **Wait** for his reaction before moving on. Do not batch.

## Step 3 — Apply his edits (full structural, confirm-by-instruction)

When Fabien states a change, **apply it directly** to Linear via `mcp__linear__save_issue` — his instruction is the go-ahead (don't re-ask). If *you* are proposing a change he hasn't requested, show the draft first. Never invent facts, numbers, names, or IDs.

Supported edits:
- **Rewrite** Problem/Solution (and QA rows only if they'd contradict the new solution — keep them consistent, don't expand them here).
- **Retitle** when the title no longer fits.
- **Merge** two stories: create a **parent** umbrella story capturing the shared intent, then set the originals as **subtasks** (`parentId`); or cancel one and fold its scope into the other with a merge note. Renumber/relabel scope lists for cleanliness.
- **Split** a story into a parent + one subtask per case.
- **Cancel**: `save_issue(state="Canceled")` with a one-line reason (and "Merged into NET-xxx" if merged).
- **Relate / block**: `relatedTo`, `blockedBy`, `parentId` (use `removeRelatedTo` to drop a stale link).
- **Keep cross-references consistent**: after a merge/cancel/retitle, fix every sibling task and description that pointed at the changed issue (swap the reference, update relations). This is the part that's easy to forget — always sweep for it.

Preserve the pitch's Shape Up shape: stories describe user value; keep the Problem → Solution structure; note open questions inline as `PLACEHOLDER` rather than guessing.

## Step 4 — Evidence (when it helps or when asked)

Proactively cross-check, and always when Fabien points to a source:
- **Shaping** — the pitch's FigJam board (`get_screenshot` on the given node; crop with `sips` to read dense tables/glossaries). Ground the Solution and terminology in what was shaped.
- **Harvestr** — real verbatims to justify a problem. Resolve the discovery (`list_harvestr_discoveries`, `nested_parent_ids` for sub-discoveries), then `list_harvestr_feedback(discovery_ids=..., include_contents=true)`. **Never fabricate a quote** — if search comes up empty, leave a `PLACEHOLDER` to attach one during shaping.
- **Interviews** — the Notion Interview DB entry linked on the roadmap card; map its action items to tasks when checking coverage.

## Step 5 — Wrap up

Close with a **structure recap**: the final grouped list of active stories (+ subtasks), plus what changed this pass (merged, cancelled, created, retitled) and any open threads flagged inside tasks.

Then **offer, but don't assume**, the usual follow-ons:
- **Coverage check** — map an interview/discovery's items to the project, flag anything uncovered / out of scope.
- **Solution write-up** — synthesise the reviewed stories into a `## Solution` section on the pitch card (Notion).
- **Designer brief** — generate a brief from the reviewed stories + shaping.

## Notes

- Confirm-before-write still applies to anything **outward-facing or in another tool** (Notion, Slack) — but in-review Linear edits Fabien has just instructed are pre-approved.
- If the project has no clear user stories (only risks/DoD), say so and offer to run `create-pitch-tasks` instead.
