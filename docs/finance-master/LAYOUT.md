# finance-master · Layout (v4.6.8+)

Grok Web skill tree + local evals. Hermes GitHub watcher targets three frozen folders.

## Top-level (do not rename watcher targets)

```text
finance-master/
├── SKILL.md                 # L0 entry (Grok)
├── VERSION                  # product version (auditor may bump on sync)
├── LAYOUT.md                # this file
├── GROK_UPLOAD.md           # what to upload to Grok Web
├── sherlock-finance/        # L1 Central Brain (local product)
├── x-advanced-research/     # L2 X discovery (local product)
├── finance-skills/          # ★ Hermes-watched · do not restructure internals
├── UZI-Skill/               # ★ Hermes-watched · do not restructure internals
├── serenity-skill/          # ★ Hermes-watched · do not restructure internals
└── evals/                   # local Val-1 suite (Python OK) · optional for Grok
```

## Hermes isolation

| Folder | Upstream | Auditor policy |
|--------|----------|----------------|
| `finance-skills/` | himself65/finance-skills | PATCH / strip banned |
| `UZI-Skill/` | wbh604/UZI-Skill | NOTIFY (local rewrites); never purge blind |
| `serenity-skill/` | muxuuu/serenity-skill | NOTIFY |

Internal layouts of the three watched folders are **frozen** for `finance-master-auditor` automation.

## Deleted

| Path | When | Replacement |
|------|------|-------------|
| `_quarantine/` | 2026-07-12 | `finance-master-auditor/references/banned-patterns.yaml` |

## Counts

- Live `SKILL.md`: **20**
- L0 1 + L1 1 + L2 18

## Local-only

- `evals/` — structural checks, fixtures, LLM-judge (not required for Grok runtime)
- Sibling package `docs/finance-master-auditor/` — Hermes ops only

