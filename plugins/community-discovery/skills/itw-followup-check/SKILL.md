---
name: itw-followup-check
description: Watch the Community interview outreach — new bookings of the "Disco Community" slot, declines and cancellations, replies to the outreach email, and companies due a single reminder (3–4 days, no booking, no reply). Fully non-interactive, safe to run as a routine; reports and appends actionable lines to the inbox file, writes nothing external. Use when the PM says "who booked", "any interview booked", "who needs a reminder", "check the outreach", "itw-followup-check", or as a daily scheduled run.
---

# itw-followup-check — Who booked, who declined, who needs a nudge

Step 3 of the Community interview workflow. **Non-interactive** (it may run unattended): never ask questions, never send, never create Notion pages or Gmail drafts. It reads, reports, and writes only to the PM's inbox file if one exists (`inbox.md`, format `* [ ] item`); otherwise the report is the only output.

No state file: derive everything from Gmail + the target-list sheet each run (see `itw-target-list` to find it), so nothing goes stale.

---

## Step 1 — Read the outreach

1. Sheet rows with a `First email shoot` value (company, id, contact email, send date `d/m`, sender). Only the PM's rows are in scope unless told otherwise; colleagues' rows are theirs.
2. Gmail `in:sent subject:"recherche de fret et de sous-traitants"` since the earliest send date → recipients and dates (the source of truth for "sent", the sheet may lag).

## Step 2 — Classify each contacted company

For each recipient, in this order:

| State | How to detect |
|---|---|
| **Booked** | booking mail `Rendez-vous réservé: Disco Community (<Name>)` (or `Accepté`) naming the company or the contact's domain |
| **Declined / cancelled** | `Refusé : Disco Community`, `Annulé`, or a reply cancelling — check the thread for a reschedule already offered |
| **Replied** | any inbound message in the outreach thread or from the contact's domain since the send date (read the thread: don't surface one the PM already answered) |
| **Done** | an Interview-DB page exists for them with Progress "Itw done/processed" (Notion search by company) |
| **Waiting** | none of the above |

Match by sender domain AND company name — a booking can come from a personal Gmail (note the booking email vs the company email). Never match on name alone.

## Step 3 — Reminders due

A company is **due** when: state = Waiting, first email sent **3 to 4 or more days ago** (business days preferred: don't count weekends as silence), no second email yet (`Second email shoot` empty and no second sent mail), contact is not a generic mailbox flagged in the sheet. **One reminder per company, ever** — never a third email. Not too pushy: skip a company if the contact opened a conversation any other way.

## Step 4 — Output

Report, skimmable:
- **New bookings** (company, contact, slot, interviewers from the booking attendees) → each with the next step `itw-company-brief` + `itw-page-prep`, and the deadline (prep the day before).
- **Declined / cancelled** (company, when, reschedule offered or not).
- **Replies to read** (company, one line).
- **Due for a reminder** (company, send date, contact) with the proposed one-liner — the drafts themselves are created interactively by `itw-outreach-drafts`.
- Counts: contacted, booked, declined, waiting, done.

- **HubSpot notes missing** — for each booked or done interview with an Interview-DB page, search NOTE in HubSpot (read-only, per [hubspot-interview-note](../shared-references/hubspot-interview-note.md)) for the Notion page id. List the companies with no note. Never create one from this skill.

Append to the inbox file (one `* [ ] …` per item, no duplicates: grep first): a prep item per new booking (`Prep itw <company> (<date> <time>)`), a reply item per unanswered reply, one grouped item `Send reminders: <companies>` when some are due, and one grouped item `HubSpot notes missing: <companies>` (next step: `itw-page-prep` Step 7 or `itw-process` Step 6).

## Scheduling

Intended as a daily routine (morning, weekdays). Create it only when the PM asks, with the scheduled-tasks / `/schedule` mechanism, with this skill as the prompt; the run must stay read-only apart from the inbox file.
