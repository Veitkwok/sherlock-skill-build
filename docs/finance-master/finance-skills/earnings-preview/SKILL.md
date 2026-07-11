---
name: earnings-preview
description: >
  Pre-earnings briefing for US stocks: date, consensus, beat/miss history, setup.
  v4.6.6: Brain DATA_PACK + Web/X; IBKR for price reaction context. No yfinance required.
  Triggers: earnings preview, what to expect, consensus estimates, before earnings, whisper.
version: 4.6.8
ecosystem: 4.6.8
metadata:
  tags: [finance, us-stocks, earnings, preview]
  market_scope: US_EQUITIES_ONLY
  role: L2_TOOL
---

# Earnings Preview · v4.6.6

## Consumer rules

- Pack quote + options_summary if present (IV crush risk).  
- **Web:** earnings date, EPS/rev consensus, prior beat rate, guidance snippets.  
- **X (optional):** street narrative / whisper tone.  
- IBKR snapshot for spot + short-term perf.  
- No yfinance/funda/longbridge requirement. Cap ~6–8 tool calls.

## Deliver

| Block | Content |
|-------|---------|
| When | Next report date / BMO/AMC if known |
| Street | EPS & rev consensus; YoY if available |
| History | Last 4–8 quarters beat/miss if available |
| Setup | Price into print, IV if known, key watch items |
| Scenarios | Beat / in-line / miss — qualitative price framing |
| Risks | What would break the setup |

```text

## L2 confidence (Cog-4 · advisory only)

`confidence` in `### RETURN_BLOCK` is **skill-local deliverable quality**, not user investment confidence.

| Rule | Max grade |
|------|-----------|
| `status: partial` or material `fields_gap` | **B** |
| X/social-only evidence for hard claims | **C** |
| `status: blocked` | no thesis A |
| Complete skill scope + hard sources + no material gaps | **A** allowed (still advisory) |

Default `confidence_scope` for this skill: **single_dim**.

Also emit Cog-4 fields when practical: `confidence_scope`, `confidence_basis` (evidence_independence, physical_mechanical, data_gaps_material), `limiting_factors`.

**Never** emit Brain `### CONFIDENCE_BLOCK` or `mode:` — the Central Brain re-grades via §H.6.

### RETURN_BLOCK
skill: earnings-preview
status: ok|partial
ticker: SYM
confidence: A|B|C
confidence_scope: single_dim
confidence_basis:
  evidence_independence: strong|weak|gap
  physical_mechanical: strong|weak|gap
  data_gaps_material: true|false
limiting_factors: []
fields_filled: [date, consensus, history?]
fields_gap: [...]
artifacts:
  earnings_date: ...
  eps_consensus: ...
  rev_consensus: ...
  setup_one_liner: "..."
counterfactuals: []
raw_notes: <≤250 words>
```

Legacy yfinance API notes were moved to `REMOVED (banned yfinance refs)`.

*v4.6.6 · DATA_PACK consumer · Cog-4 conf advisory · IBKR market-data only*
