#!/bin/bash

# IP-SAKTI Dashboard - Local Setup Script
# For development on Linux / macOS
# Idempotent: safe to re-run

echo "=========================================="
echo "  IP-SAKTI Dashboard - Local Setup Script"
echo "  Ministry of Ayush - SIH 2026"
echo "=========================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/ip-sakti-backend"

# ------------------------------------------------------------------
# [1/8] Check Python
# ------------------------------------------------------------------
echo "[1/8] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3.11+ is not installed. Please install Python from python.org"
    exit 1
fi
python3 --version
echo "Python found!"
echo ""

# ------------------------------------------------------------------
# [2/8] Check PostgreSQL
# ------------------------------------------------------------------
echo "[2/8] Checking PostgreSQL installation..."
if ! command -v psql &> /dev/null; then
    echo "WARNING: PostgreSQL not found. Please install PostgreSQL 16"
    echo "Ubuntu/Debian: sudo apt install postgresql-16"
    echo "macOS: brew install postgresql@16"
    exit 1
fi
psql --version
echo "PostgreSQL found!"
echo ""

# ------------------------------------------------------------------
# [3/8] Check Redis
# ------------------------------------------------------------------
echo "[3/8] Checking Redis installation..."
if ! command -v redis-cli &> /dev/null; then
    echo "WARNING: Redis not found. Please install Redis"
    echo "Ubuntu/Debian: sudo apt install redis-server"
    echo "macOS: brew install redis"
    exit 1
fi
redis-cli --version
echo "Redis found!"
echo ""

# ------------------------------------------------------------------
# [4/8] Virtual environment
# ------------------------------------------------------------------
echo "[4/8] Setting up Python virtual environment..."
cd "$BACKEND_DIR" || { echo "ERROR: Cannot access backend directory $BACKEND_DIR"; exit 1; }

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created!"
else
    echo "Virtual environment already exists."
fi
echo ""

# ------------------------------------------------------------------
# [5/8] Activate venv + install dependencies
# ------------------------------------------------------------------
echo "[5/8] Activating virtual environment and installing dependencies..."
source venv/bin/activate || { echo "ERROR: Failed to activate venv"; exit 1; }
pip install --upgrade pip || { echo "ERROR: pip upgrade failed"; exit 1; }
pip install -r requirements.txt || { echo "ERROR: pip install failed"; exit 1; }
echo "Dependencies installed!"
echo ""

# ------------------------------------------------------------------
# [6/8] Collect DB credentials and create .env
# ------------------------------------------------------------------
echo "[6/8] Database configuration..."
read -p "Database name (default: ipsakti_db): " DB_NAME
DB_NAME=${DB_NAME:-ipsakti_db}
read -p "App DB username (default: ipsakti_user): " APP_USER
APP_USER=${APP_USER:-ipsakti_user}
read -p "App DB password: " APP_PASSWORD

# Generate a DJANGO_SECRET_KEY
DJANGO_SECRET_KEY=$(openssl rand -hex 32)

ENV_FILE="$BACKEND_DIR/.env"
cat > "$ENV_FILE" << EOF
DEBUG=True
DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
DB_NAME=$DB_NAME
DB_USER=$APP_USER
DB_PASSWORD=$APP_PASSWORD
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=IP-SAKTI <no-reply@ipsakti.gov.in>
IP_INDIA_API_URL=https://ipindia.gov.in
TKDL_API_URL=https://tkdl.csir.res.in
GI_REGISTRY_URL=https://ipindia.gov.in/girindia
MSG91_API_KEY=
MSG91_SENDER_ID=IPSKTI
EOF

echo ".env created at $ENV_FILE"
echo ""

# ------------------------------------------------------------------
# [7/8] Create DB + run migrations
# ------------------------------------------------------------------
echo "[7/8] Creating database and running migrations..."
if command -v psql &> /dev/null; then
    echo "Creating database '$DB_NAME' if it does not exist..."
    sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME';" | grep -q 1 || \
        sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
    echo "Database '$DB_NAME' ready."

    echo "Creating/updating app user '$APP_USER'..."
    sudo -u postgres psql -c "CREATE USER $APP_USER WITH PASSWORD '$APP_PASSWORD';" 2>/dev/null || \
        sudo -u postgres psql -c "ALTER USER $APP_USER WITH PASSWORD '$APP_PASSWORD';"
    echo "User '$APP_USER' created/updated."

    echo "Granting privileges and fixing schema ownership..."
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $APP_USER;" 2>/dev/null || true
    sudo -u postgres psql -d "$DB_NAME" -c "ALTER SCHEMA public OWNER TO $APP_USER;" 2>/dev/null || true
    sudo -u postgres psql -d "$DB_NAME" -c "GRANT ALL ON SCHEMA public TO $APP_USER;" 2>/dev/null || true
    echo "Database setup completed!"
fi

python manage.py makemigrations || { echo "ERROR: makemigrations failed"; exit 1; }
python manage.py migrate || { echo "ERROR: migrate failed"; exit 1; }
echo "Migrations completed!"
echo ""

# ------------------------------------------------------------------
# [8/8] Summary
# ------------------------------------------------------------------
echo "=========================================="
echo "  Setup Summary"
echo "=========================================="
echo ""
echo "Backend URL: http://localhost:8000"
echo "API Docs: http://localhost:8000/api/docs/"
echo "Frontend: http://localhost:5173"
echo ""
echo "Next steps:"
echo "  1. Run: python manage.py createsuperuser"
echo "  2. Run: python manage.py seed_data"
echo "  3. Run: python manage.py runserver"
echo "  4. In a new terminal: celery -A ip_sakti worker -l info"
echo "  5. In another terminal: cd ../ip-sakti-frontend && npm install && npm run dev"
echo "  6. Open: http://localhost:5173"
echo ""
echo "Admin credentials:"
echo "  Email: admin@ipsakti.gov.in"
echo "  Password: admin123"
echo ""
echo "=========================================="
