---
name: release-translations
description: Extract new or changed i18n translation keys from GitHub PRs linked to a list of Linear tasks. Finds PRs (including on sub-issues and in comments), scans locale-file diffs, deduplicates and sorts keys alphabetically. Use whenever Fabien says things like "extract translation keys for FLO-xxx", "what translations does [pitch] need", "i18n keys from these tickets", "list new locale strings", "translations to send to the team", or any equivalent request tied to preparing translation work at release time. Requires `gh` CLI access to the `dashdoc/dashdoc` repo.
---

# release-translations — Extract Translation Keys from Linear Tasks

Given a list of Linear issue IDs, find all linked GitHub PRs, scan locale file changes in those PRs, and output a deduplicated alphabetically sorted list of translation keys that were introduced or changed.

## Usage

```
release-translations [issue-id] [[issue-id]...]
```

**Examples:**
```
release-translations FLO-412
release-translations FLO-412 FLO-415 FLO-418
```

---

## Step 1 — Collect PR numbers from Linear issues

For each issue ID, run in parallel:
- `mcp__54d3c450-50e8-43e9-a5fd-211855d395e3__get_issue` — attachments include linked GitHub PRs; extract PR numbers from URLs matching `github.com/.*/pull/(\d+)`
- `mcp__54d3c450-50e8-43e9-a5fd-211855d395e3__list_issues` with `parentId` set to the issue ID — fetch sub-issues, then for each sub-issue run `mcp__54d3c450-50e8-43e9-a5fd-211855d395e3__get_issue` to get their attachments too
- `mcp__54d3c450-50e8-43e9-a5fd-211855d395e3__list_comments` on the top-level issue — scan comment bodies for GitHub PR URLs

Collect all unique PR numbers found across the issue, its sub-issues, and all comments.

If no PR is found for an issue, note it but continue with the others.

---

## Step 2 — Extract translation keys from each PR

Fetch all PR diffs at once with a single bash command, piping through Python for key extraction (required — macOS awk does not support capture groups):

```bash
for pr in [PR1] [PR2] ...; do
  gh pr diff $pr --repo dashdoc/dashdoc 2>&1 \
    | awk '
        /^diff --git/ { file=$3; inLocale=0 }
        /packages\/i18n\/locales\// { inLocale=1 }
        /platform\/internals\/locale\// { inLocale=1 }
        inLocale && /^\+[^+]/ { print "ADD " $0 }
        inLocale && /^-[^-]/ { print "DEL " $0 }
      '
done | python3 -c "
import sys, re
add, del_ = {}, {}
for line in sys.stdin:
    m = re.search(r'\"([^\"]+)\": \"([^\"]+)\"', line)
    if not m: continue
    key, val = m.group(1), m.group(2)
    if line.startswith('ADD'):
        add[key] = val
    elif line.startswith('DEL'):
        del_[key] = val
keys = [k for k in add if k not in del_ or add[k] != del_[k]]
for k in sorted(keys):
    print(k)
"
```

This command:
- Scopes to locale files only (`packages/i18n/locales/*.ts` and `platform/internals/locale/`)
- Tags added vs removed lines
- Keeps a key only if it is **new** (not in DEL) or its **value changed** (ADD and DEL present but with different values)
- Skips keys that were merely reordered (same key + same value on both sides)

---

## Step 3 — Output

Merge all keys from all PRs, deduplicate, sort alphabetically, and print one key per line:

```
error.mustBeAPositiveInteger
flow.settings.zoneSetupTab.currentOpenings
flow.settings.zoneSetupTab.currentOpenings.slotDuration
flow.settings.zoneSetupTab.editSlotSettings.slotsSection
...
```

If a PR had no locale file changes, note it inline (e.g. `PR #28507 — no locale changes (DB migration)`).

If no keys were found across all PRs, say so explicitly.
