# Cron job diagnosis · skill-watchdog (v4.6.8 monitor-only)

## Current policy

- Cron runs **detect/classify only** — no import, no patch, no purge.  
- Notify human only when `skill-watch-diff.json` has `"notify": true` (meaningful skill logic).  
- Auditor version = product version = **4.6.8**.

## Root causes found (historical — pre-fix)

### 1. Auto-import on every change (destructive)

**Symptom:** Cron “succeeds” but local UZI/serenity product rewrites disappear.

**Cause:** Old `skill-watchdog.py` always imported on SHA change. Config had:

- `UZI-Skill.purge_on_sync: true` → wipes entire `UZI-Skill/` then re-copies upstream  
- `serenity-skill.purge_on_sync: true` → same  
- `lhb-analyzer` still in import list → reintroduces banned A-share skill  

**Fix:** Default `--mode detect` (no import). Apply only after audit. UZI apply never purges protected skills; `lhb-analyzer` banned.

### 2. Missing `skill-watch-diff.json` contract

**Symptom:** Auditor SKILL Step 1 expects `diff_report_path` / `~/.hermes/data/skill-watch-diff.json` but old script never wrote a structured report (only printed stdout + state).

**Fix:** Always write `skill-watch-diff.json` with repo statuses, strategy hints, banned skips.

### 3. Minimal cron PATH → `git` not found

**Symptom:** Non-interactive cron fails with empty output or git errors.

**Cause:** Cron often sets `PATH=/usr/bin:/bin` without Homebrew git, or no `git` at all.

**Fix:** Explicit `which git` check; clear ERROR + exit code 2; write error into diff JSON. Cron should set:

```bash
PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin
```

### 4. Config / HOME assumptions

**Symptom:** “No repos configured” or missing paths when HOME differs.

**Cause:** Hardcoded `~/.hermes/...` without expanduser on all paths; missing config file.

**Fix:** `expanduser` + env overrides (`SKILL_WATCH_CONFIG`, etc.); missing config → exit 2 + error report.

### 5. Exit code always 0

**Symptom:** Cron marks job success even when all remotes error.

**Fix:** Exit `1` if any repo errors; `2` for config/git missing; `0` only when detection completed cleanly.

### 6. LLM vs script split

**Symptom:** Cron only runs Python; Telegram audit never runs if Hermes agent step fails after watchdog.

**Note:** Watchdog is detection only. Full audit (PATCH/NOTIFY/Telegram) is still the Hermes agent skill. Cron should:

1. `skill-watchdog.py --mode detect`  
2. If summary.updated > 0 → trigger finance-master-auditor agent with diff path  

---

## Recommended Hermes cron

```bash
#!/bin/bash
set -euo pipefail
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin"
export HOME="${HOME:-/home/hermes}"
cd "$HOME/.hermes/skills/finance-master-auditor/scripts"
/usr/bin/python3 skill-watchdog.py
# Exit 0 = monitor ok
# If jq -e '.notify == true' ~/.hermes/data/skill-watch-diff.json → message user
# Never auto-merge into finance-master
```

---

## Runtime simulation checklist

| Test | Expected |
|------|----------|
| `python3 skill-watchdog.py --mode detect` | Writes diff; no tree mutation |
| Missing git | exit 2, diff status error |
| Missing config | exit 2 |
| Unchanged SHAs | status unchanged |
| Updated SHA | status updated + strategy_hint NOTIFY/PATCH |

---

*Diagnosed 2026-07-12 against live ~/.hermes config*
