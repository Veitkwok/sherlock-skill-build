# GP05 · Max discovery / Serenity-style screen

```yaml
id: GP05
required_mode: max
mode_phrase: "max mode"
path: x-adv → serenity → deep×≤3
tickers: discovered US list
fixture: fixtures/DISCOVERY_l0_pack.md
gold_artifact: artifacts/GP05_sample_output.md
```

## User prompt

```text
max mode
Serenity 风格找 AI 基础设施链上卡点最紧的美股，给出优先研究名单
```

## Fixture

**`fixtures/DISCOVERY_l0_pack.md`** (includes FAKEHK to force US filter)

## Must pass

- [ ] mode_effective=max  
- [ ] Chain order respected; no L2 lateral skip  
- [ ] deep_count ≤ 3  
- [ ] Pre-deep names graded ≤ B  
- [ ] Final top names: CONFIDENCE_BLOCK (Brain re-grade; L2 A not auto-adopted)  
- [ ] CHALLENGE_NODES ≥3 on multi-name B screen  
- [ ] US-listed only; FAKEHK dropped  
- [ ] METHOD_CARDS_LOADED ≤6  

## Must fail if

- [ ] lite profile still runs full DAG without upgrade  
- [ ] deep×&gt;3  
- [ ] Non-US names kept in ranked output  
- [ ] Brain grade A on pre-deep shortlist only  

## Rubrics

`handoff_contracts.md` + `conf_all_modes.md` + `method_and_challenge.md`

## Structural check

```bash
python3 evals/run_structural_checks.py --file evals/artifacts/GP05_sample_output.md
```
