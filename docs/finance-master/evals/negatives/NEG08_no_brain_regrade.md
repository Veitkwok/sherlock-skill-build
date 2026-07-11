# NEG08 · intentional fail · L2 RETURN without Brain re-grade

```text
NEG_EXPECT: missing Brain re-grade after L2
NEG_RULE: GP06
```

## MSFT · DCF (broken Cog-4)
**mode_effective:** standard

### L0 Observations
- last 420 (source: IBKR)
- FCF abstract (source: WEB)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| L2 A is final | invalid | must re-grade |

### INVOKE
```text
### INVOKE
skill: finance-master/finance-skills/company-valuation
intent: DCF
ticker: MSFT
```

### RETURN_BLOCK
```text
### RETURN_BLOCK
skill: company-valuation
status: ok
ticker: MSFT
confidence: A
confidence_scope: valuation
confidence_basis:
  evidence_independence: strong
  physical_mechanical: strong
  data_gaps_material: false
limiting_factors: []
fields_filled: [dcf]
fields_gap: []
artifacts:
  dcf_base_per_share: 405
```

### CONFIDENCE_BLOCK
grade: A
mode: standard
dims:
  evidence_independence: strong
  falsification_rigor: strong
  assumption_audit: strong
  physical_mechanical: strong
  layer_integrity: strong
limiting: []
verification_density: "Copied L2 A as user grade without Cog-4 advisory log markers."
independent_chains:
  - "IBKR: last"
  - "WEB: FCF"
  - "MODEL: DCF"

### CHALLENGE_NODES
- id: CN1
  layer: L2
  claim: "DCF base fine"
  assumption: "FCF durable"
  what_would_falsify: "FCF collapse"
  conf_dim_link: physical_mechanical
- id: CN2
  layer: conf_dim
  claim: "A OK"
  assumption: "L2 sufficient"
  what_would_falsify: "§H.6 re-grade required"
  conf_dim_link: layer_integrity

METHOD_CARDS_LOADED: [M05]
