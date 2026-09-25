# deploy_mo.ps1
# استقرار فایل‌های .mo زبان فارسی در OMP Container
# سازگار با: Docker 29.x, PowerShell 5.1, Windows 11

$CONTAINER_NAME = "omp_app"
$LOCAL_LOCALES = ".\OMP_Locales"

# مسیرهای مقصد در container
$OMP_LOCALE_PATH   = "/var/www/html/locale/fa_IR"
$PKP_LOCALE_PATH   = "/var/www/html/lib/pkp/locale/fa_IR"

Write-Host "🚀 شروع استقرار فایل‌های .mo در container: $CONTAINER_NAME" -ForegroundColor Cyan

# ── تابع: بررسی وجود مسیر در container ─────────────────────────────────────
function Test-ContainerPath {
    param([string]$ContainerName, [string]$RemotePath)
    $result = docker exec $ContainerName test -d $RemotePath 2>&1
    return ($LASTEXITCODE -eq 0)
}

# ── تابع: کپی ایمن فایل‌های .mo به مسیر مقصد ───────────────────────────────
function Deploy-MoFiles {
    param(
        [string]$ContainerName,
        [string]$LocalPath,
        [string]$RemotePath
    )

    Write-Host "`n📂 مقصد: $RemotePath" -ForegroundColor Yellow

    $pathExists = Test-ContainerPath -ContainerName $ContainerName -RemotePath $RemotePath

    if (-not $pathExists) {
        Write-Host "   ℹ️  مسیر مقصد وجود ندارد — در حال ساخت..." -ForegroundColor DarkYellow
        docker exec $ContainerName mkdir -p $RemotePath
        if ($LASTEXITCODE -ne 0) {
            Write-Host "   ❌ خطا در ساخت مسیر مقصد. متوقف شد." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "   ✅ مسیر مقصد وجود دارد." -ForegroundColor Green
    }

    # استفاده از /. برای کپی محتوا (نه خود پوشه) — رفتار ایمن
    # [توضیح]: trailing /. باعث می‌شود محتوای پوشه کپی شود، نه پوشه خودش
    docker cp "${LocalPath}/." "${ContainerName}:${RemotePath}/"

    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ خطا در docker cp. متوقف شد." -ForegroundColor Red
        exit 1
    }

    Write-Host "   ✅ فایل‌ها با موفقیت کپی شدند." -ForegroundColor Green
}

# ── استقرار برای locale/fa_IR (فایل‌های مختص OMP) ──────────────────────────
$ompLocalSrc = Join-Path $LOCAL_LOCALES "omp\fa_IR"
if (Test-Path $ompLocalSrc) {
    Deploy-MoFiles -ContainerName $CONTAINER_NAME -LocalPath $ompLocalSrc -RemotePath $OMP_LOCALE_PATH
} else {
    Write-Host "⚠️  مسیر '$ompLocalSrc' یافت نشد — این مرحله رد شد." -ForegroundColor DarkYellow
}

# ── استقرار برای lib/pkp/locale/fa_IR (فایل‌های مشترک PKP) ─────────────────
$pkpLocalSrc = Join-Path $LOCAL_LOCALES "pkp\fa_IR"
if (Test-Path $pkpLocalSrc) {
    Deploy-MoFiles -ContainerName $CONTAINER_NAME -LocalPath $pkpLocalSrc -RemotePath $PKP_LOCALE_PATH
} else {
    Write-Host "⚠️  مسیر '$pkpLocalSrc' یافت نشد — این مرحله رد شد." -ForegroundColor DarkYellow
}

Write-Host "`n🎉 استقرار کامل شد." -ForegroundColor Green
Write-Host "   گام بعدی: اجرای اسکریپت پاکسازی Cache." -ForegroundColor Cyan