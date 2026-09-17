---
name: ff-review
description: Run a full ConfigCat feature flag review for Dashdoc — quality audit (global), expiration alerts, and ownership reminders. Use whenever Fabien says things like "/ff-review", "ff review", "review my feature flags", "check the feature flags", "which FFs are expired", "which FFs are mine", "FF quality check", "flag hygiene", or any equivalent phrasing about auditing or reviewing ConfigCat feature flags. Supports an optional "mine" argument to scope expiration and ownership to Fabien's domains only; default is "all" with group-by-PM.
---

# /ff-review — Feature Flag Review

Produce a structured ConfigCat FF audit for Fabien. Three sections always run:
1. **Quality** — global, every FF, FF-first flat list
2. **Expiration** — scoped by mode, FF-first flat list
3. **Ownership** — scoped by mode, FF-first flat list

**Mode:**
- `/ff-review` → mode = `all` (expiration + ownership grouped by PM)
- `/ff-review mine` → mode = `mine` (Fabien's domains only)

---

## Hardcoded IDs

```
PRODUCT_ID  = 08d9533c-6721-492d-88c3-ba1056e00ab8
CONFIG_ID   = 08dd6234-18c6-43d3-82ea-c626311c5733
ENV_PROD_EU = 08d9533c-673e-403e-82ef-7947ec34195c

# Maturity tag IDs
TAG_ALPHA     = 2222   ("alpha")
TAG_BETA      = 2223   ("beta")
TAG_RELEASED  = 2219   ("released")
TAG_TO_REMOVE = 1686   ("to-remove")
TAG_REMOVING  = 1685   ("removing")
MATURITY_TAG_IDS = {2222, 2223, 2219, 1686, 1685}

# Maturity-aware expiration thresholds (warn_days, overdue_days)
MATURITY_THRESHOLDS = {
  "alpha":     (60, 90),
  "beta":      (60, 90),
  "released":  (14, 30),
  "to-remove": (7,  21),
  "removing":  (7,  21),
  None:        (60, 90),   # no maturity tag
}

# ConfigCat domain tags → Notion Team
# Key = ConfigCat tag name (starts with "Domain / ")
# Value = Notion Team page URL
DOMAIN_TAG_TO_TEAM = {
  "Domain / Applications - Flow":     "https://www.notion.so/2b86d66c0b4a80e09a52f80377ebff20",
  "Domain / Platform - Community":    "https://www.notion.so/2b86d66c0b4a8062be52e2d0f75a5975",
  "Domain / Platform - Admin":        "https://www.notion.so/2b86d66c0b4a8062be52e2d0f75a5975",  # Community team owns Admin
  "Domain / Platform - Discuss":      "https://www.notion.so/2b86d66c0b4a8062be52e2d0f75a5975",  # Community team owns Discuss
  "Domain / TMS - Repositories":      "https://www.notion.so/2b86d66c0b4a8062be52e2d0f75a5975",  # Community team owns Repositories
  "Domain / TMS - Indicators":        "https://www.notion.so/2b86d66c0b4a8062be52e2d0f75a5975",  # Community team (Carbon footprint)
  # All other domain tags → unknown team, will be flagged
}

# Fabien's domain tags (for "mine" mode)
MY_DOMAIN_TAG_IDS = {
  56076,   # Domain / Applications - Flow
  53135,   # Domain / Platform - Community
  53137,   # Domain / Platform - Discuss
  53136,   # Domain / TMS - Repositories
  53133,   # Domain / TMS - Indicators
  68231,   # Domain / Platform - Admin
}

# Teams (pre-resolved — read from Notion at runtime to get fresh Tech/PM)
TEAM_PAGES = {
  "Flow":      "https://www.notion.so/2b86d66c0b4a80e09a52f80377ebff20",
  "Community": "https://www.notion.so/2b86d66c0b4a8062be52e2d0f75a5975",
}

# Known team members as of last update (used as fallback if Notion fetch fails)
# Flow team
FLOW_PM   = "fabien.poulard@dashdoc.com"
FLOW_TECH = ["vincent.toupet@dashdoc.com"]

# Community team
COMMUNITY_PM   = "fabien.poulard@dashdoc.com"
COMMUNITY_TECH = [
  "thomas.loiret@dashdoc.com",
  "valentin.demange@dashdoc.com",
  "charbel.abidaher@dashdoc.com",
  "alexandra.jerome@dashdoc.com",
  "loic.teixeira@dashdoc.com",
  "jules.ricou@dashdoc.com",
]
```

---

## Step 1 — Compute dates

```python
from datetime import datetime, timezone, timedelta
today = datetime.now(timezone.utc)
print(today.strftime("%Y-%m-%d"))
```

---

## Step 2 — Fetch & save data

Call `ConfigCat:list-settings(configId=CONFIG_ID)` **once**.

Immediately write the JSON response to `/tmp/ff_data.json` via bash:
```bash
cat > /tmp/ff_data.json << 'ENDJSON'
<paste the raw JSON array from the API response here>
ENDJSON
```

Then run the entire processing script in **one bash call** that reads from that file. Do NOT re-embed the FF data as a Python literal inside the script.

> Note: `list-settings` does NOT return `creatorEmail`. Do NOT call `get-setting-value-v2` by default — it's expensive (1 call per FF). Ownership is derived from domain tag → PM mapping only.

---

## Step 3+4 — Process in one bash call

Write `/tmp/ff_review.py` then run it. The script reads `/tmp/ff_data.json` and outputs the full report. Structure:

```python
#!/usr/bin/env python3
import json, sys
from datetime import datetime, timezone
from collections import defaultdict

BASE = "https://app.configcat.com/v2/08d9533c-66a6-4893-8f2b-1d7a88dd69ea/08d9533c-6721-492d-88c3-ba1056e00ab8/08dd6234-18c6-43d3-82ea-c626311c5733/08d9533c-673e-403e-82ef-7947ec34195c/{}"
MATURITY_TAG_IDS = {2222, 2223, 2219, 1686, 1685}
MY_DOMAIN_TAG_IDS = {56076, 53135, 53137, 53136, 53133, 68231}
MATURITY_THRESHOLDS = {
    "alpha":(60,90),"beta":(60,90),"released":(14,30),
    "to-remove":(7,21),"removing":(7,21),None:(60,90),
}
DOMAIN_TAG_TO_PM = {
    "Domain / Applications - Flow":"Fabien",
    "Domain / Platform - Community":"Fabien",
    "Domain / Platform - Admin":"Fabien",
    "Domain / Platform - Discuss":"Fabien",
    "Domain / TMS - Repositories":"Fabien",
    "Domain / TMS - Indicators":"Fabien",
}

today = datetime.now(timezone.utc)
raw = json.load(open("/tmp/ff_data.json"))

def lnk(f): return f"[{f['key']}]({BASE.format(f['settingId'])})"

def enrich(f):
    tags = f["tags"]
    dtags = [t for t in tags if t["name"].startswith("Domain /")]
    mtags = [t for t in tags if t["tagId"] in MATURITY_TAG_IDS]
    mat = mtags[0]["name"] if mtags else None
    hint = f.get("hint") or ""
    key = f["key"]
    created = datetime.fromisoformat(f["createdAt"].replace("Z","+00:00"))
    age = (today - created).days
    wd, od = MATURITY_THRESHOLDS.get(mat, (60,90))
    expiry = "overdue" if age>=od else ("warn" if age>=wd else "ok")
    bad = not hint or hint.strip()==key or "http" not in hint or hint.strip()=="a"
    issues = []
    if not dtags: issues.append("❌ no domain")
    if not mtags: issues.append("❌ no maturity")
    if bad: issues.append("❌ bad desc")
    dname = dtags[0]["name"] if dtags else None
    dshort = dname.replace("Domain / ","") if dname else None
    pm = DOMAIN_TAG_TO_PM.get(dname) if dname else None
    mine = any(t["tagId"] in MY_DOMAIN_TAG_IDS for t in dtags)
    return {**f,"dtags":dtags,"mtags":mtags,"mat":mat,"age":age,"expiry":expiry,
            "issues":issues,"dname":dname,"dshort":dshort,"pm":pm,"mine":mine}

ffs = [enrich(f) for f in raw]
total = len(ffs)

# QUALITY
bad_ffs = sorted([f for f in ffs if f["issues"]], key=lambda f: (-len(f["issues"]),-f["age"]))
print(f"## 🔍 Quality — {len(bad_ffs)} FFs with issues (of {total} total)\n")
for f in bad_ffs:
    ctx = " | ".join(filter(None,[*f["issues"],[f["mat"],f["dshort"],f"{f['age']}d"][-3:]]))
    # one liner: issues | maturity | domain | age
    parts = [", ".join(f["issues"])]
    if f["mat"]: parts.append(f["mat"])
    if f["dshort"]: parts.append(f["dshort"])
    parts.append(f"{f['age']}d")
    print(f"- {lnk(f)} — {' | '.join(parts)}")
print(f"\n✅ {total-len(bad_ffs)} FFs look good.\n")

# EXPIRATION
exp = [f for f in ffs if f["expiry"] in ("overdue","warn") and f["dname"]]
overdue = sorted([f for f in exp if f["expiry"]=="overdue"],key=lambda f:-f["age"])
warn = sorted([f for f in exp if f["expiry"]=="warn"],key=lambda f:-f["age"])
print(f"## ⏱️ Expiration — {len(overdue)} overdue, {len(warn)} warnings\n")

def by_pm(lst):
    d = defaultdict(list)
    for f in lst: d[f["pm"] or "?"].append(f)
    for pm in sorted(d):
        print(f"#### {pm}")
        for f in d[pm]:
            print(f"- {lnk(f)} — {f['age']}d | {f['mat'] or 'no maturity'} | {f['dshort']}")

print("### 🔴 Overdue")
by_pm(overdue)
print("\n### 🟡 Warning")
by_pm(warn)

# OWNERSHIP
mine = sorted([f for f in ffs if f["mine"]],key=lambda f:-f["age"])
other = [f for f in ffs if f["dname"] and not f["mine"]]
unattr = sorted([f for f in ffs if not f["dname"]],key=lambda f:-f["age"])
print(f"\n## 👤 Ownership — {total} FFs total\n")
print(f"### Fabien — {len(mine)} FFs")
for f in mine:
    q = "✅" if not f["issues"] else ", ".join(f["issues"])
    print(f"- {lnk(f)} — {f['mat'] or '—'} | {f['age']}d | {f['dshort']} | {q}")
print(f"\n### Other PMs — {len(other)} FFs")
bd = defaultdict(list)
for f in other: bd[f["dshort"]].append(f)
for dom in sorted(bd):
    print(f"#### {dom}")
    for f in sorted(bd[dom],key=lambda f:-f["age"]):
        q = "✅" if not f["issues"] else ", ".join(f["issues"])
        print(f"- {lnk(f)} — {f['mat'] or '—'} | {f['age']}d | {q}")
print(f"\n### ⚠️ Unattributed — {len(unattr)} FFs (no domain tag)")
for f in unattr:
    q = ", ".join(f["issues"]) if f["issues"] else "✅"
    print(f"- {lnk(f)} — {f['mat'] or '—'} | {f['age']}d | {q}")
```

Run with: `python3 /tmp/ff_review.py`

---

## Step 5 — Output format

**Format rules (apply everywhere):**
- Bullet list, one bullet per FF. No tables, no markdown headers for individual FFs.
- Each bullet: `- [key](CC_URL) — <issues or status> | <maturity> | <domain short> | <age>d`
- CC_URL = `https://app.configcat.com/v2/08d9533c-66a6-4893-8f2b-1d7a88dd69ea/08d9533c-6721-492d-88c3-ba1056e00ab8/08dd6234-18c6-43d3-82ea-c626311c5733/08d9533c-673e-403e-82ef-7947ec34195c/<settingId>`
- Domain short: strip `Domain / ` prefix (e.g. `Platform - Community`, `TMS - Indicators`)
- PM: first name only
- Age in days, no decimals
- Keep each bullet to one line — no sub-bullets
- No prose between items

---

### Section 1 — 🔍 Quality (always global)

List every FF with at least one issue. Sorted: most issues first, then by age desc within same count.

```
## 🔍 Quality — N FFs with issues (of M total)

- [ddAgentsApp](CC_URL) — ❌ no domain, ❌ no maturity, ❌ bad desc | — | 61d
- [siteOperations](CC_URL) — ❌ bad desc | beta | Platform - Community | 280d
- [customRoles](CC_URL) — ❌ no maturity | Platform - Community | 57d

✅ N FFs look good.
```

For `no_domain` FFs: call `get-setting-value-v2` on those FFs only to get `creatorEmail`, append `[creator: <email>]` to the bullet.

---

### Section 2 — ⏱️ Expiration (scoped)

Only FFs with a domain tag and `expiry = "overdue"` or `"warn"`. Sorted by age desc within each bucket.

In `all` mode: group by PM name under `### PM name` subheaders.
In `mine` mode: flat list, no grouping.

```
## ⏱️ Expiration — N overdue, M warnings

### 🔴 Overdue

#### Fabien
- [reconnectCompanies](CC_URL) — 138d | to-remove | Platform - Community
- [controlSubcontractorDocuments](CC_URL) — 89d | released | Platform - Community

#### Adam
- [shorterInvoice](CC_URL) — 433d | to-remove | TMS - Taxation

### 🟡 Warning

#### Fabien
- [fleetDocumentsForTrucker](CC_URL) — 82d | no maturity | Platform - Community
```

---

### Section 3 — 👤 Ownership (scoped)

All FFs in scope. Sorted by age desc. Quality issues shown inline.

In `all` mode: group by PM under `### PM name` subheaders; FFs with no PM in `### ⚠️ Unattributed`.
In `mine` mode: group by domain tag.

```
## 👤 Ownership — N FFs

### Fabien — N FFs
- [reconnectCompanies](CC_URL) — to-remove | 138d | ✅
- [siteOperations](CC_URL) — beta | 280d | ❌ bad desc
- [customRoles](CC_URL) — no maturity | 57d | ❌ no maturity

### ⚠️ Unattributed — N FFs
- [ddAgentsApp](CC_URL) — no maturity | 61d | ❌ no domain, ❌ no maturity, ❌ bad desc
```

---



## Notion gap warnings (append to Quality section)

If during Team fetch any of the following are true, add a `⚠️ Notion data gaps` block at the end of the Quality section:

- Team page fetch failed → `⚠️ Could not fetch <Team> team page — ownership may be stale`
- PM field empty on a team page → `⚠️ Missing PM on <Team> team page`
- Tech field empty on a team page → `⚠️ Missing Tech on <Team> team page`
