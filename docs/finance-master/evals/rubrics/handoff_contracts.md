# Rubric · Handoff & routing contracts

## Pass

- L2 only from active allowlist under `mode_effective`  
- No L2→L2 lateral calls  
- Discovery: standard deep×≤1; max deep×≤3; lite DAG blocked  
- INVOKE includes data_pack when deep  
- RETURN_BLOCK structure if L2 used  
- Trap path: only trap-detector when hard-stop  
- **Cog-4:** L2 `confidence` is advisory; RETURN may include `confidence_scope` + `confidence_basis`  
- **Cog-4:** After L2, Brain logs `L2_CONF_ADVISORY` + `BRAIN_REGRADE` and emits Brain `CONFIDENCE_BLOCK`  
- L2 does **not** emit `### CONFIDENCE_BLOCK` or `mode:`  

## Fail

- Routes to banned skills (yfinance/funda/lhb/readers)  
- lite mode full deep without auto-upgrade log  
- max discovery with deep×&gt;3  
- Missing Brain re-grade after L2 conf=A  
- Copies L2 A into user thesis without §H.6 / §1.4  
- L2 emits Brain CONFIDENCE_BLOCK  
- Loads entire method-library or &gt;mode max cards  
- lite mode loads M01–M12 card bodies  

