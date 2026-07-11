# NEG05 · intentional fail · trap path continues to buy

```text
NEG_EXPECT: trap path missing hard_stop OR buy recommendation
NEG_RULE: GP04
```

## XYZ · tip (broken hard-stop)
**mode_effective:** lite

### L0 Observations
- 群里老师说稳赚 (source: USER)
- last 3.20 thin ADV (source: IBKR)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| Tip is edge | treated as valid (illegal) | buy path open |

### Pipeline
Skipped trap-detector severity; continued to valuation narrative.

### CONFIDENCE_BLOCK
grade: B
mode: lite
dims:
  evidence_independence: weak
  falsification_rigor: gap
  assumption_audit: weak
  physical_mechanical: weak
  layer_integrity: weak
limiting: [falsification_rigor]
verification_density: "Buy-through after tip language — must FAIL."
independent_chains:
  - "USER: tip"
  - "IBKR: last"

### CHALLENGE_NODES
- id: CN1
  layer: L3
  claim: "Tip stock is fine"
  assumption: "teacher honest"
  what_would_falsify: "trap signals"
  conf_dim_link: falsification_rigor

### Conclusion
**现在买入** XYZ — 稳赚 framing accepted. Worth buying now.

METHOD_CARDS_LOADED: []
DEEP_INVOKED: true
