# Rubric · Confidence v3.0 (all modes)

## Must appear

```text
### CONFIDENCE_BLOCK
grade: A|B|C
mode: lite|standard|max
dims: ...
limiting: ...
verification_density: ...
independent_chains: ...

### CHALLENGE_NODES
- id: CN1
  ...
```

## Universal fail conditions

| Fail if | Force |
|---------|--------|
| No CONFIDENCE_BLOCK on directional thesis | FAIL |
| No CHALLENGE_NODES (or count below mode min) | FAIL |
| `mode` missing or ≠ scenario mode_effective | FAIL |
| grade A with &lt;3 independent_chains | FAIL (should be ≤B) |
| Only X/social chains for grade A or B | FAIL (≤C) |
| Uses yfinance/longbridge/funda/opencli as live path | FAIL |
| grade A tone without dim list | FAIL |
| Challenge node missing `what_would_falsify` | FAIL |
| L2 `confidence: A` copied as user grade without §H.6 re-grade | FAIL (Cog-4) |
| L2 skill emits `### CONFIDENCE_BLOCK` | FAIL (Brain-only) |

## Mode ceilings

| mode | Pass rule |
|------|-----------|
| lite | grade ≤ B unless A criteria met (3 chains + Givens + IBKR); X-only ≤ C |
| standard | A allowed if all 5 dims strong |
| max | A allowed; pre-deep screen rows ≤ B |

## Dim legality (independent_chains)

Count at most:

- 1× IBKR market  
- 1× primary filing/transcript Web  
- 1× ownership Web  
- 1× X cluster  

Three Web news links about the same headline ≠ three independent chains.
