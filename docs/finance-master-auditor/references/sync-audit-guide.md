# Sync audit guide · deprecated automation

> **v4.6.8 policy change:** finance-master-auditor no longer auto-merges upstream.  
> Use **`notify-filter-guide.md`** + **`skill-watchdog.py`** (monitor only).

## What the auditor does now

1. Detect SHA changes on finance-skills / UZI-Skill / serenity-skill  
2. Classify **meaningful** vs **trivial**  
3. Set `notify: true|false` in `skill-watch-diff.json`  
4. Human upgrades finance-master manually when notified  

## What it must not do

- AUTO / PATCH / IMPORT / purge_on_sync  
- Overwrite `UZI-Skill/deep-analysis` or other product rewrites  
- Reintroduce banned skills (see `banned-patterns.yaml`)  

## Manual upgrade checklist (human)

1. Read notify summary  
2. Diff upstream cache vs local product path  
3. Cherry-pick methodology only  
4. Preserve IBKR data plane, Cog-4 conf, US monoculture  
5. `python3 finance-master/evals/run_structural_checks.py`  
6. Bump `finance-master/VERSION` if product changed  

Historical decision trees (AUTO/PATCH/…) are retired and must not be re-enabled on cron.

