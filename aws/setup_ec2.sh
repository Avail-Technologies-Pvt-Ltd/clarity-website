#!/bin/bash
# ============================================================
# Clarity Website - AWS EC2 Initial Setup Script
# Supports both Amazon Linux 2023 / AL2 and Ubuntu Server
# ============================================================

set -e

echo "============================================================"
echo "    CLARITY WEBSITE - AWS EC2 SERVER INITIALIZATION"
echo "============================================================"

# Ensure running as root or with sudo
if [ "$EUID" -ne 0 ]; then
  echo "[ERROR] Please run with sudo or as root: sudo bash setup_ec2.sh"
  exit 1
fi

# Detect non-root target user (ec2-user or ubuntu)
TARGET_USER="${SUDO_USER:-$(whoami)}"
if [ "$TARGET_USER" = "root" ]; then
    if id -u ec2-user >/dev/null 2>&1; then
        TARGET_USER="ec2-user"
    elif id -u ubuntu >/dev/null 2>&1; then
        TARGET_USER="ubuntu"
    fi
fi

TARGET_HOME=$(getent passwd "$TARGET_USER" | cut -d: -f6)
APP_DIR="$TARGET_HOME/clarity-website"

echo "[INFO] Configuring for target user: $TARGET_USER ($TARGET_HOME)"
echo "[INFO] Target application directory: $APP_DIR"

# Detect OS Package Manager
if command -v dnf &> /dev/null; then
    PKG_MGR="dnf"
elif command -v yum &> /dev/null; then
    PKG_MGR="yum"
elif command -v apt-get &> /dev/null; then
    PKG_MGR="apt"
else
    echo "[ERROR] Unsupported package manager."
    exit 1
fi

echo "[1/6] Installing Docker Engine & dependencies ($PKG_MGR)..."
if [ "$PKG_MGR" = "apt" ]; then
    apt-get update && apt-get upgrade -y
    apt-get install -y curl git ufw ca-certificates gnupg lsb-release
    if ! command -v docker &> /dev/null; then
        curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
        sh /tmp/get-docker.sh
        rm -f /tmp/get-docker.sh
    fi
    systemctl enable docker
    systemctl start docker
    
    # Configure UFW firewall on Ubuntu
    ufw allow 22/tcp comment 'SSH' || true
    ufw allow 80/tcp comment 'HTTP Web' || true
    ufw allow 443/tcp comment 'HTTPS Web' || true
    ufw --force enable || true
else
    # Amazon Linux 2023 / RHEL / CentOS
    $PKG_MGR update -y
    if ! command -v git &> /dev/null; then
        $PKG_MGR install -y git
    fi
    if ! command -v docker &> /dev/null; then
        $PKG_MGR install -y docker
    fi
    systemctl enable --now docker

    # Install Docker Compose Plugin if missing
    if ! docker compose version &> /dev/null; then
        echo "[*] Installing Docker Compose CLI plugin..."
        CLI_PLUGINS_DIR="/usr/local/lib/docker/cli-plugins"
        mkdir -p "$CLI_PLUGINS_DIR"
        ARCH=$(uname -m)
        curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$ARCH" -o "$CLI_PLUGINS_DIR/docker-compose"
        chmod +x "$CLI_PLUGINS_DIR/docker-compose"
    fi
fi

# Add target user to docker group
usermod -aG docker "$TARGET_USER"
echo "[OK] Docker installed and user '$TARGET_USER' added to docker group."

echo "[2/6] Setting up application directories..."
mkdir -p "$APP_DIR/media" "$APP_DIR/staticfiles" "$APP_DIR/logs" "$APP_DIR/data" "$APP_DIR/tmp"
chown -R "$TARGET_USER:$TARGET_USER" "$APP_DIR"
chmod -R 775 "$APP_DIR/media" "$APP_DIR/staticfiles" "$APP_DIR/logs" "$APP_DIR/data"

echo "[3/6] Creating default .env.prod if not present..."
if [ ! -f "$APP_DIR/.env.prod" ]; then
    RANDOM_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))" 2>/dev/null || openssl rand -base64 40)
    RANDOM_DB_PASS=$(python3 -c "import secrets; print(secrets.token_urlsafe(24))" 2>/dev/null || openssl rand -base64 20)

    cat << EOF > "$APP_DIR/.env.prod"
# ============================================================
# Clarity Website — Production Configuration (.env.prod)
# ============================================================

# Django Core Security
SECRET_KEY=$RANDOM_SECRET
DEBUG=False
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=http://*.localhost,http://localhost

# Port exposed on AWS Host (default 8007 for direct web traffic alongside Hub)
HOST_PORT=8007

# PostgreSQL Production Database Credentials
DB_NAME=clarity_website
DB_USER=website_user
DB_PASSWORD=$RANDOM_DB_PASS
DB_HOST=db
DB_PORT=5432

# Docker Hub Configuration
DOCKER_REGISTRY=yourdockerhubusername
TAG=latest

# Performance & Workers (0 = dynamic auto-detect)
GUNICORN_WORKERS=0
AUTO_SEED=True
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
EOF
    chown "$TARGET_USER:$TARGET_USER" "$APP_DIR/.env.prod"
    chmod 600 "$APP_DIR/.env.prod"
    cp -f "$APP_DIR/.env.prod" "$APP_DIR/.env"
    chown "$TARGET_USER:$TARGET_USER" "$APP_DIR/.env"
    echo "[OK] Created $APP_DIR/.env.prod and .env with secure random credentials."
fi

echo "[4/6] Creating helper scripts (update.sh and rollback.sh)..."
cat << 'EOF' > "$APP_DIR/update.sh"
#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "============================================================"
echo "    CLARITY WEBSITE - PULLING LATEST & RESTARTING"
echo "============================================================"

# Ensure TAG=latest
sed -i 's/^TAG=.*/TAG=latest/' .env.prod 2>/dev/null || true
cp -f .env.prod .env 2>/dev/null || true

docker compose -f docker-compose.prod.yml --env-file .env.prod pull web
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --remove-orphans
docker image prune -f

echo "============================================================"
echo " Update complete! Current status:"
echo "============================================================"
docker compose -f docker-compose.prod.yml ps
EOF

cat << 'EOF' > "$APP_DIR/rollback.sh"
#!/bin/bash
set -e
cd "$(dirname "$0")"

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
EOF

chmod +x "$APP_DIR/update.sh" "$APP_DIR/rollback.sh"
chown "$TARGET_USER:$TARGET_USER" "$APP_DIR/update.sh" "$APP_DIR/rollback.sh"

echo ""
echo "============================================================"
echo " AWS EC2 SETUP COMPLETE!"
echo " You are ready for 1-click deployments!"
echo "============================================================"
