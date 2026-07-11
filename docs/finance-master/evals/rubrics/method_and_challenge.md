# Rubric · Method Library + Challenge Nodes (Val-1)

Complements `conf_all_modes.md` and `handoff_contracts.md`.

## Challenge Nodes

### Must appear (directional thesis)

```text
### CHALLENGE_NODES
- id: CN1
  layer: ...
  claim: "..."
  assumption: "..."
  what_would_falsify: "observable + window"
  conf_dim_link: ...
```

### Minimum counts (Brain §1.5)

| mode_effective | Minimum |
|----------------|--------:|
| lite | 1 |
| standard | 1; **2** if grade B or C |
| max | ≥2; **≥3** if grade B/C or multi-name screen |

### Fail if

| Condition | Result |
|-----------|--------|
| Missing section on directional thesis | FAIL |
| Node lacks `what_would_falsify` | FAIL |
| Count below mode min | FAIL |
| Nodes are pure fluff with no observable | FAIL |

---

## Method Library (§M)

### Caps

| mode_effective | Max cards | Note |
|----------------|----------:|------|
| lite | **0** | `METHOD_CARDS_LOADED: []` + `method_cards_skipped: lite` |
| standard | **3** | trigger-matched only |
| max | **6** | ranked; never whole library |

### Pass

- Cards only from M01–M12  
- Recorded as `METHOD_CARDS_LOADED: [M05, …]`  
- No dump of entire `method-library/` tree  

### Fail if

| Condition | Result |
|-----------|--------|
| lite loads any card body | FAIL |
| standard &gt;3 or max &gt;6 | FAIL |
| Invalid ids outside M01–M12 | FAIL |
| Cards used as excuse to call banned data tools | FAIL |

---

## Structural automation

```bash
python3 evals/run_structural_checks.py
```

Human/LLM judgment still required for semantic quality of claims and falsifiers.
