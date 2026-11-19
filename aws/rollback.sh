#!/bin/bash
# ============================================================
# rollback.sh — Clarity Website
# 1-second instant rollback script for AWS EC2 instance
# Usage: ./rollback.sh [tag_name] (e.g. ./rollback.sh v1.0.0)
# ============================================================

set -e
cd "$(dirname "$0")/.."

echo "============================================================"
echo "    CLARITY WEBSITE - ROLLBACK VERSION"
echo "============================================================"

TARGET_TAG="$1"
if [ -z "$TARGET_TAG" ]; then
    read -p "Enter version tag to rollback to (e.g. v1.0.0): " TARGET_TAG
fi

if [ -z "$TARGET_TAG" ]; then
    echo "[ERROR] No version specified. Rollback aborted."
    exit 1
fi

echo "[*] Setting TAG=$TARGET_TAG in .env.prod..."
sed -i "s/^TAG=.*/TAG=$TARGET_TAG/" .env.prod
cp -f .env.prod .env 2>/dev/null || true

echo "[*] Pulling image for tag $TARGET_TAG..."
docker compose -f docker-compose.prod.yml --env-file .env.prod pull web

echo "[*] Restarting container with version $TARGET_TAG..."
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --remove-orphans web

echo "============================================================"
echo " Rollback to $TARGET_TAG successful!"
echo "============================================================"
docker compose -f docker-compose.prod.yml ps
