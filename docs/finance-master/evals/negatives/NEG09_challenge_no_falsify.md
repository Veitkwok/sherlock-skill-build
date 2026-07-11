# NEG09 · intentional fail · challenge node missing what_would_falsify

```text
NEG_EXPECT: missing what_would_falsify
NEG_RULE: GP03
```

## AAPL · swing (broken challenge nodes)
**mode_effective:** standard

### L0 Observations
- last 190 above ma50 (source: IBKR)
- autumn catalyst (source: WEB)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| ma50 holds | valid | base |

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
verification_density: "Challenge nodes lack falsifiers."
independent_chains:
  - "IBKR: MA structure"
  - "WEB: catalysts"
  - "WEB: margins"

### CHALLENGE_NODES
- id: CN1
  layer: L2
  claim: "ma50 support holds"
  assumption: "trend intact"
  conf_dim_link: physical_mechanical
- id: CN2
  layer: assumption
  claim: "product cycle helps"
  assumption: "launch happens"
  conf_dim_link: falsification_rigor

METHOD_CARDS_LOADED: [M01]
