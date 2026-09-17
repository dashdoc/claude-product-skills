---
name: shaping-start
description: Bootstrap a Dashdoc shaping session for a next-cycle roadmap card — drafts the three FOCUSED steps (Frame, Observe, Claim) from Harvestr feedback, creates the FigJam shaping frame automatically on the correct cycle page, and updates the Notion roadmap card. Called without a URL, lists all next-cycle Flow+Community cards with their shaping status. Use whenever Fabien says things like "start shaping [card]", "bootstrap a shaping", "kick off shaping for [pitch]", "Frame/Observe/Claim this card", "FigJam for [pitch]", "which cards need shaping next cycle", or any equivalent request tied to the Dashdoc shaping workflow. Always pause for validation if Success metrics aren't already on the card.
---

# shaping-start — Bootstrap a Shaping Session

Given a roadmap card URL, pull Harvestr data, draft the three core FOCUSED steps (**Frame → Observe → Claim**), create the FigJam frame automatically, and update the Notion card. Called without a URL, lists next-cycle Flow+Community cards and their shaping status.

---

## Context

- **Roadmap DB**: `https://www.notion.so/2336d66c0b4a80a18a83c3a01afaf991`
- **Roadmap data source**: `collection://2336d66c-0b4a-806e-9203-000b7a8c4902`
- **Cycles data source**: `collection://2336d66c-0b4a-8028-b971-000b319ff0d0`
- **FigJam board**: `https://www.figma.com/board/ZsyYHB1iSYvWDZerEZfHR4/Betting-Fabien` (file key: `ZsyYHB1iSYvWDZerEZfHR4`)
- **FigJam shaping template node**: `4982:3520` — lives on the C33-C34 page (or whichever past cycle page it's on — always search all pages to find it)
- **FigJam cycle page naming**: each cycle has its own page named `C[N]` (e.g., `C35`) — new shapings go on the current cycle's page
- **Fabien's teams**: Flow (Harvestr component root: `WhMJqH40a`), Community (Harvestr component root: `YZ1rFN6GC`)

---

## Step 0 — Determine mode

**If no argument or argument is "next cycle":** → Enter **List mode** (Step 0b).

**If a Notion card URL is given:** → Enter **Single card mode**, go to Step 1.

---

## Step 0b — List mode: cards needing shaping

**Find the next cycle:**
1. Fetch `collection://2336d66c-0b4a-8028-b971-000b319ff0d0` to get all cycles with their start/end dates
2. Find the cycle with the smallest `date:Start:start` that is still in the future (> today's date from `currentDate`)
3. Note the cycle's name and its Notion page URL

**Find Flow + Community cards for that cycle:**
- Fetch the cycle's Notion page — its `Product Roadmap` property lists all linked card URLs
- Fetch each card (or batch-search) to get: Name, Status, `🌾 Harvestr discovery`, `👷‍♀️ Shaping`
- Filter to cards whose Name starts with "Flow >" or "Community >"

**Present the triage table:**

```
📋 Shaping prep — [Cycle N] ([start date] → [end date]):

| # | Card | Status | Harvestr? | Shaping? |
|---|------|--------|-----------|----------|
| 1 | Flow > Attach documents | Not specified | ❌ | ❌ |
| 2 | Community > Sourcing partners | 📐 Shaping | ✅ | ✅ |
…

Which card do you want to start? (reply with number or paste a Notion URL)
```

**Wait for Fabien's choice**, then go to Step 1 with that card.

---

## Step 1 — Fetch the card

Fetch the Notion card from the URL. Extract:
- `name` — full card title (e.g., "Flow > Attach documents")
- `short_name` — strip the team prefix for use in outputs (e.g., "Attach documents")
- `🌾 Harvestr discovery` — existing discovery URL (may be empty)
- `👷‍♀️ Shaping` — existing FigJam shaping URL (may already be set)
- `Status` — current status
- `🇺🇸 Desc` — English description (use as fallback if no Harvestr data)
- `🧩 Domains` — domain relation URLs (fetch their names for the Claim section)
- `Estimated Effort` — Small / Medium / Large / XLarge (informs appetite)
- **Page body** — read the full `# 💡 What is this about?` section and extract the `### Success criteria:` bullet list if present — these are the canonical metrics to use in FRAME

If `👷‍♀️ Shaping` is already set, warn: _"This card already has a shaping URL: [url]. Continue anyway? (yes / no)"_ — wait for confirmation.

---

## Step 2 — Find the Harvestr discovery

**If `🌾 Harvestr discovery` is already filled:**
- Extract the discovery ID from the URL (last path segment)
- Fetch it: `list_harvestr_discoveries` with `ids=[discovery_id]`
- Confirm: _"Discovery already linked: '[title]' (feedback: N). Proceeding — or search for another?"_
- If confirmed, skip to Step 3.

**If empty:**
- Extract keywords from `short_name` (e.g., "Attach documents" → "attach document")
- Search: `list_harvestr_discoveries` with `query=[keywords]`, `take=5`, `include=["feedback_count"]`
- Also try synonyms if first search returns few results
- Present top candidates:
  ```
  🔍 Harvestr discoveries for "[card name]":
  1. **[title]** — Feedback: N | State: [state] | Under: [parent component]
  2. …
  Which one? (number, or "none" to skip)
  ```
- **Wait for Fabien's choice.**

---

## Step 3 — Pull Harvestr feedback

**3a — Fetch subdiscoveries (always do this first):**
- `list_harvestr_discoveries` with `parent_ids=[discovery_id]`, `include=["feedback_count"]`
- Recursively fetch subdiscoveries until no more children
- Build flat list: `[root_id, child_1, child_2, ...]`
- Show the tree to Fabien (titles + feedback counts per node)

**3b — Fetch all feedback:**
- `list_harvestr_feedback` with `discovery_ids=[all IDs]`
- `list_harvestr_messages` for the top feedback items (most recent or highest-weight)
- `list_harvestr_customers` — note company names and context

**3c — Compute stats:**
- `total_feedback` — total count across all nodes
- `blocking_count` — feedbacks mentioning: blocker, blocking, urgent, at risk, churn, deal, signature, can't use, can't migrate, must have
- `customers_at_risk` — unique companies in blocking feedbacks
- `dominant_persona` — most common requester role/type (e.g., "Operations Manager", "IT Admin", "Transport Planner")
- `top_themes` — 3–5 recurring pain clusters (label each, e.g., "can't separate invoicing from dispatch", "no visibility on who can do what")
- `main_use_case` — the single most represented situation from feedback messages

---

## Step 4 — Draft the three FOCUSED sections

Draft all three sections. Proceed directly to Step 5 (FigJam creation) **unless metrics are absent from the card** — in that case pause and show the proposed metrics to Fabien for validation before writing anything to FigJam.

### 4a — FRAME > AMBITION

Three text nodes in the FigJam template serve as section labels only — the actual content goes in **stickies**:

- **"👍 Success criteria:"** text node → leave as label; draft 3–4 metric stickies to create:
  - **First, look for metrics in the roadmap card body** — the `### Success criteria:` section of the card's `# 💡 What is this about?` page body often already lists them. If found, use those directly and adapt them into the sticky format below.
  - **If absent or too vague**, derive from Harvestr data and **present to Fabien for validation** before creating stickies: _"I didn't find explicit metrics in the card. Here's what I'd suggest — confirm or adjust before I write them to FigJam: [list]"_
  - Sticky format:
    - `Core Metric (lagging)\n\n[Big business or community outcome this feature moves] → [where tracked, e.g. Community dashboard]`
    - `Core Metric (leading)\n\n[Adoption signal that predicts the lagging metric will improve] → [Metabase card / Screeb]`
    - `Proxy (leading) Metric\n\n[Specific, feature-level indicator measurable shortly after launch] → [Metabase card]`
    - `Proxy (lagging) Metric\n\n[Operational or CS outcome — e.g. zero escalations, support ticket drop] → [where tracked]`
  - Each sticky ends with `→ [tracking tool]` — use `→ Metabase card`, `→ Screeb todo`, `→ Community dashboard`, or `→ TBD` if unknown

- **"💣 Damage control"** text node → leave as label; create 1–2 stickies:
  - Each sticky = one specific regression risk + a concrete way to monitor it: `[What must not happen]\n\nMonitor [specific signal] → [where tracked]`
  - Draw from at-risk customer warnings and edge cases in feedback

- **"⏲️ Appetite / Timebox:"** text node → fill with a **qualitative strategic framing sentence**, NOT an effort-based list:
  - Describe the nature of the problem and the ambition: why is this the right bet now, what's the strategic context?
  - Example: _"It's a gravel in the shoe for Community but there are workarounds: we want to improve the experience so users feel that working with DD partners is more efficient than working with non DD partners"_
  - Avoid "1 cycle / 2 cycles" estimates — focus on the why and the expected impact direction
  - ⚠️ **Keep it SHORT — max 2 sentences / ~250 characters total including the "⏲️ Appetite / Timebox:" prefix.** The Appetite text node has a fixed width in the template; long paragraphs overflow the FRAME > AMBITION section. If you need more nuance, put it in the response to Fabien, not on the board.

### 4b — OBSERVE > First Use Case

Three counter text nodes (keep the label + colon on same node). ⚠️ **Keep each counter to a single short line** — they sit side-by-side in the template and wrap/overflow into each other when too long. Examples of what NOT to put in the counter: AI-suggested-feedback warnings, long parenthetical notes, multi-company lists. Mention those in the response to Fabien instead.

- `All feedbacks: [N]`  ← just a number
- `Blocking feedbacks: [N] ([company])`  ← 1–2 company names max; drop if >2
- `Customers at risk: [N]`  ← just a number

One JTBD text node (starts with `🙋 I am`):
```
🙋 I am [dominant_persona — specific role + company type]
🕹️ and when I want to [the concrete action they are trying to accomplish]
🤩 what matters the most to me is [the outcome/value they seek]
😫 but it turns out that [the specific system limitation or gap — be precise]
🤸‍♀️ so I'd like to [the capability they want — framed as user capability, not a UI feature].
```

Rules:
- **Single use case only** — the most dominant theme in feedback
- "but it turns out that" = the exact blocking point
- Solution direction = capability framing, not implementation

### 4c — CLAIM

Six sticky notes in the FigJam template:
- **"Customers asking for this: ..."** sticky → segment + count + named accounts
- **"Addressable market"** sticky → scope of who would benefit
- **"Sticky"** (under "Does it need a dedicated name?") → dedicated name (yes/no/tbd) + Pricing signal
- **"Does it need a product marketing effort? 💰 Yes / ❌ No"** sticky → answer + main value claim (3–5 lines: empowerment statement + 3 ✅ bullet points + 💡 tagline)
- **"What domain does it belong to?"** sticky → from 🧩 Domains
- **"Does it need to update the product page on the website? 💰 Yes / ❌ No"** sticky → answer + reason

---

## Step 5 — Create the FigJam frame

### Visual integrity rules (MUST follow)

1. **Every sticky you create belongs to a section — not to the clone frame.** Use `section.appendChild(sticky)`. Stickies parented to the clone drift outside section bounds and look disconnected from their group.
2. **Color-match the section.** Don't accept `createSticky()`'s default yellow. Copy fills from an existing sticky already inside the section (`peer.fills`), or from `section.fills[0]` as a fallback. Cards with off-color stickies look like they don't belong.
3. **A section child's `.x`/`.y` that you SET are RELATIVE to the section's top-left — not page-absolute.** Empirically confirmed: after `section.appendChild(node)`, the resulting `node.absoluteBoundingBox.x === section.absoluteBoundingBox.x + node.x`. So to place a child at a target absolute point, convert: `node.x = targetAbsX − section.absoluteBoundingBox.x` (and same for y). Assigning a page-absolute coord (e.g. a negative board coord) directly to a section child flings it thousands of px off-canvas. Use `absoluteBoundingBox` only to **read/verify** — never to assign. (See `../shared-references/figjam-mechanics.md`.)
4. **Keep text short:** Appetite ≤ 250 chars, metric/DC sticky ≤ 220 chars, counter text node = single short line. Longer text overflows the template's fixed-width layout.
5. **Verify before finishing:** after creating stickies, read back `absoluteBoundingBox` on each and confirm it's inside the owning section's box. If any is outside, reposition with **relative** coords (`child.x = ownerAbs.x − sectionAbs.x + margin`) before returning the URL.

Use `mcp__1ba6bdfa-e088-4566-98a8-89902a5b5b12__use_figma` on the board (file key: `ZsyYHB1iSYvWDZerEZfHR4`) to:

1. **Find the template** — iterate ALL pages with `for (const page of figma.root.children)`, call `await figma.setCurrentPageAsync(page)` on each, then `figma.getNodeById("4982:3520")`. Clone immediately when found. **Do NOT use `.find()` then switch page** — this does not work.

2. **Find the target cycle page** — look for a page named `C[N]` matching the current cycle (e.g., "C35" for Cycle 35). Derive cycle number from the cycle name fetched in Step 0b.

3. **Move the clone** — `await figma.setCurrentPageAsync(targetCyclePage)`, then `targetCyclePage.appendChild(clone)`. Position to the right of existing frames (find max x + width + 200px gap). Set `clone.y = 100`.

4. **Rename** the clone: `clone.name = "[card name]"` (full card name, e.g., "Flow > Attach documents")

5. **Fill FRAME text nodes** — use `collectTextNodes(clone)` recursively. Match by `node.name`:
   - `"💣 Damage control ...."` → update to just `"💣 Damage control"` (label only)
   - `"⏲️ Appetite / Timebox:"` → fill with the qualitative strategic framing sentence (keep the label prefix)
   - `"Text"` under `"FRAME > AMBITION"` → keep as `"👍 Success criteria:"` (label only)
   - `"All feedbacks"` → `"All feedbacks: [N]"`
   - `"Blocking feedbacks"` → `"Blocking feedbacks: [N]  ([company names])"`
   - `"Customers at risk"` → `"Customers at risk: [N]"`
   - node whose `.name` starts with `"🙋 I am"` → full JTBD formula
   - Always `await figma.loadFontAsync(textNode.fontName)` before setting `.characters`

6. **Create FRAME metric + damage-control stickies** — use `figma.createSticky()` and **append them to the `FRAME > AMBITION` section itself** (NOT to the clone). This is critical for two reasons: (a) the sticky is then logically inside the section (survives section moves/resizes), and (b) it inherits the section's visual grouping. Recipe:

   ```js
   const frame = findSectionByName(clone, "FRAME > AMBITION");
   // Read the section's fill to color-match the stickies.
   const frameFill = (frame.fills && frame.fills[0]) ? frame.fills[0] : null;
   // Find an existing sticky that already lives inside this section — use its
   // color as the reference, since sticky fills use a restricted palette and
   // picking one that's already accepted by the section avoids mismatches.
   const peerSticky = collectAll(frame).find(n => n.type === "STICKY");
   function makeSticky(text, x, y) {
     const s = figma.createSticky();
     s.text.characters = text;
     s.authorVisible = false;
     if (peerSticky) s.fills = peerSticky.fills;      // match section's sticky color
     else if (frameFill) s.fills = [frameFill];        // fallback: section fill
     frame.appendChild(s);                             // ← inside the section!
     s.x = x; s.y = y;                                 // set AFTER append
     return s;
   }
   ```

   - Compute positions from `frame.absoluteBoundingBox` (not from `section.x/y` — those can be relative). Place metric stickies in a 2×2 grid under the "👍 Success criteria:" label; place damage-control stickies in a 2×1 column under the "💣 Damage control" label.
   - Use a sticky width of 240 and gap of 20–40. Verify the whole block fits within `frame.width` minus a 60px margin — if not, drop to 1 column / smaller grid.
   - Create 4 metric stickies (Core lagging, Core leading, Proxy leading, Proxy lagging — see Step 4a) and 1–2 damage-control stickies.
   - **Keep sticky text under ~220 characters each** — FigJam stickies grow vertically with content and overlap below when overstuffed.

7. **Fill CLAIM sticky notes** — stickies have a `.text` TextNode child; set `.text.characters`. Match by `sticky.name`:
   - `"Customers asking for this: ..."` → target segment + named accounts
   - `"Addressable market"` → addressable market scope
   - `"Sticky"` (under "Does it need a dedicated name?") → name/brand + pricing
   - `"Does it need a product marketing effort? 💰 Yes / ❌ No"` → answer + full main value claim
   - `"What domain does it belong to?"` → domain
   - `"Does it need to update the product page on the website? 💰 Yes / ❌ No"` → answer + reason

8. **Add verbatim quotes** — create sticky notes **inside the `OBSERVE – FEEDBACKS` section** (same rule as FRAME: `section.appendChild(sticky)`, NOT `clone.appendChild`).

   ```js
   const obs = findSectionByName(clone, "OBSERVE – FEEDBACKS");
   const peer = collectAll(obs).find(n => n.type === "STICKY");
   const obsBB = obs.absoluteBoundingBox;
   // ...createSticky, append to obs, set fills from peer (or obs.fills[0])...
   ```

   - Pick the 5–6 most representative feedbacks: prioritize **must-have / blocker** ones first, then the most specific/illustrative.
   - Label each sticky: `[Company name] / [priority if must-have]` + two blank lines + the verbatim quote (in original language, stripped of JTBD template markers like "Quand (situation)...").
   - Avoid smart quotes or special characters in the string — use plain ASCII apostrophes and dashes to prevent syntax errors.
   - **Color-match** the section: copy fills from an existing sticky inside the section if any (`peer.fills`), else derive from `obs.fills[0]`. Do NOT accept the `createSticky()` default yellow — it will stand out and not look like it belongs to OBSERVE.
   - Use `obs.absoluteBoundingBox` to anchor positions (never the naked `section.x`, which may be relative inside a parent section after a move). Grid: 3 columns × 2 rows of 240-wide stickies with 20–40px gap, anchored at `(obsBB.x + 60, obsBB.y + 80)`. Verify the 3 columns fit within `obsBB.width - 120`; if not, drop to 2 columns.
   - Set `sticky.authorVisible = false`.
   - After creating, re-read `sticky.absoluteBoundingBox` on at least the last one to sanity-check that the stickies are inside `obsBB`; if any are outside, reposition.

9. **Verify visual integrity** — before returning, run a final sanity pass:
   - For each created sticky, confirm `sticky.absoluteBoundingBox` falls inside its owning section's `absoluteBoundingBox`. Reposition any strays.
   - Confirm stickies inside each section visually share the same fill color as their peer stickies in that section.
   - Confirm no text node overflows its section: the `⏲️ Appetite / Timebox:` text's bottom edge (`y + height`) should be inside FRAME > AMBITION; shorten the Appetite sentence and reset characters if not.
   - Report any irregularity in the final summary so Fabien can decide to tweak manually or re-run.

10. **Return** the frame URL: `https://www.figma.com/board/ZsyYHB1iSYvWDZerEZfHR4/Betting-Fabien?node-id=[clone.id with : replaced by -]`

---

## Step 6 — Update Notion card

Update the Notion card properties (only changed fields):
1. `👷‍♀️ Shaping` → the FigJam URL from Step 5
2. `Status` → `📐 Shaping` (only if current status is "Not specified" or "Specified but not started")
3. `🌾 Harvestr discovery` → Harvestr URL (if it was empty before and now linked)
4. `🔥 Harvestr Score` → discovery score from Harvestr (if available and different from current)

Confirm:
```
✅ [card name] — shaping created

FigJam: [url]
Notion: Status → 📐 Shaping, Shaping URL set
```

---

## Edge cases

- **No Harvestr discovery found**: still draft Frame and Claim from the card's `🇺🇸 Desc`. Write Observe JTBD as a hypothesis (mark clearly as "⚠️ Hypothesis — no Harvestr data"). Omit feedback stats.
- **Card already "▶️ Betted" or "🚀 Released"**: warn before changing Status — those cards shouldn't be reverted.
- **`👷‍♀️ Shaping` already set and confirmed to overwrite**: proceed normally, create a new FigJam frame anyway.
- **Cycle not determinable**: ask Fabien to specify ("Which cycle are we shaping for?").
- **Multiple dominant use cases of equal weight**: flag it — _"Two strong use cases emerged: [A] (N feedbacks) and [B] (M feedbacks). Which one is primary?"_ — wait before writing Observe.
- **Template node not found**: iterate all pages using `for...of` loop — never use `.find()` to select the page before switching. If still not found, report which pages exist.
- **AI-suggested feedback on the discovery that looks off-topic**: happens when Harvestr auto-attaches recent messages to a discovery that actually belong elsewhere. Don't inflate the counters with them and don't quote them as verbatims. Flag them in the response to Fabien: _"⚠️ N AI-suggested feedbacks on this discovery look off-topic ([customer names], dated [date]) — they're about [other subject]. Worth validating/moving in Harvestr."_
- **Stickies appear outside the section / in the wrong color**: the regression pattern — stickies were appended to `clone` instead of the specific section, or created with default yellow. Always use `section.appendChild(sticky)` and copy `fills` from a peer sticky or the section itself. See Step 5 visual integrity rules.
