# cache_clear.ps1
# پاکسازی کامل Cache در OMP 3.5.0
# متغیر را در صورت نیاز تغییر دهید

$CONTAINER_NAME = "omp_app"

Write-Host "🧹 شروع پاکسازی Cache برای container: $CONTAINER_NAME" -ForegroundColor Cyan

# ── ۱. پاکسازی Cache اپلیکیشن OMP از طریق ابزار رسمی PKP ──────────────────
# ✅ بر اساس مستندات رسمی PKP
Write-Host "`n[۱/۴] اجرای tools/clearCache.php ..." -ForegroundColor Yellow
docker exec $CONTAINER_NAME php /var/www/html/tools/clearCache.php
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  clearCache.php با خطا مواجه شد — ادامه می‌دهیم..." -ForegroundColor DarkYellow
}

# ── ۲. پاکسازی template cache (Smarty/Compiled templates) ──────────────────
# ✅ بر اساس مستندات رسمی PKP — مسیر cache/t_compile
Write-Host "`n[۲/۴] پاکسازی template cache ..." -ForegroundColor Yellow
docker exec $CONTAINER_NAME find /var/www/html/cache/t_compile -type f -name "*.php" -delete
docker exec $CONTAINER_NAME find /var/www/html/cache/t_config -type f -delete 2>$null

# ── ۳. پاکسازی data cache ───────────────────────────────────────────────────
# ✅ بر اساس مستندات رسمی PKP — مسیر cache/_db
Write-Host "`n[۳/۴] پاکسازی data cache ..." -ForegroundColor Yellow
docker exec $CONTAINER_NAME find /var/www/html/cache -maxdepth 1 -name "*.php" -delete
docker exec $CONTAINER_NAME find /var/www/html/cache -maxdepth 1 -name "*.html" -delete

# ── ۴. پاکسازی PHP OPcache از طریق ری‌استارت Apache ────────────────────────
# ⚠️ بر اساس دانش عمومی — ری‌استارت Apache داخل container OPcache را flush می‌کند
Write-Host "`n[۴/۴] ری‌استارت Apache (flush OPcache) ..." -ForegroundColor Yellow
docker exec $CONTAINER_NAME apachectl graceful 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   ℹ️  apachectl graceful کار نکرد — تلاش با service apache2 restart ..."
    docker exec $CONTAINER_NAME service apache2 restart 2>$null
}

Write-Host "`n✅ پاکسازی Cache کامل شد." -ForegroundColor Green
Write-Host "   مرورگر را Ctrl+Shift+R کنید و وضعیت ترجمه فارسی را بررسی کنید." -ForegroundColor Cyan