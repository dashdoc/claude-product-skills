---
name: shaping-step
description: Continue a Dashdoc FOCUSED shaping session one step at a time — "steal" drafts benchmark directions (what to look for and where) for a topic, "unfold" identifies the 5 key user-journey touchpoints from Harvestr feedback. Meant to follow shaping-start. Use whenever Fabien says things like "steal for [topic]", "benchmark directions for [pitch]", "continue shaping", "unfold the touchpoints", "5 touchpoints for [card]", "user journey moments", or any equivalent request for the STEAL (S) or UNFOLD (U) steps of the FOCUSED method. Requires a Notion card URL for "unfold"; a topic is enough for "steal".
---

# shaping-step — Continue a FOCUSED Shaping Step

Picks up after `shaping-start`. Handles two steps:
- **`steal [topic or card-url]`** — Benchmark directions: what to look for and where (Step 5 — S)
- **`unfold [card-url]`** — 5 key touchpoints in the user journey (Step 4 — U)

---

## Step 0 — Determine mode

Parse the argument:
- Starts with `steal` → **Steal mode** (Step 1)
- Starts with `unfold` → **Unfold mode** (Step 2)
- Unclear or missing → ask: "Which step — `steal` or `unfold`? And what's the card or topic?"

---

## Step 1 — STEAL: Benchmark directions

### 1a — Extract the topic

**If a Notion card URL is given:**
- Fetch the card: extract `name`, `🇺🇸 Desc`, `🧩 Domains`, and the Observe JTBD if available in the body
- Derive the benchmark topic from the card's functional theme (e.g., "customizable user permissions", "document attachment to slots", "variable slot duration")

**If a plain topic is given:**
- Use it directly as the benchmark focus

### 1b — Produce the benchmark guide

Output a structured guide for the **STEAL > Nuggets** section in FigJam:

```
🔍 **Benchmark guide — [topic]**

### Direct competitors to check (TMS / logistics SaaS)
[3–5 tools. For each:
- Name
- What specific pattern to capture (be precise: "how they show permission conflicts", "how they handle slot duration per cargo type", "how they display document status in a list view")
- Where to look in the product (app area / feature name)
- Why relevant: what risk or design question it helps answer]

### Adjacent SaaS to explore (non-competitors)
[3–5 tools from other industries that have solved a similar pattern well. For each:
- Name + industry
- What pattern to extract
- Why it applies here despite the different domain]

### Pattern types to evaluate
[3–5 design pattern archetypes relevant to this topic.
For each, name the pattern + the trade-off it represents.
Examples:
  "Granular checkbox list" (Salesforce/Jira) — max flexibility, high admin overhead
  "Fixed roles with presets" (Notion/Linear) — simple UX, limited for complex orgs
  "Duration picker with cargo rules" (booking tools) — precise but requires upfront config
The goal: give Fabien the vocabulary to label benchmarked patterns when pasting them into FigJam]

### Search terms
[5–8 terms to use in:
- The Dashdoc Visual Benchmark FigJam: https://www.figma.com/board/IFY07lmCkRhgRP8vjAteNV/Visual-Benchmark---Competitors?node-id=3-671
- Mobbin / Screenlane / Google (for UX pattern reference)
Terms should be functional, not branded — e.g., "role-based access control UI", "slot duration configuration", "document upload sidebar", "delegation workflow"]

### Non-SaaS inspirations (optional)
[1–2 references from outside software if relevant — physical world analogy, enterprise operations, etc. Only include if genuinely useful, skip otherwise]
```

Rules:
- Stay anchored to the JTBD from the Observe step — benchmark what solves *that specific use case*, not the feature in general
- Each tool entry must specify **what exact pattern to capture**, not just "look at this app"
- For direct competitors, prioritize those already in the Dashdoc Visual Benchmark FigJam board
- Group patterns by the design question they answer, not by tool name

---

## Step 2 — UNFOLD: 5 key touchpoints

### 2a — Load context

Fetch the Notion card. Then find and pull Harvestr data:
- Reuse the same discovery-finding logic as `shaping-start` Steps 2–3
- Pull feedback messages and compute: total_feedback, dominant_persona, main_use_case, top_themes
- If the card's body already contains a drafted JTBD (from `shaping-start`), use it as the anchoring use case

### 2b — Map the touchpoints

Identify the **5 most critical moments** in the user journey that this feature must address.

Rules for good touchpoints:
- A touchpoint is a **user action or decision point**, not a UI screen or a feature
- It corresponds to a moment where the user's intent is high and the current system fails or creates friction
- Extract them from Harvestr messages: "what were users trying to do when they hit the problem?"
- Order them **chronologically** in the user journey (discovery → setup → daily use → exception → result)
- The 5 chosen should span the full journey — avoid clustering 5 touchpoints in the same workflow phase

Output:

```
🗺️ **Key touchpoints — [card name]**

(Anchored on: [one-sentence JTBD summary from Observe])
(Based on [N] feedbacks, [M] customers)

### Touchpoint 1 — [Short name, e.g., "Setting up initial configuration"]
**Moment**: [Describe the specific moment in the user's workflow. When does this happen? What triggers it?]
**Current experience**: [What does the user encounter today at this moment? What's broken or missing?]
**What matters here**: [Why is this moment critical to the success of the feature? What failure to address it causes downstream?]
**Design question to answer**: [The open question that the design must resolve at this touchpoint]

### Touchpoint 2 — [Short name]
…(repeat for 5 touchpoints)…

---

### Suggested Happy Path prototype order
For the Execute step, prioritize these 3 touchpoints in the prototype:
1. **[Touchpoint X]** — [why: highest risk / most feedback / biggest decision]
2. **[Touchpoint Y]** — [why]
3. **[Touchpoint Z]** — [why]

These 3 cover the core hypothesis to validate before committing to the full scope.
```

Rules:
- "Design question to answer" = the open question that the shaping session must resolve for this touchpoint — not the answer
- If a touchpoint has direct customer quotes in Harvestr, include 1 short quote to anchor it: _"e.g., 'We can't let dispatchers see pricing' — Transports Martin"_
- The "Happy Path prototype order" should be the 3 touchpoints where getting it wrong would most hurt the feature's adoption or safety

---

## Edge cases

- **No card URL for `unfold`, only a topic**: ask for a Notion card URL — this step needs Harvestr feedback to be meaningful.
- **`steal` with a very broad topic** (e.g., "Flow"): ask for a more specific functional topic or a card URL to anchor the benchmark.
- **No Harvestr data for `unfold`**: still produce the 5 touchpoints from the card's `🇺🇸 Desc` and JTBD, but mark them as _"⚠️ Hypothesis — validate with customer interviews"_.
- **Card has no Observe JTBD drafted yet**: suggest running `shaping-start` first, or ask Fabien to describe the main use case before proceeding with `unfold`.
