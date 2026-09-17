---
name: shaping-steal
description: The STEAL step of a Dashdoc shaping — first drafts benchmark DIRECTIONS (what pattern to capture, in which tools, and why), then EXECUTES the benchmark: finds real competitor screenshots (from marketing/CDN pages when help-centers are gated), models concrete UX directions with trade-offs mapped back to the pitch's requirements, optionally builds a quick clickable HTML prototype, and imports reference images into the FigJam board. Use whenever Fabien says things like "steal for [topic]", "benchmark directions for [pitch]", "benchmark this", "what should I look at for [topic]", "find competitor screenshots", "model the UX directions", "how do [competitors] do [X]", "prototype the directions", or any equivalent competitive/adjacent research during shaping. Works from a plain topic or a Notion card URL; anchor to the Observe JTBD so you benchmark what solves THAT use case.

---

# shaping-steal — Benchmark Directions + Execution (STEAL step)

Two phases. **Phase A (Directions)** produces a structured benchmark guide for the **STEAL > Nuggets** section in FigJam. **Phase B (Execution)** — when the user wants to go further — pulls real screenshots, models the UX directions, prototypes, and lands references on the board. Meant to run during/after `shaping-start`, once the topic or JTBD is known.

---

## Step 1 — Extract the topic

**If a Notion card URL is given:** fetch it; extract `name`, `🇺🇸 Desc`, `🧩 Domains`, and the Observe JTBD if present. Derive the benchmark topic from the functional theme.
**If a plain topic is given:** use it directly.
**If too broad** (e.g. "Flow"): ask for a more specific functional topic or a card URL.

Stay anchored to the **Observe JTBD** — benchmark what solves *that specific use case*, not the feature in general.

---

## Phase A — Step 2: Produce the benchmark guide (STEAL > Nuggets)

```
🔍 **Benchmark guide — [topic]**

### Direct competitors to check (TMS / logistics SaaS)
[3–5 tools. Each: Name · what exact pattern to capture (precise) · where in the product · why relevant (what risk/design question it answers). Prioritise tools already in the Dashdoc Visual Benchmark FigJam.]

### Adjacent SaaS to explore (non-competitors)
[3–5 tools from other industries that solved a similar pattern. Each: Name + industry · pattern to extract · why it applies despite the different domain.]

### Pattern types to evaluate
[3–5 design archetypes; name the pattern + the trade-off it represents. Gives vocabulary to label benchmarked nuggets.]

### Search terms
[5–8 FUNCTIONAL (not branded) terms for the Dashdoc Visual Benchmark FigJam (https://www.figma.com/board/IFY07lmCkRhgRP8vjAteNV/Visual-Benchmark---Competitors?node-id=3-671), Mobbin / Screenlane / Google.]

### Non-SaaS inspirations (optional)
[1–2 outside-software references if genuinely useful.]
```

Rules: each tool entry names **what exact pattern to capture** (not just "look at this app"); group patterns by the **design question** they answer; prioritise competitors already on the Visual Benchmark board.

---

## Phase B — Execute the benchmark (when asked to go further)

Trigger when the user wants real artefacts: "find screenshots", "model the directions", "prototype", "populate the board".

### Step 3 — Find real screenshots
- **Help centers are usually gated** (403 / login). The reliable source is **marketing / product pages**, which expose direct CDN image URLs. WebFetch the product page and ask for "direct image URLs (png/jpg/webp) of product screenshots showing [the pattern]."
- Bump CDN size params for higher-res (`w_…,h_…`, `?w=…&fm=png`). Convert WebP→PNG with `sips -s format png in.webp --out out.png`.
- If nothing usable, give the user **Google Images / YouTube search URLs** + specific help-center article URLs (they render screenshots in a logged-in browser). Don't pass off a weak/irrelevant shot as the pattern — say so.
- (For an `image_search` tool if available, search the pattern not the brand — "file attachment checklist SaaS UI", not "Jira attachment".)

### Step 4 — Model the UX directions
Turn the benchmark into a **design space**: name the 1–2 axes (e.g. *where the signal lives*: look-it-up vs comes-to-you; *how it's expressed*: binary vs magnitude vs confidence), then enumerate **4–6 coherent directions**. For each: essence · a competitor proof-point · what it looks like · **which requirements it serves** (cite the pitch's requirement IDs) · trade-off · build weight. End with a **recommended stack** (MVP → later) and which to avoid first. Directions that aren't mutually exclusive should be flagged as combinable.

### Step 5 — (Optional) Illustrative dynamic prototype
If it helps the user *feel* the directions, build a **self-contained clickable HTML prototype** with realistic data drawn from the pitch's actual personas/feedbacks. Make the directions toggselectable (filter, confidence on/off, click-to-alert) so the trade-offs are tangible. Write it under `~/Documents/personal-os/prototypes/` and `open` it. Keep it one file, vanilla JS.

### Step 6 — Land references on the FigJam board
Import the chosen screenshots into a labeled **"Competitor UX references" cluster** (or the relevant STEAL/section block), each captioned with the **direction it illustrates**. Follow `~/.claude/skills/shared-references/figjam-mechanics.md` exactly — section-relative coordinates, `upload_assets` (POST bytes immediately, URLs expire), aspect-matched frames. Verify nothing overflows the section before reporting.

### The alerting / notification lens (reusable)
When the topic is alerts/warnings/visibility, **telematics platforms** (Webfleet, Geotab, Samsara, Verizon Connect, Map&Truck, Tachyshare) are the deepest benchmark — and our customers already use them. Key transferable patterns: rule/exception engine, persistent dismissable banner / alert inbox, on-map marker + sticky popup, multi-channel + quiet-hours, event-vs-state alerts, geofence/driving-time triggers. The strategic lesson is almost always **alert fatigue is the failure mode** → surface only the actionable state, in-context, not a separate tool. Map each pattern to a requirement/guardrail.

---

## Output rules
- Phase A output is paste-ready for STEAL > Nuggets; offer to place it on the board.
- Always tie nuggets/directions back to the pitch's **requirements and success criteria** — a benchmark that doesn't answer a design question for *this* pitch is noise.
- Be honest about screenshot quality and gated sources; never present a generic marketing image as "the alert UI" if it isn't.
