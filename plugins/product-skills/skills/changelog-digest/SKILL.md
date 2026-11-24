---
name: changelog-digest
description: Post the weekly product digest to #changelog — pulls the previous week's rows from the 🛎️ Changelog Notion database, keeps 🙌 Medium + 🌟 High, groups them by domain, annotates entitlement-gated features with the plans they're included in, and posts one Slack message. Excludes 🔍 Low (that's the real-time #changelog-hose feed). Runs as a Monday-morning routine and on demand. Use whenever Fabien says "weekly changelog digest", "what shipped last week", "post the changelog recap", "weekly digest in #changelog", "run the changelog digest", or any equivalent request about the weekly roundup of shipped changes. Not for writing a single release note — that's release-changelog.
---

# /changelog-digest — Weekly #changelog Digest

Post **one** Slack message per week summarising what shipped, built from the qualified rows in the 🛎️ Changelog database.

> Implements the `#changelog` row of the distribution table in the [Changelog overload PDR](https://app.notion.com/p/3996d66c0b4a8105ae93e6213d6ed0dc) (Status: **Accepted**, owner: Fabien). The PDR defines three cascading channels — a High item appears in all three, **intentionally**:
>
> | Channel | Content | Cadence | Source |
> |---|---|---|---|
> | `#changelog-hose` | all entries **incl. 🔍 Low** | real-time | native Notion→Slack automation |
> | **`#changelog`** | **🙌 Medium + 🌟 High, grouped by domain** | **weekly** | **scheduled agent ← this skill** |
> | `#general` | 🌟 High only, split by Product Line | monthly | scheduled agent → `#team-product` → PM pushes |
>
> This skill is the PDR's fallback "custom agent" for the weekly digest, and it names an owner for it. Counterpart: [release-changelog](../release-changelog/SKILL.md) creates the rows; this skill only reads them.

## Usage

```
changelog-digest                  # previous ISO week, compose + post
changelog-digest --dry-run        # compose + show, post nothing
changelog-digest --draft          # compose + save a Slack draft in #changelog, don't send
changelog-digest --week 2026-W37  # a specific ISO week instead of the previous one
```

**Runtime mode**: scheduled runs are **non-interactive and auto-post**. Never pause to ask — apply the fallbacks below and record anything ambiguous in the run log.

---

## Prerequisites

| Connector | Needed for | If unavailable |
|---|---|---|
| **Notion** | reading the Changelog DB | abort — write the reason to the run log, post nothing |
| **Slack** | posting to `#changelog` | abort — keep the composed draft in the run log so nothing is lost |

---

## Constants

- **Source DB**: `🛎️ Changelog (aka Product release notes)` — `https://app.notion.com/p/17e6d66c0b4a804ca659eb53a60266a0`
- **Data source**: `collection://4fc841cd-c4b5-4677-a76b-8469048890e7`
- **Sub-Domains data source**: `collection://b0357249-a0b8-42e7-a311-5e47658adfaf`
- **Entitlements tracker data source**: `collection://444c2190-11f3-4b35-b775-95dc00c135b2` — resolves `🔏 Gated by entitlement` to plan names
- **Target channel**: `#changelog` — `CANPU267R` (verified 2026-09-14)
- **Real-time firehose** (not this skill): `#changelog-hose` — `C0C0GNM1TRC`, plugged to the Changelog DB since 2026-09-09
- **First run**: seed the ledger with every row created before the first window, or the volume guard fires on the whole DB history (41 rows as of 2026-09-14, incl. 26 legacy `Cycle NN – Release note` pages).
- **Run ledger**: `logs/changelog-digest.md`
- **Timezone**: Europe/Paris

**Live schema facts** (verified against the data source — do not assume otherwise):
- `Type` has exactly three options: `Launch` / `Feature` / `Quickwin`. **There is no `Fix` option.**
- `Communication Priority` is a **select** and is **nullable** — unqualified rows exist in the wild.
- `Market` options: `🏭 Shippers` / `🇧🇪 Carrier Belgium` / `🇺🇸 Carrier USA` / `🇪🇸 Carrier Spain` / `🇫🇷 Carrier France` / `All`.
- `Product Line` is a **rollup** and is listed in `notAvailableInQuerySql` — it cannot be selected in SQL. Resolve it through the `🧩 Domains` relation instead.
- `🔏 Gated by entitlement` is a **relation** to the Entitlements tracker (0 or more rows — most rows have none, meaning the feature is available to everyone). There is no "Inc. in Plans" rollup column on the Changelog DB itself — resolve plans by following the relation into the Entitlements tracker's `included per Plan?` multi-select (options: `Essential` / `Advanced` / `Expert` / `Shipper` / `License self-operating` / `License sub-contracting` / `Flow +` / `Crossdock` / `Add-on` / `Legacy Add-on` / `TBD`).

---

## Step 1 — Resolve the window

**Check today's real date first** (never inherit it from earlier in the session).

- Default: the **previous ISO week**, Monday 00:00 → Sunday 23:59 Europe/Paris.
- `--week YYYY-Www` overrides it.

Read the **run ledger** (`logs/changelog-digest.md`) for the page urls already sent in a past digest.

---

## Step 2 — Pull the candidate rows

```sql
SELECT "Name", "Type", "Communication Priority", "Slack summary",
       date("Created") AS created,
       "date:Date of first activation:start" AS activation,
       "🧩 Domains" AS domains,
       "🔏 Gated by entitlement" AS entitlement, url
FROM "collection://4fc841cd-c4b5-4677-a76b-8469048890e7"
WHERE date("Created") <= date('{window_end}')
ORDER BY created DESC
```

**Selection rule — `Created` window, ledger-driven catch-up.** Include a row when **both**:
1. its `Created` timestamp is **on or before the window end**, and
2. its `url` is **not** in the run ledger.

`Created` is the routing field: **the digest announces what was written up last week**, not what went live last week. A row appearing in the DB *is* the announcement moment — that is what guarantees nothing documented ever goes unannounced.

> ⚠️ `Created` and `Date of first activation` diverge by **months**, in both directions. Rows created 9–14 Sep 2026 carry activation dates of 26 Feb, 6 Mar, 26 Jun, 21 Jul, 24 Jul and 28 Aug 2026; rows are also written up days *before* they go live. This is deliberate (see the enablement annotation in Step 6) — **never** silently present an old activation as this week's work, never present a future one as already live, and never swap this filter to `Date of first activation` without Fabien saying so.

Rows created **before** the window that are still not in the ledger are picked up too — that is the catch-up, and it covers a skipped or failed run.

**Volume guard.** If the selection holds **more than 20 rows**, this is a bulk migration (the PDR's "migrate historical cycle pages → DB rows"), not a week of work. Announce the 🌟 High rows in full, collapse the rest to a single line (`_N further changes were documented this week — <db-url|browse them>_`), still record **every** url in the ledger so they are never re-proposed, and flag the batch in the run log.

**`Date of first activation` does not gate inclusion.** Whatever it holds — past, inside the window, in the future, or empty — the row is announced. Dashdockers want to hear about an incoming feature *before* it lands, not weeks after. The date's only job is to set the **enablement annotation** in Step 6, which states on every line whether the change is enabled for everyone yet.

| Activation date | Announced? | Ledger |
|---|---|---|
| in the past or inside the window | yes | `Announced` — never proposed again |
| **in the future** | yes, as an incoming feature | `Announced` — never proposed again |
| **empty** | yes, as an incoming feature with no date | **`Pre-announced`** — see below |

A row announced with **no activation date** goes to the ledger's `Pre-announced` section instead of `Announced`. It becomes a candidate **once, again**, as soon as a date is filled in — so the actual go-live is announced too. On that second pass it is written to `Announced` and is done. A row therefore appears at most twice: once as "coming", once as "live". Never announce an undated row a third time, and never re-announce a row that already carries a date.

> **Why the second pass.** Pre-announcing an undated row is the only pressure on the PM to date it, and without the follow-up a feature announced as "not enabled yet" would never get its go-live post. Keep the second line short — it is a status change, not a new feature.

---

## Step 3 — Resolve domains and entitlement gating

`🧩 Domains` is a JSON array of page urls into the Sub-Domains data source. Query it for the names:

```sql
SELECT url, "🧩 Sub-Domain", "Product Line"
FROM "collection://b0357249-a0b8-42e7-a311-5e47658adfaf"
WHERE url IN (…)
```

`🧩 Sub-Domain` reads `Domain > Sub-domain`, e.g. `TMS – Subcontracting > Chartering/Subcontracting`.
**Group by the part before ` > `** (`TMS – Subcontracting`) — that is the PDR's "grouped by domain".

A row with several domains is filed under its **first** domain only — never duplicated across groups. A row with no domain goes to an `Uncategorised` group, sorted last, and is flagged in the run log.

**Entitlement gating.** For every announced row whose `entitlement` array (from Step 2) is non-empty, resolve it into plan names:

```sql
SELECT url, "Feature", "included per Plan?", "Status"
FROM "collection://444c2190-11f3-4b35-b775-95dc00c135b2"
WHERE url IN (…)
```

Build a `{row_url → plan list}` map from `included per Plan?`. Most rows have an empty `entitlement` array — that means the feature is available to everyone; skip the annotation entirely for those, don't write "All plans". If `included per Plan?` is itself empty on a matched entitlement row, treat it like "not resolved" and flag it in the run log rather than guessing a plan.

---

## Step 4 — Partition by Communication Priority

| Priority | Treatment |
|---|---|
| `🌟 High (now to all Dashdockers)` | in the digest, prefixed 🌟 |
| `🙌 Medium (weekly to all)` | in the digest, prefixed 🙌 |
| `🔍 Low (need to know basis)` | **excluded** — Low is the real-time `#changelog-hose` feed, not this one |
| *(empty)* | **excluded — it cannot be routed.** Flag it in the run log and in `inbox.md` |

Within a domain group, sort 🌟 High before 🙌 Medium, then `Launch` → `Feature` → `Quickwin`.

---

## Step 5 — Abort rules (before composing)

- **No High and no Medium rows → do not post.** Log `skipped: nothing to announce`. An empty digest is noise in the channel the PDR exists to de-noise.
- Never post two digests for the same window — if the ledger already holds this window with the same row set, stop.

---

## Step 6 — Compose

**Who this is for.** Dashdockers who cannot keep up with the stream of updates. They need a **quick overview of what changed and the value it brings** — not a list of feature names. Someone should be able to skim the whole post in under a minute and come away knowing what is new. If one item matters to them, they follow the link and read the full entry.

So: **lead each line with the value, in plain language. The link is the way in, not the headline.**

**Standard markdown**, English, one message, no thread. The Slack connector's send/draft tools take standard markdown (`**bold**`, `_italic_`, `[text](url)`) — **not** Slack `mrkdwn` `<url|text>` syntax.

```
📬 *What shipped last week* — {7–13 Sep}
_{5} changes across {Dispatch, Subcontracting, Contacts and Flow}._

**{TMS – Subcontracting}**
🌟 {Value sentence — what someone can now do, and why it helps.} [{Short name} →]({url}) _(rolling out)_ · 🔏 Advanced, Expert

**{Platform – Discuss}**
🙌 {Value sentence.} [{Short name} →]({url}) _(enabled for everyone)_
🙌 {Value sentence, for something not live yet.} [{Short name} →]({url}) _(from 14 Oct — not enabled yet)_

_[Browse the full changelog by domain →]({db-url})_
```

### Writing the value sentence

**Read each announced row's page body** — see [changelog-entry-reading](../shared-references/changelog-entry-reading.md) for how. `notion-fetch` the row url and derive the sentence from the body's core-value one-liner, falling back down the ladder in that reference. **`Slack summary` is a fallback, not the source** — it drops the feature-flag rollout state and the demo link.

Fetch only the rows that survive Step 4's filtering — typically 2–8 a week.

**You may re-voice what the body says. You may not change what it says.**

| Allowed | Not allowed |
|---|---|
| Turn the one-liner or `*Solution*` into `You can now…` / the concrete actor (`Dispatchers can now…`) | Adding any capability, number, customer, scope or benefit not on the page |
| Rewrite a `📖 User Story` as plain prose | Pasting the *"As a X, I want to Y"* form into the digest |
| Convert first-person body text (*"When I'm subcontracting…"*) to second/third person | Listing `⚙️ How it works` bullets — the reader clicks through for mechanics |
| Pull one concrete detail from `How it works` when the one-liner is too vague | Upgrading a hedge — *partial*, *beta*, *company-by-company* all survive |
| Append ` _(rolling out)_` / ` _(in beta)_` from the FF callout | Dropping the FF callout's rollout state |
| Append ` · [demo →](url)` for a **public** video link (loom / tella / wistia / drive) | Linking a `file://` attachment video — it does not resolve |
| Translate a non-English body into English — flag it in the run log | Inventing a sentence for a row whose body and summary are both empty |

If in doubt about a phrase, keep the page's own wording. A slightly clunky true sentence beats a smooth invented one. If the body and the `Slack summary` disagree, **trust the body** and flag it in the run log.

**Fallback** — a row with **no usable body and no `Slack summary`**: emit `{Name} — _no summary yet_ [details →]({url})` and flag it in the run log. Never paraphrase the title into a fake value statement.

### Saying whether it is enabled to all

**Every announced line ends with an enablement annotation.** The reader's first question is always *"can I promise this to a customer today?"*, and silence used to mean "fully live" — which is only legible to whoever wrote the rule. Make it explicit in both directions.

Pick the annotation from the page body first, the activation date second:

| What the row shows | Annotation |
|---|---|
| no flag, no beta, no gate, activation reached | `_(enabled for everyone)_` |
| `under FF X, activated to all today` | `_(enabled for everyone)_` |
| FF with no full-activation wording | `_(rolling out)_` |
| percentage ramp, or `company by company` | `_(rolling out company by company)_` |
| `in beta with N customers` / `enabled for N customers` | `_(in beta with N customers)_` |
| region order (`EU first, US after`) | `_(rolling out, EU first)_` |
| plan or add-on gate named in the body | `_(Advanced/Enterprise plan)_` |
| audience restriction (`site managers only`, `app version 3.68.0`) | name it — `_(site managers only)_`, `_(app version 3.68.0)_` |
| **activation date in the future** | `_(from {D Mon} — not enabled yet)_` |
| **no activation date** | `_(not enabled yet — no date set)_` |
| activation predates the window start | `_(live since {Mon YYYY})_`, or the rollout state if it is still gated |

Rules on top of the table:

- **A rollout hedge always beats a date.** A row whose activation is past but which still sits behind a flag reads `_(rolling out)_`, never `_(enabled for everyone)_`. When both a date fact and a rollout fact apply, the rollout fact wins the slot.
- **Still at most two** parenthetical hedges on a line, as in [changelog-entry-reading](../shared-references/changelog-entry-reading.md). The enablement annotation is one of the two.
- **`_(enabled for everyone)_` is a claim, not a default.** Write it only when the body actually shows a complete, unflagged, ungated release. If the body is silent on rollout and you cannot tell, write `_(rolling out)_` and flag the row in the run log — understating is cheap, overstating costs a broken customer promise.
- **An incoming feature is announced as incoming.** Never let a future or missing activation date read as shipped: the value sentence stays in the present (`Dispatchers can restrict…`), and the annotation carries the "not yet" — that is the whole point of pre-announcing.
- **The second pass on a pre-announced row** (Step 2) is one short line under its domain: the same short name and link, the value sentence trimmed to a clause, and the new enablement annotation — e.g. `🙌 Now live: carriers can bill by pallet equivalence. [Pallet equivalence (EPS) →](url) _(enabled for everyone)_`. Lead it with `Now live:` so the repeat is obviously a status change.

### Other rules

- **One sentence per change.** If a summary runs long, cut it down — this is a skim surface, not the entry itself.
- **Link text is the short feature name** plus ` →`, so the value carries the line and the link is the doorway.
- **Build the entry url** as `https://app.notion.com/p/dashdoc/{Title-Slug}-{id32}?v=0a148f9c71eb4e5f86a49a8a2af2422e` — see [changelog-entry-reading](../shared-references/changelog-entry-reading.md#building-the-link-to-a-changelog-entry). Never link the bare `https://app.notion.com/{id}` from the SQL `url` column.
- **Enablement annotation**: every line carries one — see [Saying whether it is enabled to all](#saying-whether-it-is-enabled-to-all) below. No line goes out without it.
- **Entitlement annotation**: when Step 3 resolved a non-empty plan list for the row, append ` · 🔏 {Plan, Plan}` after the link and after the enablement annotation — e.g. `[{Short name} →]({url}) _(rolling out)_ · 🔏 Advanced, Expert`. Use the plan names verbatim from `included per Plan?`. Omit entirely for ungated rows — don't write "🔏 All plans".
- **Sub-header line**: after the title, one line giving the count and the domains touched, so a skimmer knows the shape before reading.
- Group by domain (Step 3). Order the **groups** by the highest priority they contain (a group with a 🌟 High leads), then by size descending. Within a group: 🌟 High first, then `Launch` → `Feature` → `Quickwin`. Drop empty groups.
- No @channel, no @here. No per-row emoji beyond the priority marker.
- Close with the DB link — the PDR wants the posts to lead back to the domain views for history.

---

## Step 7 — Post

- `--dry-run`: print the message and the would-be ledger entry. Write nothing, post nothing. Stop.
- Otherwise: post to `CANPU267R`.

The Slack connector exposes both `slack_send_message` (posts immediately) and `slack_send_message_draft` (saves to Drafts without sending). The scheduled run uses **`slack_send_message`**; a manual run with `--draft` uses **`slack_send_message_draft`**.

> Only **one** attached draft is allowed per channel — `slack_send_message_draft` returns `draft_already_exists` if one is pending. Report that rather than overwriting, and never record "posted" when nothing was posted.

---

## Step 8 — Log the run

Append to `logs/changelog-digest.md`:

```markdown
## {YYYY-Www} — run {YYYY-MM-DD HH:MM}
- Status: posted | skipped ({reason}) | aborted ({reason})
- Permalink: {slack permalink}
- Announced ({n}): {url} {Name} [{priority}] · …
- Pre-announced — not yet enabled ({n}): {url} {Name} [{from {date} | no date set}] · …
- Go-live follow-ups this run ({n}): {url} {Name} [pre-announced {YYYY-Www}, now {state}] · …
- Enablement annotations: enabled for everyone ({n}) · rolling out / beta / gated ({n}) · not enabled yet ({n})
- Annotated as older ({n}): {url} {Name} [live since {activation}] · …
- Entitlement-gated ({n}): {Name} [{Plan, Plan}] · …
- Excluded — Low ({n}) · no priority ({n})
- ⚠️ Empty body (fell back to Slack summary): {Name} · …
- ⚠️ Body/summary divergence · translated from {lang}: {Name} · …
- ⚠️ No Communication Priority: {Name} · …
- ⚠️ Rollout state unreadable, defaulted to "rolling out": {Name} · …
- ⚠️ Entitlement relation set but plan not resolved: {Name} · …
```

The `Announced` urls are what Step 2 reads back as "already sent". The **`Pre-announced`** urls are the undated rows awaiting a go-live pass — Step 2 re-proposes one only once its `Date of first activation` is filled in, and moves it to `Announced` on that second pass.

If any ⚠️ line is non-empty, append one item to `inbox.md` — an unqualified row is invisible to **every** distribution channel, so it must get fixed at the source:

```markdown
- [ ] Changelog DB: {N} row(s) shipped without a Communication Priority / Slack summary — {names} — https://app.notion.com/p/17e6d66c0b4a804ca659eb53a60266a0
```

A row sitting in `Pre-announced` for **more than two runs** also earns an `inbox.md` item — it has been announced to the company as coming and still has no activation date:

```markdown
- [ ] Changelog DB: {N} pre-announced row(s) still without a Date of first activation after {N} weeks — {names} — https://app.notion.com/p/17e6d66c0b4a804ca659eb53a60266a0
```

---

## Scheduling

Scheduled task `changelog-digest`, **Monday 09:00 Europe/Paris** — after the week closes, before the Monday rituals.

## Verified 2026-09-14

`#changelog-hose` (`C0C0GNM1TRC`) exists and is plugged to the Changelog DB, so the real-time
firehose is already split off `#changelog`. The weekly digest does not duplicate it.
