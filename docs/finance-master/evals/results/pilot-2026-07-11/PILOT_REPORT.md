# Live pilot report · GP01 / GP02 / GP06 shape (2026-07-11)

**Ecosystem:** 4.6.6  
**IBKR isolation:** market-structure only (`search_contracts`, `get_price_snapshot`, `get_price_history`).  
**Never called:** order instructions, account orders/positions/trades/balances, watchlist mutate.

Tickers chosen: **MU** (GP01-like deep frame), **NVDA** (GP02 lite tape), **AAPL** (GP06 / swing-valuation frame).

---

## 0. Resolve (US primary)

| Ticker | contract_id | exchange | description |
|--------|------------:|----------|-------------|
| MU | 9939 | NASDAQ | MICRON TECHNOLOGY INC |
| NVDA | 4815747 | NASDAQ | NVIDIA CORP |
| AAPL | 265598 | NASDAQ | APPLE INC |

Disambiguation: exact `symbol` match + US / NASDAQ primary (dropped MEXI/TSE/CDR/levered ETFs).

---

## 1. Live IBKR snapshots (as returned)

> Session snapshot fields `open/high/low/volume` were empty / zero with `last.is_close: true` (outside RTH).  
> Use **last + misc_statistics + IV + ADV + history** as L0.

### MU (9939)

| Field | Value |
|-------|------:|
| last | **991.64** (close flag) |
| annual_iv | ~0.941 |
| avg_90d_usd_volume | ~5.04e10 |
| 52w high / low | 1255 / ~103.2 |
| 13w high / low | 1255 / 408.5 |

### NVDA (4815747)

| Field | Value |
|-------|------:|
| last | **202.78** (close flag) |
| annual_iv | ~0.377 |
| avg_90d_usd_volume | ~3.35e10 |
| 52w high / low | ~236.5 / ~162.0 |

### AAPL (265598)

| Field | Value |
|-------|------:|
| last | **316.22** (close flag) |
| annual_iv | ~0.271 |
| avg_90d_usd_volume | ~1.71e10 |
| 52w high / low | ~317.4 / ~200.9 |

---

## 2. History packs (IBKR)

| Ticker | Request | Result |
|--------|---------|--------|
| MU | daily / ONE_MONTH | 20 bars; last close **979.3** (2026-07-10); month range ~891–1255 |
| NVDA | 5m / ONE_DAY | Full RTH 5m ladder 2026-07-10; open ~202 → close **210.96**; HL sequence intact with late thrust |
| AAPL | daily / THREE_MONTHS | ~62 bars Apr–Jul; last close **315.32**; uptrend vs April lows ~256 |

---

## 3. Path exercises (contract smoke · not full LLM deep)

### GP01-like · MU deep framing (standard)

**DATA_PACK.kind:** DEEP (market skeleton only — fundamentals still DATA_GAP without Web)

```text
kind: DEEP
ticker: MU
contract_id: 9939
ibkr_available: true
quote.last: 991.64
quote.avg_90d_usd_volume: 5.04e10
quote.w52_high: 1255
quote.w52_low: 103.2
ohlcv.daily: present (1m)
fundamentals_web: DATA_GAP (not fetched this pilot)
gaps: [fundamentals_web, catalysts_web, ownership_web]
```

**Structural contract check (manual)**

| Check | Result |
|-------|--------|
| Resolve US primary | PASS |
| IBKR L0 sourced | PASS |
| No order/account tools | PASS |
| Pack gaps explicit | PASS |
| User conf without Web fund. | Must ceiling ≤ **B/C** (A1) — not A |

**Cog-4 note:** Any L2 deep RETURN with `status: partial` + material fund gaps → Brain **≤ B**.

### GP02-like · NVDA lite tape

**DATA_PACK.kind:** INTRADAY

```text
kind: INTRADAY
ticker: NVDA
contract_id: 4815747
quote.last: 202.78 (prior session close mark)
ohlcv.intraday_5m: 2026-07-10 RTH full
derived: session open~202 high~211 low~201.9 close~210.96
```

| Check | Result |
|-------|--------|
| 5m structure available | PASS |
| Mode lite → 0 method cards | (policy; not loaded) |
| X not required for tape-only | PASS |
| Grade ceiling | ≤ B without multi-chain Web |

### GP06-like · AAPL valuation frame

**DATA_PACK.kind:** SWING / DEEP market half

```text
kind: SWING
ticker: AAPL
contract_id: 265598
quote.last: 316.22
ohlcv.daily: 3m present
fundamentals_web: DATA_GAP (pilot did not scrape SEC)
```

| Check | Result |
|-------|--------|
| Price for DCF spot | PASS (IBKR) |
| DCF without FCF Web | **blocked / partial** — L2 conf ≤ B; Brain re-grade required |
| No yfinance | PASS |

---

## 4. Redline compliance log

| Tool class | Used? |
|------------|:-----:|
| search_contracts | ✓ |
| get_price_snapshot | ✓ |
| get_price_history | ✓ |
| create_order_instruction | ✗ never |
| get_account_* | ✗ never |
| get_order_instructions / delete_* | ✗ never |

---

## 5. Findings for product

1. **IBKR resolve + history work** for MU / NVDA / AAPL US primaries.  
2. **Outside RTH**, snapshot OHLC/volume can be empty while `last` + misc + history remain usable — Brain Step 0 should prefer history when session fields are zero.  
3. **DATA_PACK gaps** are mandatory for any deep/DCF claim; pilot intentionally left Web empty to prove ceiling behavior.  
4. Full GP01 semantic deep (panel + DCF) still needs a **follow-on agent run** with Web/X under standard mode — this pilot proved **data plane + pack skeleton + redline**.  
5. Structural suite after GP01 Cog-4 gold: **6/6 gold PASS**.

---

## 6. Artifacts

- Live numbers above (session 2026-07-11)  
- Gold: `evals/artifacts/GP01_sample_output.md` (Cog-4 complete)  
- Schema: `sherlock-finance/references/data-pack-schema.md`

*Pilot only · research isolation · not investment advice*
