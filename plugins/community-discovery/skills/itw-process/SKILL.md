---
name: itw-process
description: Process a Community discovery interview after the call — merge the available recordings into ONE clean transcript, fix the Notion interview page (one transcript, glossary-corrected summaries, hypothesis debrief, Progress, links), then extract JTBD insights, dedupe them against Harvestr, post and link them to the level-2 discoveries. Use whenever the PM says "process the interview", "itw-process", "clean this interview", "I have a recording to process", "debrief the interview", or gives an interview page URL plus audio files / transcripts after a Community call. Every write to Notion, Harvestr or Linear is shown first and confirmed.
---

# itw-process — From recording to Harvestr insights

Post-call pipeline for a Community interview. Output files go to `$ITW_OUTPUT_DIR` (default `./itw-notes/`). Sibling skills (before the call): `itw-company-brief`, `itw-page-prep` (if the page was not prepared, work with what is there).

**Input to collect (ask once, in one message, only what is missing):**
- Notion interview page URL
- Audio files and/or transcripts: own recording, colleague recording (a co-interviewer), Gemini doc, Notion AI Meeting Notes already on the page
- Who attended and who is the interviewee (name, role, company)

**Gates:** nothing is written to Notion, Harvestr or Linear before the PM has seen it. Posting to Harvestr sends the PM's email to the Dashdoc n8n webhook as submitter. Some sessions carry a privacy rule that blocks sending the PM's email to an external service unless they explicitly ask for it, and a blocked write wastes a round trip — so at the draft-approval step (Step 5.2) ask in the same message: "Approve posting? This sends your email to the Dashdoc n8n webhook as submitter." Their yes is the explicit approval; quote it if a block still triggers. Never put the PM's email in a file you write to disk before that yes. Dashdoc-facing text is English; verbatims stay in the original language.

---

## Step 1 — Audit the page and the sources

0. The notes can live **outside the Interview DB** (e.g. an interviewer's private notes page that also carries the audio) and the target page can be blank or hold only an image — read the page the PM names, plus any private notes they link, and keep existing blocks (don't delete the image). Set `Interviewer` / `Attendees` to the people who really interviewed; don't guess user ids — read them from a sibling interview page or `notion-get-users`.

1. Fetch the Notion page. List: blocks present, number of transcripts (target: one), AI summaries, debrief state, Progress / Cycle / Date properties, links (Moderation, Planhat), comments (don't orphan them — check before replacing text).
2. For each audio: measure the level profile (mean level, share of flat noise floor). The cause of a bad capture is usually **Notion in a Chrome tab = mic only** — only the desktop app with Screen & System Audio Recording permission captures the other side. Report which recording captured whom; don't boost a file that never captured the interviewee.
3. Pick the **base** source. Preference order: **(a) the Notion AI Meeting Notes transcript** — rely on it as much as possible — if it passes the quality check below; **(b) a Gemini/Drive transcript** (full call, speakers labelled) if (a) is bad; **(c) audio + Whisper** only if neither covers the interviewee. Others fill gaps (own questions, last minutes, speaker labels) and cross-check. Don't download big recordings (a 260 MB file) when a labelled transcript already covers the whole call.
4. **Quality check of the Notion AI block** (it has failed before, so judge, don't assume): covers the whole call start to end, both sides present (not mic only), speakers plausible, language right, no big truncation or hallucinated "Merci" runs. Verdict **clean** → keep the block as the transcript, do NOT delete or move it. Verdict **bad** → replace it (see Step 3) and say why in one line.
5. **No audio / non-French interview** (e.g. Spanish): if only notes exist, quotes are **reconstructed** — keep the original language, mark them as reconstructed in the transcript file, the page and every Harvestr message, and add a "Reconstructed quotes" line to the To-verify list.

## Step 2 — Merge into ONE transcript

- Transcribe locally with faster-whisper — see **Whisper setup** below. Run long jobs in the background; give a `--prompt` with the domain terms and gate hallucinated "Merci" lines.
- Whisper has no speakers: label by reading the dialogue, cross-check with Gemini/Notion AI labels.
- Apply the glossary: Trans.eu (not Transus/TransEU), Gayssot (not Gassot/Gacoin), Teleroute, B2PWeb, GEDTrans (not "JetTrans"; B2PWeb and GEDTrans are both products of the H2P company), DREAL, Quartix (geolocation) — extend it as new errors appear.
- Clean fillers and false starts, mark uncertain words `[?]`.
- Write the draft to `$ITW_OUTPUT_DIR/itw-<slug>-transcript.md` with a **"To verify"** list at the bottom (tool names, figures, dates, anything guessed). Show it before touching Notion.

## Step 3 — Fix the Notion page (after approval)

- One transcript only. **If the Notion AI block is clean, leave it in place** (fix glossary errors only if the PM agrees; put the cleaned/merged version in a toggle only when it adds something). **Only when its content is bad**, replace it with two toggles at the bottom (cleaned transcript + the AI summary with errors fixed) — default, don't ask again; say it in one line. A Spanish/duplicate transcript inside a bad block goes with it. Remove other duplicate recording blocks (delete nothing without saying so).
- Correct the errors found in the auto-summaries (e.g. "Teleroute **and** Trans.eu verify documents" → check against the transcript; 3k€ vs 33k€ caps).
- Fill the **debrief against the Harvestr discoveries of the Community component** (level-2 discoveries are the source of truth; there is no hypothesis database any more — decided 13 Nov 2026). One table, grey title rows ("Linked to a Community discovery", "No Community discovery yet", "New, not tied to a discovery"), columns Discovery | Direction (＋/－/±/∅) | Evidence (French verbatim + [mm:ss]). ∅ for anything only said by the interviewers; flag interviewer-led pitches. Direction rule: ＋ when the need exists, even if she meets it today through experience, a workaround or a tool (e.g. price known after 20 years = ＋, not －); － only when she denies the need, refuses the idea or says the opposite. Fetch the live discovery list from Harvestr, don't reuse ids from old drafts.
- Add what is **not in any discovery** (new needs, surprises) as rows under "New, not tied to a discovery" — keep one-off new needs by default, don't ask — and counter-signals.
- **Cross-check the claims against the account data** in the page's key-numbers table (e.g. stated 75% chartered vs actual 46%; one-shot subcontractors vs "stable network"). Record contradictions in a named row **"Surprises and contradictions"** (claim | account data).
- Properties: Progress → "Itw processed", Date. The `🧩 Sous-domaines` relation pointing to "Applications > Community" is enough — no Cycle/Discovery option needed. No hypothesis pages to link.
- Add the interviewee's **seniority/expertise** to the Context block (e.g. "20+ years, masters her job"): it changes how to read every answer.
- Single table rule: no multiple tables on the page.
- Re-fetch after editing to verify. Never start a line with `#` (Notion turns it into a heading).
- Follow-ups with an owner (e.g. an example document the interviewee promised, a referral to email) → the user's task file if there is one (e.g. `tasks.md` in the working directory), otherwise the report only. Always propose them — or state "no follow-ups" — never skip silently.

## Step 4 — Extract insights

Use the `/discovery-insights` format: **When / I want to / So I can**, a Context paragraph, Verbatims (original language, `(…)` for cuts, `[ ]` for clarifications), no priority line unless the interviewee stated one. Title in English.

- Split by distinct need. **Treat demos and workarounds as sources too** (how the interviewee uses a tool every day shows what they hire it for) — this was missed on the first pass and cost a second wave.
- Flag weak ones in the message itself with a standard line `Fit: weak | inferred | demo-only | interviewer-led` + why: reformulated by the interviewer then confirmed, praised-not-requested, ambiguous source, solved outside Dashdoc.
- Requester = the real speaker. If the notes don't attribute a quote, ask — never default to a teammate.
- Target discovery = **level-2 opportunity** only (the "so I can…" name). Level-1 are FigJam umbrellas, not Harvestr discoveries.
- Out of scope for now → don't create (opportunities the team already dropped are not recreated).
- **Counter-signals are posted to Harvestr too** (labelled as such, linked to the discovery they contradict), not kept on the page only.
- Needs with **no discovery** go into one umbrella discovery **"Other topics (to organize)"** under the Community component (created once, reused) so the PM can aggregate numbers now and split later. Name candidates for their own discovery in the report, don't create them.
- Link to the **level-2 parent** when the best fit is a level-3 sub-discovery (main numbers are aggregated first, details later).

## Step 5 — Dedupe against Harvestr, then post and link

1. List existing messages and feedbacks for the requester company and for each target discovery. Drop or merge anything already covered; say what you skipped and why.
2. Show the draft table (title, JTBD one-liner, target discovery, flags). Wait for approval.
3. Create company and user if missing. **No phone needed to post:** the `create-message` webhook upserts the requester from name + email alone (verified 17 Nov 2026) — never say a phone is required. Caveat: that upsert creates the user **without a company**; the `create-user` webhook (which does need a phone and a `companyId`) is the only way to attach the company, so for a new contact either call it first with the phone from the page, or tell the PM to attach the company in the Harvestr UI. Post via the `create-harvestr-insight` webhook path (write the script/curl only after the explicit email approval above; read `SUBMITTER_EMAIL` etc. from env vars rather than hard-coding them, so the file holds no personal data). **If the write or the call is still blocked, do not stall:** give the PM the exact one-line command to run themselves with the emails in the environment (their own `!` shell), make the script accept message codes as args so a single failed post can be retried without duplicates, and continue with resolving ids and linking once they paste the output. Never ask them to retype messages. Labels: `interview`, a type label, `client-<company-slug>`, source link = the Notion page.
4. Link each message to its discovery with a `CHUNK_CREATE` plan (read it back, confirm, execute). The webhook has no discovery field.
5. Read back: each message exists, is linked, no AI suggestion pending to another discovery.
6. **Closing message = the review table (mandatory, never replace it by a pointer to a file or ids).** The PM reviews the insights straight from your last message, so it must contain, for each interview (one table per interviewee, headed with name + company):

   | # | Insight | Linked discovery | Flag |
   |---|---|---|---|
   | 1 | [<English title>](https://app.harvestr.io/messages/search/<harvestr-id>?query=) | <level-2 discovery name> | weak / inferred / demo-only / interviewer-led / counter-signal / candidate own discovery / TMS-not-Community |

   Rules:
   - The **title itself is the clickable link** (no separate "open" column, no bare ids, no "ids are in results.json").
   - Use the **real Harvestr message id**, not the id the `create-message` webhook returns (they differ — get the real ones with `list_harvestr_messages` for the requester, matched by title). Never write `<id>` placeholders.
   - Keep the draft numbering (G1, D1…) if the PM saw it during the draft review, so the two lists can be compared.
   - Flags come from the `Fit:` line and counter-signal label; leave blank when none.
   - Then a short **"To check when you review"** list (assignee by hand, links to a level-2 parent instead of a level-3, targets outside Community, shared/missing verbatims, retries after a webhook error, pending AI suggestions — say if you did NOT check them) and **"Still open"**.
   - Note that parallel sessions can create overlapping insights — if another session is posting, check first.

## Step 6 — Close

- Optional Linear update on the interview's COM subtask (comment with the page + Harvestr links), only if the PM wants it.
- If the user keeps a work log, add one line. List open items: facts to verify, follow-ups, hypotheses whose status changed.

---

## Whisper setup (only when no usable transcript exists)

The scripts live in this skill's `scripts/` folder (base directory shown when the skill loads).

1. **Locate:** `bash <skill>/scripts/whisper_env.sh check` looks for a Python venv with `faster-whisper` at `$ITW_WHISPER_DIR`, then `~/tools/whisper`, and for `ffmpeg`. It prints `OK <dir>` or what is missing.
2. **Not found → offer to install, don't just fail.** Say in one line what is missing, then ask: "Install faster-whisper in `~/tools/whisper`? (python venv + pip install, `ffmpeg` via `brew install ffmpeg` if missing, ~1.5 GB model download on first run)". Only on a yes: `bash <skill>/scripts/whisper_env.sh install`. On a no: fall back to the Gemini/Drive transcript or ask for text notes.
3. **Run:** `<dir>/.venv/bin/python <skill>/scripts/transcribe.py AUDIO OUT.txt [--variant loud|raw8] [--lang fr] [--model medium] [--prompt TEXT]` (beam 10, no VAD, temperature fallback; output lines `[mm:ss] text`).

## Known traps
- Harvestr API **ignores `assignee_id`**: tell the PM to assign messages to the PM by hand.
- Type label (`feature-request`, `missing-info`…) is picked by you: show it in the draft table so the PM can change it; `missing-info` for a pain with no discovery yet.
- A requester may already exist under another company record (subsidiary, former employer): search by name first, reuse it.
- Don't claim "no transcription tool" before running the Whisper locate step.
- Two AI summaries often contradict each other and the transcript — the transcript wins.
- A figure heard as "32 jours" may be 30 in the notes — keep both, flag.
- Anything the interviewee said about their own stats can contradict the Metabase numbers: show both.
- Webhook response id (`cmw…`) ≠ Harvestr message id. Direct links built from the webhook id are dead — always resolve the real id before building the closing table.
