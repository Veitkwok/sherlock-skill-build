**Phase 5 – Finalized Test Suite v1.0**  
**All 6 Input Packages Complete**  
**Date:** 10 July 2026

Below are the complete, ready-to-use input packages for the first 6 test cases. Cases 4–6 now have concrete proposed tickers/situations.

---

### Test Case 1: NVDA – Earnings Quality & New Metrics

**Category:** Earnings Quality / Accounting Presentation  
**Primary Skills to Exercise:** `deep-analysis` + `earnings-recap`

**Input Package:**

- **Ticker:** NVDA
- **Focus Period:** The most recent quarter in which new defined metrics or significant segment reporting language changes appeared
- **Data to Provide Agent:**
  - Key excerpts from the 10-Q / earnings release (especially MD&A and segment reporting sections)
  - The specific new defined metric(s) and the exact surrounding language
  - Revenue breakdown by segment (current vs. prior periods)
  - Summary of options activity around the earnings date
- **Testing Focus:**
  - Quality of L0–L3 labeling on the new metric
  - Whether Physical-Trace Verification Standards are applied before accepting management framing
  - Execution of Review the Givens Gate on prior segment reporting assumptions

---

### Test Case 2: GME – 2021 Short Squeeze Period (Retrospective)

**Category:** Options / Short Interest Dynamics  
**Primary Skills to Exercise:** `options-payoff` + `deep-analysis` + `x-advanced-research`

**Input Package:**

- **Ticker:** GME
- **Focus Period:** Late January 2021 (peak squeeze period)
- **Data to Provide Agent:**
  - Short interest levels and days-to-cover at key inflection points
  - Summary of unusual options volume and sweeps
  - High-level summary of dominant X/Twitter narrative peaks during that window
  - Fundamental results and guidance available at the time (Q4 FY2020 / Q1 FY2021)
- **Testing Focus:**
  - Ability to maintain Review the Givens Gate under extreme narrative momentum
  - Integration quality of options flow vs. social narrative vs. fundamental data
  - Whether Epistemic Honesty Check is triggered during high-sentiment periods

---

### Test Case 3: TSLA – Production/Delivery vs. Guidance Narrative

**Category:** Narrative vs. Physical-Trace Conflict  
**Primary Skills to Exercise:** `deep-analysis` + `x-advanced-research`

**Input Package:**

- **Ticker:** TSLA
- **Focus Period:** Recent 2–3 quarters with notable production/delivery commentary vs. actual results
- **Data to Provide Agent:**
  - Quarterly production and delivery numbers
  - Relevant management guidance and commentary language from earnings calls/transcripts
  - Summary of X narrative tone around those periods
  - Any available channel or inventory-related signals
- **Testing Focus:**
  - Prioritization of physical delivery data (L0) over management narrative tone
  - Quality of L2/L3 hypotheses generated around demand vs. production narrative
  - Application of Physical-Trace Verification Standards

---

### Test Case 4: META – Aggressive Buybacks + Compensation Structure

**Category:** Management Incentive & Capital Allocation  
**Primary Skills to Exercise:** `deep-analysis`

**Input Package:**

- **Ticker:** META
- **Focus Period:** 2023–2024 period of large-scale share repurchases combined with compensation plan changes
- **Data to Provide Agent:**
  - Summary of buyback activity and capital return policy
  - Key elements of executive compensation structure (from Proxy/10-K)
  - Free cash flow generation and overall capital allocation context during the period
- **Testing Focus:**
  - Quality of behavioral profiling and motive reconstruction
  - Whether the agent identifies potential misalignment between incentive structure and capital allocation decisions
  - Execution of Review the Givens Gate on stated capital return rationale

---

### Test Case 5: TSLA – Equity Strength vs. Rising Rates / Credit Environment (2022)

**Category:** Cross-Market Divergence  
**Primary Skills to Exercise:** `stock-correlation` + `deep-analysis`

**Input Package:**

- **Ticker:** TSLA
- **Focus Period:** 2022 (particularly periods of rising long-term Treasury yields)
- **Data to Provide Agent:**
  - TSLA equity price action and narrative during key rate-sensitive periods
  - Movement in long-term Treasury yields and relevant credit spreads
  - Management commentary on interest rate sensitivity (if any)
- **Testing Focus:**
  - Whether the agent actively seeks and integrates cross-market signals as required by Section 5.2
  - Quality of divergence analysis between equity narrative and interest rate/credit environment
  - Application of Review the Givens Gate on rate-sensitivity assumptions

---

### Test Case 6: AMC – Extreme Narrative Capture (2021)

**Category:** High Narrative Capture Risk  
**Primary Skills to Exercise:** `deep-analysis` + `x-advanced-research` + `trap-detector`

**Input Package:**

- **Ticker:** AMC
- **Focus Period:** Peak meme/narrative period in 2021 (especially May–June)
- **Data to Provide Agent:**
  - Fundamental backdrop (revenue, cash position, dilution risk) at the time
  - Summary of dominant X/Twitter and media narrative
  - Short interest and options activity
  - Any available signals of deteriorating operational reality vs. narrative
- **Testing Focus:**
  - Whether Epistemic Honesty Check is triggered
  - Ability to resist narrative capture despite extreme social momentum
  - Quality of physical/fundamental trace evaluation vs. social narrative

---

### Summary of the First Test Suite

| # | Ticker | Category | Primary Skill Combination | Difficulty Level |
|---|--------|----------|---------------------------|------------------|
| 1 | NVDA | Earnings Quality | `deep-analysis` + `earnings-recap` | Medium |
| 2 | GME (2021) | Short Interest / Options | `options-payoff` + `deep-analysis` + `x-advanced-research` | High |
| 3 | TSLA | Narrative vs. Physical-Trace | `deep-analysis` + `x-advanced-research` | Medium-High |
| 4 | META | Management Incentive | `deep-analysis` | Medium |
| 5 | TSLA (2022) | Cross-Market Divergence | `stock-correlation` + `deep-analysis` | Medium |
| 6 | AMC (2021) | High Narrative Capture | `deep-analysis` + `x-advanced-research` + `trap-detector` | High |

---

