# Harvestr / Notion mechanics and interview glossary — shared reference

Operational know-how for the interview skills (`itw-process`, `itw-page-prep`, `itw-company-brief`, `idea-frame`) when they read or write **Notion** and **Harvestr**. Each trap below failed in a real session; read before the first write.

---

## 1. Harvestr

### Plan tools: load the schema first, arrays are mandatory

The `mcp__harvestr__*` plan tools are often deferred. Calling them without loading the schema fails with `Invalid input: expected array, received undefined`. Load them first with `ToolSearch` (`select:mcp__harvestr__create_harvestr_plan,mcp__harvestr__add_harvestr_plan_step,mcp__harvestr__execute_harvestr_plan,mcp__harvestr__read_harvestr_plan`), then:

| Tool | Required shape |
|---|---|
| `add_harvestr_plan_step` | `steps` is an **array**, even for one step |
| `execute_harvestr_plan` | `step_ids` is an **array** of the step ids to run (take them from the plan you just read) |

Linking a message to a discovery = a `CHUNK_CREATE` step (`discoveryId` + the message's chunk). Read the plan back, check it matches the table the PM approved, execute, then read it back again.

`requires_user_confirmation: true` in the response is an API flag, not a question for the PM. If the PM already approved the draft table (which names the target discovery of each message), do not ask again.

### Message ids

The `create-message` webhook returns an id (`cmw…`) that is **not** the Harvestr message id. Links built from it are dead. Resolve the real id with `list_harvestr_messages` (filter on the requester, match by title) before building any link.

### Companies and contacts

- List **every** company record that matches the name (renamed, merged, subsidiary, "formerly X"). If there is more than one, show them and ask which to use. Never pick silently, and never create a second one.
- The `create-message` webhook upserts the requester from name + email alone (no phone needed) but creates the user **without a company**. Attaching the company needs the `create-user` webhook (phone + `companyId`) or the Harvestr UI. Check the requester's company in the audit step so the PM can fix it before the draft review.

### Pending AI suggestions

After linking, check the AI suggestions pending on the new messages. Report the **count**, nothing more. The PM sorts them in the Harvestr UI; do not offer to reject them.

---

## 2. Notion

### Large pages overflow `notion-fetch`

An interview page with a transcript can return 70k+ characters, and the tool answers `result exceeds maximum allowed tokens` with the **path of a saved file**. Do not fetch again. Read the saved file with `python3 -c`/`grep` and pull only the sections you need (properties, tables, the AI block, comments). The same goes for the post-edit verification fetch.

### Page edits

- Never start a line with `#` (Notion turns it into a heading; "# of…" becomes a title).
- Re-read the page after editing. Notion rewrites links and escapes on its own.
- Inside table cells, separate items with line breaks (`<br>`), not one long run-on sentence.
- Check comments before replacing a block, so none is orphaned.

---

## 3. Interview glossary (speech-to-text corrections)

Apply when cleaning a transcript or an AI summary. Extend it whenever the PM confirms a new term.

| Heard / written | Correct | Note |
|---|---|---|
| Transus, TransEU | **Trans.eu** | |
| Transnet | **Wtransnet** | confirmed by the PM |
| Teleroot | **Teleroute** | confirmed by the PM |
| Gassot, Gacoin, Gaissot | **Gayssot** | law |
| JetTrans | **GEDTrans** | B2PWeb and GEDTrans are both products of the H2P company |
| B2P | **B2PWeb** | when the interviewee uses the load board; the interviewer may mean a payment tool, check the context |
| LKV | **LKW Walter** (lkw-walter.com) | Austrian firm; probable, keep in the To-verify list |
| Ajdak, Ajdoc | **Dashdoc** | |
| DREAL | **DREAL** | keep |
| Quartix | **Quartix** | geolocation |

Terms that cannot be resolved from the account, the page or this table go in the transcript's **To verify** list. Ask the PM once, in a batch, never one by one.
