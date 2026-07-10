**Phase 4 & 5 – Finalized Version v1.2**  
**Date:** 10 July 2026

### Phase 4: Skill Recommendations (Finalized with Direct Sub-Skill Mapping)

The System Prompt requires a focused, auditable tool surface. Below is the finalized mapping to existing sub-skills under `finance-master` and `x-advanced-research`.

#### Capability → Sub-Skill Mapping (Final)

| Prompt Requirement | Primary Sub-Skill | Supporting Sub-Skill(s) | Invocation Rule |
|--------------------|-------------------|--------------------------|-----------------|
| Financial data & filings | `yfinance-data` + `funda-data` | — | Default for all cases |
| Transcript & lexical/tone analysis | `earnings-recap` | `finance-sentiment` | Auto on any earnings or management commentary case |
| Options flow & positioning | `options-payoff` | `stock-liquidity` | Trigger on short interest > 15% or unusual options activity |
| Physical trace / alternative data verification | `deep-analysis` | `stock-correlation`, `estimate-analysis` | Called during L2/L3 verification and Review the Givens Gate |
| Cross-market signal confirmation | `stock-correlation` | `hormuz-strait` (when relevant) | Explicitly called in Section 5.2 |
| Narrative interrogation & anomaly detection | `deep-analysis` | `earnings-recap` + `x-advanced-research` | Core support for active falsification |
| Management incentive & behavioral profiling | `deep-analysis` | `investor-panel` (optional escalation) | Triggered on L3 motive reconstruction |
| X/Twitter narrative monitoring | `x-advanced-research` | `finance-sentiment` | Used when real-time narrative vs. physical trace conflict is material |
| High-conviction second opinion | `investor-panel` | — | Only for borderline A-level cases |
| Low-quality signal / trap detection | `trap-detector` | — | Auto-trigger on external recommendations or high-hype narratives |

**Invocation Philosophy (to be embedded in prompt):**
Tools are invoked **only** to support mandatory reasoning steps (especially Active Falsification, Review the Givens Gate, and physical-trace verification). Tools must improve the chain — they do not replace it.

**Recommended Initial Tool Surface (Minimal Viable):**
- `yfinance-data` + `funda-data`
- `deep-analysis`
- `earnings-recap`
- `options-payoff`
- `x-advanced-research` (situationally)
- `stock-correlation` (situationally)

---

### Phase 5: Test Suite (Finalized)

#### Test Case Categories & Skill Focus (Final)

| Category | Primary Skills Exercised | Test Objective | # of Cases (First Suite) |
|----------|---------------------------|----------------|--------------------------|
| **Earnings Quality / Accounting Presentation** | `deep-analysis` + `earnings-recap` | Anomaly detection, L2/L3 labeling, physical-trace priority | 2–3 |
| **Narrative vs. Physical-Trace Conflict** | `deep-analysis` + `x-advanced-research` | Stripping PR rhetoric + real-time narrative monitoring | 2 |
| **Options / Short Interest Dynamics** | `options-payoff` + `deep-analysis` | Cross-signal integration + Review the Givens under momentum | 1–2 |
| **Management Incentive & Capital Allocation** | `deep-analysis` | Behavioral profiling + motive reconstruction | 1–2 |
| **Cross-Market Divergence** | `stock-correlation` + `deep-analysis` | Section 5.2 integration | 1 |
| **High Narrative Capture Risk** | `deep-analysis` + `x-advanced-research` + `trap-detector` | Epistemic Honesty Check + trap detection | 1 |

**Total First Suite:** 8–11 cases.

#### Evaluation Rubric (Final)

Use the 9-dimension rubric from the Testing Protocol, plus these two additions:

- **Skill Invocation Quality** — Were the right sub-skills called at the right time? Did they meaningfully strengthen the reasoning chain?
- **Tool + Reasoning Integration** — Was tool output effectively synthesized back into the L0–L3 chain and Review the Givens Gate?

**Success Thresholds (v1.0 → v1.1)**
- Average score ≥ 4.2 across all dimensions
- Skill Invocation Quality ≥ 4.0
- No dimension below 3.5 in more than one case
- Consistent application of Review the Givens Gate and Epistemic Honesty Check

---

## First Concrete Test Suite – Initiation

We will now begin building the actual test suite. Below is the proposed first batch of **6 high-signal cases** (balanced across skill combinations and prompt stress points).

### Proposed First 6 Test Cases

| # | Ticker / Situation | Category | Primary Skills to Exercise | Key Focus Areas | Input Package Outline |
|---|--------------------|----------|----------------------------|-----------------|-----------------------|
| 1 | **NVDA** (recent quarters with new metrics & segment shifts) | Earnings Quality | `deep-analysis` + `earnings-recap` | New defined metrics, defensive language, L2/L3 labeling | 10-Q excerpts + MD&A language + segment data + options flow |
| 2 | **GME** (2021 squeeze period – retrospective) | Options / Short Interest | `options-payoff` + `deep-analysis` + `x-advanced-research` | Narrative vs. positioning conflict, Review the Givens under extreme momentum | Historical short interest, options data, X narrative peaks, fundamental backdrop |
| 3 | **TSLA** (recent period with production vs. guidance mismatch) | Narrative vs. Physical-Trace | `deep-analysis` + `x-advanced-research` | Physical delivery data vs. management narrative | Production/delivery numbers, guidance language, X sentiment, channel checks |
| 4 | Company with aggressive buybacks + compensation changes (TBD – recent example) | Management Incentive | `deep-analysis` | Incentive alignment vs. capital allocation behavior | 10-K/Proxy + buyback history + compensation structure |
| 5 | US equity with clear credit or FX divergence (TBD) | Cross-Market Divergence | `stock-correlation` + `deep-analysis` | Section 5.2 integration | Equity data + credit spread / FX movement |
| 6 | High-hype name with weak physical evidence (TBD) | High Narrative Capture Risk | `deep-analysis` + `x-advanced-research` + `trap-detector` | Epistemic Honesty Check + trap detection | Narrative summary + contradictory physical/alternative data |

