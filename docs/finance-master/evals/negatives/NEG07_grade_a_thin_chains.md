# NEG07 · intentional fail · grade A with thin independent_chains

```text
NEG_EXPECT: grade A with only N independent_chains
NEG_RULE: GP01
```

## PLTR · Deep (broken A-grade)
**mode_effective:** standard

### L0 Observations
- last 28.40 (source: IBKR)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| Single chain is enough for A | invalid | must fail |

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
verification_density: "Claims A with a single chain — illegal."
independent_chains:
  - "IBKR: last only"

### CHALLENGE_NODES
- id: CN1
  layer: L2
  claim: "A is fine"
  assumption: "one chain"
  what_would_falsify: "need ≥3 chains for A"
  conf_dim_link: evidence_independence
- id: CN2
  layer: conf_dim
  claim: "Dims strong"
  assumption: "vibe"
  what_would_falsify: "dim audit"
  conf_dim_link: assumption_audit

METHOD_CARDS_LOADED: []
