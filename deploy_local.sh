#!/bin/bash

# IP-SAKTI Dashboard - Production Deployment Script
# For local server / AWS Mumbai / NIC Cloud
# NO DOCKER - Native deployment
# Idempotent: safe to re-run

set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/ip-sakti-backend"
FRONTEND_DIR="$SCRIPT_DIR/ip-sakti-frontend"

# BUG 2 fix: resolve the real invoking user when run via sudo
DEPLOY_USER="${SUDO_USER:-$USER}"
DEPLOY_GROUP="$(id -gn "$DEPLOY_USER" 2>/dev/null || echo "$DEPLOY_USER")"

echo "=========================================="
echo "  IP-SAKTI Production Deployment"
echo "  Ministry of Ayush - SIH 2026"
echo "=========================================="
echo ""
echo "Script directory: $SCRIPT_DIR"
echo "Backend directory: $BACKEND_DIR"
echo "Frontend directory: $FRONTEND_DIR"
echo "Deploy user: $DEPLOY_USER"
echo ""

# BUG 3 fix: hard check frontend directory upfront
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "ERROR: Frontend directory not found at $FRONTEND_DIR"
    echo "Expected structure: $FRONTEND_DIR/package.json"
    exit 1
fi

ENV_FILE="$BACKEND_DIR/.env"

# ------------------------------------------------------------------
# Step 0: Create / update .env
# ------------------------------------------------------------------
if [ ! -f "$ENV_FILE" ]; then
    echo "[0] Creating .env file..."
    cat > "$ENV_FILE" << EOF
DEBUG=False
DJANGO_SECRET_KEY=$(openssl rand -hex 32)
DB_NAME=ipsakti_db
DB_USER=ipsakti_user
DB_PASSWORD=$(openssl rand -hex 16)
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gov.in
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=IP-SAKTI <no-reply@ipsakti.gov.in>
IP_INDIA_API_URL=https://ipindia.gov.in
TKDL_API_URL=https://tkdl.csir.res.in
GI_REGISTRY_URL=https://ipindia.gov.in/girindia
MSG91_API_KEY=your-msg91-key
MSG91_SENDER_ID=IPSKTI
EOF
    echo ".env file created at $ENV_FILE"
else
    echo "[0] .env already exists at $ENV_FILE — ensuring DJANGO_SECRET_KEY is present..."
    if ! grep -q '^DJANGO_SECRET_KEY=' "$ENV_FILE"; then
        echo "DJANGO_SECRET_KEY=$(openssl rand -hex 32)" >> "$ENV_FILE"
        echo "DJANGO_SECRET_KEY added."
    fi
fi

# Load env into current shell so subsequent steps can reference variables
set -a
. "$ENV_FILE"
set +a

echo ""
echo "Loaded configuration:"
echo "  DB_NAME=$DB_NAME"
echo "  DB_USER=$DB_USER"
echo "  DB_HOST=$DB_HOST"
echo "  DB_PORT=$DB_PORT"
echo ""

# ------------------------------------------------------------------
# Step 1: Install system dependencies
# ------------------------------------------------------------------
echo "[1/6] Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    echo "Detected Debian/Ubuntu"
    sudo apt-get update || true
    sudo apt-get install -y python3.11 python3.11-venv python3-pip postgresql-16 postgresql-contrib redis-server nginx
elif command -v yum &> /dev/null; then
    echo "Detected RHEL/CentOS"
    sudo yum install -y python311 python3-pip postgresql16-server redis nginx
elif command -v brew &> /dev/null; then
    echo "Detected macOS"
    brew install postgresql@16 redis nginx
else
    echo "WARNING: Could not detect package manager. Please install Python 3.11, PostgreSQL 16, Redis, and Nginx manually."
fi
echo "System dependencies step completed."
echo ""

# ------------------------------------------------------------------
# Step 2: Setup PostgreSQL
# ------------------------------------------------------------------
echo "[2/6] Setting up PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "Creating database '$DB_NAME' if it does not exist..."
    sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME';" | grep -q 1 || \
        sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
    echo "Database '$DB_NAME' ready."

    echo "Creating/updating app user '$DB_USER'..."
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || \
        sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    echo "User '$DB_USER' created/updated."

    echo "Granting privileges and fixing schema ownership..."
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || true
    # BUG 6 fix: ensure public schema is owned by the app user on PG 15+
    sudo -u postgres psql -d "$DB_NAME" -c "ALTER SCHEMA public OWNER TO $DB_USER;" 2>/dev/null || true
    sudo -u postgres psql -d "$DB_NAME" -c "GRANT ALL ON SCHEMA public TO $DB_USER;" 2>/dev/null || true
    echo "Database setup completed!"
else
    echo "WARNING: psql not found. Skipping database setup."
fi
echo ""

# ------------------------------------------------------------------
# Step 3: Python environment + migrations
# ------------------------------------------------------------------
echo "[3/6] Setting up Python environment..."
cd "$BACKEND_DIR" || { echo "ERROR: Cannot access backend directory $BACKEND_DIR"; exit 1; }

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

source venv/bin/activate || { echo "ERROR: Failed to activate venv"; exit 1; }
pip install --upgrade pip || { echo "ERROR: pip upgrade failed"; exit 1; }
pip install -r requirements.txt || { echo "ERROR: pip install failed"; exit 1; }
echo "Python environment ready."
echo ""

echo "Running Django migrations..."
python manage.py migrate || { echo "ERROR: migrate failed"; exit 1; }
python manage.py collectstatic --noinput || { echo "ERROR: collectstatic failed"; exit 1; }
echo "Django setup completed."
echo ""

# ------------------------------------------------------------------
# Step 4: Build frontend
# ------------------------------------------------------------------
echo "[4/6] Building frontend..."
cd "$FRONTEND_DIR" || { echo "ERROR: Cannot access frontend directory $FRONTEND_DIR"; exit 1; }
if [ ! -d "node_modules" ]; then
    npm install || { echo "ERROR: npm install failed"; exit 1; }
fi
npm run build || { echo "ERROR: frontend build failed"; exit 1; }
echo "Frontend built successfully."
cd "$BACKEND_DIR" || { echo "ERROR: Cannot return to backend directory"; exit 1; }
echo ""

# ------------------------------------------------------------------
# Step 5: Systemd services
# ------------------------------------------------------------------
echo "[5/6] Setting up Gunicorn / Celery systemd services..."
sudo tee /etc/systemd/system/ipsakti.service > /dev/null << EOF
[Unit]
Description=IP-SAKTI Django Application
After=network.target

[Service]
User=$DEPLOY_USER
Group=$DEPLOY_GROUP
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
ExecStart=$BACKEND_DIR/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 ip_sakti.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/ipsakti-celery.service > /dev/null << EOF
[Unit]
Description=IP-SAKTI Celery Worker
After=network.target

[Service]
User=$DEPLOY_USER
Group=$DEPLOY_GROUP
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
ExecStart=$BACKEND_DIR/venv/bin/celery -A ip_sakti worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/ipsakti-celery-beat.service > /dev/null << EOF
[Unit]
Description=IP-SAKTI Celery Beat
After=network.target

[Service]
User=$DEPLOY_USER
Group=$DEPLOY_GROUP
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
ExecStart=$BACKEND_DIR/venv/bin/celery -A ip_sakti beat --loglevel=info -S django
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload || { echo "WARNING: daemon-reload failed"; }
sudo systemctl enable ipsakti || true
sudo systemctl enable ipsakti-celery || true
sudo systemctl enable ipsakti-celery-beat || true
echo "Systemd services configured."
echo ""

# ------------------------------------------------------------------
# Step 6: Nginx
# ------------------------------------------------------------------
echo "[6/6] Setting up Nginx..."
sudo tee /etc/nginx/sites-available/ipsakti > /dev/null << EOF
server {
    listen 80;
    server_name _;

    client_max_body_size 100M;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        root $BACKEND_DIR/staticfiles;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        root $BACKEND_DIR;
    }

    location / {
        root $FRONTEND_DIR/dist;
        try_files \$uri \$uri/ /index.html;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/ipsakti /etc/nginx/sites-enabled/ || true
sudo rm -f /etc/nginx/sites-enabled/default || true
sudo nginx -t || { echo "ERROR: Nginx config test failed"; exit 1; }
sudo systemctl reload nginx || { echo "WARNING: Nginx reload failed"; }
echo "Nginx configured."
echo ""

echo "=========================================="
echo "  Deployment Complete!"
echo "=========================================="
echo ""
echo "Next: start services"
echo "  sudo systemctl start redis-server"
echo "  sudo systemctl start postgresql"
echo "  sudo systemctl start ipsakti"
echo "  sudo systemctl start ipsakti-celery"
echo "  sudo systemctl start ipsakti-celery-beat"
echo ""
echo "Application URL: http://your-server-ip"
echo "API URL: http://your-server-ip/api/"
echo ""
echo "To check status:"
echo "  sudo systemctl status ipsakti"
echo "  sudo systemctl status ipsakti-celery"
echo "  sudo systemctl status ipsakti-celery-beat"
echo "  sudo systemctl status nginx"
echo ""
