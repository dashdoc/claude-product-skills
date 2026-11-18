# Reading a 🛎️ Changelog entry for a digest

Shared by [changelog-digest](../changelog-digest/SKILL.md) (weekly) and
[changelog-digest-monthly](../changelog-digest-monthly/SKILL.md) (monthly).

## Read the page body, not the `Slack summary`

**`Slack summary` is not the source for a digest line.** It is a one-line field that feeds the
native `#changelog-hose` automation. It is routinely thinner than the entry itself, it drops
rollout state entirely, and it never carries the demo link.

Fetch the page (`notion-fetch` on the row url) and derive the digest line from its **body**.
One fetch per announced row. Do this only for rows that survive filtering — never fetch the
whole DB.

## What to extract, in priority order

| # | Source in the body | Use for |
|---|---|---|
| 1 | **`🗣️ For CS & Marketing`** — its `**Say:**` lines | **The best source there is.** Written by the PM precisely to be repeated outside the product team. Use it near-verbatim. Its `**Don't promise:**` list is a hard deny-list for the digest line. |
| 2 | **Core-value one-liner** — the first prose paragraph after any callout | The digest sentence. The PDR asks PMs to write exactly this: the value, and whether the release is partial or complete. |
| 3 | **`📖 User Story`** — *"As a X, I want to Y, so that Z"* | Who it is for and why, when the one-liner is thin. Rewrite as plain prose — **never paste the As-a/I-want form into a digest.** |
| 4 | **`*Solution*`** / **`✅ The solution`** | The value, on entries written in the informal Problem/Solution shape. |
| 5 | **`⚙️ How it works`** bullets | Only to make a vague sentence concrete. Never list these — the reader clicks through for mechanics. |
| 6 | **FF callout + rollout wording** (see below) | Rollout hedge. |
| 7 | **`⚠️ Known limitations`** / **`ℹ️ Good to know (what it does not do yet)`** | Never listed, but the digest line must **not contradict** them. |
| 8 | **Public video link** (see below) | An optional `· [demo →](url)`. |
| 9 | `Slack summary` | **Fallback only**, when the body is empty or unusable. |

> A `🗣️ For CS & Marketing` block outranks everything else because it is the same job as the digest:
> say this to people outside the team. If it has a `Don't promise:` list, **no claim on that list may
> appear in the digest line**, however the rest of the body reads.

## Structure varies — do not assume the template

The `release-changelog` template is not always followed. Handle at least:

- **Formal**: `### **The Problem:**` / `### ✅ **The solution:**`, or `📖 User Story` + `⚙️ How it works`.
- **Informal**: `*Problem*` / `*Solution*` in italics, often first person
  (*"When I'm subcontracting, I want to check…"*). Convert to third person / "you".
- **One-liner only**: a single paragraph, no headers. Use it as-is.
- **Empty body**: fall back to `Slack summary`; if that is empty too, emit
  `{Name} — _no summary yet_ [details →]({url})` and flag the row.

## Feature-flag callouts are a hedge — carry them

The body's top callout states rollout reality that exists nowhere else:

| Body says | Digest must say |
|---|---|
| `under FF X, activated to all today` | nothing — it is fully live |
| `under FF X` with no full-activation wording | `_(rolling out)_` |
| a percentage ramp (`10% → 30% → 50% → 100%`) or `company by company` | `_(rolling out company by company)_` |
| a region order (`Production EU first, US after`) | fold into the hedge: `_(rolling out, EU first)_` |
| `currently in beta` / `beta tests with N customers` / `enabled for N customers` | `_(in beta with N customers)_` — **never imply general availability** |
| a plan or add-on gate (`Advanced or Enterprise plan`, `add-on`) | name it: `_(Advanced/Enterprise plan)_` — commercial teams need this |
| an audience restriction (`site managers only, desktop only`) | name it when it materially narrows who benefits |

Combine at most **two** hedges on one line; if a change needs more caveats than that, it is not ready
for a company-wide digest — say the least and let the link carry the rest.

Same for the one-liner's own wording: if it says the release is **partial**, the digest says so.
**A hedge in the body must survive into the digest line.** This is the single most damaging thing
to lose — CS reads these posts and promises things to customers.

## Video links

- **Public** links (`loom.com`, `tella.tv`, `wistia.com`, `drive.google.com`) → append
  ` · [demo →]({url})` to the line. These are high value in a digest.
- **`file://` attachment videos** do not resolve outside Notion → ignore them silently.
- When a body offers several (an EN and a FR walkthrough, a training recording), link **one** — prefer English, prefer the short demo over a long training session.

## Hard rules

- **Never invent.** Every claim in a digest line must be traceable to that page's body (or, in
  fallback, its `Slack summary`). No capability, number, customer, market or benefit that is not there.
- **Never paste raw body text.** Bodies are written for readers who already clicked. A digest
  line is one plain sentence at value altitude.
- **Never list `How it works` bullets** in a digest.
- **Translate** a non-English body into English (house language) and flag the translation in the run log.
- **Do not upgrade** scope: *some customers* does not become *customers*, *phase 1* does not become *done*.
- If the body and the `Slack summary` **disagree**, trust the body and flag the divergence in the run log.
- **Never state or imply general availability** for a change whose body shows any flag, beta, ramp or plan gate. This is the failure mode with real cost: CS and Sales read these digests and promise things to customers.

---

# Building the link to a Changelog entry

**Do not link the raw url from the SQL `url` column** (`https://app.notion.com/{id}`) or the
`notion-fetch` url (`.../p/{id}?pvs=204`). Build the full workspace link instead:

```
https://app.notion.com/p/dashdoc/{Title-Slug}-{id32}?v=0a148f9c71eb4e5f86a49a8a2af2422e
```

| Part | Where it comes from |
|---|---|
| `dashdoc` | the workspace segment — always literal |
| `{Title-Slug}` | the row's `Name`, slugified (below) |
| `{id32}` | the 32-character **dashless** page id — exactly what the SQL `url` column already ends with |
| `?v=…` | the Changelog DB's **List view** id (`view://0a148f9c-71eb-4e5f-86a4-9a8a2af2422e`, dashes removed) — opens the entry in the context of the database |

Drop `&source=copy_link` — it is Notion's copy-button tracking parameter and is not needed.

## Slugifying the title

1. Strip accents (NFKD, drop combining marks).
2. Replace every run of non-alphanumeric characters with a single `-`.
3. Collapse repeated `-` and trim from both ends.

```python
import re, unicodedata
def slug(title):
    t = unicodedata.normalize("NFKD", title)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^A-Za-z0-9]+", "-", t)
    return re.sub(r"-{2,}", "-", t).strip("-")
```

Verified against a known-good copied link:

```
E-invoicing France — Reception (Pennylane account creation + purchase invoice sync)
→ E-invoicing-France-Reception-Pennylane-account-creation-purchase-invoice-sync
```

Em dashes, parentheses, `+`, `/` and `:` all collapse to a hyphen and then disappear into the
neighbouring separator.

> **Why this matters:** on the first weekly digest (W37, 14/09) the post initially went out with
> the bare `https://app.notion.com/{id}` urls taken straight from the SQL column. Readers could not
> open them — Benoit Joncquez and Gontran Filandre reported it within three minutes, with four 👍.
> Rebuilding the links in the full workspace form fixed it. **Never ship the bare-id form.**

> **The slug is cosmetic — Notion resolves on the id.** A slug that differs slightly from what
> Notion itself would generate still opens the right page, so never block a digest on getting a
> title exactly right. The id is the part that must be correct.
