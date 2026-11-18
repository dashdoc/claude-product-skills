# Cycle context — where it comes from

There is no local cycle file. The source of truth is the shared **Dashdoc** Google calendar: every day belongs to either an all-day **`Cycle N`** event or an all-day **`Cooldown`** event.

## 1. Current phase — Dashdoc calendar

```
list_events(
  calendarId="9kbnadb3rsipfm62nei43hn2io@group.calendar.google.com",   # "Dashdoc" shared calendar
  startTime="{today − 60 days}", endTime="{today + 120 days}",
  timeZone="Europe/Paris", orderBy="startTime"
)
```

Keep the all-day events whose summary is `Cycle <N>` or `Cooldown`. All-day `end.date` is **exclusive** (`Cycle 37` = start 2026-09-14, end 2026-10-24 → last day Fri 23/10).

- **Today's phase** = the event whose range contains today
- **Next phase** = the following one (a Cycle is always followed by a Cooldown, and vice versa)

Don't use Linear cycle dates: Linear opens each cycle a week before it actually starts.

## 2. Week label

Cycles are 6 weeks = 5 execution weeks + 1 shaping week, and the shaping week is the **4th week of the cycle** (not the last). Cooldowns sit between cycles (usually 2 weeks).

| Week of the cycle | Label |
|---|---|
| 1, 2, 3 | `Cycle N — Execution week 1/5`, `2/5`, `3/5` |
| 4 | `Cycle N — Shaping week` |
| 5, 6 | `Cycle N — Execution week 4/5`, `5/5` |
| Cooldown | `Cooldown week X/Y — before Cycle N+1` |

Example: `Cycle 37` 14/09–23/10 → week of 21/09 = `Execution week 2/5`, week of 05/10 = `Shaping week`, 12/10 = `Execution week 4/5`, 19/10 = `Execution week 5/5`, then `Cooldown` 26/10–06/11 before `Cycle 38` (09/11).

## 3. Rituals

On the same calendar, over the same window (`fullText` filter):

- `Betting table` — usually the first Monday of the cooldown
- `Roadmap review`

Keep the earliest occurrence after now for each.

## 4. Sanity check

Compare with the week file's `> Cycle N — …` header. If they disagree, say so once, trust the calendar, and offer to fix the header.

## Uses

- Deadline inference in `/triage` ("before shaping week", "before the betting table", "before Cycle 38")
- The cycle banner and shaping-week protection in `/plan-week`
- The Thursday 14:00–18:05 block is the standing shaping slot every week, whatever the phase
