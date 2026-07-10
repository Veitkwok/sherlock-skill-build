#!/usr/bin/env python3
"""
Skill Watchdog — monitors GitHub repos for skill updates and auto-imports.
Reads config from ~/.hermes/config/skill-watch.json
Tracks state in ~/.hermes/data/skill-watch-state.json
"""
import json, subprocess, shutil, os, sys
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
CONFIG_PATH = HOME / ".hermes/config/skill-watch.json"
STATE_PATH = HOME / ".hermes/data/skill-watch-state.json"
CACHE_DIR = HOME / ".hermes/scripts/skill-watch-cache"

def load_json(path, default=None):
    if path.exists():
        return json.loads(path.read_text())
    return default or {}

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str))

def get_remote_sha(url, branch="main"):
    """Get latest commit SHA from remote."""
    result = subprocess.run(
        ["git", "ls-remote", url, f"refs/heads/{branch}"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return None, result.stderr.strip()
    parts = result.stdout.strip().split()
    return parts[0] if parts else None, ""

def clone_or_pull(url, branch, target_dir):
    """Clone or pull a repo."""
    if (target_dir / ".git").exists():
        result = subprocess.run(
            ["git", "fetch", "origin", branch, "--depth", "1"],
            cwd=target_dir, capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return False, f"fetch failed: {result.stderr}"
        result = subprocess.run(
            ["git", "reset", "--hard", f"origin/{branch}"],
            cwd=target_dir, capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return False, f"reset failed: {result.stderr}"
    else:
        if target_dir.exists():
            shutil.rmtree(target_dir)
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", branch, url, str(target_dir)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            return False, f"clone failed: {result.stderr}"
    return True, ""

def import_finance_skills(src_dir, target_dir):
    """Import multi-skill repo: plugins/*/skills/*/ → target/<name>/"""
    count = 0
    target_dir = Path(os.path.expanduser(str(target_dir)))
    target_dir.mkdir(parents=True, exist_ok=True)
    
    plugins_dir = src_dir / "plugins"
    if not plugins_dir.exists():
        return 0, f"plugins/ not found in {src_dir}"
    
    for group_dir in plugins_dir.iterdir():
        if not group_dir.is_dir():
            continue
        skills_subdir = group_dir / "skills"
        if not skills_subdir.exists():
            continue
        for skill_dir in skills_subdir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            dst = target_dir / skill_dir.name
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(skill_dir, dst)
            pj = dst / "plugin.json"
            if pj.exists():
                pj.unlink()
            count += 1
    return count, ""

def import_uzi_purified(src_dir, target_dir, config):
    """Import UZI-Skill with purification (strip HTML generation)."""
    count = 0
    target_dir = Path(os.path.expanduser(str(target_dir)))
    target_dir.mkdir(parents=True, exist_ok=True)
    
    if config.get("purge_on_sync") and target_dir.exists():
        shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True)
    
    skills_src = src_dir / config.get("source_skills_dir", "skills")
    strip_rules = config.get("strip", {})
    
    for skill_name in config.get("skills", []):
        src = skills_src / skill_name
        if not src.exists():
            continue
        dst = target_dir / skill_name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        
        for item in strip_rules.get(skill_name, []):
            p = dst / item
            if p.exists():
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
        
        for pyc in dst.rglob("__pycache__"):
            shutil.rmtree(pyc)
        
        count += 1
    return count, ""

def import_single_skill(src_dir, target_dir, config):
    """Import a single-skill repo."""
    target_dir = Path(os.path.expanduser(str(target_dir)))
    
    if config.get("purge_on_sync") and target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    
    keep = config.get("keep", ["SKILL.md", "LICENSE", "references", "assets", "scripts"])
    for item_name in keep:
        src = src_dir / item_name
        if not src.exists():
            continue
        dst = target_dir / item_name
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    return 1, ""

def _import_finance_skills_wrapper(src_dir, target_dir, config):
    return import_finance_skills(src_dir, target_dir)

IMPORTERS = {
    "multi-skill": _import_finance_skills_wrapper,
    "uzi-purified": import_uzi_purified,
    "single-skill": import_single_skill,
}

def main():
    config = load_json(CONFIG_PATH)
    if not config.get("repos"):
        print("No repos configured.")
        return
    
    state = load_json(STATE_PATH, {"repos": {}, "last_run": None})
    changes = []
    
    for repo in config["repos"]:
        name = repo["name"]
        url = repo["url"]
        branch = repo.get("branch", "main")
        
        print(f"\n[{name}] Checking {url}...")
        sha, err = get_remote_sha(url, branch)
        if err:
            print(f"  ERROR: {err}")
            continue
        
        prev = state["repos"].get(name, {}).get("sha", "")
        if sha == prev and state["repos"].get(name):
            print(f"  No change (SHA: {sha[:8]})")
            continue
        
        print(f"  UPDATE DETECTED: {prev[:8] if prev else 'NEW'} → {sha[:8]}")
        
        cache_dir = CACHE_DIR / name
        ok, err = clone_or_pull(url, branch, cache_dir)
        if not ok:
            print(f"  Clone error: {err}")
            continue
        
        importer = IMPORTERS.get(repo["type"])
        if not importer:
            print(f"  Unknown type: {repo['type']}")
            continue
        
        count, err = importer(cache_dir, repo["target"], repo)
        if err:
            print(f"  Import error: {err}")
            continue
        
        print(f"  Imported {count} skills to {repo['target']}")
        
        state["repos"][name] = {
            "sha": sha,
            "url": url,
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "skills_imported": count
        }
        changes.append({"name": name, "count": count, "sha": sha[:8]})
    
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    save_json(STATE_PATH, state)
    
    print(f"\n{'='*50}")
    if changes:
        print("CHANGES DETECTED:")
        for c in changes:
            print(f"  {c['name']}: {c['count']} skills updated (SHA: {c['sha']})")
    else:
        print("No changes detected across all repos.")
    print(f"State saved to {STATE_PATH}")

if __name__ == "__main__":
    main()
