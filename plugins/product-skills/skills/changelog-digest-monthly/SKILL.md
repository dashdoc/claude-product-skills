---
name: changelog-digest-monthly
description: Post the monthly product digest to #team-product for review before a PM pushes it to #general — pulls the previous calendar month's 🌟 High + 🙌 Medium rows from the 🛎️ Changelog Notion database, merges related changes into themed value statements (keeping every source link), and splits by Product Line. Deliberately repeats what the weekly digests already said. Use whenever Fabien says "monthly changelog digest", "what shipped last month", "monthly recap", "the monthly digest", "run the monthly digest", or any equivalent request about the month's product roundup. For the weekly version see changelog-digest; for a single release note see release-changelog.
---

# /changelog-digest-monthly — Monthly Product Digest

One post a month telling the whole company what the product gained. Built from the 🛎️ Changelog database, **reviewed in `#team-product`, then pushed to `#general` by a human**.

> Implements the `#general` row of the [Changelog overload PDR](https://app.notion.com/p/3996d66c0b4a8105ae93e6213d6ed0dc) (Status: **Accepted**, owner: Fabien).
>
> | Channel | Content | Cadence | Source |
> |---|---|---|---|
> | `#changelog-hose` | all entries incl. 🔍 Low | real-time | native automation |
> | `#changelog` | 🙌 Medium + 🌟 High by domain | weekly | [changelog-digest](../changelog-digest/SKILL.md) |
> | **`#general`** | **the month's product story, split by Product Line** | **monthly** | **this skill → `#team-product` → PM pushes** |
>
> **Deviation from the PDR, decided by Fabien 14/09/2026:** the PDR line says *🌟 High only*. High runs **1–2 rows a month** (Sep 1, Aug 2, Jul 1) — a two-line post is not a digest and leaves nothing to merge. The monthly therefore covers **🌟 High + 🙌 Medium**. 🔍 Low stays out; it is the `#changelog-hose` tier.

## Usage

```
changelog-digest-monthly                # previous calendar month, post to #team-product
changelog-digest-monthly --draft        # save a Slack draft in #team-product instead
changelog-digest-monthly --dry-run      # compose + show, write nothing
changelog-digest-monthly --month 2026-08
changelog-digest-monthly --range 2026-07:2026-08   # several months as ONE digest
```

Scheduled runs are **non-interactive**. Never pause to ask — apply the fallbacks and record anything ambiguous in the run log.

---

## Repetition is the point

**This digest deliberately repeats what the weekly digests already said.** Its readers are people who do not follow `#changelog`, or who read an item three weeks ago and have forgotten it. The PDR states the tiers cascade intentionally.

Consequences — all deliberate:
- **Do not suppress a row because the weekly already announced it.** The weekly's ledger is not consulted.
- This skill keeps its **own** ledger (`logs/changelog-digest-monthly.md`), used only to avoid posting the same month twice.
- A row can legitimately appear in a weekly and a monthly, e.g. *Routing Plan Phase 3*.

---

## Constants

- **Source DB**: `🛎️ Changelog` — `https://app.notion.com/p/17e6d66c0b4a804ca659eb53a60266a0`
- **Data source**: `collection://4fc841cd-c4b5-4677-a76b-8469048890e7`
- **Sub-Domains data source**: `collection://b0357249-a0b8-42e7-a311-5e47658adfaf` (carries the `Product Line` select)
- **Target channel**: `#team-product` — `CUF1QEMC4` (verified 2026-09-14)
- **`#general`**: reached **only** by a PM copying the reviewed post. This skill never posts there, and never looks up its channel id.
- **Run ledger**: `logs/changelog-digest-monthly.md`
- **Timezone**: Europe/Paris

---

## Step 1 — Window

**Check today's real date first.** Default window: the **previous calendar month**, 1st 00:00 → last day 23:59 Europe/Paris. `--month YYYY-MM` overrides.

`--range YYYY-MM:YYYY-MM` covers **several months as one digest** — first day of the first month to last day of the last. Use it to catch up a skipped month, or to cover a quiet stretch in one post. Everything else is unchanged: same grouping, merging and volume guard, and the title names the span (`July & August 2026`). Ledger a range under its own heading listing every month it consumed, so a later per-month run does not repeat it.

Read the run ledger. If this month is already recorded as posted, stop.

---

## Step 2 — Pull the rows

```sql
SELECT "Name", "Type", "Communication Priority", "Slack summary",
       date("Created") AS created,
       "date:Date of first activation:start" AS activation,
       "🧩 Domains" AS domains, url
FROM "collection://4fc841cd-c4b5-4677-a76b-8469048890e7"
WHERE date("Created") >= date('{month_start}')
  AND date("Created") <= date('{month_end}')
ORDER BY created
```

Window on **`Created`**, same as the weekly — consistency matters more than either field being perfect, and it guarantees every row lands in exactly one monthly.

Keep `🌟 High` and `🙌 Medium`. Drop `🔍 Low`. A row with **no Communication Priority** is dropped and flagged — it is unroutable and invisible to every channel. A row with **no activation date** is dropped and flagged — not released.

---

## Step 3 — Resolve Product Line

`Product Line` is a rollup on the Changelog row and **cannot be selected in SQL**. Resolve it through the `🧩 Domains` relation:

```sql
SELECT url, "🧩 Sub-Domain", "Product Line"
FROM "collection://b0357249-a0b8-42e7-a311-5e47658adfaf"
WHERE url IN (…)
```

Group by `Product Line` (`TMS`, `Platform`, `Flow`, `Applications`, …). A multi-domain row goes under its **first** domain's Product Line. A row with no domain goes to `Other`, sorted last, and is flagged.

Order groups by the highest priority they contain (a group holding a 🌟 High leads); among groups that tie, one containing a **`Launch`** leads; then size descending, `Other` last. A Launch is the biggest thing that can happen in a month — it must not sit below a larger pile of Features.

---

## Step 4 — Merge related changes

This is what makes a monthly readable. **Merge rows that tell one story into a single value statement, keeping a link for every row merged.**

Merge when the rows are:
- **Phases of one feature** — *Routing Plan (Phase 2/4): Automated Breaks* + *Phase 3: pre-assign resources* → one sentence about routing plans doing more of the dispatcher's work.
- **One initiative shipped as several rows** — the three *Pallet Networks* rows (ADR compliance, EDI pickup requests, price recovery) → one sentence about pallet-network support maturing.
- **The same capability from different angles** — several permissions/roles changes → one sentence about finer access control.

**Do not merge** unrelated changes just to shorten the post, and never merge a 🌟 High into a Medium line — a High keeps its own line.

**Do not merge across different `Market` values or different rollout states.** Two invoicing changes — one released early to the USA behind a flag, one flagged for FR/ES/BE — read as one generally-available capability once merged. Keep them apart so each carries its own hedge.

**Every merged row keeps its link.** A merged line carries 2+ links, one per source entry, so a reader can go straight to whichever part concerns them:

```
🙌 Routing plans now do more of the dispatcher's work: breaks and legs are generated
   from your rules, and each leg can carry a pre-assigned resource.
   [Automated Breaks →](url) · [Pre-assign resources →](url)
```

Cap a merged line at **4 links**. Beyond that, split it or name the theme and link the DB view.

**Build every entry url** as `https://app.notion.com/p/dashdoc/{Title-Slug}-{id32}?v=0a148f9c71eb4e5f86a49a8a2af2422e` — see [changelog-entry-reading](../shared-references/changelog-entry-reading.md#building-the-link-to-a-changelog-entry). Never link the bare `https://app.notion.com/{id}` from the SQL `url` column.

---

## Step 5 — Compose

**Standard markdown** (the Slack connector's send/draft tools take `**bold**`, `_italic_`, `[text](url)` — *not* Slack mrkdwn `<url|text>`). English. One message, no thread.

```
🗞️ **Dashdoc product — {August 2026}**
_{8} changes across {TMS, Platform and Flow}. Here's what's new._

**{TMS}**
🌟 {Value sentence for a High — its own line.} [{Short name} →]({url})
🙌 {Merged theme sentence.} [{Short name} →]({url}) · [{Short name} →]({url})

**{Platform}**
🙌 {Value sentence.} [{Short name} →]({url})

_[Browse the full changelog by domain →]({db-url})_
```

### Writing at month altitude

**Read each covered row's page body** — see [changelog-entry-reading](../shared-references/changelog-entry-reading.md). `notion-fetch` the row url and derive from the body's core-value one-liner; `Slack summary` is a fallback only. At monthly volume this is 8–25 fetches, so fetch **after** filtering, never before.

Merging makes faithfulness harder, not easier: a merged line must be true of **every** row it covers.

| Allowed | Not allowed |
|---|---|
| Turn each body's one-liner into `You can now…` / the concrete actor | Adding any capability, number, customer, scope or benefit not on the pages |
| Combine two bodies into one theme sentence that says what **both** deliver | Writing a theme sentence whose claim is broader than the rows support |
| Rewrite a `📖 User Story` as plain prose; convert first-person body text | Pasting *"As a X, I want to Y"* or listing `⚙️ How it works` bullets |
| Lift to outcome level — *what the month changed for a user* rather than per-row mechanics | Dropping a hedge: *partial*, *beta*, *rolling out* all survive merging |
| Append ` _(rolling out)_` / ` _(in beta)_` from a body's FF callout | Letting a merged line hide that one of its rows is still gated |
| Append ` · [demo →](url)` for a **public** video link | Linking a `file://` attachment video |
| Translate a non-English body into English — flag it in the run log | Inventing a sentence for a row with no usable body |

Hedges are the thing merging most easily destroys. **If any merged row is partial, gated behind a feature flag, or in beta, the merged line says so** — a merged line inherits the weakest rollout state of its parts, never the strongest. If two rows differ too much in maturity to share one honest sentence, don't merge them.

**Fallback** — a row with no usable body and no `Slack summary`: `{Name} — _no summary yet_ [details →]({url})`, flagged. Never invent one from the title.

### Other rules

- **One sentence per line**, merged or not. This is a skim surface.
- **Age annotation**: if `Date of first activation` predates the month, append ` _(live since {Mon YYYY})_`. On a merged line, annotate only if **all** merged rows predate it.
- 🌟 High lines first within a Product Line, then merged Medium lines, then single Mediums.
- No @channel, no @here.
- Close with the DB link.

---

## Step 6 — Abort rules

- **No High and no Medium rows → do not post.** Log the skip.
- **More than 25 rows** → a bulk migration, not a month. Announce the 🌟 High rows, collapse the rest to a themed count with a DB link, flag the batch.
- Never post two digests for the same month.

---

## Step 7 — Post to `#team-product`

- `--dry-run`: print and stop.
- `--draft`: `slack_send_message_draft` to `CUF1QEMC4`. Only one attached draft per channel — on `draft_already_exists`, report it rather than overwriting.
- Default: `slack_send_message` to `CUF1QEMC4`.

Then post **one** short follow-up line in the same channel so the handoff is explicit:

> `Monthly digest for {Month} — review and push to #general when you're happy with it.`

**Never post to `#general`.** The PDR routes this through human review on purpose: a PM reads it, edits if needed, and copies it across.

---

## Step 8 — Log the run

Append to `logs/changelog-digest-monthly.md`:

```markdown
## {YYYY-MM} — run {YYYY-MM-DD HH:MM}
- Status: posted to #team-product | drafted | skipped ({reason}) | aborted ({reason})
- Permalink: {slack permalink}
- Pushed to #general: ☐ (by whom, when — filled in later)
- Covered ({n}): {url} {Name} [{priority}] · …
- Merged lines: {theme} ← {Name} + {Name} · …
- Excluded — Low ({n}) · no priority ({n}) · no activation date ({n})
- ⚠️ Empty body (fell back to Slack summary) · body/summary divergence · translated from {lang}: …
```

If any ⚠️ is non-empty, add one `inbox.md` item — an unqualified row is invisible to every channel.

---

## Scheduling

Scheduled task `changelog-digest-monthly`, **1st of each month, 09:00 Europe/Paris**. Posts to `#team-product`; the push to `#general` stays human.
