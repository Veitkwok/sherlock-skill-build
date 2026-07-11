# Fixture · Discovery shortlist (synthetic · GP05)

```text
### FIXTURE_L0
mode_intended: max
theme: US AI infrastructure chokepoints

### X_ADVANCED_SYNTH (step ① output shape)
tickers:
  - symbol: VRT
    us_listed: true
    catalyst_or_bottleneck: "data center power/thermal"
    x_evidence: [x_a1]
    risk_flags: [high_beta]
  - symbol: FIX
    us_listed: true
    catalyst_or_bottleneck: "specialty contractor capacity"
    x_evidence: [x_a2]
    risk_flags: []
  - symbol: AMAT
    us_listed: true
    catalyst_or_bottleneck: "semi equipment"
    x_evidence: [x_a3]
    risk_flags: [cyclical]
  - symbol: FAKEHK
    us_listed: false
    note: MUST BE DROPPED by Brain

### SERENITY_SYNTH (step ②)
scored_tickers:
  - symbol: VRT
    bottleneck_score: 82
    scarce_layer: "power delivery / thermal"
  - symbol: FIX
    bottleneck_score: 78
    scarce_layer: "skilled install capacity"
  - symbol: AMAT
    bottleneck_score: 70
    scarce_layer: "tool lead times"
recommended_for_deep: [VRT, FIX, AMAT]

### IBKR_MIN (per deep name — synthetic)
VRT last=95.0 ADV=high
FIX last=420.0 ADV=medium
AMAT last=210.0 ADV=high

notes: EVAL ONLY — deep count must be ≤3; FAKEHK excluded
```
