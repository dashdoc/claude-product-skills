# claude-product-skills

Claude Code marketplace for the Dashdoc product team. It holds two plugins:

| Plugin | For | Folder |
|--------|-----|--------|
| `claude-product-skills` | Every PM and designer — shaping, releasing, roadmap, feature-review | [`plugins/product-skills`](plugins/product-skills) |
| `community-discovery` | Whoever runs Community discovery interviews — target list to Harvestr insights | [`plugins/community-discovery`](plugins/community-discovery) |

## Install

In an interactive `claude` terminal (two steps, one-time):

```
plugin marketplace add dashdoc/claude-product-skills
```
```
plugin install claude-product-skills
```

For the Community discovery interview skills, also run `plugin install community-discovery` (see its [README](plugins/community-discovery/README.md)).

Then start a new session — skills load at session start.

## Update

Skills don't update automatically. When new versions are pushed to this repo, run:

```
plugin update claude-product-skills
plugin update community-discovery
```

Then start a new session to load the updated skills.

## Skills

### Shaping

| Skill | Trigger |
|-------|---------|
| `/shaping-observe` | Run customer interview analysis on a FigJam board |
| `/shaping-requirements` | Generate requirements from a pitch card |
| `/shaping-start` | Bootstrap a new pitch on the FigJam betting board |
| `/shaping-steal` | Benchmark competitor UX and import screenshots to FigJam |
| `/shaping-success` | Define success criteria and metrics for a pitch |

### Releasing

| Skill | Trigger |
|-------|---------|
| `/release-changelog` | Create the Notion changelog entry for a shipped feature |
| `/release-faq` | Draft the FAQ page for a released feature |
| `/release-harvestr` | Update Harvestr discovery state after a release |
| `/release-success-dashboard` | Build the post-release success tracking dashboard |
| `/release-translations` | Generate translated release notes |
| `/changelog-digest` | Weekly product digest from the 🛎️ Changelog DB, posted to `#changelog` |
| `/changelog-digest-monthly` | Monthly product digest, posted to `#team-product` for review before `#general` |

### Other

| Skill | Trigger |
|-------|---------|
| `/motion-designer` | Direct a short animated video (voice, music, subtitles) about any subject, from scratch or from a template (e.g. `shaping-pitch`) — needs `dcli` + fframes, ≤ $5 OpenRouter |
| `/ff-review` | Full ConfigCat feature flag audit — quality, expiration, ownership |
| `/roadmap-card` | Draft or update a roadmap card in Notion |
| `/review-pitch-tasks` | Review Linear tasks against a pitch spec |

## Shared references

`plugins/product-skills/skills/shared-references/figjam-mechanics.md` — FigJam/Figma board mechanics (section-relative coordinates, image upload, stickies). Loaded automatically by the shaping skills.

`plugins/product-skills/skills/shared-references/changelog-entry-reading.md` — how to read a 🛎️ Changelog entry for a digest line (page body over `Slack summary`, rollout state, demo link). Used by both changelog digests.

`plugins/product-skills/skills/shared-references/cycle-context.md` — where cycle dates come from: all-day `Cycle N` / `Cooldown` events on the Dashdoc calendar, shaping week = week 4 of the cycle.

## Notes

- All Dashdoc communications must be in **English**.
- Skills follow the [Shape Up](https://basecamp.com/shapeup) method and Dashdoc's DoD.
- Linear, Notion, Harvestr, ConfigCat, and Figma MCPs must be connected for full functionality.
