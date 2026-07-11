---
name: x-advanced-research
description: >
  L2 X/Twitter research meta-router for finance-master v4.6.6 (Grok-native).
  Routes intents to x_keyword_search / x_semantic_search / x_thread_fetch / x_user_search,
  prioritizes key accounts, and returns structured US ticker discoveries for the Central
  Brain. Does NOT call serenity-skill or deep-analysis. Triggers: X research, Serenity
  movers, high-risk US scans, sentiment on X, profile dive, bottleneck signals on Twitter.
version: 4.6.8
ecosystem: 4.6.8
metadata:
  tags: [finance, us-stocks, x-twitter, research, discovery, serenity]
  market_scope: US_EQUITIES_ONLY
  role: L2_ORCHESTRATOR_X
  related_skills:
    - finance-master/sherlock-finance
    - finance-master/serenity-skill
---

# x-advanced-research · v4.6.6

> **L2 skill under Central Brain (`sherlock-finance`).**  
> You plan and run **Grok-native X tools only** for social discovery.  
> You **do not** INVOKE `serenity-skill`, `deep-analysis`, or other L2 skills — the Brain owns the chain.

---

## Consumer rules

1. Prefer Brain `budget` and any prior `SESSION_CACHE.social_x`.  
2. **US tickers only** in discovery lists (`$AAPL`, NYSE/Nasdaq names). Drop pure A/HK codes.  
3. Quality > volume: engagement filters, key accounts, de-spam.  
4. Always cite posts (URL / id) + engagement when available.  
5. End with user-facing summary **and** `### RETURN_BLOCK` for the Brain.  
6. **No scaffold questions** (“要不要我创建 references?”) — refs already exist.  
7. Cap tool calls: general research ~8–12; mover scan ~10–15 unless Brain raises budget.

---

## Tools (Grok native)

| Tool | Use |
|------|-----|
| `x_semantic_search` | Broad theme discovery |
| `x_keyword_search` | Operators: `from:`, `min_faves:`, `since:`, `-filter:replies`, `$TICKER` |
| `x_thread_fetch` | Deep threads |
| `x_user_search` | Resolve handles |

Fallback if X tools missing: Web search for public X mirrors + label confidence ≤ B.

---

## Intent router

| Intent | Strategy |
|--------|----------|
| Trend / monitor | semantic → keyword (time + engagement) → top threads |
| Profile dive | user_search → `from:@handle` high faves → thread fetch |
| Thread transform | `x_thread_fetch` → structured notes |
| High-engagement scrape | keyword + `min_faves` + niche terms |
| Sentiment | semantic + keyword → bull/bear/neutral mix + cites |
| Bottleneck / supply signals | semantic + expert `from:` accounts + chokepoint keywords |
| **High-risk US / Serenity movers** | See below + `references/serenity-high-risk-movers.md` |
| Complex multi-part | Parallel semantic + targeted keyword; still one RETURN |

Key accounts: `references/key-accounts.md` — **@aleabitoreddit Top #1** for Serenity-style AI infra / bottleneck.

Search craft: `references/search-strategies.md`.  
Templates: `references/output-templates.md`.

---

## High-risk mover mode (Brain discovery chain step ①)

**Triggers:** Serenity 风格、卡点、高风险快涨美股、catalyst movers、asymmetric upside、监控 @aleabitoreddit  

**Steps**
1. Pull Serenity + other high-priority accounts (7–30d window, engagement floor).  
2. Extract **US** `$TICKER` + context (bottleneck / catalyst / risk).  
3. Optional second pass on top tickers (semantic + keyword).  
4. Optional Web cross-check list (do not block on third-party sites): analysissite / serenity panels / Reddit Alpha — as **leads only**.  
5. Rank ≤**15** candidates (Brain will serenity-score then deep ≤3).  

**Do not** run deep valuation or full bottleneck scoring here (that is serenity / deep).

---

## Chain contract (finance-master)

```text
Brain §9 high-beta path:
  ① INVOKE x-advanced-research  → RETURN tickers[≤15 US] + evidence
  ② INVOKE serenity-skill       → RETURN scored[≤5]     (Brain does this)
  ③ INVOKE deep-analysis ×≤3   → full D0–D19           (Brain does this)
```

This skill **stops after ①**. Never self-call ②/③.

---


## L2 confidence (Cog-4 · advisory only)

`confidence` in `### RETURN_BLOCK` is **skill-local deliverable quality**, not user investment confidence.

| Rule | Max grade |
|------|-----------|
| `status: partial` or material `fields_gap` | **B** |
| X/social-only evidence for hard claims | **C** |
| `status: blocked` | no thesis A |
| Complete skill scope + hard sources + no material gaps | **A** allowed (still advisory) |

Default `confidence_scope` for this skill: **discovery**.

Grade = quality of the **ticker list / post pack**, not pre-deep investment rank. Brain keeps pre-deep names **≤ B**. Pure X-only heat without cites → **≤ C**.

Also emit Cog-4 fields when practical: `confidence_scope`, `confidence_basis` (evidence_independence, physical_mechanical, data_gaps_material), `limiting_factors`.

**Never** emit Brain `### CONFIDENCE_BLOCK` or `mode:` — the Central Brain re-grades via §H.6.

## Output

### User-facing
- Intent summary  
- Key posts / quotes with links  
- Themes / sentiment  
- **US ticker table** (if discovery): ticker, why, signal strength, risk flags, source posts  

### RETURN_BLOCK (required)

```text
### RETURN_BLOCK
skill: x-advanced-research
status: ok|partial
ticker: MULTI|SYM|none
confidence: A|B|C
confidence_scope: discovery
confidence_basis:
  evidence_independence: strong|weak|gap
  physical_mechanical: strong|weak|gap
  data_gaps_material: true|false
limiting_factors: []
fields_filled: [posts, tickers?]
fields_gap: [...]
artifacts:
  mode: trend|profile|thread|sentiment|bottleneck|high_risk_movers|mixed
  tickers:
    - symbol: XXX
      us_listed: true
      catalyst_or_bottleneck: "..."
      x_evidence: [url_or_id, ...]
      engagement_note: "..."
      risk_flags: [...]
  themes: [...]
  key_accounts_used: [...]
  next_brain_hint: serenity_score|none|sentiment_only
counterfactuals: []
raw_notes: <≤400 words>
```

`tickers` array **max 15**. Prefer 5–10 high-signal names.

---

## Safety

- Filter obvious spam / paid signal spam; downrank pump language (Brain may still run trap-detector separately).  
- Research only — no trade execution.  
- Do not invent tickers not grounded in posts or Web.

---

*v4.6.6 · DATA_PACK consumer · Cog-4 conf advisory · IBKR market-data only*
