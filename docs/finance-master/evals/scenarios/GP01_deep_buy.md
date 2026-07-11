# GP01 · Deep analysis + buy judgment

```yaml
id: GP01
required_mode: standard   # or max
mode_phrase: "standard mode"
path: deep + §10
tickers: [PLTR]
fixture: fixtures/PLTR_l0_pack.md
gold_artifact: artifacts/GP01_sample_output.md
```

## User prompt (template)

```text
standard mode
PLTR 深度分析，现在值得买吗？
```

## Fixture

Use **`fixtures/PLTR_l0_pack.md`** (frozen L0). Do not live-scrape for structural pass.  
(`fixtures/sample_ibkr_quote.md` remains a generic IBKR shape reference.)

## Must pass

- [ ] `mode_effective` ≥ standard  
- [ ] Step 0 L0 with sources (`source: IBKR|WEB|X`)  
- [ ] Givens table  
- [ ] deep-analysis allowlisted with `### INVOKE` + `### RETURN_BLOCK`  
- [ ] DATA_PACK.kind DEEP (or equivalent pack fields)  
- [ ] Cog-4: `L2_CONF_ADVISORY` + `BRAIN_REGRADE` (L2 A must not auto-become user A if gaps)  
- [ ] CONFIDENCE_BLOCK with `mode: standard`  
- [ ] CHALLENGE_NODES ≥2 when grade B/C  
- [ ] §6 before buy framing  
- [ ] §10 three layers if buy language  
- [ ] METHOD_CARDS_LOADED ≤3 (standard)  
- [ ] No quarantine / banned tools / IBKR order endpoints  

## Must fail if

- [ ] No CONFIDENCE_BLOCK on directional buy thesis  
- [ ] Routes to yfinance / longbridge / funda / opencli / banned skill paths  
- [ ] grade A with &lt;3 independent_chains  
- [ ] Accepts L2 conf=A as Brain A without re-grade when gaps material  


## Rubrics

`conf_all_modes.md` + `handoff_contracts.md` + `step0_data_plane.md` + `method_and_challenge.md`

## Structural check

```bash
python3 evals/run_structural_checks.py --file evals/artifacts/GP01_sample_output.md
```
