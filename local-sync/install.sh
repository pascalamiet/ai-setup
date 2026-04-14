#!/usr/bin/env bash
# install.sh — first-time setup for skill-sync
#
# Steps:
#   1. Check system requirements (bash, python, pip, git)
#   2. Install Python dependencies (PyYAML)
#   3. Preview what will be synced (dry-run)
#   4. Optionally run the actual sync
#   5. Optionally register a daily cron job

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYNC_PY="$SCRIPT_DIR/sync.py"
LOG_FILE="$HOME/.skill-sync/sync.log"

# ── Formatting helpers ────────────────────────────────────────────────────────
RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'
BOLD='\033[1m'; RESET='\033[0m'

ok()   { echo -e "  ${GREEN}✔${RESET}  $*"; }
warn() { echo -e "  ${YELLOW}⚠${RESET}  $*"; }
fail() { echo -e "  ${RED}✖${RESET}  $*"; }

print_header() {
    echo ""
    echo -e "${BOLD}$*${RESET}"
    printf '%.0s─' {1..50}; echo ""
}

require_fail() {
    # $1 = human-readable tool name, $2 = install hint
    echo ""
    echo -e "${RED}${BOLD}Requirement not met: $1${RESET}"
    echo -e "  $2"
    echo ""
    echo -e "${YELLOW}Fix the issue above and re-run install.sh.${RESET}"
    echo ""
    exit 1
}

# ── 1. Requirements check ─────────────────────────────────────────────────────
print_header "Checking requirements"

# Bash >= 4 (needed for ${var,,} lowercase and associative arrays)
BASH_MAJOR="${BASH_VERSINFO[0]}"
if (( BASH_MAJOR < 4 )); then
    fail "Bash ${BASH_VERSION} found — version 4.0 or later required"
    require_fail "Bash >= 4" \
        "macOS ships with Bash 3. Install a newer version via Homebrew: brew install bash"
fi
ok "Bash ${BASH_VERSION}"

# Python 3.10+ (needed for 'X | Y' union type hints used in sync.py)
if ! command -v python3 &>/dev/null; then
    fail "python3 not found"
    require_fail "Python 3.10+" \
        "Install Python from https://www.python.org/downloads/ or via your package manager."
fi

PY_VERSION="$(python3 -c 'import sys; print(sys.version_info[:2])')"
PY_MAJOR="$(python3 -c 'import sys; print(sys.version_info.major)')"
PY_MINOR="$(python3 -c 'import sys; print(sys.version_info.minor)')"
PY_DISPLAY="$(python3 -c 'import sys; v=sys.version_info; print(f"{v.major}.{v.minor}.{v.micro}")')"

if (( PY_MAJOR < 3 || (PY_MAJOR == 3 && PY_MINOR < 10) )); then
    fail "Python ${PY_DISPLAY} found — version 3.10 or later required"
    require_fail "Python >= 3.10" \
        "Upgrade Python via https://www.python.org/downloads/ or your package manager."
fi
ok "Python ${PY_DISPLAY}"

# pip
if ! command -v pip3 &>/dev/null && ! python3 -m pip --version &>/dev/null 2>&1; then
    fail "pip not found"
    require_fail "pip" \
        "Install pip: python3 -m ensurepip --upgrade   or   curl https://bootstrap.pypa.io/get-pip.py | python3"
fi
ok "pip $(python3 -m pip --version | awk '{print $2}')"

# git
if ! command -v git &>/dev/null; then
    fail "git not found"
    require_fail "git" \
        "Install git: https://git-scm.com/downloads   or via your package manager (apt/brew/dnf)."
fi
ok "git $(git --version | awk '{print $3}')"

# sync.py present
if [[ ! -f "$SYNC_PY" ]]; then
    fail "sync.py not found at $SYNC_PY"
    require_fail "sync.py" \
        "Make sure you are running install.sh from inside the skill-sync directory."
fi
ok "sync.py found"

# ── 2. Python dependencies ────────────────────────────────────────────────────
print_header "Installing Python dependencies"

if python3 -c "import yaml" 2>/dev/null; then
    ok "PyYAML already installed"
else
    echo "  Installing PyYAML..."
    if python3 -m pip install --quiet -r "$SCRIPT_DIR/requirements.txt"; then
        ok "PyYAML installed"
    else
        fail "pip install failed"
        require_fail "PyYAML" \
            "Try manually: pip3 install pyyaml    or    pip3 install --user pyyaml"
    fi
fi

# ── 3. Dry-run preview ────────────────────────────────────────────────────────
print_header "Preview (dry-run)"
echo ""
python3 "$SYNC_PY" --dry-run
echo ""

# ── 4. Run the sync now? ──────────────────────────────────────────────────────
read -rp "$(echo -e "${BOLD}Run the actual sync now?${RESET} [y/N] ")" RUN_NOW
if [[ "${RUN_NOW,,}" == "y" ]]; then
    echo ""
    python3 "$SYNC_PY"
fi

echo ""

# ── 5. Cron job ───────────────────────────────────────────────────────────────
read -rp "$(echo -e "${BOLD}Set up a daily cron job (09:00) for automatic syncing?${RESET} [y/N] ")" SETUP_CRON
if [[ "${SETUP_CRON,,}" == "y" ]]; then
    if ! command -v crontab &>/dev/null; then
        warn "crontab not available on this system — skipping."
    else
        mkdir -p "$(dirname "$LOG_FILE")"
        CRON_ENTRY="0 9 * * * cd \"$SCRIPT_DIR\" && python3 \"$SYNC_PY\" >> \"$LOG_FILE\" 2>&1  # skill-sync"
        if crontab -l 2>/dev/null | grep -q "skill-sync"; then
            warn "Cron job already registered — skipping."
        else
            (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
            ok "Cron job added (daily at 09:00)"
            echo -e "       Log file: $LOG_FILE"
        fi
    fi
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}Setup complete.${RESET}"
echo -e "  Sync manually:    python3 ${SYNC_PY} --help"
echo -e "  Project-local:    python3 ${SYNC_PY} --project"
echo -e "  Edit targets:     ${SCRIPT_DIR}/config.yaml"
echo ""
