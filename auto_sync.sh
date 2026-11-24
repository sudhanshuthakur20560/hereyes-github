#!/usr/bin/env bash
# ==============================================================================
# B.Tech Academic Repository - Auto Sync Script
# Author: Sudhanshu Thakur
# Automatically pulls, stages, commits, and pushes all study materials to GitHub
# ==============================================================================

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

echo "=============================================="
echo "🔄 B.Tech Auto Sync - Starting Sync Pipeline"
echo "📅 Time: $(date)"
echo "📂 Repository: $REPO_DIR"
echo "=============================================="

# 1. Pull latest changes from remote
echo "📥 Fetching latest remote updates..."
git pull --rebase origin main || {
    echo "⚠️  Rebase pull failed or was already up to date. Continuing..."
}

# 2. Check for changes
STATUS=$(git status --porcelain)

if [ -z "$STATUS" ]; then
    echo "✅ Working tree is already clean. Nothing new to commit."
else
    echo "📦 Staging changes..."
    git add .

    COMMIT_MSG="Auto sync study materials: $(date '+%Y-%m-%d %H:%M:%S')"
    if [ -n "$1" ]; then
        COMMIT_MSG="$1"
    fi

    echo "💾 Committing changes: '$COMMIT_MSG'..."
    git commit -m "$COMMIT_MSG"

    echo "🚀 Pushing updates to GitHub (origin/main)..."
    git push origin main
    echo "✅ Successfully synced and pushed to GitHub!"
fi

echo "=============================================="
echo "🎉 Sync completed successfully!"
echo "=============================================="
