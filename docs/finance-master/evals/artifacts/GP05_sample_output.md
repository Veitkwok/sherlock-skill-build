# GP05 sample agent output (structural gold · synthetic analysis)

```text
max mode
```

## Discovery · AI infrastructure chokepoints (US)
**mode_effective:** max  
**mode_profile:** max  
**path:** x-advanced-research → serenity-skill → deep-analysis×3 (cap)

### Chain order (Brain-owned)
1. x-advanced-research → shortlist (US only)
2. serenity-skill → bottleneck scores
3. deep-analysis × ≤3 on recommended names

### Dropped (non-US)
- FAKEHK — us_listed=false → **excluded** (source: FIXTURE)

### Pre-deep shortlist (grade ceiling ≤B)
| Symbol | Bottleneck | Score | pre_deep_grade | US |
|--------|------------|------:|:--------------:|:--:|
| VRT | power/thermal | 82 | B | ✓ |
| FIX | install capacity | 78 | B | ✓ |
| AMAT | tool lead times | 70 | B | ✓ |

deep_count: 3  
deep_tickers: [VRT, FIX, AMAT]

### INVOKE · deep×1 VRT (shape; others analogous)
```text
### INVOKE
skill: finance-master/UZI-Skill/deep-analysis
intent: DEEP pack bottleneck diligence
ticker: VRT
contract_id: synth
budget: { max_new_tool_calls: 8, may_fetch: false }
data_pack: |
  IBKR: last=95.0 ADV=high
  theme: data center power/thermal
return_schema: RETURN_BLOCK
```

### RETURN_BLOCK · VRT (advisory L2 conf)
```text
### RETURN_BLOCK
skill: finance-master/UZI-Skill/deep-analysis
status: partial
ticker: VRT
confidence: A
confidence_scope: skill_local
confidence_basis:
  evidence_independence: weak
  physical_mechanical: strong
  data_gaps_material: true
limiting_factors: ["full_dcf gap", "panel36 gap"]
fields_filled: [quote, theme]
fields_gap: [full_dcf, panel36]
artifacts: { bottleneck: "power delivery / thermal" }
counterfactuals: ["capex pause in hyperscale"]
raw_notes: L2 conf=A advisory only; status partial + gaps → Brain ≤B (§H.6).
```

L2_CONF_ADVISORY: A (deep-analysis, scope=skill_local)
BRAIN_REGRADE: B (reason: partial + material gaps + pre/post deep screen ceiling)


### Brain merge · ranked names (after re-grade)
| Rank | Ticker | View | Brain grade | Notes |
|-----:|--------|------|:-----------:|-------|
| 1 | VRT | Prefer research queue | B | Power/thermal scarce layer |
| 2 | FIX | Prefer research queue | B | Capacity bottleneck |
| 3 | AMAT | Watch / cyclical | B | Tool cycle risk |

### L0 Observations (aggregate)
- VRT/FIX/AMAT US-listed with IBKR min quotes (source: IBKR)
- Bottleneck scores from serenity synth (source: WEB/SKILL)
- X evidence ids x_a1..x_a3 as discovery leads only (source: X)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| Hyperscale power/thermal remains scarce 12–24m | valid until capex pause evidence | ranks VRT/FIX high |

### CONFIDENCE_BLOCK
grade: B
mode: max
dims:
  evidence_independence: weak
  falsification_rigor: strong
  assumption_audit: strong
  physical_mechanical: strong
  layer_integrity: strong
limiting: [evidence_independence]
verification_density: "Screen + partial deep packs; pre-deep and post-merge grades capped at B. L2 A not adopted as Brain A."
independent_chains:
  - "IBKR: min quotes ADV for deep names"
  - "WEB/SKILL: serenity bottleneck scores"
  - "X: discovery lead cluster (≤1 chain)"

### CHALLENGE_NODES
- id: CN1
  layer: L2
  claim: "Power/thermal remains the scarcest AI infra layer among shortlist"
  assumption: "hyperscale capex does not pause"
  what_would_falsify: "WEB: multi-hyperscaler capex cut guidance within 2 quarters"
  conf_dim_link: falsification_rigor
- id: CN2
  layer: conf_dim
  claim: "Brain grade B is correct ceiling pre full filings pack"
  assumption: "fields_gap on DCF/panel remains"
  what_would_falsify: "Full DEEP pack closes fields_gap with ≥3 Tier-A chains per name"
  conf_dim_link: evidence_independence
- id: CN3
  layer: L1
  claim: "FAKEHK correctly excluded as non-US"
  assumption: "us_listed flag trusted"
  what_would_falsify: "Primary listing evidence shows US primary listing for that symbol"
  conf_dim_link: layer_integrity

### Conclusion
Max discovery DAG completed within deep×3. US-only. Pre-deep ≤B. Brain re-grade after L2. Prefer VRT/FIX for further work; not execution orders.

METHOD_CARDS_LOADED: [M05, M03, M01, M11]
deep_count: 3
