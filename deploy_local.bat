@echo off
chcp 65001 >nul
echo ==========================================
echo   IP-SAKTI Production Deployment
echo   Ministry of Ayush - SIH 2026
echo   Windows Native (NO DOCKER)
echo ==========================================
echo.

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%ip-sakti-backend"
set "FRONTEND_DIR=%SCRIPT_DIR%ip-sakti-frontend"

echo Script directory: %SCRIPT_DIR%
echo Backend directory: %BACKEND_DIR%
echo Frontend directory: %FRONTEND_DIR%
echo.

cd /d "%BACKEND_DIR%" || (
    echo ERROR: Cannot access backend directory %BACKEND_DIR%
    pause
    exit /b 1
)

REM ------------------------------------------------------------------
REM Step 0: Create / update .env
REM ------------------------------------------------------------------
if not exist ".env" (
    echo [0] Creating .env file...
    for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_hex(32))"') do set RANDOM_SECRET=%%i
    for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_hex(16))"') do set RANDOM_DB_PASS=%%i

    (
        echo DEBUG=False
        echo DJANGO_SECRET_KEY=%RANDOM_SECRET%
        echo DB_NAME=ipsakti_db
        echo DB_USER=ipsakti_user
        echo DB_PASSWORD=%RANDOM_DB_PASS%
        echo DB_HOST=localhost
        echo DB_PORT=5432
        echo REDIS_URL=redis://127.0.0.1:6379/0
        echo CELERY_BROKER_URL=redis://127.0.0.1:6379/0
        echo CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
        echo EMAIL_HOST=smtp.gmail.com
        echo EMAIL_PORT=587
        echo EMAIL_USE_TLS=True
        echo EMAIL_HOST_USER=your-email@gov.in
        echo EMAIL_HOST_PASSWORD=your-app-password
        echo DEFAULT_FROM_EMAIL=IP-SAKTI ^<no-reply@ipsakti.gov.in^>
        echo IP_INDIA_API_URL=https://ipindia.gov.in
        echo TKDL_API_URL=https://tkdl.csir.res.in
        echo GI_REGISTRY_URL=https://ipindia.gov.in/girindia
        echo MSG91_API_KEY=your-msg91-key
        echo MSG91_SENDER_ID=IPSKTI
    ) > .env
    echo .env file created at %BACKEND_DIR%\.env
) else (
    echo [0] .env already exists at %BACKEND_DIR%\.env
    echo      Ensure DJANGO_SECRET_KEY is set inside it.
)
echo.

echo Configuration loaded from .env by Django at runtime.
for /f "tokens=2 delims==" %%a in ('findstr /b "DB_NAME=" .env') do echo   DB_NAME=%%a
for /f "tokens=2 delims==" %%a in ('findstr /b "DB_USER=" .env') do echo   DB_USER=%%a
echo.

REM ------------------------------------------------------------------
REM Step 1: Install Python dependencies
REM ------------------------------------------------------------------
echo [1/5] Setting up Python environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate venv
    pause
    exit /b 1
)

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

pip install waitress
if errorlevel 1 (
    echo ERROR: waitress install failed
    pause
    exit /b 1
)
echo Python environment ready.
echo.

REM ------------------------------------------------------------------
REM Step 2: Setup PostgreSQL
REM ------------------------------------------------------------------
echo [2/5] Setting up PostgreSQL...
echo Creating database if it does not exist...
psql -U postgres -c "CREATE DATABASE ipsakti_db;" 2>nul
echo Database ipsakti_db created or already exists.

echo Creating/updating app user...
psql -U postgres -c "CREATE USER ipsakti_user WITH PASSWORD 'ipsakti_secure_password';" 2>nul
if errorlevel 1 (
    psql -U postgres -c "ALTER USER ipsakti_user WITH PASSWORD 'ipsakti_secure_password';" 2>nul
)
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ipsakti_db TO ipsakti_user;" 2>nul
echo Database setup completed.
echo.

REM ------------------------------------------------------------------
REM Step 3: Django migrations
REM ------------------------------------------------------------------
echo [3/5] Running Django migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: migrate failed
    pause
    exit /b 1
)
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo ERROR: collectstatic failed
    pause
    exit /b 1
)
echo Django setup completed.
echo.

REM ------------------------------------------------------------------
REM Step 4: Build frontend (if Node is available)
REM ------------------------------------------------------------------
echo [4/5] Building frontend...
if exist "%FRONTEND_DIR%\package.json" (
    cd /d "%FRONTEND_DIR%" || exit /b 1
    where npm >nul 2>&1
    if not errorlevel 1 (
        if not exist "node_modules" (
            call npm install
            if errorlevel 1 (
                echo WARNING: npm install failed. Frontend not built.
            ) else (
                echo npm install completed.
            )
        )
        call npm run build
        if errorlevel 1 (
            echo WARNING: npm run build failed. Frontend not built.
        ) else (
            echo Frontend built successfully.
        )
    ) else (
        echo WARNING: npm not found. Skipping frontend build.
        echo Install Node.js from https://nodejs.org/
    )
    cd /d "%BACKEND_DIR%" || exit /b 1
) else (
    echo ERROR: Frontend directory not found at %FRONTEND_DIR%
    echo Expected structure: %FRONTEND_DIR%\package.json
    pause
    exit /b 1
)
echo.

REM ------------------------------------------------------------------
REM Step 5: Create run scripts for Windows
REM ------------------------------------------------------------------
echo [5/5] Creating Windows run scripts...

REM Django run script (using waitress)
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo cd /d "%BACKEND_DIR%"
    echo call venv\Scripts\activate.bat
    echo echo Starting IP-SAKTI Django server with Waitress...
    echo "%BACKEND_DIR%\venv\Scripts\waitress-serve.exe" --host 0.0.0.0 --port 8000 ip_sakti.wsgi:application
) > "%BACKEND_DIR%\run_django.bat"

REM Celery worker script
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo cd /d "%BACKEND_DIR%"
    echo call venv\Scripts\activate.bat
    echo echo Starting IP-SAKTI Celery worker...
    echo celery -A ip_sakti worker --pool^=solo -l info
) > "%BACKEND_DIR%\run_celery.bat"

REM Frontend dev script
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo cd /d "%FRONTEND_DIR%"
    echo echo Starting IP-SAKTI frontend dev server...
    echo npm run dev
) > "%FRONTEND_DIR%\run_frontend.bat"

echo Created run scripts:
echo   %BACKEND_DIR%\run_django.bat
echo   %BACKEND_DIR%\run_celery.bat
echo   %FRONTEND_DIR%\run_frontend.bat
echo.

echo ==========================================
echo   Deployment Complete!
echo ==========================================
echo.
echo To run the application:
echo.
echo   1. Start Redis server
echo      redis-server
echo.
echo   2. Start Django (in a new terminal):
echo      cd %BACKEND_DIR%
echo      run_django.bat
echo.
echo   3. Start Celery worker (in a new terminal):
echo      cd %BACKEND_DIR%
echo      run_celery.bat
echo.
echo   4. Start frontend dev server (in a new terminal):
echo      cd %FRONTEND_DIR%
echo      run_frontend.bat
echo.
echo   Application URL: http://localhost:5173
echo   API URL: http://localhost:8000/api/
echo.
echo For production, consider:
echo   - Using NSSM to run waitress as a Windows service
echo   - Using Windows Task Scheduler for Celery
echo   - Using IIS or Nginx for Windows as reverse proxy
echo.
pause
