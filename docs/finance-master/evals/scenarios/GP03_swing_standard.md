# GP03 · Standard 1–3 month research path

```yaml
id: GP03
required_mode: standard
mode_phrase: "standard mode"
path: §13 / single-name research
tickers: [AAPL]
fixture: fixtures/AAPL_l0_pack.md
gold_artifact: artifacts/GP03_sample_output.md
```

## User prompt

```text
standard mode
AAPL 未来一到三个月的关键价位、催化剂和情景？
```

## Fixture

**`fixtures/AAPL_l0_pack.md`**

## Must pass

- [ ] SWING/DEEP pack elements (price history + Web catalysts)  
- [ ] CONFIDENCE_BLOCK mode=standard  
- [ ] Sources beyond X alone  
- [ ] Scenario / support-resistance or catalyst table  
- [ ] CHALLENGE_NODES ≥2 if grade B/C  
- [ ] METHOD_CARDS_LOADED ≤3  

## Must fail if

- [ ] X-only independent_chains with grade A/B  
- [ ] No levels / catalysts  

## Rubrics

`conf_all_modes.md` + `step0_data_plane.md` + `method_and_challenge.md`

## Structural check

```bash
python3 evals/run_structural_checks.py --file evals/artifacts/GP03_sample_output.md
```
