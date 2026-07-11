---
name: earnings-recap
description: >
  Post-earnings recap for US stocks: beat/miss, reaction, guidance, takeaways.
  v4.6.6: Web + X + IBKR price reaction; no yfinance required.
  Triggers: earnings recap, did they beat, post-earnings, surprise, how did earnings go.
version: 4.6.8
ecosystem: 4.6.8
metadata:
  tags: [finance, us-stocks, earnings, recap]
  market_scope: US_EQUITIES_ONLY
  role: L2_TOOL
---

# Earnings Recap · v4.6.6

## Consumer rules

- Web: actual EPS/rev vs estimate, guidance, call highlights.  
- IBKR: spot vs prior close / session move; optional history around print.  
- X: immediate narrative (optional).  
- No yfinance install path.

## Deliver

1. Headline beat/miss (EPS, revenue) with magnitudes  
2. Stock reaction (intraday / 1d if known)  
3. Guidance vs prior / street  
4. Three takeaways + three open questions  
5. What changes for thesis (if pack/deep context exists)

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
skill: earnings-recap
status: ok|partial
ticker: SYM
confidence: A|B|C
confidence_scope: single_dim
confidence_basis:
  evidence_independence: strong|weak|gap
  physical_mechanical: strong|weak|gap
  data_gaps_material: true|false
limiting_factors: []
fields_filled: [actuals, reaction, guidance?]
fields_gap: [...]
artifacts:
  eps_actual_vs_est: ...
  rev_actual_vs_est: ...
  price_reaction_pct: ...
  takeaways: [...]
counterfactuals: []
raw_notes: <≤250 words>
```

*v4.6.6 · DATA_PACK consumer · Cog-4 conf advisory · IBKR market-data only*
