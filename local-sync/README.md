# local-sync

Pulls skills and subagent definitions from the
[ai-setup](https://github.com/pascalamiet/ai-setup) repository and installs
them into the local config directories of Claude Code, Gemini CLI, or Codex CLI.
This way, in one clean command you have all your agents equipped with the latest skills and
subagents instead of copying manually.

## What gets synced

| Source | Destination (global) | Destination (project) |
|---|---|---|
| `skills/<name>/` *(all files)* | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` |
| `agents/<name>.md` | `~/.claude/agents/<name>.md` | `.claude/agents/<name>.md` |
| `skills/<name>/` *(all files)* | `~/.gemini/skills/<name>/` *(if enabled)* | `.gemini/skills/<name>/` |
| `skills/<name>/` *(all files)* | `~/.codex/skills/<name>/` *(if enabled)* | `.codex/skills/<name>/` |

Skill files are written as-is, including their YAML frontmatter. Agents are
written to Claude only (Gemini and Codex have no equivalent concept).

## Requirements

| Tool | Minimum version |
|---|---|
| Bash | 4.0 |
| Python | 3.10 |
| pip | any |
| git | any |

## Platform support

| Platform | `sync.py` | `install.sh` |
|---|---|---|
| macOS | ✔ | ✔ |
| Linux | ✔ | ✔ |
| Windows | ✔ | ✖ |

`sync.py` is pure Python and works on all platforms. `install.sh` is a Bash
script and requires macOS or Linux (or WSL on Windows). On Windows, run the
setup steps manually:

```powershell
pip install pyyaml
python sync.py --dry-run   # preview
python sync.py             # run
```

To auto-sync on Windows, add a task in **Task Scheduler** pointing to
`python path\to\sync.py`.

## First-time setup

```bash
cd local-sync
bash install.sh
```

The installer will:
1. Check all requirements and print a clear error if anything is missing
2. Install the `pyyaml` Python dependency
3. Show a dry-run preview of what will be synced
4. Ask whether to run the actual sync
5. Optionally register a daily cron job (09:00) so skills stay up to date automatically

## Global command

The installer offers to create a `local-sync` symlink in `~/.local/bin/` so you
can run the script from anywhere without typing the full path:

```bash
local-sync                  # same as python3 /path/to/sync.py
local-sync --project        # project-local sync
local-sync --dry-run        # preview
```

To set it up manually instead:

```bash
mkdir -p ~/.local/bin
ln -s /path/to/local-sync/sync.py ~/.local/bin/local-sync
```

Make sure `~/.local/bin` is on your `PATH` (add to `~/.bashrc` or `~/.zshrc` if not):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Manual usage

```bash
# Sync to global ~/.claude/skills  (default)
python3 sync.py

# Sync into the current project folder  →  ./.claude/skills/
python3 sync.py --project

# Sync into a specific project folder
python3 sync.py --project ~/my-project

# Sync only Claude Code (skip Gemini / Codex)
python3 sync.py --target claude

# Preview without writing anything
python3 sync.py --dry-run

# List all available skills and agents
python3 sync.py --list

# Skip agents, sync skills only
python3 sync.py --no-agents
```

### Global vs. project-local

By default, skills are installed into your **home directory** (`~/.claude/skills`),
making them available in every Claude Code session you open.

Pass `--project` to install into the **current folder's** `.claude/skills` instead.
This is useful when you want a project-specific set of skills that colleagues can
also pick up by running `sync.py --project` inside the same repo.

```
my-project/
├── .claude/
│   ├── skills/        ← project-local skills (from --project)
│   └── agents/
└── ...
```

## Configuration

Targets are **opt-in**: the script does not auto-detect which AI tools you have
installed. It only syncs to targets that are explicitly set to `enabled: true`
in `config.yaml`. If you have Gemini or Codex installed, flip the corresponding
flag to start syncing to them.

Edit `config.yaml` to change targets, directories, or the source branch.

```yaml
source:
  repo: https://github.com/pascalamiet/ai-setup.git
  branch: master

targets:
  claude:
    enabled: true
    skills_dir: ~/.claude/skills
    agents_dir: ~/.claude/agents

  gemini:
    enabled: false          # flip to true to enable
    skills_dir: ~/.gemini/skills

  codex:
    enabled: false          # flip to true to enable
    skills_dir: ~/.codex/skills
```

## How it works

1. **Fetch** — the repo is cloned into `~/.local-sync/cache/ai-setup` on first
   run, then updated via `git pull` on subsequent runs.
2. **Collect** — `skills/index.json` and `agents/index.json` are read to
   discover all available files.
3. **Write** — for each enabled target, skill and agent files are written to
   the appropriate directory. Each file is written verbatim from the source.

## Automatic updates (cron)

If you chose to set up a cron job during installation, sync runs daily at 09:00:

```
0 9 * * * cd /path/to/local-sync && python3 sync.py >> ~/.local-sync/sync.log 2>&1
```

To remove it:

```bash
crontab -e   # delete the line containing "local-sync"
```

To change the schedule, run `crontab -e` and edit the time expression directly.
