# GP02 · Lite 1–7d tape + X sentiment

```yaml
id: GP02
required_mode: lite
mode_phrase: "lite mode"
path: §12-like + sentiment
tickers: [NVDA]
fixture: fixtures/NVDA_l0_pack.md
gold_artifact: artifacts/GP02_sample_output.md
```

## User prompt

```text
lite mode
NVDA 近几天走势和 X 上讨论情绪，短线怎么看？
```

## Fixture

**`fixtures/NVDA_l0_pack.md`**

## Must pass

- [ ] mode=lite in CONFIDENCE_BLOCK and mode_effective  
- [ ] Prefer IBKR short history + X; no full deep default  
- [ ] grade ceiling per lite rules (X-only ≤C; default max B unless A criteria)  
- [ ] Discovery multi-deep **not** run  
- [ ] Kill condition present  
- [ ] CHALLENGE_NODES ≥1  
- [ ] METHOD_CARDS_LOADED: [] and method_cards_skipped: lite  

## Must fail if

- [ ] Loads investor-panel 36 or serenity universe  
- [ ] grade A without IBKR chain + ≥3 independent_chains  
- [ ] Loads any M01–M12 card body  

## Rubrics

`conf_all_modes.md` + `step0_data_plane.md` + `method_and_challenge.md`

## Structural check

```bash
python3 evals/run_structural_checks.py --file evals/artifacts/GP02_sample_output.md
```
