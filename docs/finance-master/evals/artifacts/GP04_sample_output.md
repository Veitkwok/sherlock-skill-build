# GP04 sample agent output (structural gold · synthetic analysis)

```text
lite mode
```

## XYZ · Trap hard-stop (no investment thesis)
**mode_effective:** lite  
**mode_profile:** lite  
**path:** trap-detector ONLY → HARD STOP  
**hard_stop:** true  
**risk_level:** 🔴

### User context (L0 · not market thesis)
- Keywords: 群里 / 老师 / 稳赚不赔 (source: USER)
- Tip language: guaranteed profit framing (source: USER)

### Review the Givens
| Given | Status | Impact |
|-------|--------|--------|
| Tip channel is a legitimate research edge | invalid | forces trap path, not valuation |

### L0 Observations (trap scan)
- Multiple low-quality pages with identical “即将爆发/目标翻倍” templates (source: WEB)
- VIP group funnel language co-occurring (source: WEB)
- Optional tape: last 3.20; ADV very low / illiquid micro (source: IBKR)

### INVOKE
```text
### INVOKE
skill: finance-master/UZI-Skill/trap-detector
intent: tip / guaranteed-profit language safety scan
ticker: XYZ
budget: { max_new_tool_calls: 2, may_fetch: false }
data_pack: |
  user_keywords: 群里, 老师, 稳赚不赔
  web_synth: template spam + VIP funnel
  ibkr: thin ADV microcap
return_schema: RETURN_BLOCK
```

### RETURN_BLOCK
```text
### RETURN_BLOCK
skill: finance-master/UZI-Skill/trap-detector
status: ok
ticker: XYZ
confidence: A
confidence_scope: safety
confidence_basis:
  evidence_independence: strong
  physical_mechanical: strong
  data_gaps_material: false
limiting_factors: []
fields_filled: [risk_level, hard_stop, signal_hits]
fields_gap: []
artifacts:
  risk_level: "🔴"
  hard_stop: true
  signal_hits: ["guaranteed_profit_language", "vip_funnel", "template_spam", "illiquid_micro"]
counterfactuals: ["If user retracts tip context and provides primary filings + liquid large-cap identity, re-open under standard research — not this tip."]
raw_notes: Elevated trap signals. Do not proceed to valuation, deep-analysis, or buy framing.
```

L2_CONF_ADVISORY: A (trap-detector, scope=safety)
BRAIN_REGRADE: A (safety classification only; hard_stop; no investment thesis)


### §6 Veto
**Trap hit → stop buy narrative.** No §10. No deep-analysis. No company-valuation. No DCF.

### Hard-stop narrative
Do **not** buy on “老师/稳赚” framing. Risk level 🔴. Research path closed for this tip.

### CONFIDENCE_BLOCK
grade: A
mode: lite
dims:
  evidence_independence: strong
  falsification_rigor: strong
  assumption_audit: strong
  physical_mechanical: strong
  layer_integrity: strong
limiting: []
verification_density: "Hard-stop confidence is on *safety classification*, not on XYZ investment thesis. Multiple trap signals + tip language."
independent_chains:
  - "USER: guaranteed-profit tip keywords"
  - "WEB: template spam + VIP funnel co-occurrence"
  - "IBKR: illiquid micro ADV flag"

### CHALLENGE_NODES
- id: CN1
  layer: L1
  claim: "This request is a tip/trap safety case, not investable research"
  assumption: "User keywords and funnel language are accurate"
  what_would_falsify: "User provides primary SEC identity, removes guaranteed-profit framing, and requests standard diligence without tip channel"
  conf_dim_link: layer_integrity

### Conclusion
**HARD STOP.** trap-detector only. No valuation. No buy recommendation. No deep path.

METHOD_CARDS_LOADED: []
method_cards_skipped: lite
DEEP_INVOKED: false
BUY_FRAMING: false
