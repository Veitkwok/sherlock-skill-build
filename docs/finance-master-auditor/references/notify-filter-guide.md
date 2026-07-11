# Notify filter guide · finance-master-auditor v4.6.8

Used by `skill-watchdog.py` and by Hermes when reading `skill-watch-diff.json`.

## Goal

Ping the human **only** when an upstream change could justify a **manual** finance-master upgrade.

## Meaningful → notify

| Pattern | Why |
|---------|-----|
| `**/SKILL.md` | Skill logic / triggers / workflow |
| `**/references/**/*.md` | Methodology the agent loads |
| New skill folder with SKILL.md | Possible new capability |
| Removal of a product skill path | Inventory change |

## Trivial → do not notify

| Pattern | Why |
|---------|-----|
| `**/*.{html,css,svg,png,jpg,gif}` | Formatting / visual assets (e.g. UZI HTML reports) |
| `**/assets/**`, `**/personas/**` | Non-product for Grok Markdown pack |
| `**/scripts/**/*.py`, `run.py` | Script era; product does not execute |
| `plugin.json`, lockfiles, `.github/` | Packaging / CI |
| `README.md` only | Docs noise |
| Changes only under banned skills (`lhb-analyzer`, yfinance, …) | Must not re-enter product |

## Structure check (before recommending upgrade)

Ask: if we merged this into finance-master **today**, would Brain/L2 behavior change?

| Touches | Recommendation |
|---------|----------------|
| Upstream deep-analysis HTML only | Ignore (trivial) |
| Upstream deep-analysis SKILL.md | Notify — human reviews (local rewrite is heavy) |
| finance-skills company-valuation references | Notify — human may cherry-pick |
| New unrelated crypto skill | Notify optional / skip product import |

## Human upgrade (not auditor)

1. Read notify summary  
2. Diff upstream vs local  
3. Manually edit finance-master  
4. Bump VERSION if needed  
5. Re-run `evals/run_structural_checks.py`  

Auditor **never** performs steps 3–5 automatically.

---

*Aligned with product 4.6.8*
