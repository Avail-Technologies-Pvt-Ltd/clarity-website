#!/bin/bash
# entrypoint.sh — Avail Technologies (Clarity Website)
# Automated database migrations, smart static file handling & production startup

set -e

echo "========================================"
echo "  Avail Technologies Website - Starting"
echo "========================================"

# Ensure data, media, static, and logs directories exist
mkdir -p /app/data /app/media /app/staticfiles /app/logs /app/tmp

# Wait for PostgreSQL if DB_HOST is set
if [ -n "$DB_HOST" ] && [ "$DB_ENGINE" != "sqlite3" ] && [ -z "$SQLITE_PATH" ]; then
    PORT="${DB_PORT:-5432}"
    echo "Waiting for PostgreSQL database at $DB_HOST:$PORT..."
    while ! nc -z "$DB_HOST" "$PORT"; do
        sleep 0.2
    done
    echo "[OK] PostgreSQL database is reachable and ready!"
fi

# Generate fingerprint using the build-time git SHA or manage.py timestamp
CURRENT_HASH="${APP_BUILD_HASH:-$(stat -c %Y /app/manage.py 2>/dev/null || echo "unknown")}"
MARKER_FILE="/app/staticfiles/.image_hash"

NEEDS_SETUP=false
if [ ! -f "$MARKER_FILE" ]; then
    NEEDS_SETUP=true
    echo "[INFO] First boot detected — running migrations and static collection."
elif [ "$(cat $MARKER_FILE 2>/dev/null)" != "$CURRENT_HASH" ]; then
    NEEDS_SETUP=true
    echo "[INFO] New image version detected (${CURRENT_HASH}) — running migrations and static collection."
else
    echo "[OK] Same image as last boot — fast startup."
fi

echo "Running database migrations..."
python manage.py migrate --noinput
echo "[OK] Database migrations up to date!"

if [ "${AUTO_SEED:-True}" = "True" ] || [ "${AUTO_SEED:-True}" = "true" ] || [ "${AUTO_SEED:-True}" = "1" ]; then
    echo "Seeding website production data (idempotent)..."
    python manage.py seed_website_data || true
    echo "[OK] Database seeding complete!"
fi

if [ "$NEEDS_SETUP" = true ]; then
    if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ] || [ "$DEBUG" = "1" ]; then
        echo "Dev mode: skipping static file collection"
    else
        echo "Collecting static files..."
        python manage.py collectstatic --noinput
        echo "[OK] Static files collected!"
    fi

    mkdir -p /app/staticfiles
    echo "$CURRENT_HASH" > "$MARKER_FILE"
fi

echo ""
echo "  Avail Technologies Website is ready!"
echo "========================================"

# Dynamic Gunicorn workers (2 * cores + 1, capped at 4, or GUNICORN_WORKERS env)
if [ "${GUNICORN_WORKERS:-0}" -gt 0 ] 2>/dev/null; then
    WORKERS="$GUNICORN_WORKERS"
else
    WORKERS=$(python -c "import os; print(min((os.cpu_count() or 1) * 2 + 1, 4))")
fi

if [ "$1" = "gunicorn" ]; then
    echo "[INFO] Starting Gunicorn with $WORKERS workers on port 8000..."
    exec "$@" --workers "$WORKERS"
else
    exec "$@"
fi
