# GP01 sample agent output (structural gold · synthetic analysis)

```text
standard mode
```

## PLTR · Deep + buy framing
**mode_effective:** standard  
**path:** deep-analysis + §6 + §10  
**DATA_PACK.kind:** DEEP

### L0 Observations
- last 28.40 +1.97% d/d; ADV strong (source: IBKR)
- FCF positive last two quarters abstract (source: WEB)
- Next earnings ~2026-08-05 (source: WEB)
- ARK add chatter (source: X)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| Commercial growth remains elevated | weakened if Aug print <20% | thesis load-bearing |

### Hypotheses (multi-cause)
| ID | Streams (&) | Status | Kill | Occam rank |
|----|-------------|--------|------|------------|
| H1 | Gov AI demand & commercial expansion & multiple compression relief | live | growth <20% | 1 |
| H2 | Narrative only; cash conversion stalls | live | FCF turns neg | 2 |
| H3 | Distribution into strength | live | Form 4 cluster sales | 3 |

### INVOKE
```text
### INVOKE
skill: finance-master/UZI-Skill/deep-analysis
intent: full deep + buy framing support
ticker: PLTR
contract_id: 999001
budget: { max_new_tool_calls: 6, may_fetch: false }
data_pack: |
  kind: DEEP
  asof: 2026-07-11T16:00:00Z
  mode_effective: standard
  ticker: PLTR
  contract_id: 999001
  ibkr_available: true
  sources_used: [IBKR, WEB, X]
  quote:
    last: 28.40
    prior_close: 27.85
    high: 28.85
    low: 27.70
    volume: 41000000
    avg_90d_usd_volume: 8.5e8
    w52_high: 36.00
    w52_low: 18.50
  fundamentals_web:
    fcf_positive_last_2q: true
    commercial_growth_yoy_cite: 0.34
    quality: estimate
  catalysts_web:
    next_earnings: 2026-08-05
  social_x:
    heat: medium
    posts: [x1, x2]
  gaps: [full_segment_model, panel36]
return_schema: RETURN_BLOCK
```

### RETURN_BLOCK
```text
### RETURN_BLOCK
skill: finance-master/UZI-Skill/deep-analysis
status: partial
ticker: PLTR
confidence: A
confidence_scope: skill_local
confidence_basis:
  evidence_independence: strong
  physical_mechanical: strong
  data_gaps_material: true
limiting_factors: ["full_segment_model", "panel36", "pre-print falsification thin"]
fields_filled: [D0, D1, D2, D8, D11, D12, D14, D15, D16]
fields_gap: [full_segment_model, panel36, D17]
artifacts:
  dcf_fair: null
  comps_range: [24, 32]
  trap_level: green
  panel_mode: top10
  one_liner: "Constructive into print; growth/FCF confirmation required"
counterfactuals:
  - {signal: "commercial growth <20%", window: "2026-08 earnings"}
  - {signal: "FCF turns negative", window: "next 10-Q"}
raw_notes: L2 advisory A with material gaps — Brain must re-grade ≤B for user thesis.
```

L2_CONF_ADVISORY: A (deep-analysis, scope=skill_local)
BRAIN_REGRADE: B (reason: data_gaps_material + weak pre-print falsification; §H.6)

### L1–L3 Inference
[L1] Tape liquid via ADV (IBKR).  
[L2] Growth story requires print confirmation (assumption: guidance hold).  
[L3] Buy-the-dip only if Aug confirms.

### Falsification notes
Stress: growth −10pp → H1 weakens; no evidence yet of FCF collapse in fixture.

### CONFIDENCE_BLOCK
grade: B
mode: standard
dims:
  evidence_independence: strong
  falsification_rigor: weak
  assumption_audit: strong
  physical_mechanical: strong
  layer_integrity: strong
limiting: [falsification_rigor]
verification_density: "IBKR tape + WEB cash/growth abstract; L2 A not adopted (gaps). Limited active stress on margin path pre-print."
independent_chains:
  - "IBKR: price/ADV/52w"
  - "WEB: FCF positive abstract"
  - "WEB: earnings calendar + growth print history abstract"

### CHALLENGE_NODES
- id: CN1
  layer: L2
  claim: "Commercial growth remains high enough to support multiple"
  assumption: "Aug print growth >= 20%"
  what_would_falsify: "WEB earnings release growth <20% in 2026-08 window"
  conf_dim_link: falsification_rigor
- id: CN2
  layer: conf_dim
  claim: "Physical cash support holds"
  assumption: "FCF stays non-negative"
  what_would_falsify: "WEB 10-Q CFO < 0 next print"
  conf_dim_link: physical_mechanical

### §6 Veto
VIX/liquidity from fixture: pass (synthetic). Trap: N/A (green).

### §10 Direct judgment
1. Capital: conditionally OK given ADV (IBKR).  
2. Catalyst: Aug print primary.  
3. Counterfactuals: growth miss; FCF break; break of 27.70 low (IBKR).  
4. Position framework only: max$loss / stop%.  
Conclusion: not a naked buy signal; B-grade constructive into print.

METHOD_CARDS_LOADED: [M05, M01]
