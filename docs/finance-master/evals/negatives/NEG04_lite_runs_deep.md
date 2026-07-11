# NEG04 · intentional fail · lite runs deep-analysis

```text
NEG_EXPECT: lite path appears to run deep
NEG_RULE: GP02
```

## NVDA · lite (broken allowlist)
**mode_effective:** lite

### L0 Observations
- last 128.50 (source: IBKR)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| Deep allowed in lite | invalid | must fail |

### Pipeline
Invoked deep-analysis full D0–D19 and investor-panel 36 under lite mode.

### CONFIDENCE_BLOCK
grade: B
mode: lite
dims:
  evidence_independence: weak
  falsification_rigor: weak
  assumption_audit: strong
  physical_mechanical: strong
  layer_integrity: strong
limiting: [evidence_independence]
verification_density: "Illegal multi-deep under lite."
independent_chains:
  - "IBKR: last"

### CHALLENGE_NODES
- id: CN1
  layer: L2
  claim: "Deep OK in lite"
  assumption: "allowlist ignored"
  what_would_falsify: "mode allowlist check"
  conf_dim_link: layer_integrity

METHOD_CARDS_LOADED: []
