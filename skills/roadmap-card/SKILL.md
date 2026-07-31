---
name: roadmap-card
description: Update Dashdoc roadmap cards in Notion — link the Harvestr discovery, draft the English Desc, and write the "💡 What is this about?" body (Problem/Opportunity, Success criteria, Scope, out of Scope) from Harvestr feedback. Works on a single card URL, or without a URL surfaces Flow+Community cards needing attention for a cycle. Use whenever Fabien says things like "update the roadmap card for [feature]", "fill in the roadmap card", "link Harvestr discovery on this card", "write the pitch card content", "what cards need work next cycle", "prepare next cycle roadmap", "Desc for [card]", or any equivalent request about the Notion roadmap DB. Always present the draft for confirmation before writing to Notion.
---

# roadmap-card — Update a Roadmap Card

Given a Notion roadmap card URL, enrich it with a linked Harvestr discovery and write the card's content (English description + "What is this about?" body). Propose before writing anything.

Can also be called without a URL to **surface cards needing attention** (missing Desc, missing Harvestr link, or status "Not specified") for Fabien's teams — Fabien then picks which one(s) to work on.

## Context

- **Roadmap DB**: `https://www.notion.so/2336d66c0b4a80a18a83c3a01afaf991`
- **Card naming**: `[Team/Domain] > [Feature]` (e.g., "Flow > Variable slot duration")
- **Fabien's teams**: Flow (Harvestr root: `WhMJqH40a`), Community (Harvestr root: `YZ1rFN6GC`)
- **Harvestr discovery URL format**: `https://app.harvestr.io/components/0/list/[discovery_id]`

---

## Step 0 — Determine mode

**If no argument is given, or argument is "next cycle" / "cycle N":**
→ Enter **Discovery mode** (see Step 0b), then let Fabien pick a card.

**If a Notion URL is given:**
→ Enter **Single card mode**, go directly to Step 1.

---

## Step 0b — Discovery mode: surface cards needing attention

Search the Product Roadmap DB for Fabien's cards (PM Owner = Fabien, teams = Flow or Community) that need work:
- Status is "Not specified" OR "Specified but not started"
- OR `🌾 Harvestr discovery` is empty
- OR `🇺🇸 Desc` is empty

Use `notion-search` + `notion-fetch` to build the list. Group by cycle if "next cycle" / "cycle N" was specified. Filter to that cycle only.

Present a triage table:

```
📋 Cards needing attention (Flow + Community):

| # | Card | Status | Desc? | Harvestr? |
|---|------|--------|-------|-----------|
| 1 | Flow > Variable slot duration | ▶️ Betted | ✅ | ✅ |
| 2 | Community > Sourcing partners | Not specified | ❌ | ❌ |
| 3 | … | … | … | … |

Which card do you want to work on? (reply with number, or a Notion URL)
```

**Wait for Fabien's choice**, then go to Step 1 with that card.

---

## Step 1 — Fetch the card

Fetch the Notion card from the URL provided as argument (or ask for it if missing).

Extract:
- `name` — card title
- `🇺🇸 Desc` — current short English description (may be empty)
- `🌾 Harvestr discovery` — current Harvestr URL (may be empty)
- `🔥 Harvestr Score` — current score (may be empty)
- `Status` — current status
- `Team` — team relation URL
- body content — the "💡 What is this about?" section (may be an empty template)

---

## Step 2 — Find the Harvestr discovery

**If `🌾 Harvestr discovery` is already filled:**
- Extract the discovery ID from the URL (last path segment)
- Fetch the discovery: `list_harvestr_discoveries` with `ids=[discovery_id]`
- Confirm to Fabien: _"Discovery already linked: '[title]' (score: X, feedback: Y). Proceeding with this one — or do you want to search for another?"_
- If confirmed, skip to Step 3.

**If `🌾 Harvestr discovery` is empty:**
- Extract keywords from the card name (strip team prefix, e.g., "Flow > Variable slot duration" → "variable slot duration")
- Search Harvestr: `list_harvestr_discoveries` with `query=[keywords]`, `take=5`, `include=["feedback_count"]`
- Also try broader searches if the first returns few results (synonyms, shorter keywords)
- Present top candidates (up to 5) with: title, feedback count, state, parent component
- Format:
  ```
  🔍 Found Harvestr discoveries for "[card name]":

  1. **[title]** (ID: `abc123`)
     State: [state] | Feedback: [N] | Under: [parent component]
  2. …
  3. …

  Which one should I link? (reply with number, or "none" to skip linking)
  ```
- **Wait for Fabien's choice** before continuing.
- If Fabien picks one → note the discovery ID and URL. If "none" → skip Harvestr linking, proceed with card content only.

---

## Step 3 — Pull Harvestr feedback

With the chosen discovery ID:

**3a — Fetch subdiscoveries (always do this first):**
- `list_harvestr_discoveries` with `parent_ids=[discovery_id]`, `include=["feedback_count"]` to get all direct subdiscoveries
- If subdiscoveries exist, treat them as part of the same discovery scope — collect all their IDs
- Recursively fetch subdiscoveries of subdiscoveries if any are found (repeat until no more children)
- Build a flat list of all IDs: `[root_id, subdisc_id_1, subdisc_id_2, ...]`
- Show Fabien the subdiscovery tree: titles + feedback counts, so he can see the full scope

**3b — Fetch all feedback:**
- `list_harvestr_feedback` with `discovery_ids=[all IDs from 3a]` — get all feedback items across the full tree
- `list_harvestr_messages` for the top feedback items — get the actual message content
- `list_harvestr_customers` or check customer attributes — note company names and context
- Note: feedback count per subdiscovery, unique customer count, any mentions of blocked deals / ARR / urgency
- When drafting, tag each piece of feedback with its subdiscovery theme (e.g., "(labels)", "(doc visibility)") to make scope structure clearer

---

## Step 4 — Draft the card content

Draft the following. Do NOT write to Notion yet.

### 4a — `🇺🇸 Desc` (one to two sentences, English)
Concise, external-facing. States the problem and the value unlock. Example:
> "Enable variable slot durations in Flow based on cargo characteristics (pallet count, weight, load type) using configurable 'atomic slots' that automatically calculate required booking time, solving a critical deployment blocker for 75+ customers."

### 4b — Card body: `# 💡 What is this about?`

Use this exact structure:

```markdown
# 💡 What is this about?

### Problem/Opportunity:
[2-4 paragraphs. Lead with the core pain. Quantify: number of customers, feedback count, blocked ARR if known.
Include specific customer names (max 5-6 representative examples) and their specific pain.
Name the current workaround and why it's insufficient.]

### Success criteria:
[2-4 bullet points. Measurable outcomes: adoption targets, % improvement, deal unlock.
Always include a 💣 Damage control line: what must not regress.]

### What should be included in Scope:
- [bullet list, specific and testable]

### What's already identified as out of Scope:
- ❌ [bullet list — be explicit about what won't be done]
- ❌ → see [Other Card Name](notion-url) ← use this pattern when a topic is out of scope HERE but covered by another existing roadmap card
```

**Tone & style rules:**
- Use customer names from Harvestr feedback directly (they ground the problem)
- Be concrete: "75+ feedback entries", "~€15,780 ARR", "blocking point for signature"
- Success criteria must be measurable, not vague ("at least 5 customers configure this within 2 months")
- Scope is a **draft to be refined by Fabien** — keep it directional, not exhaustive
- Out-of-scope items prevent scope creep — include edge cases raised in feedback but explicitly excluded
- **Cross-card linking**: if a feedback theme is excluded from scope because it belongs to another roadmap card, name and link that card (e.g., "❌ Carrier-based durations → see [Flow > Carrier profiles](url)"). Search the roadmap DB if needed to find the right card.
- Keep it readable by non-PM stakeholders (sales, CS, devs)

---

## Step 5 — Present the draft

Show the full proposal before writing anything:

```
📋 **Proposed updates for: [card name]**

**🌾 Harvestr discovery**: [URL] ("[discovery title]", score: X)

**🇺🇸 Desc**:
> [drafted desc]

**Card body** ("💡 What is this about?"):
[full drafted content]

---
Write these to Notion? (yes / edit first / skip)
```

**Wait for confirmation.**
- `yes` → proceed to Step 6
- `edit first` → apply any corrections Fabien provides, re-show, wait again
- `skip` → stop, nothing written

---

## Step 6 — Write to Notion

Update the Notion card with confirmed content:

1. **Properties to update** (only if changed / newly set):
   - `🌾 Harvestr discovery` → the Harvestr URL
   - `🔥 Harvestr Score` → discovery score from Harvestr (if available and different from current)
   - `🇺🇸 Desc` → the drafted description

2. **Page body** → replace (or fill in) the `# 💡 What is this about?` section with the drafted content. Keep the `# 🚧 Shaping` section intact.

Confirm: _"✅ Card updated: [notion URL]"_

---

## Edge cases

- **No Harvestr discoveries found**: tell Fabien, offer to write the card body based on card name + existing context only, ask for key pain points manually.
- **Card already has body content**: show a diff-like comparison ("current vs proposed") and ask before overwriting.
- **Card is not in the Product Roadmap DB**: warn Fabien and stop.
- **Score in Harvestr**: discoveries don't always expose a numeric score directly — if not available, omit the `🔥 Harvestr Score` update.
