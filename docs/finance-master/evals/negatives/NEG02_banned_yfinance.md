# NEG02 · intentional fail · banned yfinance live route

```text
NEG_EXPECT: banned live-route
NEG_RULE: GP01
```

## PLTR · Deep (broken data plane)
**mode_effective:** standard

### L0 Observations
- last 28.40 fetched via yfinance download (source: yfinance)
- also tried longbridge quote as backup (source: longbridge)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| Price from banned stack is OK | invalid | must fail checker |

### CONFIDENCE_BLOCK
grade: B
mode: standard
dims:
  evidence_independence: weak
  falsification_rigor: weak
  assumption_audit: strong
  physical_mechanical: weak
  layer_integrity: strong
limiting: [evidence_independence]
verification_density: "Uses yfinance as primary — must FAIL structural ban."
independent_chains:
  - "yfinance: last price"
  - "WEB: IR summary"

### CHALLENGE_NODES
- id: CN1
  layer: L1
  claim: "Price is valid"
  assumption: "yfinance OK"
  what_would_falsify: "Policy forbids yfinance"
  conf_dim_link: evidence_independence
- id: CN2
  layer: L2
  claim: "Thesis holds"
  assumption: "growth"
  what_would_falsify: "growth miss"
  conf_dim_link: falsification_rigor

METHOD_CARDS_LOADED: []
