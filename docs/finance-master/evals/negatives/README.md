# Negative fixtures (intentional checker fails)

These transcripts are **designed to FAIL** `run_structural_checks.py` under a named Golden Path rule set.  
The suite **meta-passes** only when each negative file produces at least the expected error class.

## Why

Regression-test that the structural checker still catches:

- missing conf / challenge nodes  
- banned data routes  
- mode / method-card violations  
- trap buy-through  
- discovery deep over-cap  
- missing Brain re-grade (Cog-4)  

## Layout

| File | Applies rule | Intended fail class |
|------|--------------|---------------------|
| `NEG01_missing_conf.md` | GP01 | no CONFIDENCE_BLOCK |
| `NEG02_banned_yfinance.md` | GP01 | banned live-route (yfinance) |
| `NEG03_lite_method_cards.md` | GP02 | lite loads method cards |
| `NEG04_lite_runs_deep.md` | GP02 | lite runs deep/panel |
| `NEG05_trap_buy_through.md` | GP04 | trap path buy / missing hard_stop |
| `NEG06_deep_over_cap.md` | GP05 | deep_count > 3 |
| `NEG07_grade_a_thin_chains.md` | GP01 | grade A with &lt;3 chains |
| `NEG08_no_brain_regrade.md` | GP06 | L2 RETURN without re-grade |
| `NEG09_challenge_no_falsify.md` | GP03 | challenge node missing falsifier |
| `NEG10_mode_mismatch.md` | GP02 | conf mode ≠ mode_effective |

## Run

```bash
# Full suite: gold PASS + negatives must FAIL as expected
python3 docs/finance-master/evals/run_structural_checks.py

# Negatives only
python3 docs/finance-master/evals/run_structural_checks.py --negatives-only

# Gold only (skip negatives)
python3 docs/finance-master/evals/run_structural_checks.py --gold-only
```

## Authoring rules

1. Keep files **minimal** — enough structure to trip one primary rule (side fails OK).  
2. Mark header: `NEG_EXPECT: <short fail class>`.  
3. Register in `run_structural_checks.py` → `NEGATIVE_CASES`.  
4. Never put negatives under `artifacts/` (gold-only glob).  
5. Synthetic / EVAL ONLY — not market truth.
