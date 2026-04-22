#!/usr/bin/env python3
"""
skill-sync — pull skills and agents from the ai-setup GitHub repo and install
them into the local config directories of Claude Code, Gemini CLI, or Codex CLI.

Usage:
    skill-sync                      # sync to global ~/.claude/skills, etc.
    skill-sync --project            # sync into .claude/skills in current folder
    skill-sync --project /some/dir  # sync into /some/dir/.claude/skills
    skill-sync --target claude      # sync only Claude
    skill-sync --dry-run            # print what would happen
    skill-sync --list               # list available skills and agents
    skill-sync --help               # show all options
"""

import argparse
from datetime import datetime
import json
import re
import shutil
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
DEFAULT_CONFIG = Path.home() / ".skill-sync" / "config.yaml"
DEFAULT_CACHE  = Path.home() / ".skill-sync" / "cache"
SCRIPT_DIR     = Path(__file__).resolve().parent
VERSION        = "0.1.0"

ANSI_RESET  = "\033[0m"
ANSI_BOLD   = "\033[1m"
ANSI_RED    = "\033[0;31m"
ANSI_GREEN  = "\033[0;32m"
ANSI_YELLOW = "\033[1;33m"
ANSI_CYAN   = "\033[0;36m"
ANSI_RE     = re.compile(r"\x1b\[[0-9;]*m")
OUTPUT_INDENT = ""

# ---------------------------------------------------------------------------
# Terminal display helpers
# ---------------------------------------------------------------------------

def is_interactive_terminal() -> bool:
    """Return True when both stdin and stdout are attached to a terminal."""
    return sys.stdin.isatty() and sys.stdout.isatty()


def clear_terminal() -> None:
    """Clear the current terminal using ANSI escape codes."""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def center_text(line: str, width: int) -> str:
    if not line:
        return ""
    visible_width = len(ANSI_RE.sub("", line))
    padding = max((width - visible_width) // 2, 0)
    return (" " * padding) + line


def compute_centered_block_padding(lines: list[str]) -> int:
    """Return the left padding needed to center a left-aligned block."""
    width = shutil.get_terminal_size(fallback=(80, 24)).columns
    block_width = max(len(ANSI_RE.sub("", line)) for line in lines) if lines else 0
    return max((width - block_width) // 2, 0)


def print_centered_status_block(lines: list[str]) -> None:
    """Print a centered, left-aligned status block for interactive terminals."""
    left_padding = compute_centered_block_padding(lines)
    for line in lines:
        print((" " * left_padding) + line)


def print_centered_divider() -> None:
    """Print a centered horizontal divider in interactive terminals."""
    width = shutil.get_terminal_size(fallback=(80, 24)).columns
    print(center_text("─" * min(100, max(width - 8, 24)), width))


def style_text(text: str, color: str, bold: bool = False) -> str:
    """Apply ANSI styling in interactive terminals only."""
    if not is_interactive_terminal():
        return text
    prefix = (ANSI_BOLD if bold else "") + color
    return f"{prefix}{text}{ANSI_RESET}"


def format_display_path(path: str | Path) -> str:
    """Render paths more compactly by replacing the home prefix with ~."""
    text = str(path)
    home = str(Path.home())
    if text == home:
        return "~"
    if text.startswith(home + "/"):
        return "~/" + text[len(home) + 1:]
    return text


def format_status(label: str, value: str) -> str:
    """Format a single aligned status line."""
    label_text = f"{label + ':':<9}"
    if is_interactive_terminal():
        label_text = style_text(label_text, ANSI_CYAN, bold=True)
    return f"{label_text} {value}"


def set_output_indent(spaces: int) -> None:
    """Set the shared indent used for main body output."""
    global OUTPUT_INDENT
    OUTPUT_INDENT = " " * max(spaces, 0)


def print_status(label: str, value: str) -> None:
    """Print an aligned status line in normal flow output."""
    print(f"{OUTPUT_INDENT}{format_status(label, value)}")


def print_success(message: str) -> None:
    """Print a green success line."""
    print(f"{OUTPUT_INDENT}{style_text(f'✔ {message}', ANSI_GREEN, bold=True)}")


def print_warning(message: str) -> None:
    """Print a yellow warning line."""
    print(f"{OUTPUT_INDENT}{style_text(f'⚠ {message}', ANSI_YELLOW, bold=True)}", file=sys.stderr)


def print_failure(message: str) -> None:
    """Print a red failure line to stderr."""
    print("", file=sys.stderr)
    print(f"{OUTPUT_INDENT}{style_text(f'✖ {message}', ANSI_RED, bold=True)}", file=sys.stderr)


def print_startup_banner() -> None:
    """Render the SKILL-SYNC banner in interactive terminals."""
    if not is_interactive_terminal():
        return

    clear_terminal()
    width = shutil.get_terminal_size(fallback=(80, 24)).columns

    banner_lines = [
        " ███████╗██╗  ██╗██╗██╗     ██╗        ███████╗██╗   ██╗███╗   ██╗ ██████╗",
        " ██╔════╝██║ ██╔╝██║██║     ██║        ██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝",
        " ███████╗█████╔╝ ██║██║     ██║        ███████╗ ╚████╔╝ ██╔██╗ ██║██║     ",
        " ╚════██║██╔═██╗ ██║██║     ██║        ╚════██║  ╚██╔╝  ██║╚██╗██║██║     ",
        " ███████║██║  ██╗██║███████╗███████╗   ███████║   ██║   ██║ ╚████║╚██████╗",
        " ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝",
    ]

    for line in banner_lines:
        print(center_text(f"{ANSI_BOLD}{line}{ANSI_RESET}", width))
    print("")

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
        print_status("Cache", f"Updating {repo_name}")
        r = subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=local_path, capture_output=True, text=True,
        )
        if r.returncode != 0:
            detail = r.stderr.strip() or r.stdout.strip() or "unknown git error"
            print_failure("Sync failed!")
            print(f"Error: git pull failed — {detail}", file=sys.stderr)
            print("", file=sys.stderr)
            print("skill-sync refuses to continue with a stale cache.", file=sys.stderr)
            print(f"Cached repo: {format_display_path(local_path)}", file=sys.stderr)
            print("If this is caused by an edited cache config, move your settings to ~/.skill-sync/config.yaml", file=sys.stderr)
            print(f"and remove the stale cache with: rm -rf {format_display_path(local_path)}", file=sys.stderr)
            sys.exit(1)
        print_status("Cache", f"Ready at {format_display_path(local_path)}")
    else:
        print_status("Cache", f"Cloning {repo_name}")
        cache_dir.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(
            ["git", "clone", "--branch", branch, "--depth", "1", repo_url, str(local_path)],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print_failure("Sync failed!")
            print(f"Error: git clone failed:\n{r.stderr.strip()}", file=sys.stderr)
            sys.exit(1)
        print_status("Cache", f"Ready at {format_display_path(local_path)}")

    return local_path

# ---------------------------------------------------------------------------
# Collect skills and agents from the source repo
# ---------------------------------------------------------------------------

def collect_skills(source_dir: Path) -> list[dict]:
    """Read all skills indexed in skills/index.json.

    Each skill carries a 'files' dict mapping relative paths (e.g. 'SKILL.md',
    'template.tex') to their text content — every file in the skill's directory
    is included, not just SKILL.md.
    """
    index_path = source_dir / "skills" / "index.json"
    if not index_path.exists():
        print_warning("skills/index.json not found")
        return []

    with open(index_path) as f:
        index = json.load(f)

    skills = []
    for entry in index.get("skills", []):
        skill_dir = source_dir / "skills" / entry["directory"]
        if not skill_dir.exists():
            print_warning(f"skill directory missing: {entry['directory']}")
            continue

        # Collect every file in the skill folder (recursive), keyed by path
        # relative to the skill directory (e.g. "SKILL.md", "assets/fig.png")
        files: dict[str, bytes] = {}
        for fpath in sorted(skill_dir.rglob("*")):
            if fpath.is_file():
                rel = fpath.relative_to(skill_dir)
                files[str(rel)] = fpath.read_bytes()

        skills.append({
            "name":        entry["name"],
            "description": entry.get("description", ""),
            "tags":        entry.get("tags", []),
            "files":       files,   # {relative_path: bytes}
        })

    return skills


def collect_agents(source_dir: Path) -> list[dict]:
    """Read all agents indexed in agents/index.json."""
    index_path = source_dir / "agents" / "index.json"
    if not index_path.exists():
        print_warning("agents/index.json not found")
        return []

    with open(index_path) as f:
        index = json.load(f)

    agents = []
    for entry in index.get("agents", []):
        agent_path = source_dir / "agents" / entry["file"]
        if not agent_path.exists():
            print_warning(f"agent file missing: {entry['file']}")
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
      skills → <base>/.claude/skills/<name>/     (full skill folder, all files)
      agents → <base>/.claude/agents/<name>.md   (full file as-is)

    <base> is ~/.claude when project_dir is None, else <project_dir>/.claude
    """
    skills_dir = resolve_path(cfg.get("skills_dir", "~/.claude/skills"), project_dir)
    agents_dir = resolve_path(cfg.get("agents_dir", "~/.claude/agents"), project_dir)
    count = 0

    if cfg.get("sync_skills", True):
        for skill in skills:
            skill_dest = skills_dir / skill["name"]
            if dry_run:
                for rel in skill["files"]:
                    print(f"    [skills] {skill_dest / rel}")
            else:
                skill_dest.mkdir(parents=True, exist_ok=True)
                for rel, data in skill["files"].items():
                    dest = skill_dest / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(data)
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
      skills → <base>/.gemini/skills/<name>/     (full skill folder, all files)
      Gemini CLI has no native agent concept — agents are skipped.
    """
    skills_dir = resolve_path(cfg.get("skills_dir", "~/.gemini/skills"), project_dir)
    count = 0

    if cfg.get("sync_skills", True):
        for skill in skills:
            skill_dest = skills_dir / skill["name"]
            if dry_run:
                for rel in skill["files"]:
                    print(f"    [skills] {skill_dest / rel}")
            else:
                skill_dest.mkdir(parents=True, exist_ok=True)
                for rel, data in skill["files"].items():
                    dest = skill_dest / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(data)
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
      skills → <base>/.codex/skills/<name>/      (full skill folder, all files)
      Codex CLI has no native agent concept — agents are skipped.
    """
    skills_dir = resolve_path(cfg.get("skills_dir", "~/.codex/skills"), project_dir)
    count = 0

    if cfg.get("sync_skills", True):
        for skill in skills:
            skill_dest = skills_dir / skill["name"]
            if dry_run:
                for rel in skill["files"]:
                    print(f"    [skills] {skill_dest / rel}")
            else:
                skill_dest.mkdir(parents=True, exist_ok=True)
                for rel, data in skill["files"].items():
                    dest = skill_dest / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(data)
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

DEFAULT_CONFIG_TEMPLATE = {
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


def resolve_config_path(config_arg: str | None) -> Path:
    if config_arg:
        return Path(config_arg).expanduser()
    return DEFAULT_CONFIG


def ensure_user_config(config_path: Path) -> None:
    """Create the user config from the bundled template on first run.

    This keeps user settings out of the tracked repo so cache updates can fast-
    forward cleanly.
    """
    if config_path.exists():
        return

    template_path = SCRIPT_DIR / "config.yaml"

    if not template_path.exists():
        return

    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template_path, config_path)
    except OSError as exc:
        print(f"Error: could not create default config at {config_path}: {exc}", file=sys.stderr)
        print("Pass --config /path/to/config.yaml or fix permissions on the target directory.", file=sys.stderr)
        sys.exit(1)


def load_config(config_path: Path) -> dict:
    ensure_user_config(config_path)

    if not config_path.exists():
        return DEFAULT_CONFIG_TEMPLATE
    with open(config_path) as f:
        user_cfg = yaml.safe_load(f) or {}

    # Deep-merge user config on top of defaults
    import copy
    merged = copy.deepcopy(DEFAULT_CONFIG_TEMPLATE)
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
        prog="skill-sync",
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
  skill-sync                      Sync to global ~/.claude/skills
  skill-sync --project            Sync to ./.claude/skills (current folder)
  skill-sync --project ~/myproj   Sync to ~/myproj/.claude/skills
  skill-sync --target claude      Sync only Claude Code
  skill-sync --target gemini      Sync only Gemini CLI
  skill-sync --dry-run            Print what would be written (no changes)
  skill-sync --list               List available skills and agents
  skill-sync --no-agents          Skip agent sync
""",
    )
    parser.add_argument(
        "--config",
        help="Path to config.yaml (default: ~/.skill-sync/config.yaml)",
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
    parser.add_argument("--no-banner", action="store_true", help="Disable the startup banner and terminal clear")
    parser.add_argument("--cache-dir", help="Override local cache directory")
    args = parser.parse_args()

    if not args.no_banner:
        print_startup_banner()

    # Resolve project_dir (None = global home-based install)
    project_dir: Path | None = None
    if args.project is not None:
        project_dir = Path(args.project).expanduser().resolve()

    # Load and merge config
    config_path = resolve_config_path(args.config)
    config    = load_config(config_path)
    repo_url  = args.repo   or config["source"]["repo"]
    branch    = args.branch or config["source"]["branch"]
    cache_dir = Path(args.cache_dir or config["cache_dir"]).expanduser()
    run_time  = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Fetch source
    scope_label = format_display_path(project_dir) if project_dir else "global (~)"
    status_lines = [
        format_status("Source", f"{repo_url} ({branch})"),
        format_status("Config", format_display_path(config_path)),
        format_status("Scope", scope_label),
        format_status("Version", VERSION),
        format_status("Run", run_time),
    ]
    if is_interactive_terminal():
        set_output_indent(compute_centered_block_padding(status_lines))
        print_centered_status_block(status_lines)
        print("")
        print_centered_divider()
        print("")
    else:
        set_output_indent(0)
        for line in status_lines:
            print(line)
    source_dir = fetch_source(repo_url, branch, cache_dir)

    # Collect items
    print_status("Catalog", "Reading skills and agents")
    skills = [] if args.no_skills else collect_skills(source_dir)
    agents = [] if args.no_agents else collect_agents(source_dir)
    print_status("Found", f"{len(skills)} skills | {len(agents)} agents")

    # --list mode
    if args.list:
        print("")
        print(f"{OUTPUT_INDENT}Skills ({len(skills)}):")
        for s in skills:
            nfiles = len(s["files"])
            print(f"{OUTPUT_INDENT}  {s['name']:<28}  {nfiles} file(s)   {s['description'][:50]}")
        print("")
        print(f"{OUTPUT_INDENT}Agents ({len(agents)}):")
        for a in agents:
            print(f"{OUTPUT_INDENT}  {a['name']:<28}  {a['description'][:65]}")
        if is_interactive_terminal():
            print("")
            print_centered_divider()
            print("")
        return

    # Sync targets
    total = 0
    target_summary: list[str] = []
    for target_name, adapter_fn in ADAPTERS.items():
        target_cfg = config["targets"].get(target_name, {})

        # Skip if not selected or not enabled
        if args.target != "all" and args.target != target_name:
            if args.target == "all":
                target_summary.append(f"{target_name.capitalize()}: skipped")
            continue
        if args.target == "all" and not target_cfg.get("enabled", False):
            target_summary.append(f"{target_name.capitalize()}: skipped")
            continue

        print("")
        print_status("Target", target_name)
        if args.dry_run:
            print_status("Mode", style_text("Dry run", ANSI_YELLOW, bold=True))

        count = adapter_fn(skills, agents, target_cfg, dry_run=args.dry_run, project_dir=project_dir)
        if not args.dry_run:
            print_status("Wrote", f"{count} file(s)")
            target_summary.append(f"{target_name.capitalize()}: {count} file(s)")
        else:
            target_summary.append(f"{target_name.capitalize()}: preview ready")
        total += count

    if args.dry_run:
        print("")
        print_status("Result", style_text("Dry run complete; no files written", ANSI_YELLOW, bold=True))
        print("")
        print_warning("Dry run complete")
    else:
        print("")
        print_status("Result", f"Done; total files synced: {total}")
        print("")
        print_success("Sync complete!")

    if is_interactive_terminal():
        print("")


if __name__ == "__main__":
    main()
