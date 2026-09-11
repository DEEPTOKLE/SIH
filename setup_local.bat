@echo off
chcp 65001 >nul
echo ==========================================
echo   IP-SAKTI Dashboard - Local Setup Script
echo   Ministry of Ayush - SIH 2026
echo ==========================================
echo.

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%ip-sakti-backend"

cd /d "%BACKEND_DIR%" || (
    echo ERROR: Cannot access backend directory %BACKEND_DIR%
    pause
    exit /b 1
)

echo [1/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.11+ is not installed. Please install Python from python.org
    pause
    exit /b 1
)
python --version
echo Python found!
echo.

echo [2/8] Checking PostgreSQL installation...
psql --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: PostgreSQL not found. Please install PostgreSQL 16
    echo Download from: https://www.postgresql.org/download/windows/
    pause
    exit /b 1
)
psql --version
echo PostgreSQL found!
echo.

echo [3/8] Checking Redis installation...
redis-cli --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Redis not found. Please install Redis for Windows
    echo Download from: https://github.com/microsoftarchive/redis/releases
    pause
    exit /b 1
)
redis-cli --version
echo Redis found!
echo.

echo [4/8] Setting up Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists.
)
echo.

echo [5/8] Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated!
echo.

echo [6/8] Installing Python dependencies...
pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: pip upgrade failed
    pause
    exit /b 1
)
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed
    pause
    exit /b 1
)
echo Dependencies installed!
echo.

echo [7/8] Database configuration...
set /p DB_NAME="Database name (default: ipsakti_db): "
if "%DB_NAME%"=="" set DB_NAME=ipsakti_db
set /p APP_USER="App DB username (default: ipsakti_user): "
if "%APP_USER%"=="" set APP_USER=ipsakti_user
set /p APP_PASSWORD="App DB password: "

echo Creating database...
psql -U postgres -c "CREATE DATABASE \"%DB_NAME%\";" 2>nul
echo Database %DB_NAME% created or already exists!

echo Creating/updating app user...
psql -U postgres -c "CREATE USER \"%APP_USER%\" WITH PASSWORD '%APP_PASSWORD%';" 2>nul
if errorlevel 1 (
    psql -U postgres -c "ALTER USER \"%APP_USER%\" WITH PASSWORD '%APP_PASSWORD%';" 2>nul
)
echo User %APP_USER% configured.

echo Granting privileges...
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE \"%DB_NAME%\" TO \"%APP_USER%\";" 2>nul
echo.

REM Generate a random DJANGO_SECRET_KEY for Windows
for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_hex(32))"') do set DJANGO_SECRET_KEY=%%i

echo Creating .env file...
(
echo DEBUG=True
echo DJANGO_SECRET_KEY=%DJANGO_SECRET_KEY%
echo DB_NAME=%DB_NAME%
echo DB_USER=%APP_USER%
echo DB_PASSWORD=%APP_PASSWORD%
echo DB_HOST=localhost
echo DB_PORT=5432
echo REDIS_URL=redis://127.0.0.1:6379/0
echo CELERY_BROKER_URL=redis://127.0.0.1:6379/0
echo CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
echo EMAIL_HOST=smtp.gmail.com
echo EMAIL_PORT=587
echo EMAIL_USE_TLS=True
echo EMAIL_HOST_USER=
echo EMAIL_HOST_PASSWORD=
echo DEFAULT_FROM_EMAIL=IP-SAKTI ^<no-reply@ipsakti.gov.in^>
echo IP_INDIA_API_URL=https://ipindia.gov.in
echo TKDL_API_URL=https://tkdl.csir.res.in
echo GI_REGISTRY_URL=https://ipindia.gov.in/girindia
echo MSG91_API_KEY=
echo MSG91_SENDER_ID=IPSKTI
) > .env
echo .env created at %BACKEND_DIR%\.env
echo.

echo [8/8] Running Django migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo ERROR: makemigrations failed
    pause
    exit /b 1
)
python manage.py migrate
if errorlevel 1 (
    echo ERROR: migrate failed
    pause
    exit /b 1
)
echo Migrations completed!
echo.

echo Configuration summary:
for /f "tokens=2 delims==" %%a in ('findstr /b "DB_NAME=" .env') do echo   DB_NAME=%%a
for /f "tokens=2 delims==" %%a in ('findstr /b "DB_USER=" .env') do echo   DB_USER=%%a
for /f "tokens=2 delims==" %%a in ('findstr /b "DJANGO_SECRET_KEY=" .env') do echo   DJANGO_SECRET_KEY=%%a
echo Configuration loaded from .env by Django at runtime.
echo.

echo ==========================================
echo   Setup Summary
echo ==========================================
echo.
echo Backend URL: http://localhost:8000
echo API Docs: http://localhost:8000/api/docs/
echo Frontend: http://localhost:5173
echo.
echo Next steps:
echo   1. Run: python manage.py createsuperuser
echo   2. Run: python manage.py seed_data
echo   3. Run: python manage.py runserver
echo   4. Run: celery -A ip_sakti worker --pool^=solo -l info
echo   5. Open: http://localhost:5173
echo.
echo Admin credentials:
echo   Email: admin@ipsakti.gov.in
echo   Password: admin123
echo.
echo ==========================================

pause
