# Serenity-style high-risk US movers · v4.5

> Used by `x-advanced-research` in **high_risk_movers** mode.  
> Output feeds Brain → `serenity-skill` → `deep-analysis` (Top ≤3). This file does **not** authorize calling those skills directly.

## Principles

1. **Serenity priority** — @aleabitoreddit and key-accounts.md high-priority handles.  
2. **Bottleneck language** — single supplier, long lead time, capacity, scarce materials, AI infra physics.  
3. **Catalyst language** — orders, design wins, earnings, regulatory, tech validation.  
4. **US-listed only** — `$TICKER` on NYSE/Nasdaq/ARCA; drop pure A/HK codes.  
5. **Asymmetry framing** — small-cap / high beta possible; always risk_flags.  
6. **X is lead-gen** — not proof; serenity + deep verify.

## Execution checklist

| Step | Action |
|------|--------|
| 1 | Semantic + keyword on theme + `from:@aleabitoreddit` (and other key accounts) |
| 2 | Window: since last 7–30d; `min_faves` tuned to niche; `-filter:replies` when noisy |
| 3 | Extract tickers + quote snippet + post URL/id |
| 4 | Cluster by bottleneck vs pure meme; demote pure hype |
| 5 | Optional Web lead sites (non-blocking): analysissite.vercel.app, serenity.bemix.cc, Reddit Alpha, etc. |
| 6 | Emit ≤15 US tickers in RETURN_BLOCK |

## Candidate row shape

```text
symbol: XXX
us_listed: true
catalyst_or_bottleneck: <one line>
x_evidence: [urls]
engagement_note: likes/reposts/views if known
risk_flags: [illiquidity, dilution, hype, single_customer, ...]
signal_strength: high|med|low
```

## Ranking heuristic

1. Serenity / key-account endorsement with specific constraint logic  
2. Multi-account convergent mention  
3. Clear catalyst window  
4. Engagement quality (not bot spam)  
5. Demote: no business logic, only emoji pumps, non-US

## Brain handoff line

```text
next_brain_hint: serenity_score
# Brain will score ≤5 then deep-analysis ≤3 with DATA_PACK.DEEP (dims D0–D19)
```

## Disclaimer

High risk. Research only. Not investment advice.
