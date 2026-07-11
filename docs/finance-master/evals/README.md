# finance-master · Val-1 Evaluation Suite (full)

**Status:** full (structural) + pilot log  
**Ecosystem:** 4.6.7  
**Purpose:** Freeze six Golden Paths + conf/mode/method/challenge/L2-regrade contracts with offline fixtures, gold artifacts, and automated structural checks.

## Principles

1. Tests are **offline-friendly**: use frozen L0 fixtures (mock IBKR + Web/X text), not live prices.  
2. **CONFIDENCE_BLOCK is mandatory** on every scenario that produces a directional thesis or safety classification (all modes).  
3. **mode_profile / mode_effective** must match scenario tags.  
4. Banned tools (yfinance, longbridge, funda, opencli readers, quarantine paths) must never appear as live routes.  
5. **CHALLENGE_NODES** and **METHOD_CARDS_LOADED** caps are machine-checkable.  
6. Full LLM-as-judge scoring is optional later; structural pass is required first.

## Layout

```text
evals/
  README.md
  run_structural_checks.py    ← gold PASS + negatives must FAIL
  rubrics/
    conf_all_modes.md
    handoff_contracts.md
    step0_data_plane.md
    method_and_challenge.md
  scenarios/
    GP01_deep_buy.md … GP06_single_dcf.md
  fixtures/
    PLTR|NVDA|AAPL|XYZ|DISCOVERY|MSFT packs + sample_ibkr_quote
  artifacts/
    GP01…GP06_sample_output.md   ← structural gold (must PASS)
  negatives/
    NEG01…NEG10_*.md             ← intentional fails (must FAIL as expected)
    README.md
```

## How to run

### 1) Structural (CI / local · no LLM)

From repo root or `docs/finance-master/`:

```bash
python3 docs/finance-master/evals/run_structural_checks.py
# or
cd docs/finance-master && python3 evals/run_structural_checks.py
```

Variants:

```bash
python3 evals/run_structural_checks.py --gold-only
python3 evals/run_structural_checks.py --negatives-only
python3 evals/run_structural_checks.py --file evals/artifacts/GP02_sample_output.md
```

Exit code `0` only if:

1. All gold artifacts **PASS**, and  
2. All registered negatives **META_PASS** (they fail structural checks with the expected error class).

### 2) Manual / agent Val-1

1. Set mode phrase from scenario (`lite mode` / `standard mode` / `max mode`).  
2. Feed **User prompt** + **Fixture L0** (do not invent tools outside §D).  
3. Compare output shape to `artifacts/GP##_sample_output.md`.  
4. Score semantics with rubrics in `rubrics/`.  
5. Re-run structural checker on the new transcript if saved under `artifacts/`.

## Scenario index

| ID | required_mode | Path family | Fixture | Gold | Core assert |
|----|---------------|-------------|---------|------|-------------|
| GP01 | standard (or max) | Deep + buy | `PLTR_l0_pack.md` | `GP01_sample_output.md` | conf + §6/§10 + deep allow |
| GP02 | lite | 1–7d + X | `NVDA_l0_pack.md` | `GP02_sample_output.md` | conf; no multi-deep; 0 cards |
| GP03 | standard | 1–3m swing | `AAPL_l0_pack.md` | `GP03_sample_output.md` | conf + Web beyond X |
| GP04 | any (lite) | Trap stop | `XYZ_trap_l0.md` | `GP04_sample_output.md` | trap only; hard stop |
| GP05 | max | Discovery DAG | `DISCOVERY_l0_pack.md` | `GP05_sample_output.md` | deep×≤3; pre-deep ≤B |
| GP06 | standard | Single DCF | `MSFT_l0_pack.md` | `GP06_sample_output.md` | RETURN; Brain re-grade |

## What the checker enforces

| Check | Rule |
|-------|------|
| CONFIDENCE_BLOCK | Present; `grade`; `mode`; 5 dims; limiting; verification_density; independent_chains |
| mode match | `mode_effective` + conf `mode` == scenario |
| CHALLENGE_NODES | Min count by mode/grade; each has `what_would_falsify` |
| Method cards | lite=0; standard≤3; max≤6; ids M01–M12 |
| Banned stacks | No live yfinance/longbridge/funda/opencli/quarantine/lhb/readers |
| Trap (GP04) | hard_stop + trap-detector; no buy path |
| Discovery (GP05) | deep_count ≤3 |
| DCF (GP06) | RETURN_BLOCK + Brain re-grade language |
| L0 tags | At least one `source: IBKR\|WEB\|X\|CACHE\|USER` |
| Givens | Section present |

Semantic quality (claim truth, Occam rank sense) remains human/LLM-judge.

## Cog-4 notes (L2 conf alignment)

Gold GP04/GP05/GP06 include extended RETURN conf fields + `L2_CONF_ADVISORY` / `BRAIN_REGRADE` lines.  
Canonical contract: `sherlock-finance/references/l2-confidence-contract.md`.

## Negative suite (checker regression)

| ID | Rule | Fail class |
|----|------|------------|
| NEG01 | GP01 | missing CONFIDENCE_BLOCK |
| NEG02 | GP01 | banned yfinance/longbridge |
| NEG03 | GP02 | lite method cards |
| NEG04 | GP02 | lite deep/panel |
| NEG05 | GP04 | trap buy-through |
| NEG06 | GP05 | deep_count > 3 |
| NEG07 | GP01 | grade A thin chains |
| NEG08 | GP06 | missing Brain re-grade |
| NEG09 | GP03 | challenge missing falsifier |
| NEG10 | GP02 | conf mode ≠ mode_effective |

See `negatives/README.md`. Register new cases in `NEGATIVE_CASES` inside `run_structural_checks.py`.

## Pilot logs

| Path | Content |
|------|---------|
| `results/pilot-2026-07-11/PILOT_REPORT.md` | Live IBKR MU / NVDA / AAPL (market-data only) |

## Semantic judge (Priority 8)

After structural PASS:

1. Load `rubrics/llm_as_judge.md`  
2. Score transcript vs scenario + fixture  
3. Save JSON under `results/<date>/judge_GP##.json`  

| Layer | Tool |
|-------|------|
| Structure | `run_structural_checks.py` |
| Semantics | `rubrics/llm_as_judge.md` |

## Next

- Handbook rewrite: **deferred** (user-owned after core complete)  
- Repo folder restructure: **deferred** (after this pass)  
- Optional: batch-judge gold artifacts for baseline scores