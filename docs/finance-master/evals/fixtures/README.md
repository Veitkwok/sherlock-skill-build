# Fixtures (Val-1 full)

Store **frozen** L0 packs so evals do not depend on live IBKR/Web.

## Index

| File | Scenario | Content |
|------|----------|---------|
| `sample_ibkr_quote.md` | generic | Mock snapshot field shape |
| `PLTR_l0_pack.md` | GP01 | Deep + buy L0 |
| `NVDA_l0_pack.md` | GP02 | Lite tape + X |
| `AAPL_l0_pack.md` | GP03 | Swing 1–3m |
| `XYZ_trap_l0.md` | GP04 | Tip/trap context |
| `DISCOVERY_l0_pack.md` | GP05 | Discovery shortlist (+ FAKEHK drop) |
| `MSFT_l0_pack.md` | GP06 | DCF fundamentals synth |

## Format

```text
### FIXTURE_L0
ticker: SYM
source: IBKR|WEB|X|CACHE
asof: 2026-07-11
fields:
  last: ...
  ...
notes: synthetic for eval only
```

## Rules

1. **EVAL ONLY** — numbers are synthetic, not market truth.  
2. Never commit live account secrets or real PII.  
3. Structural checks read **artifacts**, not fixtures directly; fixtures feed human/LLM runs.  
4. Prefer IBKR field names aligned with Brain §D (`last`, ADV, 52w, IV flags).

## Updating fixtures

When Brain pack shapes change, update the matching fixture and re-validate gold artifacts:

```bash
python3 evals/run_structural_checks.py
```
