---
name: finance-master
description: >
  US equity research unified entry for Grok (Web / Build). On any US stock /
  finance intent, load sherlock-finance as the Central Brain (L1 v4.6.8 Cog-4).
  Modes lite|standard|max; conf v3.0; Method Library; L2 conf; DATA_PACK; Val-1;
  LLM-judge rubric; IBKR market-data only. L0 detects and delegates only.
version: 4.6.8
ecosystem: 4.6.8
author: Veit Kwok
license: MIT
metadata:
  tags: [finance, us-stocks, valuation, analysis, research, orchestrator, grok, ibkr]
  market_scope: US_EQUITIES_ONLY
  related_skills:
    - finance-master/sherlock-finance
    - finance-master/UZI-Skill/deep-analysis
    - finance-master/x-advanced-research
    - finance-master/serenity-skill
---

# Finance Master · L0 Entry v4.6.8

> **Your only job:** detect a US-equity / finance request → **load and obey** `finance-master/sherlock-finance` (the Central Brain).  
> Pass through any user mode phrase (`lite mode` / `standard mode` / `max mode`) unchanged.  
> You do **not** pick L2 tools, fetch market data, or write investment conclusions at L0.

---

## Scope (hard)

| In scope | Out of scope |
|----------|----------------|
| US listed equities / ETFs | A-share, HK LHB/游资, multi-market microstructure |
| Grok Web + Grok Build | Hermes opencli readers as primary path |
| Research, valuation, catalysts, safety | Trade execution / order staging (never in-tree) |

If the user asks non-US markets: state **v4.6.x is US-only** and stop non-US pipelines.

### Runtime modes (user text → Brain)

| Phrase | Profile |
|--------|---------|
| `lite mode` / `LITE` | Short-horizon tape + X; conf always on |
| `standard mode` / `STD` (default if omitted) | 1–3m research |
| `max mode` / `MAX` | Screening / deep alpha / multi-tool |

L0 does not interpret modes beyond ensuring Brain is loaded with the user message intact.

---

## Trigger (any layer hits → load Brain)

### L1 · Ticker / name
US tickers (`AAPL`, `NVDA`, `PLTR`, …) and US company names.

### L2 · Finance intent
分析 / 估值 / DCF / 财报 / 值得买 / 走势 / 期权 / SEPA / Serenity / 卡点 / X 情绪 / …

### L3 · Dialogue context
Follow-ups on a prior US name → load Brain (reuse `SESSION_CACHE`).

---

## Load instruction

1. Open skill: **`finance-master/sherlock-finance`**
2. Execute only Brain protocols. L0 ends after Brain load.

Do **not** call L2 or IBKR/Web/X from L0.

---

## Active inventory (filesystem · S6)

**Exactly 20** live `SKILL.md` files (this tree):

| Role | Paths | n |
|------|-------|--:|
| L0 | `SKILL.md` | 1 |
| L1 Brain | `sherlock-finance/` | 1 |
| Discovery | `x-advanced-research/`, `serenity-skill/` | 2 |
| UZI | `deep-analysis`, `investor-panel`, `trap-detector` | 3 |
| US tools | `company-valuation`, `earnings-preview`, `earnings-recap`, `estimate-analysis`, `sepa-strategy`, `options-payoff`, `stock-liquidity`, `stock-correlation`, `finance-sentiment`, `etf-premium`, `saas-valuation-compression`, `startup-analysis`, `hormuz-strait` | 13 |
| **Total** | | **20** |

### Banned (do not load · not in tree)

Full list: `finance-master-auditor/references/banned-patterns.yaml` (Hermes ops package).

- `lhb-analyzer`, China 游资 / 龙虎榜 pipelines  
- `yfinance-data`, `funda-data`  
- Hermes readers: twitter/discord/telegram/linkedin/tradingview/opencli  
- Legacy deep refs (task2.5, old dim scoring, multi-market fin-methods)

Layout map: `LAYOUT.md` · Grok upload: `GROK_UPLOAD.md`

---

## Architecture

```
L0  finance-master/SKILL.md          ← trigger only
        │
        ▼
L1  sherlock-finance/                ← sole orchestrator
        │ §0 cache · §D IBKR→Web/X · §9 route · §H handoff
        ▼
L2  18 execution skills (active only)
    finance-skills/ · UZI-Skill/ · serenity-skill/ · x-advanced-research/
```

**Data plane:** Interactive Brokers MCP (Tier-1 **market structure only**) → Web / X (Tier-2).  
**IBKR redline:** never orders, order instructions, positions, balances, trades, or account management — even if the user asks to stage a trade.  
**Banned primary stacks:** longbridge, yfinance skill, funda skill, Hermes readers.

**Discovery chain:** x-advanced-research → serenity-skill → deep-analysis×≤3 (Brain-owned).

---

## Version

- Ecosystem **4.6.8** — quarantine deleted; bans in auditor; Grok layout freeze on watcher folders

---

*v4.6.8 — no _quarantine; LAYOUT/GROK_UPLOAD; IBKR research-only; 20 skills*
