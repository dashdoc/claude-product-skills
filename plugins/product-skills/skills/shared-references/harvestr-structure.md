# Harvestr — how discoveries are structured and how to act on them

Shared by `release-harvestr`, `shaping-observe`, `discovery-insights` and any skill that reads, restructures or writes Harvestr. It covers **structure and working rules**. For tool mechanics (plan schemas, `CHUNK_CREATE`, link formats used by the interview skills) see `harvestr-notion-mechanics.md` (shipped with the community-discovery plugin only; locally in this same folder).

---

## 1. Vocabulary

- **"Feedback"** in Fabien's mouth = any customer insight. In Harvestr that is BOTH:
  - `message` — the raw inbound (Intercom, Slack, note, email). The verbatim.
  - `feedback` — a message, or part of one, linked to a discovery (validated) or proposed by AI (suggested).
  When consolidating, sweep messages AND feedbacks, per customer record too.
- **Requester vs submitter.** The requester is the customer. A CS teammate who relayed it is only the submitter. Search by the customer's record, not the teammate.
- **Weight** on a feedback: 1 = nice to have, 2 = must have, 3 = blocking.

## 2. Structure rules

| Rule | Detail |
|---|---|
| **One component per team** | Each team has a top component holding its discoveries (sub-components only if needed). |
| **Discovery = a job to be done** | Marked with **👷‍♀️** in the title. Sub-discoveries are an aspect or a specialisation of that job. |
| **Pitch discovery = 🍫** | A discovery handled by a pitch (roadmap card that was bet on) is titled `🍫 [Feature name]`. |
| **Pitches are siblings, not children** | Harvestr allows **only one sub-discovery level**. Pitches need their own sub-discoveries (to measure aspects of the pitch), so a 🍫 discovery sits next to the 👷‍♀️ JTBD discoveries, never under one. |
| **Few top-level discoveries** | One per roadmap card / pitch, plus one umbrella "backlog" discovery per theme. Never promote many small topics to top level: Fabien dispatches from the inbox and needs a short list of targets. |
| **Same rule for everyone** | Apply a splitting rule (e.g. "business privacy is its own sub-discovery") to all feedbacks consistently, or the tree gets out of hand. |
| **Shaping reduces scope → new pitch discovery** | When shaping cuts scope, create a 🍫 discovery for the pitch, move the in-scope feedbacks to it, keep the rest in the original, and update the roadmap card's `🌾 Harvestr discovery` link. |
| **Release alignment is per sub-discovery** | At release, coverage and state are checked on each sub-discovery of the pitch, not only on the top discovery. |
| **Start small** | First put feedbacks in the discovery; split into sub-discoveries once there is enough to organise. |

## 3. Working rules

- **Clickable links with titles, never ids.** Messages: `https://app.harvestr.io/messages/search/<id>?query=`. Discoveries: `https://app.harvestr.io/components/0/list/<id>`. Never show bare ids or plan ids (`MEqC_UHbk`) to Fabien; he cannot find them in the UI.
- **One plan at a time.** Harvestr writes go through a plan (`create_harvestr_plan` → `add_harvestr_plan_step` → `read_harvestr_plan` → `execute_harvestr_plan`). Before creating one, check whether another session or agent already has a plan in progress on the same discoveries (ask Fabien if unsure). Never run two parallel plans on the same tree.
- **Show the change table first.** Present the moves/renames/state changes as one table (feedback title link → from → to) and wait for approval before executing. Read the plan back after executing.
- **What the MCP can't do → give manual links.** Some actions are not possible through the MCP (e.g. some unlink/unprocess/reassign cases, creating a contact). List those as "do manually" with the direct link to each item, so Fabien can click through.
- **New insights from raw content** go through `/discovery-insights` or the `create-harvestr-insight` flow, not ad-hoc plan steps.
- **Processing a message** = all its content is linked to discoveries. If part of it belongs to another PM, link your part, then reassign the message to them.
