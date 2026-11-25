---
name: shaping-terminology
description: Review product terminology against Dashdoc's official glossary — check consistency, flag missing or misused terms, and produce actionable recommendations for product managers. Use whenever the PM says things like "review terminology in this pitch", "check terms against the glossary", "terminology audit", "is this term in the glossary", "check the wording of this FAQ/Linear task/pitch", "audit terms", or any equivalent request involving terminology consistency during shaping or release. Also trigger when the PM pastes a pitch page, Linear task, FAQ entry, or any product content and asks for a review or consistency check.
---

# shaping-terminology — Terminology Review

Given product content (pitch, Linear tasks, FAQ entries, changelog, etc.), fetch the live Dashdoc glossary from Prismy, then produce a structured terminology audit: term-by-term analysis, consistency issues, and an actionable recommendations table.

---

## Step 1 — Fetch the glossary

Always start by fetching the live glossary from Prismy:

```bash
ENV_FILE="${DASHDOC_SKILLS_ENV:-$HOME/.config/dashdoc-product-skills/.env}"
[ -f "$ENV_FILE" ] && set -a && . "$ENV_FILE" && set +a
curl -s https://app.prismy.io/api/public/glossary \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PRISMY_API_TOKEN"
```

The Prismy API token is a secret: **never write it in a skill file, in the repo or in your output.** It comes from `PRISMY_API_TOKEN`, either already exported or loaded from `~/.config/dashdoc-product-skills/.env` (outside any repo, survives plugin updates). Setup, once: copy `.env.example` (next to this file) to that path and fill in the token. If `PRISMY_API_TOKEN` is empty, tell the user to do that setup (never ask them to paste the token in chat) or ask for a pasted glossary export.

**JSON structure:** The response is a flat array of entry objects:
```json
[
  {
    "description": "A responsive web interface where drivers self-declare arrival...",
    "terms": {
      "en-US": { "value": "Driver Check-in Portal" },
      "fr-FR": { "value": "Portail d'enregistrement conducteur" },
      ...
    }
  },
  ...
]
```

- The canonical English term is at `terms["en-US"].value`
- `description` may be `null` — meaning the term exists as a translation entry but has no formal definition yet
- Build a lookup map: `{ "Driver Check-in Portal": "A responsive web interface..." }` (skip entries where `en-US.value` is empty or null)

**Fallback:** If the fetch fails, inform the user and ask them to paste the glossary content, or proceed with Notion FAQ terms as a secondary source if available.

---

## Step 2 — Parse the input content

Accept any product content:
- Pitch pages (Notion URLs or pasted text)
- Linear issue titles / descriptions
- FAQ entries
- Changelog drafts
- Any free-form product text

If a Notion URL is provided, fetch it via the Notion MCP. If a Linear issue ID is provided, fetch it via the Linear MCP. Otherwise work with the pasted text directly.

**Extract all domain terms** — nouns and noun phrases that describe product concepts, features, entities, roles, or states. Ignore generic words.

---

## Step 3 — Analyse each term

For each extracted term, cross-reference against the glossary lookup map (case-insensitive):

| Case | Action |
|------|--------|
| Term matches glossary, has a `description` | ✅ Confirm it's used consistently with its definition |
| Term matches glossary, but `description` is `null` | ⚠️ Term exists (translation only) — no formal definition yet; flag if a definition would help |
| Term is a variant/synonym of a glossary term | 🔁 Flag — recommend using the canonical `en-US` term |
| Term is not in the glossary at all | 🆕 Flag — suggest adding, replacing, or clarifying |
| Term is in the glossary but used inconsistently with its `description` | 🛠 Flag — cite the inconsistency and suggest a fix |

---

## Step 4 — Output

Produce the analysis in this format:

---

### [Term name]  [emoji flag]
**Glossary definition:** [definition if exists, or "Not in glossary"]
**Used as:** [how it's used in the input content, with a direct quote]
**Assessment:** [clear one-liner]
[Suggestion if needed — provide a formal rephrasing when recommending a definition change]

---

Repeat for each flagged term. Then close with:

### ✅ Terms used correctly
List terms that were found in the glossary and used consistently — brief, one line each.

### Summary

| Original term | Suggested change | Reason |
|---------------|-----------------|--------|
| … | … | … |

---

## Conventions

- **Tone:** formal, concise, actionable — written for product managers
- **Cite examples:** always quote the exact passage from the input where the term appears
- **Formal definitions:** when suggesting a new definition, use the form: "A [category] that [does/represents X], [constraint or scope]."
- **Glossary is source of truth** — don't invent canonical terms; flag gaps instead
- **Also check the Notion FAQ** for terms in common use that may not be in the glossary yet, if Notion MCP is available

---

## Example output snippet

```
### Waiting Queue
**Glossary definition:** Not in glossary
**Used as:** "vehicles accumulate in the waiting queue before being called" (pitch p.3)
**Assessment:** 🆕 Term not in glossary — should be added or replaced.
**Suggested definition:** A list of Slots that have arrived at the site but are awaiting handling in a staging area. The waiting queue has no size limit.

### Handled Queue  🛠 Rename
**Glossary definition:** Not in glossary
**Used as:** "moved to the handled queue once processing begins" (FAQ entry #12)
**Assessment:** "Handled" implies a completed state. Rename to **Handling Queue** to reflect the in-progress nature.
**Suggested definition:** A list of vehicles currently being handled in a designated Zone, limited by Zone capacity.

### ✅ Terms used correctly
- **Slot** — used consistently with glossary definition throughout
- **Zone** — used consistently

### Summary

| Original term | Suggested change | Reason |
|---------------|-----------------|--------|
| Handled Queue | Handling Queue | Reflects ongoing state, not completed action |
| Waiting Queue | Add to glossary | Widely used, no canonical definition yet |
```
