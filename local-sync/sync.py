#!/usr/bin/env python3
"""
skill-sync — pull skills and agents from the ai-setup GitHub repo and install
them into the local config directories of Claude Code, Gemini CLI, or Codex CLI.

Usage:
    python3 sync.py                      # sync to global ~/.claude/skills, etc.
    python3 sync.py --project            # sync into .claude/skills in current folder
    python3 sync.py --project /some/dir  # sync into /some/dir/.claude/skills
    python3 sync.py --target claude      # sync only Claude
    python3 sync.py --dry-run            # print what would happen
    python3 sync.py --list               # list available skills and agents
    python3 sync.py --help               # show all options
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_REPO   = "https://github.com/pascalamiet/ai-setup.git"
DEFAULT_BRANCH = "master"
DEFAULT_CACHE  = Path.home() / ".skill-sync" / "cache"

# ---------------------------------------------------------------------------
# Path resolution — global (~/) vs. project-local (./)
# ---------------------------------------------------------------------------

def resolve_path(path_str: str, project_dir: Path | None) -> Path:
    """
    Expand a path string.

    If project_dir is set, paths starting with ~/.claude, ~/.gemini, or ~/.codex
    are re-rooted under project_dir (e.g. ~/.claude/skills → <project>/.claude/skills).
    All other paths are expanded normally.
    """
    if project_dir is not None:
        for tool_dir in (".claude", ".gemini", ".codex"):
            prefix = f"~/{tool_dir}"
            if path_str.startswith(prefix):
                suffix = path_str[len(prefix):]          # e.g. /skills or /agents
                return project_dir / tool_dir / suffix.lstrip("/")
    return Path(path_str).expanduser()

# ---------------------------------------------------------------------------
# Frontmatter helpers (used only for metadata extraction, not for output)
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter dict without modifying the content."""
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(content[3:end].strip()) or {}
    except yaml.YAMLError:
        return {}

# ---------------------------------------------------------------------------
# Source fetching (git clone / pull into cache)
# ---------------------------------------------------------------------------

def fetch_source(repo_url: str, branch: str, cache_dir: Path) -> Path:
    """Clone or update the source repo. Returns the local path."""
    repo_name = repo_url.rstrip("/").split("/")[-1].removesuffix(".git")
    local_path = cache_dir / repo_name

    if local_path.exists():
        print(f"  Updating cached repo ({repo_name})...")
        r = subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=local_path, capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"  Warning: git pull failed — {r.stderr.strip()}", file=sys.stderr)
            print(f"  Using existing cached copy.", file=sys.stderr)
    else:
        print(f"  Cloning {repo_url}...")
        cache_dir.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(
            ["git", "clone", "--branch", branch, "--depth", "1", repo_url, str(local_path)],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"Error: git clone failed:\n{r.stderr.strip()}", file=sys.stderr)
            sys.exit(1)

    return local_path

# ---------------------------------------------------------------------------
# Collect skills and agents from the source repo
# ---------------------------------------------------------------------------

def collect_skills(source_dir: Path) -> list[dict]:
    """Read all skills indexed in skills/index.json."""
    index_path = source_dir / "skills" / "index.json"
    if not index_path.exists():
        print("  Warning: skills/index.json not found", file=sys.stderr)
        return []

    with open(index_path) as f:
        index = json.load(f)

    skills = []
    for entry in index.get("skills", []):
        skill_path = source_dir / "skills" / entry["file"]
        if not skill_path.exists():
            print(f"  Warning: skill file missing: {entry['file']}", file=sys.stderr)
            continue
        content = skill_path.read_text()
        skills.append({
            "name":        entry["name"],
            "description": entry.get("description", ""),
            "tags":        entry.get("tags", []),
            "content":     content,     # full SKILL.md, YAML header included
        })

    return skills


def collect_agents(source_dir: Path) -> list[dict]:
    """Read all agents indexed in agents/index.json."""
    index_path = source_dir / "agents" / "index.json"
    if not index_path.exists():
        print("  Warning: agents/index.json not found", file=sys.stderr)
        return []

    with open(index_path) as f:
        index = json.load(f)

    agents = []
    for entry in index.get("agents", []):
        agent_path = source_dir / "agents" / entry["file"]
        if not agent_path.exists():
            print(f"  Warning: agent file missing: {entry['file']}", file=sys.stderr)
            continue
        agents.append({
            "name":        entry["name"],
            "description": entry.get("description", ""),
            "model":       entry.get("model", ""),
            "tools":       entry.get("tools", []),
            "tags":        entry.get("tags", []),
            "content":     agent_path.read_text(),
        })

    return agents

# ---------------------------------------------------------------------------
# Target adapters
# ---------------------------------------------------------------------------

def sync_claude(
    skills: list[dict],
    agents: list[dict],
    cfg: dict,
    dry_run: bool,
    project_dir: Path | None,
) -> int:
    """
    Claude Code:
      skills → <base>/.claude/skills/<name>.md   (full SKILL.md, YAML header kept)
      agents → <base>/.claude/agents/<name>.md   (full file as-is)

    <base> is ~/.claude when project_dir is None, else <project_dir>/.claude
    """
    skills_dir = resolve_path(cfg.get("skills_dir", "~/.claude/skills"), project_dir)
    agents_dir = resolve_path(cfg.get("agents_dir", "~/.claude/agents"), project_dir)
    count = 0

    if cfg.get("sync_skills", True):
        if not dry_run:
            skills_dir.mkdir(parents=True, exist_ok=True)
        for skill in skills:
            dest = skills_dir / f"{skill['name']}.md"
            if dry_run:
                print(f"    [skills] {dest}")
            else:
                dest.write_text(skill["content"])
                count += 1

    if cfg.get("sync_agents", True):
        if not dry_run:
            agents_dir.mkdir(parents=True, exist_ok=True)
        for agent in agents:
            dest = agents_dir / f"{agent['name']}.md"
            if dry_run:
                print(f"    [agents] {dest}")
            else:
                dest.write_text(agent["content"])
                count += 1

    return count


def sync_gemini(
    skills: list[dict],
    agents: list[dict],
    cfg: dict,
    dry_run: bool,
    project_dir: Path | None,
) -> int:
    """
    Google Gemini CLI:
      skills → <base>/.gemini/skills/<name>.md   (full SKILL.md, YAML header kept)
      Gemini CLI has no native agent concept — agents are skipped.
    """
    skills_dir = resolve_path(cfg.get("skills_dir", "~/.gemini/skills"), project_dir)
    count = 0

    if cfg.get("sync_skills", True):
        if not dry_run:
            skills_dir.mkdir(parents=True, exist_ok=True)
        for skill in skills:
            dest = skills_dir / f"{skill['name']}.md"
            if dry_run:
                print(f"    [skills] {dest}")
            else:
                dest.write_text(skill["content"])
                count += 1

    return count


def sync_codex(
    skills: list[dict],
    agents: list[dict],
    cfg: dict,
    dry_run: bool,
    project_dir: Path | None,
) -> int:
    """
    OpenAI Codex CLI:
      skills → <base>/.codex/skills/<name>.md    (full SKILL.md, YAML header kept)
      Codex CLI has no native agent concept — agents are skipped.
    """
    skills_dir = resolve_path(cfg.get("skills_dir", "~/.codex/skills"), project_dir)
    count = 0

    if cfg.get("sync_skills", True):
        if not dry_run:
            skills_dir.mkdir(parents=True, exist_ok=True)
        for skill in skills:
            dest = skills_dir / f"{skill['name']}.md"
            if dry_run:
                print(f"    [skills] {dest}")
            else:
                dest.write_text(skill["content"])
                count += 1

    return count


ADAPTERS: dict[str, callable] = {
    "claude": sync_claude,
    "gemini": sync_gemini,
    "codex":  sync_codex,
}

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "source": {
        "repo":   DEFAULT_REPO,
        "branch": DEFAULT_BRANCH,
    },
    "cache_dir": str(DEFAULT_CACHE),
    "targets": {
        "claude": {
            "enabled":     True,
            "skills_dir":  "~/.claude/skills",
            "agents_dir":  "~/.claude/agents",
            "sync_skills": True,
            "sync_agents": True,
        },
        "gemini": {
            "enabled":     False,
            "skills_dir":  "~/.gemini/skills",
            "sync_skills": True,
            "sync_agents": False,
        },
        "codex": {
            "enabled":     False,
            "skills_dir":  "~/.codex/skills",
            "sync_skills": True,
            "sync_agents": False,
        },
    },
}


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        return DEFAULT_CONFIG
    with open(config_path) as f:
        user_cfg = yaml.safe_load(f) or {}

    # Deep-merge user config on top of defaults
    import copy
    merged = copy.deepcopy(DEFAULT_CONFIG)
    if "source" in user_cfg:
        merged["source"].update(user_cfg["source"])
    if "cache_dir" in user_cfg:
        merged["cache_dir"] = user_cfg["cache_dir"]
    if "targets" in user_cfg:
        for t, tcfg in user_cfg["targets"].items():
            if t in merged["targets"]:
                merged["targets"][t].update(tcfg)
            else:
                merged["targets"][t] = tcfg

    return merged

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Sync skills and agents from the ai-setup repo to local AI tool configs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Scope:
  By default, skills are written to the global config in your home directory
  (~/.claude/skills, ~/.gemini/skills, etc.).

  Use --project to sync into the .claude/skills directory of the current folder
  (or an explicit path) instead — useful when you want skills available only
  inside a specific project.

Examples:
  python3 sync.py                      Sync to global ~/.claude/skills
  python3 sync.py --project            Sync to ./.claude/skills (current folder)
  python3 sync.py --project ~/myproj   Sync to ~/myproj/.claude/skills
  python3 sync.py --target claude      Sync only Claude Code
  python3 sync.py --target gemini      Sync only Gemini CLI
  python3 sync.py --dry-run            Print what would be written (no changes)
  python3 sync.py --list               List available skills and agents
  python3 sync.py --no-agents          Skip agent sync
""",
    )
    parser.add_argument(
        "--config", default=str(Path(__file__).parent / "config.yaml"),
        help="Path to config.yaml (default: config.yaml next to this script)",
    )
    parser.add_argument("--repo",   help="Override source repo URL")
    parser.add_argument("--branch", help="Override source branch")
    parser.add_argument(
        "--target",
        choices=list(ADAPTERS.keys()) + ["all"],
        default="all",
        help="Which tool to sync to (default: all enabled targets)",
    )
    parser.add_argument(
        "--project",
        nargs="?",          # 0 or 1 argument: --project alone → CWD; --project /path → that path
        const=".",          # value when flag is present but no path given
        metavar="DIR",
        help="Sync into <DIR>/.claude/skills instead of ~/.claude/skills. "
             "Omit DIR to use the current working directory.",
    )
    parser.add_argument("--dry-run",   action="store_true", help="Show actions without writing files")
    parser.add_argument("--list",      action="store_true", help="List available skills and agents, then exit")
    parser.add_argument("--no-skills", action="store_true", help="Skip skills sync")
    parser.add_argument("--no-agents", action="store_true", help="Skip agents sync")
    parser.add_argument("--cache-dir", help="Override local cache directory")
    args = parser.parse_args()

    # Resolve project_dir (None = global home-based install)
    project_dir: Path | None = None
    if args.project is not None:
        project_dir = Path(args.project).expanduser().resolve()

    # Load and merge config
    config    = load_config(Path(args.config))
    repo_url  = args.repo   or config["source"]["repo"]
    branch    = args.branch or config["source"]["branch"]
    cache_dir = Path(args.cache_dir or config["cache_dir"]).expanduser()

    # Fetch source
    scope_label = str(project_dir) if project_dir else "global (~)"
    print("=== skill-sync ===")
    print(f"Source: {repo_url} ({branch})")
    print(f"Scope:  {scope_label}")
    source_dir = fetch_source(repo_url, branch, cache_dir)

    # Collect items
    print("Collecting skills and agents...")
    skills = [] if args.no_skills else collect_skills(source_dir)
    agents = [] if args.no_agents else collect_agents(source_dir)
    print(f"  Found {len(skills)} skills, {len(agents)} agents")

    # --list mode
    if args.list:
        print(f"\nSkills ({len(skills)}):")
        for s in skills:
            print(f"  {s['name']:<28}  {s['description'][:65]}")
        print(f"\nAgents ({len(agents)}):")
        for a in agents:
            print(f"  {a['name']:<28}  {a['description'][:65]}")
        return

    # Sync targets
    total = 0
    for target_name, adapter_fn in ADAPTERS.items():
        target_cfg = config["targets"].get(target_name, {})

        # Skip if not selected or not enabled
        if args.target != "all" and args.target != target_name:
            continue
        if args.target == "all" and not target_cfg.get("enabled", False):
            continue

        print(f"\nSyncing to {target_name}...")
        if args.dry_run:
            print("  (dry-run — no files will be written)")

        count = adapter_fn(skills, agents, target_cfg, dry_run=args.dry_run, project_dir=project_dir)
        if not args.dry_run:
            print(f"  Wrote {count} file(s)")
        total += count

    if args.dry_run:
        print("\nDry-run complete. No files were written.")
    else:
        print(f"\nDone. Total files synced: {total}")


if __name__ == "__main__":
    main()
