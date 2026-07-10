### Upgraded Confidence Grading Framework (v3.0)

The new system moves beyond passive labeling. Every confidence grade must now be earned through measurable verification density across multiple dimensions.

#### Core Principle
A confidence grade is not a subjective feeling about the conclusion. It is an objective assessment of **how thoroughly and independently the inference chain has been stress-tested and corroborated**.

---

### Multidimensional Confidence Criteria

Each hypothesis or conclusion is scored across **five verification dimensions**. The final grade is determined by the weakest dimension (the system is only as strong as its weakest link).

| Dimension | Description | What “Strong” Looks Like | Scoring Weight |
|---------|-------------|--------------------------|----------------|
| **1. Evidence Chain Independence** | How independent are the supporting data sources? | ≥3 truly independent sources (e.g., filings + options flow + supplier data + insider behavior) | High |
| **2. Falsification Rigor** | How aggressively was the hypothesis tested against disconfirming evidence? | Multiple active attempts to disprove it were made and survived | High |
| **3. Assumption Audit Depth** | How recently and thoroughly were core assumptions reviewed? | Key assumptions were explicitly re-audited in Step 1 with documented stress tests | High |
| **4. Physical/Mechanical Confirmation** | How much of the support comes from hard, difficult-to-manipulate data vs. narrative? | Majority of weight comes from cash flow, inventory, capex reality, options positioning, or insider filings | Medium-High |
| **5. Layer Integrity** | Are L0–L3 clearly separated and labelled without collapse? | All inference layers are explicitly shown and no L2/L3 claims are presented as L1 | Medium |

---

### Revised Confidence Grade Definitions

**A-Grade (High Confidence)**  
All five dimensions must meet the following minimums:

- **Evidence Independence**: At least 3 independent evidence chains converge.
- **Falsification Rigor**: The hypothesis has survived deliberate attempts to disprove it across multiple angles.
- **Assumption Audit**: Core assumptions were re-audited within this analysis cycle and stress-tested.
- **Physical/Mechanical Weight**: At least 60% of the supporting weight comes from hard data rather than narrative or management guidance.
- **Layer Integrity**: All layers (L0–L3) are explicitly labelled with no collapse of higher-order inferences into lower ones.

**Requirement**: The inference chain must be strong enough that a competent skeptic would struggle to dismantle it without introducing new contradictory data.

**B-Grade (Moderate Confidence)**  
The conclusion is directionally supported, but at least one dimension is materially weaker:

- Usually fails on either **Evidence Independence** (only 1–2 strong chains) or **Falsification Rigor** (limited active disproving performed).
- May have one or more material untested assumptions.
- Physical/mechanical confirmation is present but not dominant.

**C-Grade (Low Confidence / Speculative)**  
The hypothesis is logically coherent but fails multiple dimensions:

- Heavy reliance on narrative or unverified assumptions.
- Limited independent evidence chains.
- Little to no active falsification performed.
- Inference layers are often collapsed or poorly labelled.

**Iron Rule**: A C-grade conclusion must be explicitly labelled as such and cannot be presented with the same tone or weight as A or B-grade conclusions.

---

### Integration into the Enhanced Reasoning Engine

This upgraded grading system is now embedded primarily in **Step 4**, with supporting requirements in Steps 0, 3, and 5.

**Updated Step 4 Requirements**:

When assigning confidence, the agent must:

1. Explicitly evaluate the conclusion against all five dimensions above.
2. State which dimension(s) are the limiting factor(s) if the grade is not A.
3. Provide a short **Verification Density Summary** (1–2 sentences) explaining the grade.

**Example Output Format (Step 4)**:

**Confidence Assessment**  
- **Grade**: B  
- **Limiting Dimensions**: Evidence Chain Independence (only two strong independent sources) and Falsification Rigor (limited stress-testing on margin sustainability assumption).  
- **Verification Density Summary**: Supported by earnings quality analysis and options flow, but channel inventory build has not yet been triangulated against distributor data. One key assumption (pricing power persistence) has not been aggressively falsified.

---

### Strengthened Requirements in Other Steps

- **Step 0 (Pre-Observation)**: Must document which data sources will be used to build independent evidence chains.
- **Step 3 (Falsification)**: Must include deliberate attempts to attack the hypothesis along its weakest dimension(s).
- **Step 5 (Path Exposure)**: Must include the Verification Density Summary and highlight the weakest dimension(s) as explicit Challenge Nodes for the user.

---

### Before vs After Example

**Old Style (Passive)**:  
“Confidence: B. The thesis is supported by the earnings beat and short interest data, but there is still some uncertainty around guidance credibility.”

**New Style (Active Quality Gate)**:  
**Confidence: B**  
**Limiting Dimensions**: Falsification Rigor and Physical Confirmation.  
**Verification Density Summary**: Supported by two independent chains (earnings quality + elevated short interest), but the hypothesis that margins are structurally improved has not been aggressively tested against a 150 bps pricing reversal scenario. Physical confirmation from cash flow conversion remains only moderate.

---

This upgraded Confidence Grading system transforms the mechanism from a simple label into a diagnostic instrument that forces visible verification density and highlights structural weaknesses in the inference chain.

---
