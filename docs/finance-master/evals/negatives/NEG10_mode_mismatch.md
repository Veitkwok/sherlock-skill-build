# NEG10 · intentional fail · conf mode ≠ mode_effective

```text
NEG_EXPECT: conf mode mismatch
NEG_RULE: GP02
```

## NVDA · lite (broken mode field)
**mode_effective:** lite

### L0 Observations
- last 128.50 (source: IBKR)
- X heat (source: X)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| mode fields consistent | invalid | must fail |

### Kill condition
Break 124.80.

### CONFIDENCE_BLOCK
grade: B
mode: standard
dims:
  evidence_independence: weak
  falsification_rigor: strong
  assumption_audit: strong
  physical_mechanical: strong
  layer_integrity: strong
limiting: [evidence_independence]
verification_density: "mode: standard while mode_effective lite."
independent_chains:
  - "IBKR: last"
  - "X: heat"

### CHALLENGE_NODES
- id: CN1
  layer: L2
  claim: "mode OK"
  assumption: "fields independent"
  what_would_falsify: "mode equality check"
  conf_dim_link: layer_integrity

METHOD_CARDS_LOADED: []
method_cards_skipped: lite
