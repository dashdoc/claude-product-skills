# HubSpot interview note — one note per interview, on the contact and the company

Used by `itw-page-prep` (planned), `itw-process` (done / processed), `itw-followup-check` (detects missing notes). Learned when notes were created in bulk after the fact.

## Gate

- Writing a note is a write to an external tool: show the table (contact, company, note text) and get a yes first. In a session where the PM has already said "create the notes", that yes covers the batch.
- Check write access before drafting: `discover_hubspot_schema` GET_OBJECT_TYPES `NOTE` → `writeAccess` must be `AVAILABLE`. If it says `REQUIRES_PERMISSION_MODIFICATION`, the connector was authorised read-only (every write type shows the same). Don't force the call: tell the PM to reconnect the HubSpot connector with write scopes, and list the note as "not done" in the report.

## One note per interview

- **One note** per interview, associated to **both** the contact and the company (it shows on both timelines). It is updated as the interview moves, never duplicated.
- Before creating, look for an existing note: `search_crm_objects` NOTE with `associatedWith` the company, then match the Notion page id inside `hs_note_body`. Found → update it (`updateRequest`, `hs_note_body`).
- Two interviews at the same company = two notes on the company.

## Find the person

1. **The calendar invite first.** `list_events` on the interview day with `fullText` = the person's surname. The attendee email (not Dashdoc, not the co-interviewers) is the booking email; the description often repeats it ("Booked by"). Search the HubSpot CONTACT by that **email** (`filterGroups` `email EQ`).
2. Else name search. Surnames are not unique (a common surname can return 15+ contacts, and one person can exist twice with two emails): never pick on a name alone.
3. No contact in HubSpot → note on the **company only** (don't create contacts). Say it in the report.

## Find the company

1. Through the contact: `search_crm_objects` COMPANY with `associatedWith` the contact id. A contact can exist with no company linked (seen for several interviewees).
2. Else by the contact's email domain (`domain` property; search the domain text).
3. Still ambiguous (several records with the same short name, a legacy record next to the real customer) → check **Planhat** (better maintained than HubSpot) via `search_records`, or ask the PM. Don't pick one.
4. Interviewee not in HubSpot and not in Planhat → skip and report.

## Note text

HTML body, one line of context and the link:

| Moment | `hs_note_body` | `hs_timestamp` |
|---|---|---|
| Planned | `Community discovery interview planned, <d Mon yyyy>.<br>Notion interview page: <a href="URL">URL</a>` | the booked slot (ISO, UTC) |
| Done / processed | `Customer interview (Community discovery), <d Mon yyyy>.<br>Notion interview page: <a href="URL">URL</a>` (add `Processed: <n> insights in Harvestr.` after processing) | the interview start (ISO, UTC) |

- English. Facts only, no summary of the content.
- **URL** = `https://app.notion.com/p/dashdoc/<page-id>` where `<page-id>` is the 32-character id at the end of the page URL, with no title slug. Never the bare `app.notion.com/<id>` returned by Notion tools: it shows "This page couldn't be found".
- Create with `manage_crm_objects` `createRequest`, `objectType: notes`, `associations` to `contacts` and `companies`. Max 10 objects per call.

## Report

List one HubSpot link per note (`https://app.hubspot.com/contacts/<portal-id>/contacts/<contact-id>?engagement=<note-id>`, company-only notes: the company record) so the PM can check. Say which interviews got no note and why.
