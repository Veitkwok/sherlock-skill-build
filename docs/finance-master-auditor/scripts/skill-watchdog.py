#!/usr/bin/env python3
"""
Skill Watchdog — GitHub update monitor for finance-master (v4.6.8).

Role (product policy):
  - Monitor ONLY: finance-skills, UZI-Skill, serenity-skill upstreams
  - DETECT only — never import, patch, or mutate finance-master
  - Classify updates as meaningful vs trivial for human notification filter
  - Write skill-watch-diff.json for Hermes / Telegram / manual review

Config: ~/.hermes/config/skill-watch.json
State:  ~/.hermes/data/skill-watch-state.json
Diff:   ~/.hermes/data/skill-watch-diff.json

Cron:
  PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin
  python3 skill-watchdog.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


HOME = Path.home()

# Skills that must never be treated as product-relevant imports
BANNED_SKILL_NAMES = frozenset(
    {
        "lhb-analyzer",
        "yfinance-data",
        "funda-data",
        "twitter-reader",
        "discord-reader",
        "telegram-reader",
        "linkedin-reader",
        "tradingview-reader",
        "opencli-reader",
        "generative-ui",
        "skill-creator",
        "hyperliquid-reader",
        "yc-reader",
    }
)

# Path patterns → trivial (do not notify alone)
TRIVIAL_PATH_RES = [
    re.compile(r"(^|/)\.github/"),
    re.compile(r"(^|/)docs?/"),
    re.compile(r"\.(html?|css|scss|svg|png|jpe?g|gif|webp|ico)$", re.I),
    re.compile(r"(^|/)assets/"),
    re.compile(r"(^|/)personas/"),
    re.compile(r"(^|/)__pycache__/"),
    re.compile(r"\.DS_Store$"),
    re.compile(r"plugin\.json$"),
    re.compile(r"package(-lock)?\.json$"),
    re.compile(r"requirements\.txt$"),
    re.compile(r"(^|/)scripts/.*\.(py|sh)$"),
    re.compile(r"run\.py$"),
    re.compile(r"\.(yml|yaml)$"),  # agents yaml etc. — product is md methodology
    re.compile(r"LICENSE$"),
    re.compile(r"\.gitignore$"),
    re.compile(r"README\.md$", re.I),  # readme-only = trivial for notify filter
]

# Path patterns → meaningful (notify)
MEANINGFUL_PATH_RES = [
    re.compile(r"(^|/)SKILL\.md$"),
    re.compile(r"(^|/)references/.*\.md$"),
    re.compile(r"(^|/)skills/[^/]+/SKILL\.md$"),
    re.compile(r"plugins/.*/skills/.*/SKILL\.md$"),
]


def expand(path: str | Path) -> Path:
    return Path(os.path.expanduser(str(path))).resolve()


def load_json(path: Path, default: Any = None) -> Any:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"ERROR: invalid JSON {path}: {e}", file=sys.stderr)
            raise
    return default if default is not None else {}


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str) + "\n", encoding="utf-8")


def which_git() -> Optional[str]:
    return shutil.which("git")


def get_remote_sha(git: str, url: str, branch: str = "main") -> Tuple[Optional[str], str]:
    try:
        result = subprocess.run(
            [git, "ls-remote", url, f"refs/heads/{branch}"],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return None, "ls-remote timeout"
    except OSError as e:
        return None, f"ls-remote OSError: {e}"
    if result.returncode != 0:
        return None, (result.stderr or result.stdout or "ls-remote failed").strip()
    parts = result.stdout.strip().split()
    return (parts[0] if parts else None), ""


def clone_or_pull(git: str, url: str, branch: str, target_dir: Path) -> Tuple[bool, str]:
    try:
        if (target_dir / ".git").exists():
            result = subprocess.run(
                [git, "fetch", "origin", branch, "--depth", "1"],
                cwd=target_dir,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode != 0:
                return False, f"fetch failed: {(result.stderr or '').strip()}"
            result = subprocess.run(
                [git, "reset", "--hard", f"origin/{branch}"],
                cwd=target_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode != 0:
                return False, f"reset failed: {(result.stderr or '').strip()}"
        else:
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(
                [git, "clone", "--depth", "1", "--branch", branch, url, str(target_dir)],
                capture_output=True,
                text=True,
                timeout=180,
            )
            if result.returncode != 0:
                return False, f"clone failed: {(result.stderr or '').strip()}"
    except subprocess.TimeoutExpired:
        return False, "clone/fetch timeout"
    except OSError as e:
        return False, f"clone/fetch OSError: {e}"
    return True, ""


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:16]


def is_trivial_path(rel: str) -> bool:
    rel = rel.replace("\\", "/")
    for rx in TRIVIAL_PATH_RES:
        if rx.search(rel):
            return True
    return False


def is_meaningful_path(rel: str) -> bool:
    rel = rel.replace("\\", "/")
    if is_trivial_path(rel):
        return False
    for rx in MEANINGFUL_PATH_RES:
        if rx.search(rel):
            return True
    # unknown md under skill trees often methodology
    if rel.endswith(".md") and not is_trivial_path(rel):
        return True
    return False


def inventory_skill_files(src_dir: Path, repo_type: str, config: Dict[str, Any]) -> Dict[str, str]:
    """Map relative path → content hash for classification."""
    out: Dict[str, str] = {}
    if repo_type == "multi-skill":
        plugins = src_dir / "plugins"
        if not plugins.exists():
            return out
        for p in plugins.rglob("*"):
            if not p.is_file():
                continue
            rel = str(p.relative_to(src_dir))
            if p.name == "SKILL.md" or "/references/" in rel.replace("\\", "/") or rel.endswith(".md"):
                out[rel] = file_sha256(p)
            elif not is_trivial_path(rel):
                # track other non-trivial for completeness
                out[rel] = file_sha256(p)
    elif repo_type == "uzi-purified":
        skills_src = src_dir / config.get("source_skills_dir", "skills")
        for skill_name in config.get("skills", ["deep-analysis", "investor-panel", "trap-detector"]):
            if skill_name in BANNED_SKILL_NAMES:
                continue
            skill_dir = skills_src / skill_name
            if not skill_dir.exists():
                continue
            for p in skill_dir.rglob("*"):
                if p.is_file():
                    rel = str(p.relative_to(src_dir))
                    out[rel] = file_sha256(p)
    else:  # single-skill serenity
        for item in ("SKILL.md", "references", "assets", "examples", "evals"):
            p = src_dir / item
            if p.is_file():
                out[item] = file_sha256(p)
            elif p.is_dir():
                for f in p.rglob("*"):
                    if f.is_file():
                        rel = str(f.relative_to(src_dir))
                        out[rel] = file_sha256(f)
    return out


def classify_delta(
    prev_inv: Dict[str, str], new_inv: Dict[str, str]
) -> Dict[str, Any]:
    prev_keys = set(prev_inv)
    new_keys = set(new_inv)
    added = sorted(new_keys - prev_keys)
    removed = sorted(prev_keys - new_keys)
    changed = sorted(k for k in (prev_keys & new_keys) if prev_inv[k] != new_inv[k])

    meaningful_files: List[str] = []
    trivial_files: List[str] = []
    for k in added + removed + changed:
        if is_meaningful_path(k):
            meaningful_files.append(k)
        else:
            trivial_files.append(k)

    # skill-level signal: which skill names touched
    skills_touched: Set[str] = set()
    for k in meaningful_files:
        m = re.search(r"skills/([^/]+)/", k.replace("\\", "/"))
        if m:
            skills_touched.add(m.group(1))
        elif k == "SKILL.md" or k.startswith("references/"):
            skills_touched.add("serenity-skill")

    banned_touched = sorted(s for s in skills_touched if s in BANNED_SKILL_NAMES)
    product_skills = sorted(s for s in skills_touched if s not in BANNED_SKILL_NAMES)

    notify = bool(meaningful_files) and (
        bool(product_skills) or any("SKILL.md" in f or "/references/" in f.replace("\\", "/") for f in meaningful_files)
    )
    # if only banned skills meaningful, still note but notify=false for product
    if banned_touched and not product_skills and not any(
        "SKILL.md" in f for f in meaningful_files if "lhb" not in f
    ):
        # e.g. only lhb-analyzer changed upstream
        if set(product_skills) == set() and all(
            "lhb" in f or any(b in f for b in BANNED_SKILL_NAMES) for f in meaningful_files
        ):
            notify = False

    if not added and not removed and not changed:
        kind = "unchanged_content"
        notify = False
    elif notify:
        kind = "meaningful"
    else:
        kind = "trivial"

    return {
        "kind": kind,
        "notify": notify,
        "meaningful_files": meaningful_files[:80],
        "trivial_files": trivial_files[:80],
        "meaningful_count": len(meaningful_files),
        "trivial_count": len(trivial_files),
        "skills_touched_product": product_skills,
        "skills_touched_banned": banned_touched,
        "summary": (
            f"{len(meaningful_files)} meaningful / {len(trivial_files)} trivial path changes"
            if (meaningful_files or trivial_files)
            else "no file-level delta (first inventory or empty)"
        ),
    }


def list_skill_names(src_dir: Path, repo_type: str, config: Dict[str, Any]) -> List[str]:
    if repo_type == "multi-skill":
        names = []
        plugins = src_dir / "plugins"
        if not plugins.exists():
            return []
        for group in plugins.iterdir():
            skills = group / "skills"
            if not skills.is_dir():
                continue
            for s in skills.iterdir():
                if s.is_dir() and (s / "SKILL.md").exists():
                    names.append(s.name)
        return sorted(set(names))
    if repo_type == "uzi-purified":
        return [s for s in config.get("skills", []) if s not in BANNED_SKILL_NAMES]
    return ["serenity-skill"]


def resolve_paths(args: argparse.Namespace) -> Dict[str, Path]:
    config_path = expand(
        args.config
        or os.environ.get("SKILL_WATCH_CONFIG", HOME / ".hermes/config/skill-watch.json")
    )
    config = load_json(config_path, {}) if config_path.exists() else {}
    return {
        "config": config_path,
        "state": expand(
            args.state
            or os.environ.get("SKILL_WATCH_STATE")
            or config.get("state_file")
            or (HOME / ".hermes/data/skill-watch-state.json")
        ),
        "diff": expand(
            args.diff
            or os.environ.get("SKILL_WATCH_DIFF")
            or config.get("diff_file")
            or (HOME / ".hermes/data/skill-watch-diff.json")
        ),
        "cache": expand(
            args.cache
            or os.environ.get("SKILL_WATCH_CACHE")
            or config.get("cache_dir")
            or (HOME / ".hermes/scripts/skill-watch-cache")
        ),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="finance-master update monitor (detect + notify filter only)"
    )
    parser.add_argument("--config", default=None)
    parser.add_argument("--state", default=None)
    parser.add_argument("--diff", default=None)
    parser.add_argument("--cache", default=None)
    args = parser.parse_args(argv)

    paths = resolve_paths(args)
    git = which_git()
    if not git:
        print("ERROR: git not found on PATH (set PATH for cron).", file=sys.stderr)
        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": "monitor",
            "status": "error",
            "error": "git_not_found",
            "notify": False,
            "repos": [],
            "product_structure_ref": "finance-master LAYOUT.md / skill-registry.yaml",
        }
        try:
            save_json(paths["diff"], report)
            print(f"diff_report_path={paths['diff']}")
        except OSError:
            pass
        return 2

    if not paths["config"].exists():
        print(f"ERROR: config missing: {paths['config']}", file=sys.stderr)
        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": "monitor",
            "status": "error",
            "error": "config_missing",
            "notify": False,
            "repos": [],
        }
        try:
            save_json(paths["diff"], report)
            print(f"diff_report_path={paths['diff']}")
        except OSError:
            pass
        return 2

    try:
        config = load_json(paths["config"], {})
    except json.JSONDecodeError:
        return 2

    repos = config.get("repos") or []
    if not repos:
        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": "monitor",
            "status": "ok",
            "notify": False,
            "message": "no_repos_configured",
            "repos": [],
        }
        save_json(paths["diff"], report)
        print(f"diff_report_path={paths['diff']}")
        return 0

    state = load_json(paths["state"], {"repos": {}, "last_run": None})
    if "repos" not in state:
        state["repos"] = {}

    repo_reports: List[Dict[str, Any]] = []
    hard_errors = 0
    any_notify = False

    for repo in repos:
        name = repo["name"]
        url = repo["url"]
        branch = repo.get("branch", "main")
        rtype = repo.get("type", "multi-skill")

        entry: Dict[str, Any] = {
            "name": name,
            "url": url,
            "branch": branch,
            "type": rtype,
            "local_product_path": {
                "finance-skills": "finance-master/finance-skills/",
                "UZI-Skill": "finance-master/UZI-Skill/",
                "serenity-skill": "finance-master/serenity-skill/",
            }.get(name, ""),
            "status": "unchanged",
            "sha_prev": state["repos"].get(name, {}).get("sha_remote", "")
            or state["repos"].get(name, {}).get("sha", ""),
            "sha_remote": None,
            "notify": False,
            "classification": None,
            "skills_upstream": [],
            "error": None,
        }

        print(f"\n[{name}] Checking {url}...")
        sha, err = get_remote_sha(git, url, branch)
        if err or not sha:
            print(f"  ERROR: {err or 'empty sha'}")
            entry["status"] = "error"
            entry["error"] = err or "empty_sha"
            hard_errors += 1
            repo_reports.append(entry)
            continue

        entry["sha_remote"] = sha
        prev = entry["sha_prev"]
        sha_changed = not (sha == prev and prev)

        if not sha_changed:
            print(f"  No change (SHA: {sha[:8]})")
            entry["status"] = "unchanged"
            entry["notify"] = False
            repo_reports.append(entry)
            # keep state
            st = state["repos"].get(name, {})
            state["repos"][name] = {
                **st,
                "sha_remote": sha,
                "url": url,
                "last_check": datetime.now(timezone.utc).isoformat(),
            }
            continue

        print(f"  UPDATE DETECTED: {(prev[:8] if prev else 'NEW')} → {sha[:8]}")
        entry["status"] = "updated"

        cache_dir = paths["cache"] / name
        ok, err = clone_or_pull(git, url, branch, cache_dir)
        if not ok:
            print(f"  Clone error: {err}")
            entry["status"] = "error"
            entry["error"] = err
            hard_errors += 1
            # SHA changed but unknown content → notify so human can inspect
            entry["notify"] = True
            entry["classification"] = {
                "kind": "unknown_clone_failed",
                "notify": True,
                "summary": f"SHA changed but clone failed: {err}",
            }
            any_notify = True
            repo_reports.append(entry)
            continue

        new_inv = inventory_skill_files(cache_dir, rtype, repo)
        prev_inv = state["repos"].get(name, {}).get("inventory") or {}
        # first time with inventory: if only first see, compare empty → all files "added"
        # For first run after upgrade, treat as inventory baseline without flood notify
        # unless prev sha existed (true upgrade)
        if not prev_inv and not prev:
            classification = {
                "kind": "baseline",
                "notify": False,
                "summary": "Initial inventory stored; no prior baseline to compare",
                "meaningful_files": [],
                "trivial_files": [],
                "meaningful_count": 0,
                "trivial_count": 0,
                "skills_touched_product": [],
                "skills_touched_banned": [],
            }
            print("  Baseline inventory stored (no notify).")
        else:
            classification = classify_delta(prev_inv, new_inv)
            print(f"  Classification: {classification['kind']} — {classification['summary']}")
            if classification["notify"]:
                print(f"  NOTIFY: meaningful skills {classification.get('skills_touched_product')}")
            else:
                print("  No notify (trivial or empty product delta).")

        entry["classification"] = classification
        entry["notify"] = bool(classification.get("notify"))
        entry["skills_upstream"] = list_skill_names(cache_dir, rtype, repo)
        if entry["notify"]:
            any_notify = True

        state["repos"][name] = {
            "sha_remote": sha,
            "url": url,
            "last_check": datetime.now(timezone.utc).isoformat(),
            "last_classified": classification.get("kind"),
            "inventory": new_inv,
        }
        repo_reports.append(entry)

    state["last_run"] = datetime.now(timezone.utc).isoformat()
    state["product_version"] = "4.6.8"
    try:
        save_json(paths["state"], state)
    except OSError as e:
        print(f"ERROR: cannot write state: {e}", file=sys.stderr)
        hard_errors += 1

    # Human-facing notify block
    notify_repos = [r for r in repo_reports if r.get("notify")]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "monitor",
        "product_version": "4.6.8",
        "status": "error" if hard_errors else "ok",
        "notify": any_notify,
        "notify_repos": [r["name"] for r in notify_repos],
        "diff_report_path": str(paths["diff"]),
        "config_path": str(paths["config"]),
        "state_path": str(paths["state"]),
        "policy": {
            "role": "monitor_and_notify_only",
            "auto_import": False,
            "auto_patch": False,
            "meaningful": "SKILL.md / references methodology changes",
            "trivial": "HTML/assets/scripts/plugin.json/README-only",
            "manual_upgrade": "Human upgrades finance-master after notify",
        },
        "product_structure": {
            "entry": "finance-master/SKILL.md",
            "brain": "finance-master/sherlock-finance/",
            "watched_frozen_internals": [
                "finance-master/finance-skills/",
                "finance-master/UZI-Skill/",
                "finance-master/serenity-skill/",
            ],
            "local_product": [
                "finance-master/x-advanced-research/",
                "finance-master/evals/",
            ],
            "live_skill_count": 20,
            "ban_list": "references/banned-patterns.yaml",
        },
        "banned_skill_names": sorted(BANNED_SKILL_NAMES),
        "repos": repo_reports,
        "summary": {
            "updated": sum(1 for r in repo_reports if r["status"] == "updated"),
            "unchanged": sum(1 for r in repo_reports if r["status"] == "unchanged"),
            "errors": sum(1 for r in repo_reports if r["status"] == "error"),
            "notify_count": len(notify_repos),
        },
        "telegram_hint": (
            _format_telegram(notify_repos)
            if any_notify
            else "No meaningful upstream skill-logic updates."
        ),
    }
    try:
        save_json(paths["diff"], report)
    except OSError as e:
        print(f"ERROR: cannot write diff: {e}", file=sys.stderr)
        return 2

    print(f"\n{'=' * 50}")
    print(f"status={report['status']} notify={report['notify']}")
    print(f"diff_report_path={paths['diff']}")
    print(report["telegram_hint"])
    return 1 if hard_errors else 0


def _format_telegram(notify_repos: List[Dict[str, Any]]) -> str:
    lines = [" mon finance-master upstream · meaningful updates", ""]
    # fix emoji - user might want proper - use plain
    lines = ["[finance-master] Meaningful upstream skill updates", ""]
    for r in notify_repos:
        c = r.get("classification") or {}
        lines.append(f"• {r['name']}: {r.get('sha_prev', '')[:8]} → {(r.get('sha_remote') or '')[:8]}")
        lines.append(f"  {c.get('summary', '')}")
        skills = c.get("skills_touched_product") or []
        if skills:
            lines.append(f"  skills: {', '.join(skills)}")
        mf = c.get("meaningful_files") or []
        for f in mf[:12]:
            lines.append(f"  - {f}")
        if len(mf) > 12:
            lines.append(f"  … +{len(mf) - 12} more")
        lines.append("  → Manual review/upgrade of finance-master required.")
        lines.append("")
    return "\n".join(lines).strip()


if __name__ == "__main__":
    sys.exit(main())
