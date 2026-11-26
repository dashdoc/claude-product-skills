# Writing to Notion — house style and placement rules

Read this before any skill writes to a Notion page (create, update, append). Each rule below comes from a correction Fabien had to make in a real session. A skill's own format rules (FAQ structure, changelog sections, roadmap card body) win when they are more specific.

---

## 1. Where to write

| Rule | Detail |
|---|---|
| **Write under the named section** | When Fabien names a section ("in Solution", "under Scenarios and use cases"), that is a heading on the page. Write the content under it. It is not a subpage, and not the top of the page. |
| **Edit only the targeted section** | Don't touch, rephrase or "improve" neighbouring sections. If another section looks wrong, say so in chat instead of editing it. |
| **Append at the bottom by default** | When adding a new block to an existing page without a named section, add it at the end, not at the top. |
| **Check the page version** | Re-fetch the page right before writing. Fabien edits pages in parallel; never write from a copy fetched earlier in the session. |
| **Check the right page** | When several pages share a name (old pitch page vs roadmap card, FAQ page vs FAQ Moderation), confirm the URL before writing. |
| **Keep Fabien's comments** | Leave existing comments, callouts and notes he left on the page. He removes them himself. |

## 2. How to write

- **Factual, not chronological.** Describe how things are, not the story of how we got there. No "first we tried…, then…", no history section unless asked.
- **Audience stated.** Know who reads the page (devs + PM, CS, a new joiner) and write for them. Use common words. When the page is technical, start with a short **Terminology** section.
- **Bullets over prose. Schemas over text.** Use mermaid diagrams for flows and sequences. After writing, re-fetch and check the diagram renders as a diagram (a ```mermaid code block); if it shows as raw text, fix it.
- **One table, not several.** When Fabien asks for a plan or a script as a table, make ONE table. Use rows for titles/steps (e.g. one row per question or per day), not one table per week or per section.
- **Facts only on prep pages.** Interview prep, company briefs and onboarding pages hold facts and links, not your questions or speculation.
- **High level stays high level.** If a section is meant as an overview, don't expand it with detail that belongs elsewhere.
- **Simple wording.** For pages others will read, apply `/anthropic-skills:simple-writing` style: short sentences, no jargon, no em dashes.
- **English** for every Dashdoc artifact, using the glossary terms (see `/shaping-terminology`).

## 3. Links and references

- **Linear keys → full URLs.** Never leave a bare `FLO-123` / `NET-456` in a page body. Write `[FLO-123 Title](https://linear.app/dashdoc/issue/FLO-123/...)`.
- **Harvestr, Metabase, Figma** — full clickable URLs with the title as link text, never ids.
- **Notion page links outside Notion (HubSpot notes, Slack, Linear, emails): `https://app.notion.com/p/dashdoc/<page-id>`.** The id is the 32-hex string at the end of the page URL (no dashes). The title slug is optional, so don't build one: accents and emojis in titles make it unreliable. This form is **broken** ("This page couldn't be found"): `https://app.notion.com/<id>` (no `/p/dashdoc/`). `https://app.notion.com/p/<id>` (no workspace) is untested: don't use it. `notion-fetch` / `notion-query-data-sources` return `app.notion.com/<id>` or `app.notion.com/p/<id>`: take the id from them and rebuild the link. Tested 26 Nov 2026 on Community interview pages.
- **Durable links only.** Notion file/media URLs expire; for videos use the hosted link (Tella) instead of an uploaded file link.

## 4. Notion markdown traps

- **Never start a line or bullet with `#`.** "# of customers" becomes a heading and breaks the list. Write "Number of customers", or escape as `\#`.
- **Toggle headings** appear in fetched markdown as `<toggle heading="h3">…</toggle>`. Write new ones in the same form as the existing ones on the page.
- **Don't break formatting around your edit.** When replacing a block, keep the surrounding bullets' indentation and style consistent with the first bullet of the list.
- **Database rows:** set properties through the row's data source schema; leave read-only and automation-trigger properties alone (e.g. changelog properties re-fire the Slack automation).

## 5. After writing — always

1. Re-fetch the page.
2. Check the edited block: right section, renders as intended (headings, tables, mermaid, toggles), nothing else changed.
3. Report the direct URL of the page (and section anchor when there is one).
