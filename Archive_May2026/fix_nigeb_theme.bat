@echo off
chcp 65001 >nul
echo ============================================================
echo   NigebTheme Plugin Fix Script
echo   OMP 3.5 - Docker-based deployment
echo ============================================================
echo.

REM ---------------------------------------------------------
REM Step 1: Database Cleanup
REM ---------------------------------------------------------
echo [Step 1/5] Querying versions table for nigebTheme rows...
docker exec omp_db mysql -u omp_user -pomp_password omp_db -e "SELECT * FROM versions WHERE product LIKE '%%nigeb%%' OR product LIKE '%%Nigeb%%';"
echo.

echo [Step 1/5] Deleting stale nigebTheme rows from versions table...
docker exec omp_db mysql -u omp_user -pomp_password omp_db -e "DELETE FROM versions WHERE product LIKE '%%nigeb%%' OR product LIKE '%%Nigeb%%';"
if %ERRORLEVEL% EQU 0 (
    echo           ✓ Database cleanup completed successfully.
) else (
    echo           ✗ Database cleanup failed or no rows found.
)
echo.

REM ---------------------------------------------------------
REM Step 2: Docker Compose Down / Up
REM ---------------------------------------------------------
echo [Step 2/5] Stopping containers (docker compose down)...
docker compose down
echo.

echo [Step 3/5] Starting containers with new volume mount (docker compose up -d)...
docker compose up -d
echo.

echo           Waiting 15 seconds for containers to fully start...
timeout /t 15 /nobreak >nul
echo.

REM ---------------------------------------------------------
REM Step 3: Cache Clearing
REM ---------------------------------------------------------
echo [Step 4/5] Clearing PKP cache inside container...
docker exec omp_app php /var/www/html/lib/pkp/tools/clearCache.php
if %ERRORLEVEL% EQU 0 (
    echo           ✓ Cache cleared successfully.
) else (
    echo           ✗ Cache clear command failed. Check logs.
)
echo.

echo [Step 4/5] Running upgrade check...
docker exec omp_app php /var/www/html/tools/upgrade.php check
echo.

REM ---------------------------------------------------------
REM Step 4: Verify Plugin Files Inside Container
REM ---------------------------------------------------------
echo [Step 5/5] Verifying plugin files inside the container...
echo.
echo --- Directory listing: /var/www/html/plugins/themes/nigebTheme/ ---
docker exec omp_app ls -la /var/www/html/plugins/themes/nigebTheme/
echo.
echo --- version.xml contents ---
docker exec omp_app cat /var/www/html/plugins/themes/nigebTheme/version.xml
echo.
echo --- NigebThemePlugin.inc.php (first 5 lines) ---
docker exec omp_app head -5 /var/www/html/plugins/themes/nigebTheme/NigebThemePlugin.inc.php
echo.

REM ---------------------------------------------------------
REM Step 5: Check for PHP Fatal Errors
REM ---------------------------------------------------------
echo --- Checking PHP/Apache error logs for nigebTheme errors ---
docker exec omp_app bash -c "grep -i 'nigeb' /var/log/apache2/error.log 2>/dev/null || echo 'No nigebTheme errors found in Apache logs.'"
echo.

echo ============================================================
echo   Fix script completed!
echo   Please open http://localhost:8080 and check:
echo     1. Website Settings > Plugins > Theme Plugins tab
echo     2. Website Settings > Appearance > Theme
echo ============================================================
pause
