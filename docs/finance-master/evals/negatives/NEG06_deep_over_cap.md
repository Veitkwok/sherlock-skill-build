# NEG06 · intentional fail · discovery deep_count > 3

```text
NEG_EXPECT: deep_count > cap
NEG_RULE: GP05
```

## Discovery · max (broken deep cap)
**mode_effective:** max

### L0 Observations
- VRT/FIX/AMAT/NVDA/AMD shortlist (source: IBKR)
- FAKEHK excluded non-US (source: WEB)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| deep×5 OK | invalid | over cap |

deep_count: 5
deep_tickers: [VRT, FIX, AMAT, NVDA, AMD]

### INVOKE
```text
### INVOKE
skill: finance-master/UZI-Skill/deep-analysis
intent: over-cap deep
ticker: VRT
```

### RETURN_BLOCK
```text
### RETURN_BLOCK
skill: deep-analysis
status: partial
ticker: VRT
confidence: B
confidence_scope: skill_local
fields_filled: [quote]
fields_gap: [dcf]
```

L2_CONF_ADVISORY: B (deep-analysis, scope=skill_local)
BRAIN_REGRADE: B (reason: screen)

### CONFIDENCE_BLOCK
grade: B
mode: max
dims:
  evidence_independence: weak
  falsification_rigor: strong
  assumption_audit: strong
  physical_mechanical: strong
  layer_integrity: strong
limiting: [evidence_independence]
verification_density: "deep×5 violates max cap 3."
independent_chains:
  - "IBKR: quotes"
  - "WEB: scores"
  - "X: leads"

### CHALLENGE_NODES
- id: CN1
  layer: L2
  claim: "Five deeps OK"
  assumption: "no cap"
  what_would_falsify: "deep_count policy ≤3"
  conf_dim_link: layer_integrity
- id: CN2
  layer: L2
  claim: "Screen complete"
  assumption: "budget infinite"
  what_would_falsify: "tool budget"
  conf_dim_link: evidence_independence
- id: CN3
  layer: conf_dim
  claim: "Grade B fine"
  assumption: "gaps OK"
  what_would_falsify: "full packs"
  conf_dim_link: falsification_rigor

METHOD_CARDS_LOADED: [M01, M05]
