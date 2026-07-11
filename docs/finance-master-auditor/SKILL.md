---
name: finance-master-auditor
description: >
  Monitor-only GitHub watcher for finance-master v4.6.8. Detects upstream updates to
  finance-skills, UZI-Skill, and serenity-skill; classifies meaningful vs trivial;
  notifies for skill-logic upgrades only. Never auto-imports or patches finance-master.
  Hermes cron tool — not a Grok Web skill.
version: 4.6.8
ecosystem: 4.6.8
author: Veit Kwok
license: MIT
metadata:
  hermes:
    tags: [finance, devops, monitor, notify, cron]
    trigger_keywords:
      - 检查上游
      - 同步监控
      - skill 更新
      - 审计监控
---

# Finance Master Auditor · v4.6.8 (monitor & notify)

> **Monitor only.** You do **not** upgrade finance-master.  
> **Human** performs all upgrades after a **meaningful** notify.  
> Version aligned with product: **4.6.8**.

---

## Role (hard limits)

| Do | Do not |
|----|--------|
| Watch 3 GitHub repos | AUTO import / PATCH / purge local trees |
| Classify meaningful vs trivial | Merge upstream into product blindly |
| Notify on skill-logic upgrades | Notify on HTML/assets/script noise |
| Keep structure awareness | Execute complex multi-step upgrades |

---

## Watched upstreams

| Repo | Local product path (internals frozen) |
|------|----------------------------------------|
| himself65/finance-skills | `finance-master/finance-skills/` |
| wbh604/UZI-Skill | `finance-master/UZI-Skill/` |
| muxuuu/serenity-skill | `finance-master/serenity-skill/` |

Local-only (not watched for auto-notify): `sherlock-finance/`, `x-advanced-research/`, `evals/`, L0 `SKILL.md`.

---

## Notification filter

### Notify (meaningful)

Any of:

- `SKILL.md` content change  
- `references/**/*.md` methodology change  
- New/removed product-relevant skill directory  
- Logic that would affect how analysis is done if merged  

→ Message: *meaningful update; manual finance-master upgrade recommended* + file/skill list.

### Do not notify (trivial)

Only:

- HTML / CSS / SVG / PNG / assets / personas avatars  
- `scripts/**/*.py`, `run.py`, `plugin.json`, package locks  
- `.github/`, LICENSE, README-only  
- Agent YAML configs without SKILL/references delta  
- Banned skills only (e.g. upstream `lhb-analyzer` churn)  

→ Silent / log as `trivial` in diff JSON.

---

## Product structure awareness (high level)

```text
finance-master/                    # product 4.6.8 · Grok skill pack
├── SKILL.md                       # L0
├── sherlock-finance/              # L1 Brain (local)
├── x-advanced-research/           # local
├── finance-skills/                # ★ watched · frozen layout
├── UZI-Skill/                     # ★ watched · frozen layout (3 live skills)
├── serenity-skill/                # ★ watched · frozen layout
└── evals/                         # local tests only
```

- Live skills: **20**  
- Bans: `references/banned-patterns.yaml`  
- Layout: product `LAYOUT.md` / `GROK_UPLOAD.md`  
- Data plane: IBKR market-data only + Web/X · no yfinance/lhb/order APIs  

Use this map to judge whether an upstream file change matters to the **product** (e.g. HTML report scripts in UZI do **not**).

---

## Cron workflow

```bash
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin"
cd ~/.hermes/skills/finance-master-auditor/scripts
python3 skill-watchdog.py
# reads:  ~/.hermes/config/skill-watch.json
# writes: ~/.hermes/data/skill-watch-diff.json
# stdout: diff_report_path=...  notify=true|false
```

| `notify` | Action |
|----------|--------|
| `false` | Optional quiet log; **no** user ping |
| `true` | Telegram / message user with `telegram_hint` from diff JSON |

**Never** run import/apply automation.

---

## Manual / agent steps when notify=true

1. Read `skill-watch-diff.json` → `repos[].classification`  
2. Summarize meaningful files & skills for the user  
3. **Stop.** Wait for user to upgrade finance-master themselves  
4. Do not modify `finance-master` unless the user explicitly orders a manual upgrade task  

---

## Key files

| Path | Purpose |
|------|---------|
| `scripts/skill-watchdog.py` | Monitor + classify + write diff |
| `references/banned-patterns.yaml` | Ban signatures |
| `references/skill-registry.yaml` | Live 20-skill map |
| `references/notify-filter-guide.md` | Meaningful vs trivial rules |
| `references/skill-watch.config.example.json` | Config sample |
| `references/cron-diagnosis.md` | PATH / git / exit codes |

---

## Version

**4.6.8** — same as `finance-master/VERSION`.

---

*v4.6.8 · monitor & notify only · no auto-upgrade*
