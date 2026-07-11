# GP06 · Single-dimension DCF (standard)

```yaml
id: GP06
required_mode: standard
mode_phrase: "standard mode"
path: company-valuation
tickers: [MSFT]
fixture: fixtures/MSFT_l0_pack.md
gold_artifact: artifacts/GP06_sample_output.md
```

## User prompt

```text
standard mode
MSFT 做 DCF 和同业估值三角，现在贵不贵？
```

## Fixture

**`fixtures/MSFT_l0_pack.md`**

## Must pass

- [ ] company-valuation (or Brain-native DCF) under allowlist  
- [ ] DATA_PACK / IBKR price used; no yfinance  
- [ ] ### INVOKE + ### RETURN_BLOCK structure  
- [ ] Brain CONFIDENCE_BLOCK (re-grade; L2 conf advisory)  
- [ ] RETURN includes Cog-4 `confidence_scope: valuation` (+ basis preferred)  
- [ ] `L2_CONF_ADVISORY` + `BRAIN_REGRADE` log lines  
- [ ] Explicit assumptions + sensitivity or range  
- [ ] CHALLENGE_NODES ≥2 if grade B  
- [ ] METHOD_CARDS_LOADED ≤3  

## Must fail if

- [ ] Live yfinance / funda / longbridge route  
- [ ] Accepts L2 conf=A as Brain A without re-grade note  
- [ ] L2 emits CONFIDENCE_BLOCK  
- [ ] Missing sensitivity / assumption list  

## Rubrics

`handoff_contracts.md` + `conf_all_modes.md` + `step0_data_plane.md` + `method_and_challenge.md`

## Structural check

```bash
python3 evals/run_structural_checks.py --file evals/artifacts/GP06_sample_output.md
```
