---
name: idea-frame
description: Capture a product idea for the Community product, challenge it against customer evidence, and formalise it in the Figma opportunity tree — one shaping-format frame (journey logigrams, illustrative visuals, hypotheses, evidence, backtest spec) plus basic solution blocks in the opportunity solution tree, hyperlinked both ways with no dotted lines. Use when the PM says "I have an idea", "capture this idea", "formalise this idea in Figma", "add this to the opportunity tree", "idea-frame", "promote this idea", or when an interview insight sounds like a solution rather than a need. Writes to Figma only after the plan is confirmed.
---

# idea-frame — From a loose idea to a frame and solutions in the tree

Ideas come from the PM, the dev and the designer, and from interviews. They are cheap to have and easy to lose. This skill gives them one path: **capture → challenge → place in the tree → frame → backtest spec → review → backtest task**. The tree stays alive: an idea enters it as soon as it is formalised, it does not wait for a "promotion" ceremony.

Read first: the PM's Community vision and the current opportunity solution tree (OST) in the Figma file. Find the Figma link of the tree in the PM's memory or notes first; ask only if it is not there, and then save it for next time. Never ask for it twice.

Before any Figma write, load the Figma tools' own skills with `get_figma_skill` and `uri` = `skill://figma/figma-use/SKILL.md` and `skill://figma/figma-use-figjam/SKILL.md` (the `Skill` tool does not know them), and show the plan (Step 2 and 3 summary). Confirm before writing. Everything in Figma is in English.

---

## Step 1 — Capture and challenge

1. Restate the idea in **one sentence** plus: who it is for (which side of the network), what changes for them, where it came from (which interview, which date, or a colleague).
2. **One idea or several?** If the idea mixes things with different owners, scopes or legal questions (a private list vs a shared signal, two sides of the network, a list vs an indicator built from it), propose to **split it into separate ideas**, one frame each, linked to each other by hyperlink. Build only the one the PM picks; note the others as related ideas.
3. **Overlap check**: look in the tree and in the product screens already in the file for something that does the same job (an existing list, page or solution). If it exists, say so and propose a **dedicated frame for the new idea, linked both ways to the existing one**, rather than rewriting the existing frame. Reuse and rename the existing tree block only when it is the same solution (the new idea just makes it more precise). Never edit a frame the PM owns beyond a one-line link without asking. Also look for the need in the Harvestr discovery tree: if a discovery already holds it, say where, and do not propose a duplicate.
4. Ask at most 3 sharp questions, only on what changes the design, **numbered, in plain words, each with your recommended answer** so the PM can reply inline. Do not use jargon the PM did not use: say "opportunity tree", not "OST"; do not write "anonymous aggregate", "escrow" or similar without a plain-words explanation. This holds for hypotheses and frame text too. Typical questions: who is the target (one side or both)? what must stay private? who does the work to make this work, and what do they get back (the incentive)? Do not ask what you can read in the tree or in the evidence.
5. **Evidence sweep** (read-only): Harvestr discoveries and messages, the Notion interview database, interview drafts in the repo. Sort into **For**, **Against or mixed**, **Gap**. Cite company and date for every item. Sort an item by what it says about the **mechanism of the idea**, not about the pain: a manual workaround that does what the idea would do (for example asking for prepayment by hand) is a **For**. Note which side of the network the speaker is on (a quote about offering freight is not about looking for freight). Never invent a quote or a number. If a data claim is needed, pull the real figure with the `dashdoc-data` skill or write "xxx". Say what you read in full and what only as a summary.
6. **Push back**, with evidence, when: the idea is really a need ("they want X" without a mechanism); it conflicts with a recorded decision; or its **key assumption** looks weak (for example a flag on a company only works if bad actors reuse a stable identity, but the cases found were impersonation, where the flagged identity is the victim). The PM may correct you with facts you did not have: update the idea, and keep what is still unknown as a hypothesis. **Never state the business model or who pays as a fact**, even if a past decision says something about one side (for example "no fees for carriers"): leave it blank unless the PM states it for this idea.

## Step 2 — Place it in the tree

Rules (from continuous discovery):
- A solution always sits under **one** opportunity. Compare solutions only under the same opportunity.
- A global idea that spans several opportunities is **split into several solutions**, each under its own opportunity. The global idea lives in the frame; the solutions live in the tree.
- Each idea has one **key assumption** (the thing that, if false, makes it fall).
- If no opportunity fits, propose a **new opportunity** and ask. Place it under the outcome, worded as the user's need ("I know partners I never want to deal with"), with **one evidence sticky per source** (company, date, short quote). Do not reuse a sticky already placed under another opportunity: use another source, or say the overlap to the PM.
- Tag opportunities by side (shipper, carrier, both) when the product is a network.

Output a short table: solution title | parent opportunity | key assumption. Wait for the PM's OK.

## Step 3 — Build the frame (the shaping format)

One frame in an **Ideas** section of the same Figma file, **stacked below the previous idea frames**, named "<Idea> (shaping format)", in the shaping style: **few shapes, few colours, illustrations first**. Layout, left to right:

1. **Title + one sentence** on a light pink frame (`#FFE0E0`).
2. **Four salmon blocks** (`#FFAFA3`, about 420×620, text only): *How it works*, *Rules & properties*, *Limits / Out of scope / Open*, and a fourth if a second side exists. Short bullets, plain words.
3. **Journey logigram, Today vs With the idea**: one white box per step, arrows between steps, one row for each. This is the part the PM values most. Add one logigram per side when there are two (demand, supply) as its own titled section.
4. **Illustrative visuals** of what each user would see. They help picture the idea, they are **not mock-ups and not a spec**. When a screen already exists, **adapt it** (its list, its page) instead of inventing a new UI. Use placeholders for prices ("xxx – yyy €") and for anything not measured. When the user can choose between modes, show the modes as options.
   Say in the Rules block **what the user gains** from doing the work (the incentive), not only what the idea does.
5. **Solution cards**: one per tree solution, with the title, "Under: <opportunity>" hyperlinked to the opportunity node, "Covers: …", and "Open in the tree →" hyperlinked to the solution block.
6. **Hypotheses table**: `# | Hypothesis (if false, the idea falls) | How to test`. One plain sentence per hypothesis, one condition only, no chained "if… then… unless…". Include the legal and operational question when a third party acts on someone's behalf.
7. **Evidence block** (salmon): For / Against or mixed / Gap / Next, from Step 1.
8. **Backtest section** when data can test it (Step 5).

Unknowns are drawn as **red boxes starting with "?"**, with a hypothesis number. Leave business model and pricing blank on purpose unless asked.

## Step 4 — Add the solution blocks to the tree

- **Clone** an existing solution block and its connector from the tree so the new blocks inherit the tree's style. Do not restyle.
- Block text: a **basic title** on the first line, then "<Idea name> (idea) →" **hyperlinked to the frame** (`setRangeHyperlink`, URL `…/board/<fileKey>/?node-id=<nodeId with a dash>`).
- Connect each block to its parent opportunity with an elbowed connector. **No dotted lines** between the tree and the idea: the hyperlink is the link.
- Several sessions may edit the same file at once. Just before writing, re-read the current positions and sizes of the Ideas section, the sections to shift and the nodes you target (they may have moved or been deleted), and never shift from numbers read earlier.
- Make room: grow the parent section and shift the sections below by the same amount, then grow the enclosing container. Check the Ideas section was pushed down too.
- Read the hyperlinks back (`getRangeHyperlink`) on every block and every card.

## Step 5 — Backtest spec (when the idea can be tested on past data)

A numbered logigram section in the frame, four boxes and a red "?" box:
1. Which past events to replay (period, cohort, proxy). 2. What the actor would have seen. 3. How the candidate pool is built (distance, time window, detour rules). 4. What to measure (coverage at ≥1 and ≥3, rank of the real choice, number of past prices).
5. **Limits and data to check first** (coordinates, price fields, who is in the pool).

Rules: **thresholds are set after the first run, from the real baseline, never before**. Map each measure to a hypothesis number. Running it is a separate step: load the `dashdoc-data` skill, check the data exists with cheap probes, then query. When the backtest relies on a label or a field (a tag, a coordinate, a price), do the cheap count now (aggregates only, no personal data) and write the result in the limits box instead of "to check".

## Step 6 — Verify and review

- Screenshot the frame and the tree sections. Shorten any text truncated in a fixed-height box rather than shrinking the font. Check that connectors still reach their boxes.
- Read the hyperlinks back. Keep the previous version of a replaced board, renamed "to delete once validated", until the PM confirms.
- Review loop: read the file's **unresolved comments** (`get_comments`, filtered on the new frame). Sort them into *keep*, *change*, *question*. Do not edit anything the PM added or changed in the file without asking. Report in a table.
- Do not run or write anything outside Figma without asking (Linear, Notion, Harvestr), except the backtest task of Step 7 once the PM said to create it.
- Before updating anything the PM or a colleague may have touched (a Figma link, a Linear task), re-read its current version first.

## Step 7 — Backtest task in Linear (once the PM validates the frame)

Propose, then create when the PM says yes:
- A task in the PM's team **backlog** (for Community: team COM), label **"Idea backtest"** (create the label, with a one-line description, if it does not exist). No priority, assignee, project or cycle unless asked.
- Structure: copy the latest "Idea backtest" task (Why / What to do / Check first / Rules / Done when) and link to it as a related task.
- Content: the backtest section of the frame, as written (period, what is replayed, how the pool is built, what is measured, data limits, **no threshold before the first run**), plus a definition of done: the baseline pulled and reported next to each hypothesis it tests.
- Link both ways: the Figma frame attached to the task, and a link from the frame's backtest section back to the task (the PM may add it).

## Lifecycle of an idea

| Stage | Where it lives |
|---|---|
| Captured | One line in the PM's inbox or the Ideas section |
| Formalised | Frame + solution blocks in the tree (Steps 3-4) |
| Tested | Backtest result and interview feedback added to the evidence block |
| Bet | Becomes a shaping and a pitch (continue with the shaping skills) |
| Parked | Stays under its opportunity in the tree, tagged with a revisit trigger (what new evidence would reopen it) |

## Figma API gotchas (FigJam)

- Shapes with text: `createShapeWithText`, `shapeType = 'SQUARE'` (or rounded). Text through `shape.text.*`; plain TEXT nodes use `node.characters` and `getRangeFontName` on the node itself.
- `textAlignVertical` is **not supported** on FigJam text nodes: it throws. Do not set it.
- Load the font before writing text (`loadFontAsync`). Inter Regular, Medium and Semi Bold are available.
- Connectors: `createConnector`, `connectorStart` / `connectorEnd` = `{ endpointNodeId, magnet }`, `connectorLineType` `'ELBOWED'` or `'STRAIGHT'`, `connectorEndStrokeCap = 'ARROW_LINES'`. A cloned connector can be re-attached by setting both endpoints.
- Tables: `figma.createTable(rows, cols)`, `cellAt(r, c).text`.
- Cloning a section clones its children and keeps connectors attached to the clones.
- Text in a fixed-height shape is truncated with "…" when it does not fit on its lines. Shorten.
- `use_figma` returns at most 48,000 bytes: return ids and short summaries, not whole trees; an over-limit run commits nothing.
- Elbowed connectors refuse the `CENTER` magnet: use `TOP`, `BOTTOM`, `LEFT` or `RIGHT`.
- A node id can disappear when another session deletes or rebuilds it: look it up again before using it.
- `get_metadata` does not work on FigJam files; use `use_figma` to list children and `get_screenshot` to look.
