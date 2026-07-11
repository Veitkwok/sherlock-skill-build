# DATA_PACK canonical schema (v4.6.6)

**Owner:** Central Brain §D  
**Consumers:** All L2 skills via `### INVOKE` → `data_pack:`  
**Rule:** Prefer pack fields over re-fetch. Missing key → `DATA_GAP` or gap-fill only if `budget.may_fetch`.

---

## Pack kinds

| Kind | Typical mode | Purpose |
|------|--------------|---------|
| `QUOTE` | any | Single snapshot resolve |
| `INTRADAY` | lite / §12 | Session tape + short bars |
| `SWING` | standard / §13 | Daily structure + catalysts |
| `DEEP` | standard deep / max | Full research handoff |

Emit one kind per ticker (or nested `tickers.<SYM>` for multi-name).

---

## Top-level envelope

```text
DATA_PACK:
  kind: QUOTE|INTRADAY|SWING|DEEP
  asof: ISO-8601
  mode_effective: lite|standard|max
  ibkr_available: true|false
  ticker: SYM                    # or MULTI for discovery intermediate
  contract_id: <int|null>        # IBKR underlying_contract_id
  security_type: STK|ETF|...     # default STK
  currency: USD
  exchange_hint: SMART|null
  sources_used: [IBKR, WEB, X, CACHE]
  gaps: [field.path, ...]        # explicit DATA_GAP list
  notes: "≤200 chars"
```

---

## Field groups

### 1. `quote` (IBKR · Tier-1)

| Field | Type | Source | Required for |
|-------|------|--------|--------------|
| `last` | number | IBKR snapshot | QUOTE+ |
| `prior_close` | number | IBKR | QUOTE+ |
| `open` / `high` / `low` | number | IBKR | INTRADAY+ preferred |
| `volume` | number | IBKR | QUOTE+ |
| `change_pct` | number | IBKR or derived | optional |
| `bid` / `ask` | number | IBKR bid_ask | optional |
| `avg_90d_usd_volume` | number | IBKR | SWING/DEEP liquidity |
| `w52_high` / `w52_low` | number | IBKR misc_statistics | SWING/DEEP |
| `implied_vol_underlying` | number | IBKR | options paths |
| `underlying_today_option_volume` | number | IBKR | options paths |

### 2. `ohlcv` (IBKR history)

| Field | Type | Notes |
|-------|------|-------|
| `daily` | list[{date,o,h,l,c,v}] | SWING/DEEP; max ~90–260 bars as needed |
| `intraday_5m` | list[{ts,o,h,l,c,v}] | INTRADAY; session or last N bars |
| `derived` | object | optional: ma20/ma50/ma200, rsi, stage_hint |

Do **not** invent OHLCV. If IBKR fails → `gaps` + conf ceiling.

### 3. `fundamentals_web` (Web · never IBKR statements)

| Field | Type | Notes |
|-------|------|-------|
| `revenue_ttm` / `fcf_ttm` / `eps_ttm` | number\|null | label estimate vs reported |
| `gross_margin` / `op_margin` | number\|null | |
| `shares_diluted` | number\|null | |
| `guidance_notes` | string\|null | |
| `filing_refs` | list[url_or_id] | 10-K/10-Q/8-K |
| `quality` | reported\|estimate\|gap | |

### 4. `ownership_web`

| Field | Type |
|-------|------|
| `form4_net_30d` | string\|null |
| `holders_top` | list\|null |
| `short_interest_note` | string\|null |

### 5. `catalysts_web`

| Field | Type |
|-------|------|
| `next_earnings` | date\|null |
| `events` | list[{date, label, source}] |

### 6. `peers` (IBKR themes/connections + optional Web)

| Field | Type |
|-------|------|
| `symbols` | list[str] |
| `theme_labels` | list[str] |
| `source` | IBKR\|WEB\|MIXED |

### 7. `social_x` (Tier C · ≤1 conf chain)

| Field | Type |
|-------|------|
| `posts` | list[{id_or_url, stance, engagement_note}] |
| `heat` | low\|medium\|high\|unknown |
| `spam_risk` | bool |

### 8. `options_summary` (optional)

| Field | Type |
|-------|------|
| `iv` / `iv_percentile` | number\|null |
| `call_put_volume_note` | string\|null |
| `chain_bounded` | bool |

### 9. `risk_flags`

| Field | Type |
|-------|------|
| `trap_level` | green\|yellow\|orange\|red\|null |
| `liquidity` | high\|medium\|low\|micro\|unknown |
| `name_bucket` | A\|B\|C\|D\|unknown |

---

## Minimum viable packs

| Kind | Must include |
|------|----------------|
| `QUOTE` | envelope + `quote.last` (+ `contract_id` if IBKR ok) |
| `INTRADAY` | QUOTE + `ohlcv.intraday_5m` or daily short + optional `social_x` |
| `SWING` | QUOTE + daily ohlcv or ma stack + `catalysts_web` preferred |
| `DEEP` | SWING + `fundamentals_web` core + peers preferred + gaps list |

---

## INVOKE embedding

```text
### INVOKE
skill: finance-master/UZI-Skill/deep-analysis
ticker: PLTR
contract_id: 999001
budget: { max_new_tool_calls: 8, may_fetch: false }
data_pack: |
  kind: DEEP
  asof: 2026-07-11T16:00:00Z
  ...
```

When `may_fetch: false`, L2 **must not** call IBKR/Web for keys already present.

---

## IBKR redline (research isolation)

**Allowed:** `search_contracts`, `get_price_snapshot`, `get_price_history`, option parameters/data (structure), `get_company_themes`, `get_company_connections`, `search_futures` (macro context only).

**Forbidden in finance-master research paths (absolute — no user override):**  
`create_order_instruction`, `delete_order_instruction`, `get_order_instructions`,  
`get_account_orders`, `get_account_positions`, `get_account_trades`, `get_account_balances`,  
watchlist mutate/delete, any order submission or account management endpoint.  
Never stage orders inside this product tree.

---

*Canonical pack schema · Brain-owned · US equities*
