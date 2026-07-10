**Hermes System Prompt v1.0 – Testing Execution Guide**  
**Version:** 1.0  
**Date:** 10 July 2026

### 1. Overview & Objectives

This guide provides a standardized process for testing **System Prompt v1.0** against the finalized 6-case suite. The goal is to generate consistent, comparable, and actionable feedback on the prompt’s effectiveness.

**Primary Objectives:**
- Validate that the mandatory reasoning steps (especially Review the Givens Gate and Epistemic Honesty Check) are followed reliably.
- Assess the quality of layered inference (L0–L3), physical-trace prioritization, and tool integration.
- Identify specific friction points and improvement opportunities for v1.1.

### 2. General Testing Process (Step-by-Step)

For **every** test case, follow this exact sequence:

1. **Prepare Input**  
   Use the exact Input Package defined for that case. Do not add extra context unless explicitly allowed in the package.

2. **Run the Prompt**  
   Feed the input into System Prompt v1.0.  
   - Do **not** pre-load hypotheses or desired outcomes.  
   - If the prompt asks clarifying questions, answer only with information from the Input Package.

3. **Capture Full Output**  
   Save the complete response (do not summarize).

4. **Score the Output**  
   Use the Scoring Rubric (Section 4). Score each dimension 1–5 with a short justification.

5. **Complete Post-Test Reflection**  
   Answer the reflection questions in Section 5.

6. **Log Results**  
   Record everything in the standardized log format (Section 6).

### 3. Per-Case Execution Notes

- **Case 1 (NVDA)**: Focus on how cleanly the agent handles new defined metrics. Push for explicit L2/L3 labeling.
- **Case 2 (GME 2021)**: This is a high-momentum retrospective case. Pay special attention to whether Review the Givens Gate is applied multiple times.
- **Case 3 (TSLA)**: Emphasize physical delivery data vs. narrative tone. Note whether Physical-Trace Verification Standards are followed.
- **Case 4 (META)**: Focus on incentive vs. capital allocation analysis quality.
- **Case 5 (TSLA 2022)**: Test whether cross-market signals are actively sought and integrated.
- **Case 6 (AMC 2021)**: High narrative capture risk. Evaluate whether Epistemic Honesty Check is triggered and whether trap detection behavior appears.

### 4. Scoring Rubric (Final)

Score each dimension from **1 (Poor)** to **5 (Excellent)**.

| # | Dimension | Description | Score | Justification |
|---|-----------|-------------|-------|---------------|
| 1 | **Reasoning Transparency** | Full inference chain visible and labeled (L0–L3). Easy to challenge any node. | | |
| 2 | **Review the Givens Gate** | Explicitly performed and documented. Clear impact on conclusion. | | |
| 3 | **Active Falsification** | Evidence of deliberate search for disconfirming data. | | |
| 4 | **Physical-Trace Priority** | Prioritized hard-to-fabricate traces over narrative-compatible explanations. | | |
| 5 | **Epistemic Honesty** | Explicit check performed. Confidence level appropriately calibrated. Emotional/cognitive factors acknowledged when relevant. | | |
| 6 | **Non-Obvious Insight** | Surfaced connections or questions a standard analyst would likely miss. | | |
| 7 | **Language Quality** | Concise, high-velocity, low fluff. No unnecessary softening. | | |
| 8 | **Collaboration Readiness** | Output invites challenge and shows where user input would be valuable. | | |
| 9 | **Skill Invocation Quality** | Right sub-skills called at right time. Tool output meaningfully improved the chain. | | |
| 10 | **Tool + Reasoning Integration** | Tool output was effectively synthesized back into L0–L3 chain and Review the Givens Gate. | | |

**Overall Score** (Average of 1–10): ____

**Pass / Fail for this case**: (Average ≥ 4.0 = Pass)

### 5. Post-Test Reflection Questions

After scoring, answer the following:

1. **What worked well** in this test case?
2. **What friction points** or weaknesses did you observe?
3. **Which prompt section(s)** performed best or worst?
4. **One specific, actionable improvement** you would make to the prompt based on this case.
5. **Any missing capability** that became obvious during this test?

### 6. Standardized Logging Format

Use this format for every test case:

```markdown
**Test Case #X – [Ticker/Situation]**
**Date Run:** 
**Overall Score:** __ / 5.0
**Pass/Fail:** 

**Dimension Scores:**
1. Reasoning Transparency: __
2. Review the Givens Gate: __
...
3. Tool + Reasoning Integration: __

**Strengths:**
- 

**Weaknesses / Friction Points:**
- 

**Specific Improvement Recommendation:**
- 

**Prompt Section Most Impacted:**
- 
```

### 7. Overall Suite Tracking

After completing all 6 cases, produce a **Testing Summary Report** containing:

- Average score across all 10 dimensions
- Number of cases that passed
- Top 3 recurring strengths
- Top 3 recurring weaknesses
- Prioritized list of changes for v1.1 (ranked by impact)
- Recommendation on whether the prompt is ready to move to broader testing or needs another iteration round

---

**This Testing Execution Guide is now complete and ready for use.**

You can begin running the test cases immediately using this guide.

**Recommended Immediate Next Step:**

Would you like me to:

**A.** Start running **Test Case 1 (NVDA)** now and produce the full scored output + reflection using this guide?

**B.** Adjust anything in the Testing Execution Guide first?

**C.** Prepare a blank scoring + logging template file for easier use during testing?

Please state your preference.