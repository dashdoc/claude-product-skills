---
name: shaping-requirements
description: Derive a prioritised, evidence-traced requirements list for a Dashdoc pitch from everything collected during shaping — Harvestr feedbacks, success criteria, pitch scope, interviews, and competitor benchmark. Groups requirements by capability area, assigns MoSCoW priority anchored to feedback criticality + success criteria + customer commitments, traces each to its evidence, separates functional requirements from constraints/guardrails (incl. interview counter-signals), makes explicit in/out-of-scope calls, and emits a single copy-paste FigJam-ready table. Use whenever Fabien says things like "derive requirements", "list the requirements", "turn this into requirements", "what are the requirements for [pitch]", "requirements table", "scope this pitch", "what should we build", or any equivalent request to convert shaping evidence into buildable scope. Always trace each requirement to evidence, always cross-check against the success criteria, and always confirm in/out-of-scope before finalising.

---

# shaping-requirements — Evidence → Requirements

Turn the material gathered during shaping into a **prioritised, traceable requirements list** that a team can build from and a betting table will trust. The output is defensible because every requirement points back to a feedback, an interview, a success criterion, the pitch scope, or the benchmark — and because what's *out* of scope is named, not silently dropped.

This is the bridge step between OBSERVE/CLAIM (what customers need) and the build: it consumes the outputs of `shaping-observe` (feedbacks + First Use Case), `shaping-success` (measurable criteria), and `shaping-steal` (benchmark + UX directions).

---

## Principle

> A requirement with no evidence is an opinion; a success criterion with no requirement is a wish. Make both links explicit.

---

## Step 1 — Gather all the material (don't work from feedbacks alone)

Pull together whatever exists for the pitch — ask the user for links if missing:
- **Harvestr feedbacks** (per the discovery + subdiscoveries), each with **company/segment + criticality** (must-have / nice-to-have). → functional requirements + priority.
- **Success criteria** (from the card or a `shaping-success` run). → ensures each metric has a requirement that moves it; surfaces instrumentation requirements.
- **Pitch scope** (card body: in-scope / out-of-scope / prerequisites). → in/out calls + technical enablers.
- **Interviews** (incl. field visits). → real constraints and **counter-signals** (a customer rejecting a mechanism the pitch assumes — e.g. "don't auto-reprioritise").
- **Benchmark / UX directions** (from `shaping-steal`). → non-functional lessons (e.g. alert-fatigue → a trust guardrail).

## Step 2 — Cluster into capability areas

Group requirements by **capability area**, not by source (e.g. A. Computation engine, B. Detection, C. List/surfacing, D. Alerting, E. Customer visibility, F. Constraints). Areas keep the list scannable and make scope trade-offs legible.

## Step 3 — Write each requirement

For every requirement capture four things:
- **Statement** — one outcome-oriented sentence ("Flag a transport probably-late before the asked datetime"), not an implementation.
- **Priority (MoSCoW)** —
  - **Must** = backed by a must-have feedback, *or* required to move a success criterion, *or* a customer commitment.
  - **Should** = strong but non-blocking signal.
  - **Could** = single/weak signal, nice-to-have.
  - **Won't (now)** = explicitly deferred (becomes Out-of-scope).
- **Evidence** — the feedback (with company), interview, success-criterion, or scope line it derives from. No orphan requirements.
- **Area**.

Separate **functional requirements** from **constraints / non-functional** (guardrails, counter-signals, cost ceilings, data-quality limits). Constraints are first-class — the trust guardrail and the "don't auto-reprioritise" counter-signal matter as much as features.

**Instrumentation requirements:** if a success criterion can't be measured today (no signal exists), the instrumentation itself is a Must requirement (e.g. "record the first-detection timestamp to measure lead time"). Don't leave it as an open question if the user confirmed the metric matters.

## Step 4 — Make in/out-of-scope explicit (confirm, don't assume)

- List what's **out of scope** as rows, each with a one-line reason — adjacent clusters (a different mechanism or purpose) are the usual candidates.
- **Ask the user** before excluding an adjacent cluster that has real demand; note when an excluded need could be served later by a mechanism this pitch builds (reusability).
- Silent truncation reads as "we covered everything" when we didn't — always surface the dropped scope.

## Step 5 — Cross-check (the part that catches mistakes)

- **Every Must** should map to a success criterion or a commitment — if not, question whether it's really a Must.
- **Every success criterion** should have at least one requirement that moves it — if not, flag the orphan (a metric with nothing built for it).
- **Every First-Use-Case beat** (situation → objective → workaround) should be answered by a requirement — gaps mean the hero journey isn't fully covered.
- Reconcile with **constraints**: does any requirement violate a counter-signal? (e.g. an "auto-reorder" feature against a "don't auto-reprioritise" constraint.)

## Step 6 — Output (one copy-paste table)

Emit a **single markdown table** (FigJam pastes it as a table object), columns: `# | Area | Requirement | Priority | Evidence / source`. Use stable IDs (A1, A2, B1…) so requirements can be referenced elsewhere (Linear, FigJam, the card). Follow with:
- an **Out-of-scope** mini-section (rows with reasons),
- an **Open questions** list (genuine unknowns that block build-readiness — e.g. an eligibility definition, a cost ceiling owner).

Keep statements one sentence; betting-table-readable.

If asked to put it on the board, see `shared-references/figjam-mechanics.md (in this plugin root)` for the FigJam table/section + coordinate mechanics. Otherwise output text only and offer to (a) write it into the card's Scope section, or (b) scaffold Linear user stories via `create-pitch-tasks` once the pitch is bet.

---

## Edge cases
- **Thin evidence** (few feedbacks): still produce the table, but mark low-evidence requirements and recommend more discovery (`shaping-observe`) rather than inventing Musts.
- **No success criteria yet**: produce functional requirements, but flag that priority/measurability is provisional until `shaping-success` runs.
- **Counter-signal vs feedback conflict** (a customer wants X, another rejects it): record both, make the constraint explicit, and raise it as an open question — don't quietly pick a side.
- **Adjacent-cluster temptation** (the pitch could swallow a neighbouring need): default to keeping the pitch focused; offer the broader-scope option explicitly with its cost.
- **Pending-instrumentation metric**: convert to a Must instrumentation requirement once the user confirms the metric matters; otherwise leave in Open questions.
