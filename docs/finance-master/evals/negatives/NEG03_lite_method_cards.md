# NEG03 · intentional fail · lite loads method cards

```text
NEG_EXPECT: lite must not load method cards
NEG_RULE: GP02
```

## NVDA · lite tape (broken §M)
**mode_effective:** lite

### L0 Observations
- last 128.50 (source: IBKR)
- X heat cluster (source: X)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| HL holds | valid | tape |

### Kill condition
Break 124.80.

### CONFIDENCE_BLOCK
grade: B
mode: lite
dims:
  evidence_independence: weak
  falsification_rigor: strong
  assumption_audit: strong
  physical_mechanical: strong
  layer_integrity: strong
limiting: [evidence_independence]
verification_density: "IBKR + X; illegal card load in lite."
independent_chains:
  - "IBKR: snapshot"
  - "X: cluster"

### CHALLENGE_NODES
- id: CN1
  layer: L2
  claim: "HL holds"
  assumption: "support 124.80"
  what_would_falsify: "print <124.80"
  conf_dim_link: physical_mechanical

METHOD_CARDS_LOADED: [M01, M05, M12]
