---
name: saas-valuation-compression
description: >
  SaaS / software valuation compression: ARR or revenue multiples over time, Rule of 40,
  public or late-stage comps. v4.6.6: Web fundamentals + IBKR price for publics. US focus.
  Triggers: valuation compression, ARR multiple, Rule of 40, SaaS multiple, round-to-round.
version: 4.6.8
ecosystem: 4.6.8
metadata:
  tags: [finance, us-stocks, saas, valuation]
  market_scope: US_EQUITIES_ONLY
  role: L2_TOOL
---

# SaaS Valuation Compression · v4.6.6

## Consumer rules

- **Public US ticker:** IBKR price + Web (ARR/rev, growth, FCF margin, guidance).  
- **Private / rounds:** Web funding history only (label uncertainty).  
- No yfinance/funda required.  
- Prefer tables over walls of numbers.

## Framework

1. Multiple timeline (EV/ARR or EV/Rev at key dates)  
2. Compression % peak→now or round→round  
3. Drivers: rates/macro, growth slowdown, margin, narrative, dilution  
4. Rule of 40: growth % + FCF margin %  
5. Public comps band if available  

```text

## L2 confidence (Cog-4 · advisory only)

`confidence` in `### RETURN_BLOCK` is **skill-local deliverable quality**, not user investment confidence.

| Rule | Max grade |
|------|-----------|
| `status: partial` or material `fields_gap` | **B** |
| X/social-only evidence for hard claims | **C** |
| `status: blocked` | no thesis A |
| Complete skill scope + hard sources + no material gaps | **A** allowed (still advisory) |

Default `confidence_scope` for this skill: **valuation**.

Also emit Cog-4 fields when practical: `confidence_scope`, `confidence_basis` (evidence_independence, physical_mechanical, data_gaps_material), `limiting_factors`.

**Never** emit Brain `### CONFIDENCE_BLOCK` or `mode:` — the Central Brain re-grades via §H.6.

### RETURN_BLOCK
skill: saas-valuation-compression
status: ok|partial
ticker: SYM|NAME
confidence: A|B|C
confidence_scope: valuation
confidence_basis:
  evidence_independence: strong|weak|gap
  physical_mechanical: strong|weak|gap
  data_gaps_material: true|false
limiting_factors: []
fields_filled: [multiples_timeline, rule_of_40?]
fields_gap: [...]
artifacts:
  current_multiple: ...
  peak_multiple: ...
  compression_pct: ...
  rule_of_40: ...
  one_liner: "..."
counterfactuals: []
raw_notes: <≤300 words>
```

*v4.6.6 · DATA_PACK consumer · Cog-4 conf advisory · IBKR market-data only*
