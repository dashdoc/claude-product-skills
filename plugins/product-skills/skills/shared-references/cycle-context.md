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

Cycles are 6 weeks, followed by a cooldown (usually 2 weeks). There is no dedicated shaping week anymore (dropped Nov 2026). Cadence may evolve: see [`product-process.md`](product-process.md).

| Week | Label |
|---|---|
| 1–6 of the cycle | `Cycle N — Week X/6` |
| Cooldown | `Cooldown week X/Y — before Cycle N+1` |

Example: `Cycle 38` from 09/11 → week of 23/11 = `Cycle 38 — Week 3/6`.

## 3. Rituals

On the same calendar, over the same window (`fullText` filter):

- `Betting table` — usually the first Monday of the cooldown
- `Roadmap review`

Keep the earliest occurrence after now for each.

## 4. Sanity check

Compare with the week file's `> Cycle N — …` header. If they disagree, say so once, trust the calendar, and offer to fix the header.

## Uses

- Deadline inference in `/triage` ("before the betting table", "before Cycle 39")
- The cycle banner in `/plan-week`
- Thursday is team weeklys day; there is no standing shaping slot anymore
