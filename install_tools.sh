#!/usr/bin/env bash
#===============================================================================
#  IP-SAKTI Dashboard — Prerequisite Installer (Windows 11 + winget)
#  Ministry of Ayush | Smart India Hackathon 2026 (SIH26045)
#
#  Installs: Node.js LTS, PostgreSQL 16, Memurai Developer (Redis for Windows)
#  NO DOCKER. NO manual downloads — winget only.
#  Run from Git Bash on Windows 11.
#
#  Usage:
#    chmod +x install_tools.sh
#    ./install_tools.sh
#===============================================================================

set -e

# --- Output helpers ----------------------------------------------------------
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
info()    { echo -e "${CYAN}ℹ️  $*${NC}"; }
success() { echo -e "${GREEN}✅ $*${NC}"; }
warn()    { echo -e "${YELLOW}⚠️  $*${NC}"; }
fail()    { echo -e "${RED}❌ $*${NC}" >&2; }

# =============================================================================
# STEP 0 — Verify winget is available
# =============================================================================
info "Step 0/3: Verifying winget..."
if ! command -v winget >/dev/null 2>&1; then
    fail "winget not found in PATH."
    fail "Fix: open Microsoft Store → search 'App Installer' → click Update."
    fail "Then close and reopen Git Bash and re-run this script."
    exit 1
fi
WINGET_VERSION="$(winget --version 2>/dev/null || echo 'unknown')"
success "winget found: ${WINGET_VERSION}"
warn "You may see UAC prompts for each installer — click 'Yes'."
echo

# =============================================================================
# Helper — install one package; print exact winget error on failure
# =============================================================================
install_pkg() {
    local label="$1"
    local pkg="$2"

    info "Installing ${label}  →  winget install ${pkg}"
    echo "        (this can take a few minutes; accept any UAC prompt)"

    local log rc
    set +e
    log="$(winget install "${pkg}" --silent --accept-source-agreements --accept-package-agreements 2>&1)"
    rc=$?
    set -e

    if [ "${rc}" -eq 0 ]; then
        success "${label} installed successfully."
    elif echo "${log}" | grep -qi "already installed"; then
        warn "${label} is already installed — skipping."
    else
        fail "${label} installation FAILED (winget exit code: ${rc})."
        fail "----- winget output (last 15 lines) -----"
        echo "${log}" | tail -n 15 >&2
        fail "----- end winget output -----"
        fail "Fix: open Microsoft Store → update the 'App Installer' package,"
        fail "then close and reopen the terminal and re-run this script."
        exit 1
    fi
    echo
}

# =============================================================================
# STEP 1 — Node.js LTS
# =============================================================================
info "Step 1/3: Node.js LTS"
install_pkg "Node.js LTS" "OpenJS.NodeJS.LTS"

# =============================================================================
# STEP 2 — PostgreSQL 16
# =============================================================================
info "Step 2/3: PostgreSQL 16"
install_pkg "PostgreSQL 16" "PostgreSQL.PostgreSQL.16"

# =============================================================================
# STEP 3 — Memurai Developer Edition (Redis for Windows)
# =============================================================================
info "Step 3/3: Memurai Developer Edition"
install_pkg "Memurai Developer" "Memurai.MemuraiDeveloper"

# =============================================================================
# DONE — summary + verification instructions
# =============================================================================
echo -e "${GREEN}===================================================${NC}"
success "All prerequisites installed for IP-SAKTI Dashboard!"
echo -e "${GREEN}===================================================${NC}"
echo
warn "IMPORTANT: CLOSE AND REOPEN your terminal (including VS Code terminals)"
warn "so the updated PATH takes effect. Then run these 4 verify commands:"
echo
echo    "  node --version        # e.g. v22.x.x"
echo    "  npm --version"
echo    "  psql --version        # psql (PostgreSQL) 16.x"
echo    "  memurai-cli ping      # should reply: PONG"
echo
info "Next steps: run setup_local.bat, then npm install && npm run dev"

# =============================================================================
# OPTIONAL ALTERNATIVE — Redis via WSL instead of Memurai (skip Step 3 above)
# =============================================================================
# 1) Install WSL (run in PowerShell as Administrator, then reboot):
#      wsl --install
#
# 2) Inside the WSL/Ubuntu terminal:
#      sudo apt update && sudo apt install redis-server -y
#      sudo service redis-server start
#      redis-cli ping        # should reply: PONG
#
# 3) Windows reaches WSL Redis via localhost forwarding — backend .env stays:
#      REDIS_URL=redis://127.0.0.1:6379/0
#
# NOTE: Run either Memurai (Windows) OR WSL Redis — not both on port 6379.
