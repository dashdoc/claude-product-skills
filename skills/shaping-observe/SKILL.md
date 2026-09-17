---
name: shaping-observe
description: Build the OBSERVE step of a Dashdoc shaping — exhaustively gather the customer evidence behind a pitch and compose its First Use Case. Given a Harvestr discovery (and/or roadmap card), it maps the subdiscovery tree, pulls every existing signal, then hunts for what the discovery is MISSING — searching Harvestr by content AND by known requester/customer when keyword search fails, AND the Notion Interview database by domain language and by customer name — before composing a First Use Case in the JTBD emoji format. Treat "feedback" as any customer signal: in Harvestr that means BOTH messages and extracted feedbacks, so sweep both. Use whenever Fabien says things like "build the observe", "what do customers say about [pitch/need]", "find all the feedbacks for [discovery]", "search Harvestr and interviews for [topic]", "did we miss any feedback", "check our discovery covers [customer X/Y/Z]", "did we capture all of [customer]'s complaints", "customer evidence for [pitch]", "compose a First Use Case / JTBD for [pitch]", "re-cluster / reorganize / restructure the discovery", or "put the feedbacks on the FigJam / build the OBSERVE board". Always hunt by requester/customer when content search comes up short, always sweep messages as well as feedbacks, and always propose a primary + an alternate persona for the use case.

---

# shaping-observe — Gather Evidence & Compose the First Use Case

Given a Harvestr discovery (and optionally a roadmap card and its success criteria), produce a **consolidated feedback inventory** and a **First Use Case**, and — on request — a **subdiscovery restructure plan** and/or a **FigJam OBSERVE board**.

This is the OBSERVE deep-dive: the goal is *evidence completeness*. Most shaping starts from the signal already attached to a discovery — but the most valuable signal is often **not** attached, because customers describe the need in their own words, not product vocabulary. This skill's core job is to find that hidden signal.

**Writes:** the Harvestr and Notion MCPs are **read-only** for our purposes — you gather and you hand back navigable links; the user attaches/edits in Harvestr. The only write this skill performs is the **optional FigJam render** (Step 5d), and only when the user asks for it.

---

## The core insight (why this skill exists)

Customers almost never say "ETA" or "anticipate late transports." They say *"pas de trou dans la production"* (a shipper), *"l'ETA dans le planning"* (a DO), *"alerte si l'ETA est trop éloignée des heures planifiées"* (a carrier). The same need is scattered across **segments, eras, and vocabularies**, and a keyword search on the product term finds almost none of it.

**"Feedback" is shorthand for any customer signal — and in Harvestr it lives as TWO object types:**
- a **`message`** — the raw inbound (Intercom, Slack, NOTE, email, HubSpot…), the verbatim;
- a **`feedback`** — an insight chunk *extracted* from a message and linked to a discovery (VALIDATED), or AI-suggested (SUGGESTED, pending validation).

The signal you're missing very often exists as a **message that was never extracted into a feedback on this discovery**. So always sweep **both**, per customer. A message with on-topic content but no feedback toward the discovery is a consolidation candidate.

So this skill searches **three ways**, and the second one is the one people forget:
1. by **content** (keywords),
2. by **known requester/customer** (when you know *who* asked but search can't find *what* they said),
3. in the **Notion Interview DB** (where needs live as transcripts, not feedbacks).

---

## Context & resources

- **Harvestr discovery**: the card's `🌾 Harvestr discovery` (or a URL the user gives). Discovery URLs look like `https://app.harvestr.io/components/0/list/<discoveryId>`.
- **Notion Interview DB**: data source `collection://524c887f-b4ac-45f8-a46b-60f94236e9bc` (the 🎙️ Interview database).
- **Success criteria** (optional but valuable): from the roadmap card body or a prior shaping-success run — used to ground the *problem* line of the First Use Case in real baselines.
- **Harvestr tools** (all **read-only**): `list_harvestr_discoveries`, `list_harvestr_feedback`, `list_harvestr_customers`, `search_harvestr_customers_by_attributes`, `list_harvestr_messages`.

### Navigable links to hand the user (the MCP exposes no permalinks)
- **Message** (the reliable form): `https://app.harvestr.io/messages/search/<messageId>?query=` — the plain `/messages/<id>` and `/messages/archived/<id>` forms **404**; always use the `/messages/search/<id>?query=` form.
- **Discovery**: `https://app.harvestr.io/components/0/list/<discoveryId>`.
- **Contributor pages**: users `https://app.harvestr.io/contributors/users/<id>`, companies `https://app.harvestr.io/contributors/companies/<id>`.

### ⚠️ Tool quirks learned the hard way
- **`list_harvestr_feedback` `query` (semantic) frequently returns 0** even when matching feedback exists. The reliable modes are the **`discovery_ids`** and **`requester_ids`** filters. An empty `query` result is *inconclusive*, not negative — pivot to requester search (3b).
- **`list_harvestr_messages` `query` searches title + content, but matches SINGLE tokens.** Multi-word phrases return 0 — search one keyword at a time. Generic tokens (`dédié`, `location`) return hundreds incl. noise (e.g. "champ dédié" = a UI field) — prefer **discriminating** tokens (a brand, `loueur`, `rapatrier`, `factice`, a plate).
- **CS teammates are the message `submitter`, not the `requester`.** When CS logs a customer's words, the `requesterId` is the *customer*; the CS person is the submitter. There is **no submitter filter**, and `assignee` ≠ submitter — so you can't list "everything Cécile Niquet wrote." Reach CS-relayed signal via the **customer's** record instead.
- **Large message pulls exceed the tool's token cap and get saved to a file.** When that happens, don't try to re-pull smaller blindly — read the file with `jq`, filtering for your keywords (e.g. `jq '.messages[] | select(.content|ascii_downcase|test("dédi|locati|loueur|rapatri|plaque")) | {id,requesterId,title}'`), so a 150k-char dump becomes a handful of candidates.

---

## Step 1 — Map the discovery tree

Fetch the discovery and **all its subdiscoveries** — signal usually lives in the children, not the parent:
- `list_harvestr_discoveries` with `ids=[discoveryId]` → confirm title + state.
- `list_harvestr_discoveries` with `parent_ids=[discoveryId]`, `include=["feedback_count"]` → the subdiscoveries and how many feedbacks each holds. (The parent itself often reports `feedbackCount: 0`.)

Present the tree with counts and **ask which subdiscoveries are in scope.** A discovery often bundles an adjacent theme the pitch doesn't cover. Confirm exclusions before gathering — don't silently include or drop.

## Step 2 — Pull existing signal (per kept subdiscovery)

For each in-scope subdiscovery: `list_harvestr_feedback` with `discovery_ids=[subId]`, `take=25/50`. Paginate with the returned `cursor` until exhausted.

For every item capture **content, `requesterId`, criticality** (parse "must have / nice to have / point bloquant" from the text), and the source **message** (`messageId`). Resolve companies in one batch: `list_harvestr_customers` with `ids=[all requesterIds]`. Unnamed requesters are worth naming for segmentation.

Remember Step 2 only shows *extracted* feedbacks. The hunt (Step 3) is where you find the messages and interviews that never became feedbacks on this discovery.

## Step 3 — Hunt for what the discovery is MISSING

This is the heart of the skill. Run all three angles; expect content search to underperform.

### 3a — By content, using *customers' own language*
Don't search the product term. Build keyword sets from the **vocabulary customers used** in Step 2, across segments. Search **one discriminating token at a time** (multi-word phrases return 0; generic terms are noisy). Treat empty results as inconclusive.

### 3b — By known requester/customer (the one people forget)
When you know a customer voiced the need but search can't surface it, go find the customer and read everything they said — **messages and feedbacks both**:
- `list_harvestr_customers` / `search_harvestr_customers_by_attributes` with `query=<name>`. Name match is weak — try **variants**: the HQ, the specific site (e.g. "VEOLIA DOMBASLE (54)"), the parent group, *and the carrier that serves them* (a shipper's signal sometimes sits under its haulier, e.g. Mauffrey).
- If the user gives a contributor URL (`.../contributors/users/<id>`), the id is the `requesterId`.
- `list_harvestr_feedback` with `requester_ids=[ids]` **and** `list_harvestr_messages` with `requester_ids=[ids]` (`include_contents=true`), paginate. Read all of it — the relevant one is often titled blandly ("New Feedback") and only recognisable by content.
- If a CS teammate relayed it: don't search the teammate (they're the submitter) — search the **customer** they were writing for.

### 3c — In the Notion Interview database
Needs also live as interview transcripts, never logged as feedback:
- `notion-search` with `data_source_url=collection://524c887f-b4ac-45f8-a46b-60f94236e9bc`, **two ways**: by the same domain-derived keywords, **and by customer name** (the interview that holds a customer's dedicated complaint is often titled with their name, not the topic).
- Interviews are frequently **tagged to a *different* pitch** (e.g. a chartering or planning interview) yet contain on-topic lines. Open them and **read critically**: extract only the on-topic verbatim; flag **counter-signals** (a customer rejecting the mechanism the pitch assumes) — they're as valuable as supporting ones.

## Step 3-bis — Coverage check (when the user hands you a customer list)

A common request: *"check our discovery covers customers X, Y, Z who complain about [topic]."* For **each** named customer:
1. Resolve their record(s) — try the name + HQ/site/group/serving-carrier variants. If nothing resolves, **say so** and ask for the exact account/contact (don't silently drop it).
2. Sweep **both** their messages and feedbacks (3b).
3. Classify each on-topic item as **core** (the pitch's actual job) vs **adjacent** (a neighbouring need — pricing, reporting, planning view…). Be honest: a customer can use the feature heavily yet have no *core* complaint in Harvestr.
4. For each item, check whether it's already linked to the discovery tree → report per customer: **covered / gap (give the link to attach) / only-adjacent / nothing-on-topic / not-found**.

The honest negative — *"in Harvestr this customer has no complaint about this; their captured signal is X (adjacent)"* — is a real finding. Surface it rather than forcing a match. The complaint may live in CS/verbal/interviews; that's what Step 3c is for.

## Step 4 — De-duplicate, classify, flag what's missing

- Cluster all signal (existing + found) into the in-scope themes.
- De-dupe (the same message can appear as multiple feedbacks).
- Mark each as **already in the discovery** or **not yet attached** (candidate to enrich), with **company + criticality**.

## Step 5 — Outputs

### 5a — Consolidated feedback inventory
A clustered list, one line per item: `Company (segment) · criticality — the need in their own words`. Group by subdiscovery; lead each cluster with its must-haves. Note any out-of-scope subdiscoveries you excluded.

### 5b — "Not yet in the discovery" list with locating links
The MCP is read-only and exposes no permalinks, so hand the user what they need to find and attach each item themselves:
- the **message deep-link** `https://app.harvestr.io/messages/search/<messageId>?query=`,
- the **discovery URL** to attach into,
- the **contributor page** as a fallback,
- message **title + date** so a content search lands on it.

Do **not** say you'll attach it — you can't (read-only). Offer to *format* it as a paste-ready insight if helpful.

### 5c — The First Use Case
Compose **one** dominant use case (not a blend) in this exact format:

```
🙋 I am <persona>
🕹️ and when <situation>
🤩 what matters the most to me is <objective>
😫 but it turns out that <problem>
🤸‍♀️ so <alternative or consequence>
```

Rules that make it land:
- **Persona / situation / objective** come from the *most-represented* cluster and its must-haves.
- The **`but it turns out that`** line is the *real gap*. Ground it in success criteria/baselines if available (e.g. "only ~214 partner pairs are linked, +~10/month; truckers have no plate to auto-match") — far stronger than a vague "it's not visible."
- The **`so`** line is the **painful consequence / workaround customers actually described** (external tools, duplicate records, calling support) — NOT the solution. This matches Dashdoc's house JTBD style.
- If the scope spans several capabilities, the objective line can carry them as named sub-clauses (connect / lifecycle / shared-data), but keep one persona and one situation.
- Then offer an **alternate persona framing** (e.g. receiver vs owner, dispatcher vs shipper) in 2-3 lines and ask which is the hero — the right one depends on which team owns the pitch and where the pain actually bites.

### 5d — (Optional, on request) Render the OBSERVE block on FigJam
When the user asks to "put the feedbacks on the FigJam" / "build the OBSERVE board": create **one sticky per feedback**, organised into **sub-blocks (FigJam sections) per subdiscovery**.
- **ALWAYS use the full verbatim — never rephrase the customer.** Trim only the non-verbatim tails (Source-URL lines, image refs, "(effacer les mentions inutiles)" template instructions). Lead each sticky with `Customer · criticality`, then the verbatim.
- **Colour-code** each sub-block; **mark out-of-scope blocks in the title** (e.g. `3 · Unified view — ❌ HORS SCOPE`).
- **Mechanics** (see `../shared-references/figjam-mechanics.md` if present): append each sticky to *its section* (not the parent), set fills per block, set `x`/`y` **after** append (relative to the section), let stickies auto-grow and **stack by reading `sticky.height`** (their settled height differs from the value right after creation — re-read before relying on it), then resize section + parent to fit. **Verify with a screenshot** before declaring done; watch for stale-height overlap when appending to an existing column.

### 5e — (Optional, on request) Re-cluster & propose a subdiscovery restructure
When the current organisation muddles *process-steps* with *data-types* (a frequent smell), re-cluster **all** feedbacks (parent + subs) by **underlying job/capability**, deliberately ignoring the current structure (it anchors you to the wrong cut).
- Propose the target subdiscoveries; map current→new: **rename** an existing one to preserve its history, **create** the genuinely new ones, **archive** the emptied ones.
- Give a **per-feedback move plan**: `feedbackId · customer · need → target` (from → to). The MCP is read-only, so this is a plan the user executes in Harvestr.
- Surface **scope levers** (e.g. a whole sub-block that's currently out-of-scope but holds must-haves / a deployment blocker) and **loose ends** (blank "New Feedback" items, duplicates, items that belong to a different discovery entirely).

---

## Edge cases
- **Parent discovery has 0 direct feedback** → normal; enumerate children.
- **A subdiscovery is off-topic** → ask before excluding; report the exclusion so coverage isn't silently overstated.
- **Content search returns nothing** → don't conclude "no signal." Pivot to requester search (3b), message sweep, and interviews (3c).
- **Customer not found by name** → try site/HQ/group variants and the serving carrier; if still nothing, flag it and ask for the exact account — don't drop it.
- **Customer has only adjacent signal** → report it honestly ("no core complaint in Harvestr; their captured signal is X"); the real complaint may be in interviews/CS.
- **CS teammate named as the source** → search the customer, not the teammate (submitter ≠ requester, no submitter filter).
- **Interview tagged to another pitch** → still mine it; extract only the on-topic sentence; surface counter-signals prominently.
- **No success criteria available** → still compose the use case, but mark the `but it turns out that` line as needing a baseline (offer to run shaping-success).
- **Multiple equally-dominant personas** → present both as candidate First Use Cases and ask which is primary.
- **FigJam render overlap** → a sticky's height right after creation differs from its settled height; re-read `.height` before stacking, and screenshot to confirm no overlap.
