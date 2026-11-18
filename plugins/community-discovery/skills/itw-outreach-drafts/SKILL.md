---
name: itw-outreach-drafts
description: Create the next batch (default 10) of Gmail DRAFTS inviting Community interview targets, from the target-list sheet — template taken from the PM's latest sent email, one per company with first name, language, subject, booking link, HubSpot BCC and signature, flags for generic mailboxes and odd names, no duplicates. Never sends. Use when the PM says "draft the next 10 emails", "outreach batch", "emails for the next companies", "itw-outreach-drafts", "second email to X", or after itw-target-list. Hands back the exact values to put in the sheet's "First email shoot" column once they are sent.
---

# itw-outreach-drafts — Next 10 emails, drafted, never sent

Step 2 of the Community interview workflow. the PM does this about 10 at a time, a bit every day. **Only creates Gmail drafts.** Sending, and the sheet update, stay with the PM.

Sheet: the target-list sheet, tab `loadboard-scoring` (find it as described in `itw-target-list`). Preview files of past batches: `$ITW_OUTPUT_DIR` (default `./itw-notes/`).

---

## Step 1 — Pick the batch

1. Read the sheet (Drive `read_file_content`). **The Drive read returns only a ~16-row sample, so it cannot show the next uncontacted rows**: ask the PM to paste the next rows (company, contact, email, country, flag) unless a CSV export is allowed. Candidates = rows with an empty `First email shoot`, in sheet order (it is sorted by score; pushed-by rows come after). Default batch size 10, or what the PM asks.
2. Skip, and say why: company already contacted by someone else (a colleague's row), no contact email, row flagged by `itw-target-list`.
3. **Duplicate check, always:** Gmail `in:sent` and `list_drafts` for each recipient address and domain. Same address already mailed → skip. A draft already exists → don't create another; offer to update it. Search by **domain**, not only address: a shared domain can hide a long relationship (years of threads with the PM or Dashdoc colleagues) → not a cold email, skip and tell the PM.

## Step 2 — Take the template from the PM's latest sent email

Do NOT reuse a template remembered from an earlier session: the PM reworks it after sending (first draft run matched an old version and 9 drafts had to be regenerated). Search `in:sent subject:"recherche de fret et de sous-traitants"` newest first, read the body, and use it as the base: greeting line, why we write, 30 minutes video, optional screen share of the freight board, booking link, sign-off. Keep that subject as is (at the time of writing: `Dashdoc : recherche de fret et de sous-traitants`).

Consistency checks before creating anything: subject says the same duration as the body; the **booking link** is the one in the latest sent email (it changes between waves — always use the newest one actually sent); no pricing or product promise (carriers paying nothing is a hypothesis now); no data reveal ("we saw you chartered 218 new carriers" feels like surveillance).

## Step 3 — Personalise (light touch)

- **First name** from `champion_first_name`; fix case ("DEBORA" → "Debora"), strip placeholders.
- **Language:** French by default; Spain-based (`ES`) → Spanish or English draft, ask once per batch; Belgium/NL → French or English as the contact's domain suggests.
- **Angle:** carriers/chartering companies → "trouver du fret et des sous-traitants". Shippers (e.g. industrial customers pushed by CS) → "trouver des transporteurs de confiance"; "tu" only when the PM already knows the person.
- **One personalised sentence** for pushed-by rows (e.g. "L'équipe Dashdoc qui vous accompagne m'a suggéré de vous contacter", or a concrete hub / usage fact). Mark it in bold in the preview file so the PM can spot it; remove the bold in the draft.
- **Known contact** (already spoke, Harvestr user): "Nous avons déjà échangé par le passé", and no cold-email framing.
- Fresh customers flagged `onboarding?`: softer opener or hold for a later wave.

## Step 4 — Create the drafts

- Gmail `create_draft`, one per company, **To** = champion email. Add the HubSpot logging BCC address: copy it from the BCC of the latest sent outreach email (it is personal to each sender); if that email has none, ask once. Drafts created without it lose the CRM log (if the tool can't set BCC, say so in the report so it is added by hand).
- Signature: the Gmail signature is attached when the PM sends from Gmail; don't paste a manual one if the body already ends with the sign-off.
- Never `send`. Never touch the PM's existing drafts except to replace one you created in this same session.
- Write a preview file `$ITW_OUTPUT_DIR/outreach-<date>-drafts.md` (company, to, subject, personalised sentence, flags) so the PM can review without opening Gmail.

## Step 5 — Report

Table: company, contact, language, flags, draft link. Then **Flags** to decide on (generic mailbox, placeholder name, ES language, onboarding, existing contact). Then, only after the PM confirms they sent them, give the exact value for the sheet's `First email shoot` column in the sheet's format — `<sender first name> – d/m` (e.g. `Anna – 12/11`) — as a paste-ready column in sheet order; offer to write it only if the PM asks.

## Second emails

`itw-followup-check` lists who is due (3–4 days, no booking, no reply, not declined). Create at most **one** reminder per company, softer and shorter than the first, reply in the same thread; never a third email. Sheet column: `Second email shoot`.
