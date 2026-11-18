# community-discovery

Community discovery interviews, end to end. The skills chain in this order:

| Step | Skill | What it does |
|------|-------|--------------|
| 1 | `/itw-target-list` | Score customers on load-board proxies (Metabase), resolve the champion contact, hand over the next wave |
| 2 | `/itw-outreach-drafts` | Gmail drafts inviting the next 10 targets — never sends |
| 3 | `/itw-followup-check` | Bookings, declines, replies, single reminders due — read-only, can run daily |
| 4 | `/itw-company-brief` | Facts-only brief on the interviewee and their company before the call |
| 5 | `/itw-page-prep` | Notion interview page ready to record (one guideline table, debrief rows, meeting-notes block) |
| 6 | `/itw-process` | After the call: clean transcript, debrief against Harvestr discoveries, JTBD insights posted and linked |

## Needs

- Connectors: Notion, Harvestr (read), Gmail, Google Drive, Google Calendar, HubSpot, Metabase. Linear is optional.
- Skills from the Dashdoc workspace plugin: `dashdoc-data` (any Metabase query) and `discovery-insights` (insight format).
- For local transcription of recordings: Python 3.9+ and `ffmpeg`. `itw-process` checks for a Whisper install (`$ITW_WHISPER_DIR`, default `~/tools/whisper`) and offers to install it when missing. The Notion AI transcript is used first, so this is only a fallback.

## Settings (optional environment variables)

| Variable | Default | Used for |
|----------|---------|----------|
| `ITW_OUTPUT_DIR` | `./itw-notes/` | Transcripts, preview files, scoring queries |
| `ITW_WHISPER_DIR` | `~/tools/whisper` | Local faster-whisper environment |

## Install

```
plugin marketplace add dashdoc/claude-product-skills
plugin install community-discovery
```

Start a new session after installing or updating.
