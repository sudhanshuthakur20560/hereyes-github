#!/usr/bin/env bash
# ==============================================================================
# B.Tech Academic Repository - Automated Cloud Sync Daemon
# Automatically ingests new study materials, stages, commits, and pushes to GitHub
# ==============================================================================

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCK_FILE="/tmp/btech_autosync.lock"
LOG_FILE="$HOME/Library/Logs/btech_autosync.log"

mkdir -p "$HOME/Library/Logs"

# Ensure single instance runs at a time
exec 200>"$LOCK_FILE"
flock -n 200 2>/dev/null || {
    # If flock is not available on BSD/macOS, use a directory-based lock fallback
    if [ -d "${LOCK_FILE}.d" ]; then
        exit 0
    fi
    mkdir "${LOCK_FILE}.d" 2>/dev/null || exit 0
    trap 'rm -rf "${LOCK_FILE}.d"' EXIT
}

cd "$REPO_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

# 1. Run study file intake
python3 "$REPO_DIR/intake_study_files.py" >> "$LOG_FILE" 2>&1 || true

# 2. Check if git status has changes
STATUS=$(git status --porcelain)

if [ -n "$STATUS" ]; then
    log "Changes detected in repository. Initiating auto-sync..."

    # Pull latest changes from remote
    git pull --rebase origin main >> "$LOG_FILE" 2>&1 || {
        log "Warning: Rebase pull encountered conflicts or remote is unavailable."
    }

    # Stage all changes
    git add .

    # Commit
    COMMIT_MSG="Auto sync study materials: $(date '+%Y-%m-%d %H:%M:%S')"
    if [ -n "$1" ]; then
        COMMIT_MSG="$1"
    fi

    git commit -m "$COMMIT_MSG" >> "$LOG_FILE" 2>&1 || true

    # Push to origin main
    git push origin main >> "$LOG_FILE" 2>&1 && {
        log "✅ Successfully synced and pushed updates to GitHub!"
    } || {
        log "❌ Push failed. Will retry on next cycle."
    }
fi

# Rotate log file if larger than 2MB
if [ -f "$LOG_FILE" ] && [ $(stat -f%z "$LOG_FILE" 2>/dev/null || echo 0) -gt 2097152 ]; then
    tail -n 1000 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
fi
