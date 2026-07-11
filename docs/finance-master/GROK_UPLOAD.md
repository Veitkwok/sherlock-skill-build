# Grok Web upload checklist

`finance-master` is a **Markdown skill pack** for Grok custom Skills.

## Upload set (recommended)

Include:

- `SKILL.md`, `VERSION`, `LAYOUT.md` (optional)
- `sherlock-finance/` (entire)
- `x-advanced-research/`
- `finance-skills/`
- `UZI-Skill/`
- `serenity-skill/`

Optional exclude (smaller zip; local-only):

- `evals/` (contains `run_structural_checks.py` + fixtures — fine locally, not needed at Grok runtime)

**Never** upload `finance-master-auditor` as part of this skill (Hermes ops skill, separate).

## Compliance rules (validated)

| Rule | Status |
|------|--------|
| Every live `SKILL.md` has YAML frontmatter (`name`, `description`, `version`) | Required |
| Product tree is Markdown-first | Required |
| No `plugin.json` / Python scripts inside L2 skill folders | Required |
| No `_quarantine/` directory | Required (deleted) |
| Data plane: IBKR market-data only + Web/X | Product policy |

## Frontmatter minimum

```yaml
---
name: example-skill
description: >
  One or more lines for triggers.
version: 4.6.8
---
```

## Runtime note

Grok loads skills by `SKILL.md` + on-demand `references/`. It does not execute `evals/*.py`.

