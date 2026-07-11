#!/usr/bin/env python3
"""
Val-1 structural checker for finance-master golden-path artifacts.

Offline, regex-based assertions aligned with:
  - rubrics/conf_all_modes.md
  - rubrics/handoff_contracts.md
  - rubrics/step0_data_plane.md
  - Brain §1.4 / §1.5 / §M / §H

Usage:
  python3 evals/run_structural_checks.py
  python3 evals/run_structural_checks.py --gold-only
  python3 evals/run_structural_checks.py --negatives-only
  python3 evals/run_structural_checks.py --file evals/artifacts/GP01_sample_output.md

Exit code: 0 if gold all pass AND negatives all fail as expected; else 1.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Scenario rules (positive / gold)
# ---------------------------------------------------------------------------

BANNED_LIVE_PATTERNS = [
    r"\byfinance\b",
    r"\blongbridge\b",
    r"\bfunda(?:-data)?\b",
    r"\bopencli(?:-reader)?\b",
    r"\bakshare\b",
    r"_quarantine/",
    r"\blhb-analyzer\b",
    r"\btwitter-reader\b",
    r"\bdiscord-reader\b",
    r"\btelegram-reader\b",
    r"\blinkedin-reader\b",
    r"\btradingview-reader\b",
]

# Mentions of banned tools are OK only in explicit "not used" / ban context
BANNED_ALLOW_CONTEXT = re.compile(
    r"(no\s+yfinance|not\s+yfinance|banned|never|do\s+not\s+use|"
    r"no\s+longbridge|without\s+yfinance|not\s+.*funda)",
    re.I,
)


@dataclass
class ScenarioRule:
    id: str
    required_mode: str
    conf_required: bool = True
    min_challenge_nodes: int = 1
    max_method_cards: int = 3
    require_method_empty: bool = False  # lite
    require_hard_stop: bool = False
    forbid_deep: bool = False
    require_deep_cap: Optional[int] = None  # max deep_count
    require_return_block: bool = False
    require_brain_regrade: bool = False
    require_us_only_drop: bool = False
    require_givens: bool = True
    require_l0_source: bool = True
    min_independent_chains_if_grade_a: int = 3
    extra_checks: List[Callable[[str, "CheckResult"], None]] = field(default_factory=list)


RULES: dict[str, ScenarioRule] = {
    "GP01": ScenarioRule(
        id="GP01",
        required_mode="standard",
        min_challenge_nodes=2,  # B-grade → ≥2
        max_method_cards=3,
        require_return_block=True,
        require_brain_regrade=True,
    ),
    "GP02": ScenarioRule(
        id="GP02",
        required_mode="lite",
        min_challenge_nodes=1,
        max_method_cards=0,
        require_method_empty=True,
        forbid_deep=True,
    ),
    "GP03": ScenarioRule(
        id="GP03",
        required_mode="standard",
        min_challenge_nodes=2,
        max_method_cards=3,
    ),
    "GP04": ScenarioRule(
        id="GP04",
        required_mode="lite",
        conf_required=True,
        min_challenge_nodes=1,
        max_method_cards=0,
        require_method_empty=True,
        require_hard_stop=True,
        forbid_deep=True,
        require_return_block=True,
        require_brain_regrade=True,
    ),
    "GP05": ScenarioRule(
        id="GP05",
        required_mode="max",
        min_challenge_nodes=3,
        max_method_cards=6,
        require_deep_cap=3,
        require_us_only_drop=True,
        require_return_block=True,
        require_brain_regrade=True,
    ),
    "GP06": ScenarioRule(
        id="GP06",
        required_mode="standard",
        min_challenge_nodes=2,
        max_method_cards=3,
        require_return_block=True,
        require_brain_regrade=True,
    ),
}


# ---------------------------------------------------------------------------
# Negative cases (must FAIL under named rule; at least one expected error)
# ---------------------------------------------------------------------------

@dataclass
class NegativeCase:
    filename: str
    rule_id: str
    expect_error_substrings: List[str]  # any match counts as expected class hit
    description: str = ""


NEGATIVE_CASES: List[NegativeCase] = [
    NegativeCase(
        "NEG01_missing_conf.md",
        "GP01",
        ["missing ### CONFIDENCE_BLOCK"],
        "no conf block on directional thesis",
    ),
    NegativeCase(
        "NEG02_banned_yfinance.md",
        "GP01",
        ["banned live-route"],
        "yfinance/longbridge live route",
    ),
    NegativeCase(
        "NEG03_lite_method_cards.md",
        "GP02",
        ["lite must not load method cards"],
        "lite loads M-cards",
    ),
    NegativeCase(
        "NEG04_lite_runs_deep.md",
        "GP02",
        ["lite path appears to run deep"],
        "lite deep/panel allowlist break",
    ),
    NegativeCase(
        "NEG05_trap_buy_through.md",
        "GP04",
        [
            "trap path missing hard_stop",
            "trap path missing trap-detector",
            "trap path appears to issue buy recommendation",
            "trap path must not invoke deep",
        ],
        "trap buy-through / missing hard stop",
    ),
    NegativeCase(
        "NEG06_deep_over_cap.md",
        "GP05",
        ["deep_count=", "deep_count"],
        "discovery deep×>3",
    ),
    NegativeCase(
        "NEG07_grade_a_thin_chains.md",
        "GP01",
        ["grade A with only"],
        "A-grade without ≥3 chains",
    ),
    NegativeCase(
        "NEG08_no_brain_regrade.md",
        "GP06",
        ["missing Brain re-grade"],
        "L2 without Brain re-grade",
    ),
    NegativeCase(
        "NEG09_challenge_no_falsify.md",
        "GP03",
        ["what_would_falsify"],
        "challenge nodes missing falsifier",
    ),
    NegativeCase(
        "NEG10_mode_mismatch.md",
        "GP02",
        [
            "CONFIDENCE_BLOCK mode=",
            "conf mode (",
            "!= mode_effective",
        ],
        "conf mode ≠ mode_effective",
    ),
]


@dataclass
class CheckResult:
    scenario: str
    path: Path
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _section_after(text: str, header: str, stop_headers: Sequence[str]) -> str:
    """Return text from header until next stop header or EOF."""
    idx = text.find(header)
    if idx < 0:
        return ""
    rest = text[idx + len(header) :]
    end = len(rest)
    for h in stop_headers:
        j = rest.find(h)
        if j >= 0:
            end = min(end, j)
    return rest[:end]


def extract_confidence_block(text: str) -> str:
    """Extract conf body; accept ### CONFIDENCE_BLOCK or ### Brain CONFIDENCE_BLOCK as a heading line only."""
    m = re.search(r"(?m)^###[^\n]*\bCONFIDENCE_BLOCK\b[^\n]*$", text)
    if not m:
        return ""
    return _section_after(
        text,
        m.group(0),
        ("### CHALLENGE_NODES", "### Conclusion", "### §", "## ", "METHOD_CARDS"),
    )


def extract_challenge_nodes(text: str) -> str:
    m = re.search(r"(?m)^###\s*CHALLENGE_NODES\s*$", text)
    if not m:
        # fallback: allow trailing annotation on heading
        m = re.search(r"(?m)^###\s*CHALLENGE_NODES\b[^\n]*$", text)
    if not m:
        return ""
    return _section_after(
        text,
        m.group(0),
        ("### Conclusion", "### §", "## ", "METHOD_CARDS", "DEEP_", "BUY_"),
    )


def parse_grade(conf: str) -> Optional[str]:
    m = re.search(r"^grade:\s*([ABC])\b", conf, re.M | re.I)
    return m.group(1).upper() if m else None


def parse_mode(conf: str) -> Optional[str]:
    m = re.search(r"^mode:\s*(lite|standard|max)\b", conf, re.M | re.I)
    return m.group(1).lower() if m else None


def parse_mode_effective(text: str) -> Optional[str]:
    m = re.search(r"\*\*mode_effective:\*\*\s*(lite|standard|max)\b", text, re.I)
    if m:
        return m.group(1).lower()
    m = re.search(r"^mode_effective:\s*(lite|standard|max)\b", text, re.M | re.I)
    return m.group(1).lower() if m else None


def count_challenge_nodes(cn: str) -> int:
    return len(re.findall(r"^\s*-\s*id:\s*CN\d+", cn, re.M | re.I))


def challenge_nodes_have_falsify(cn: str) -> bool:
    nodes = re.split(r"^\s*-\s*id:\s*CN\d+", cn, flags=re.M | re.I)
    bodies = nodes[1:] if len(nodes) > 1 else []
    if not bodies:
        return False
    for body in bodies:
        if not re.search(r"what_would_falsify\s*:", body, re.I):
            return False
    return True


def parse_method_cards(text: str) -> List[str]:
    m = re.search(r"METHOD_CARDS_LOADED:\s*\[([^\]]*)\]", text, re.I)
    if not m:
        return []
    inner = m.group(1).strip()
    if not inner:
        return []
    return [p.strip().upper() for p in re.split(r"[,\s]+", inner) if p.strip()]


def count_independent_chains(conf: str) -> int:
    m = re.search(r"independent_chains\s*:\s*(.+?)(?:\n\n|\n###|\nMETHOD_|\Z)", conf, re.S | re.I)
    if not m:
        return 0
    block = m.group(1)
    items = re.findall(r'^\s*-\s*["\']?.+', block, re.M)
    if items:
        return len(items)
    inline = re.search(r"\[([^\]]+)\]", block)
    if inline:
        parts = [p.strip() for p in inline.group(1).split(",") if p.strip()]
        return len(parts)
    return 0


def dims_present(conf: str) -> bool:
    required = [
        "evidence_independence",
        "falsification_rigor",
        "assumption_audit",
        "physical_mechanical",
        "layer_integrity",
    ]
    return all(re.search(rf"{d}\s*:", conf, re.I) for d in required)


def banned_hits(text: str) -> List[str]:
    hits = []
    for pat in BANNED_LIVE_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            start = max(0, m.start() - 40)
            end = min(len(text), m.end() + 40)
            window = text[start:end]
            if BANNED_ALLOW_CONTEXT.search(window):
                continue
            if re.search(r"banned\s*(primary)?\s*stacks?", window, re.I):
                continue
            hits.append(m.group(0))
    return sorted(set(hits))


def check_file(path: Path, rule: ScenarioRule) -> CheckResult:
    text = path.read_text(encoding="utf-8")
    res = CheckResult(scenario=rule.id, path=path)

    # --- banned tools ---
    hits = banned_hits(text)
    if hits:
        res.errors.append(f"banned live-route tokens: {hits}")

    # --- mode_effective ---
    me = parse_mode_effective(text)
    if not me:
        res.errors.append("missing mode_effective")
    elif me != rule.required_mode:
        res.errors.append(f"mode_effective={me} != required {rule.required_mode}")

    # --- L0 sources ---
    if rule.require_l0_source:
        if not re.search(r"source:\s*(IBKR|WEB|X|CACHE|USER)", text, re.I):
            res.errors.append("no L0 source: IBKR|WEB|X|CACHE|USER tags")

    # --- Givens ---
    if rule.require_givens:
        if not re.search(r"Review the Givens|Givens", text, re.I):
            res.errors.append("missing Givens section")

    conf = extract_confidence_block(text)
    if rule.conf_required:
        if not conf.strip():
            res.errors.append("missing ### CONFIDENCE_BLOCK")
        else:
            grade = parse_grade(conf)
            mode = parse_mode(conf)
            if not grade:
                res.errors.append("CONFIDENCE_BLOCK missing grade: A|B|C")
            if not mode:
                res.errors.append("CONFIDENCE_BLOCK missing mode:")
            elif mode != rule.required_mode:
                res.errors.append(f"CONFIDENCE_BLOCK mode={mode} != {rule.required_mode}")
            if me and mode and mode != me:
                res.errors.append(f"conf mode ({mode}) != mode_effective ({me})")
            if not dims_present(conf):
                res.errors.append("CONFIDENCE_BLOCK missing one or more of 5 dims")
            if not re.search(r"limiting\s*:", conf, re.I):
                res.errors.append("CONFIDENCE_BLOCK missing limiting:")
            if not re.search(r"verification_density\s*:", conf, re.I):
                res.errors.append("CONFIDENCE_BLOCK missing verification_density:")
            if not re.search(r"independent_chains\s*:", conf, re.I):
                res.errors.append("CONFIDENCE_BLOCK missing independent_chains:")
            n_chains = count_independent_chains(conf)
            if grade == "A" and n_chains < rule.min_independent_chains_if_grade_a:
                res.errors.append(
                    f"grade A with only {n_chains} independent_chains "
                    f"(need ≥{rule.min_independent_chains_if_grade_a})"
                )
            chains_blob = conf.lower()
            if grade in ("A", "B"):
                has_hard = bool(re.search(r"ibkr|web|filing|fcf|model", chains_blob))
                only_x = "x:" in chains_blob or "x " in chains_blob
                if only_x and not has_hard and grade == "A":
                    res.errors.append("grade A appears X-only (need hard chains)")
            if rule.required_mode == "lite" and grade == "A":
                if n_chains < 3 and not rule.require_hard_stop:
                    res.errors.append("lite grade A without ≥3 independent_chains")

    # --- Challenge nodes ---
    if rule.conf_required:
        cn = extract_challenge_nodes(text)
        if not cn.strip():
            res.errors.append("missing ### CHALLENGE_NODES")
        else:
            n = count_challenge_nodes(cn)
            if n < rule.min_challenge_nodes:
                res.errors.append(
                    f"CHALLENGE_NODES count={n} < min {rule.min_challenge_nodes}"
                )
            if not challenge_nodes_have_falsify(cn):
                res.errors.append("one or more challenge nodes missing what_would_falsify")

    # --- Method cards ---
    cards = parse_method_cards(text)
    if rule.require_method_empty:
        if cards:
            res.errors.append(f"lite must not load method cards; got {cards}")
        if not re.search(r"method_cards_skipped\s*:\s*lite", text, re.I):
            if not cards:
                res.warnings.append("prefer method_cards_skipped: lite on lite path")
    if len(cards) > rule.max_method_cards:
        res.errors.append(
            f"METHOD_CARDS_LOADED count={len(cards)} > max {rule.max_method_cards}"
        )
    for c in cards:
        if not re.fullmatch(r"M(0[1-9]|1[0-2])", c):
            res.errors.append(f"invalid method card id: {c}")

    # --- Trap hard stop ---
    if rule.require_hard_stop:
        if not re.search(r"hard_stop\s*:\s*true|HARD STOP|hard stop", text, re.I):
            res.errors.append("trap path missing hard_stop")
        if not re.search(r"trap-detector", text, re.I):
            res.errors.append("trap path missing trap-detector")
        if re.search(r"naked buy|worth buying now|建议买入|现在买入", text, re.I):
            res.errors.append("trap path appears to issue buy recommendation")
        if re.search(r"DEEP_INVOKED:\s*true", text, re.I):
            res.errors.append("trap path must not invoke deep")

    # --- forbid deep ---
    if rule.forbid_deep and not rule.require_hard_stop:
        if re.search(r"deep-analysis|investor-panel|serenity-skill", text, re.I):
            if not re.search(r"no deep|not deep|without deep|discovery DAG", text, re.I):
                res.errors.append("lite path appears to run deep/panel/serenity")

    # --- deep cap ---
    if rule.require_deep_cap is not None:
        m = re.search(r"deep_count\s*:\s*(\d+)", text, re.I)
        if not m:
            res.errors.append("missing deep_count for discovery scenario")
        else:
            n = int(m.group(1))
            if n > rule.require_deep_cap:
                res.errors.append(f"deep_count={n} > cap {rule.require_deep_cap}")

    # --- US drop ---
    if rule.require_us_only_drop:
        if not re.search(r"FAKEHK|us_listed\s*=\s*false|non-US|excluded", text, re.I):
            res.warnings.append("expected explicit non-US drop documentation")

    # --- RETURN_BLOCK ---
    if rule.require_return_block:
        if not re.search(r"###\s*RETURN_BLOCK", text):
            res.errors.append("missing ### RETURN_BLOCK")
        if not re.search(r"###\s*INVOKE", text):
            res.warnings.append("prefer ### INVOKE with RETURN_BLOCK")

    # --- Brain re-grade ---
    # Require explicit Cog-4 log markers (not prose mention of "re-grade")
    if rule.require_brain_regrade:
        if not re.search(
            r"BRAIN_REGRADE\s*:|L2_CONF_ADVISORY\s*:|###\s*Brain CONFIDENCE_BLOCK",
            text,
            re.I,
        ):
            res.errors.append("missing Brain re-grade after L2")
        if not re.search(r"L2_CONF_ADVISORY\s*:", text, re.I):
            res.warnings.append("prefer L2_CONF_ADVISORY log line (Cog-4)")
        if re.search(r"confidence:\s*A", text) and parse_grade(conf or "") == "A":
            if not re.search(r"BRAIN_REGRADE\s*:|safety classification|hard_stop", text, re.I):
                res.warnings.append(
                    "L2 conf A and Brain A — ensure this is intentional with full chains"
                )

    # Cog-4: if RETURN_BLOCK present, prefer confidence_scope
    if re.search(r"###\s*RETURN_BLOCK", text):
        if not re.search(r"confidence_scope\s*:", text, re.I):
            res.warnings.append("RETURN_BLOCK missing confidence_scope (Cog-4 preferred)")
        if re.search(r"###\s*CONFIDENCE_BLOCK", text) and "L2" in text:
            if conf and not parse_mode(conf):
                res.errors.append("CONFIDENCE_BLOCK missing mode: (Brain-owned)")

    return res


def discover_artifacts(artifacts_dir: Path) -> List[Path]:
    return sorted(artifacts_dir.glob("GP*_sample_output.md"))


def scenario_id_from_path(path: Path) -> Optional[str]:
    m = re.match(r"(GP\d+)", path.name, re.I)
    return m.group(1).upper() if m else None


def expected_error_hit(errors: Sequence[str], substrings: Sequence[str]) -> bool:
    blob = " | ".join(errors)
    return any(s.lower() in blob.lower() for s in substrings)


def run_gold(files: Sequence[Path]) -> Tuple[List[CheckResult], int]:
    results: List[CheckResult] = []
    failed = 0
    for f in files:
        sid = scenario_id_from_path(f)
        if not sid or sid not in RULES:
            r = CheckResult(scenario=sid or "?", path=f)
            r.errors.append(f"no ScenarioRule for {f.name}")
            results.append(r)
            failed += 1
            continue
        r = check_file(f, RULES[sid])
        results.append(r)
        if not r.ok:
            failed += 1
    return results, failed


def run_negatives(neg_dir: Path) -> Tuple[List[Tuple[NegativeCase, CheckResult, str]], int]:
    """
    Returns list of (case, result, meta_status) where meta_status is
    META_PASS | META_FAIL | MISSING.
    failed count = number that are not META_PASS.
    """
    out: List[Tuple[NegativeCase, CheckResult, str]] = []
    failed = 0
    for case in NEGATIVE_CASES:
        path = neg_dir / case.filename
        if not path.is_file():
            dummy = CheckResult(scenario=case.rule_id, path=path)
            dummy.errors.append(f"missing negative fixture: {path}")
            out.append((case, dummy, "MISSING"))
            failed += 1
            continue
        if case.rule_id not in RULES:
            dummy = CheckResult(scenario=case.rule_id, path=path)
            dummy.errors.append(f"unknown rule_id {case.rule_id}")
            out.append((case, dummy, "META_FAIL"))
            failed += 1
            continue
        r = check_file(path, RULES[case.rule_id])
        if r.ok:
            # Negative that passes structural checks = suite failure
            meta = "META_FAIL"
            failed += 1
        elif expected_error_hit(r.errors, case.expect_error_substrings):
            meta = "META_PASS"
        else:
            meta = "META_FAIL"
            failed += 1
        out.append((case, r, meta))
    return out, failed


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Val-1 structural checks (+ negatives)")
    parser.add_argument(
        "--artifacts-dir",
        type=Path,
        default=None,
        help="Directory of GP*_sample_output.md (default: <this>/artifacts)",
    )
    parser.add_argument(
        "--negatives-dir",
        type=Path,
        default=None,
        help="Directory of NEG*.md (default: <this>/negatives)",
    )
    parser.add_argument(
        "--file",
        type=Path,
        action="append",
        default=None,
        help="Check a specific gold artifact (repeatable); skips negatives",
    )
    parser.add_argument(
        "--gold-only",
        action="store_true",
        help="Only run positive gold artifacts",
    )
    parser.add_argument(
        "--negatives-only",
        action="store_true",
        help="Only run intentional-fail negatives",
    )
    args = parser.parse_args(argv)

    here = Path(__file__).resolve().parent
    artifacts_dir = args.artifacts_dir or (here / "artifacts")
    negatives_dir = args.negatives_dir or (here / "negatives")

    run_gold_suite = not args.negatives_only
    run_neg_suite = not args.gold_only and args.file is None

    if args.file:
        run_gold_suite = True
        run_neg_suite = False

    exit_bad = 0

    if run_gold_suite:
        if args.file:
            files = args.file
        else:
            files = discover_artifacts(artifacts_dir)
        if not files:
            print(f"No gold artifacts found under {artifacts_dir}", file=sys.stderr)
            return 1
        gold_results, gold_failed = run_gold(files)
        print("Val-1 structural checks · GOLD")
        print("=" * 60)
        for r in gold_results:
            status = "PASS" if r.ok else "FAIL"
            print(f"[{status}] {r.scenario}  ({r.path.name})")
            for e in r.errors:
                print(f"    ERROR: {e}")
            for w in r.warnings:
                print(f"    WARN:  {w}")
        print("=" * 60)
        print(f"Gold: {len(gold_results) - gold_failed}/{len(gold_results)} passed")
        if gold_failed:
            exit_bad = 1
        print()

    if run_neg_suite:
        neg_rows, neg_failed = run_negatives(negatives_dir)
        print("Val-1 structural checks · NEGATIVES (must fail as expected)")
        print("=" * 60)
        for case, r, meta in neg_rows:
            print(f"[{meta}] {case.filename}  rule={case.rule_id}  ({case.description})")
            if meta == "META_PASS":
                # show which errors fired (compact)
                for e in r.errors[:4]:
                    print(f"    caught: {e}")
                if len(r.errors) > 4:
                    print(f"    … +{len(r.errors) - 4} more errors")
            elif meta == "MISSING":
                for e in r.errors:
                    print(f"    ERROR: {e}")
            else:
                if r.ok:
                    print("    ERROR: negative unexpectedly PASSed structural checks")
                else:
                    print("    ERROR: failed, but not with expected error class")
                    print(f"    expected any of: {case.expect_error_substrings}")
                    for e in r.errors:
                        print(f"    actual: {e}")
        print("=" * 60)
        meta_ok = len(neg_rows) - neg_failed
        print(f"Negatives: {meta_ok}/{len(neg_rows)} meta-passed (failed as intended)")
        if neg_failed:
            exit_bad = 1

    return exit_bad


if __name__ == "__main__":
    sys.exit(main())
