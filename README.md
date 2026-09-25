# 📚 سامانه بومی‌سازی و نشر دانشگاهی Open Monograph Press (OMP 3.5.0)
### Persian Academic Localization, RTL Theme & Docker Orchestration for OMP

![OMP Version](https://img.shields.io/badge/OMP-3.5.0-blue.svg)
![Language](https://img.shields.io/badge/Language-Persian%20%28فارسی%29-green.svg)
![Layout](https://img.shields.io/badge/Layout-Full%20RTL-orange.svg)
![Docker](https://img.shields.io/badge/Deployment-Docker%20Compose-2496ED.svg)
![License](https://img.shields.io/badge/License-GPL--3.0-blue.svg)

---

## 📖 درباره پروژه (About the Project)

نرم‌افزار **Open Monograph Press (OMP)** توسعه داده شده توسط **پروژه دانش عمومی (PKP)**، یکی از معتبرترین و استانداردترین پلتفرم‌های متن‌باز جهانی برای مدیریت فرآیند داوری، ویراستاری و انتشار کتاب‌ها و تک‌نگاشت‌های علمی و دانشگاهی (Monographs & Edited Volumes) است.

این مخزن شامل **بومی‌سازی کامل، ترجمه تخصصی بر مبنای واژگان مصوب دانشگاهی، قالب اختصاصی راست‌چین (RTL) و بستر آماده استقرار با Docker** برای سامانه **OMP نسخه 3.5.0** می‌باشد.

---

## ✨ ویژگی‌های برجسته (Key Features)

### ۱. ترجمه دانشگاهی و استاندارد (Academic Localization)
- **ترجمه کامل هسته (Core)**: تمامی بخش‌های مدیریتی، پیشخوان کاربری، و تنظیمات اصلی.
- **ترجمه کتابخانه مشترک PKP (Shared Library)**:
  - پنل‌های ارسال اثر و ثبت دست‌نوشته (`submission`)
  - فرآیند داوری علمی و تخصصی (`reviewer`)
  - بخش ویراستاری، صفحه‌آرایی و تولید نهایی اثر (`editor`, `production`)
  - ایمیل‌های خودکار سیستم (`emails`) با نگارش رسمی و محترمانه دانشگاهی
  - رده‌بندی استاندارد موضوعی (`bic21subjects.xml` و `bic21qualifiers.xml`)
- **ترجمه افزونه‌ها و پلاگین‌های حیاتی (Plugins)**:
  - افزونه‌های متاداده (`Dublin Core`, `Google Scholar`, `DOI`, `URN`)
  - افزونه‌های خروجی و ورودی استاندارد (`ONIX 3.0`, `Native XML`, `CSV`)
  - افزونه‌های نمایشگر درون‌برنامه‌ای فایل‌های کتاب (`PDF.js Viewer`, `HTML Monograph File`)
  - افزونه‌های آماری و نمایه‌سازی (`Google Analytics`, `SUSHI/COUNTER`)

### ۲. واژه‌نامه تخصصی مصوب (Academic Glossary)
در تمامی ترجمه‌ها، لحن کاملاً رسمی و دانشگاهی رعایت شده و معادل‌های استاندارد به‌کار رفته است:
| اصطلاح لاتین | معادل استاندارد دانشگاهی در این سامانه |
| :--- | :--- |
| **Submission** | ارسال اثر / ثبت دست‌نوشته |
| **Review / Reviewer** | داوری علمی / داور همتا |
| **Copyediting** | ویراستاری فنی و ادبی |
| **Production** | فرآیند تولید و نشر |
| **Monograph / Edited Volume** | تک‌نگاشت / مجموعه مقالات گردآوری‌شده |
| **Press / Catalog** | مرکز نشر / کاتالوگ و ویترین آثار |
| **Series** | مجموعه‌کتاب / سلسله منشورات |

### ۳. قالب اختصاصی و راست‌چین آکادمیک (Academic RTL Theme)
- توسعه و بهینه‌سازی قالب اختصاصی دانشگاهی (`nigebTheme`)
- پشتیبانی کامل و اصولی از چیدمان راست‌به‌چپ (RTL) در تمامی بخش‌های کاربری و کاتالوگ
- تایپوگرافی زیبا، خوانا و متناسب با پرستیژ مراکز دانشگاهی و پژوهشگاه‌ها

### ۴. استقرار آنی با داکر (Instant Docker Deployment)
- دارای فایل `docker-compose.yml` پیکربندی‌شده شامل OMP 3.5.0 و پایگاه‌داده MariaDB
- مانت (Mount) خودکار و تفکیک‌شده فایل‌های زبان و تم بدون نیاز به تغییر دستی کانتینرها

### ۵. ابزارهای مدیریت و اعتبارسنجی (Localization Tools)
- اسکریپت‌های پایتون جهت بررسی یکپارچگی (`full_locale_audit_fix.py`)، استخراج کلیدهای مفقوده و تولید فایل‌های کامپایل‌شده `.mo`

---

## 🚀 راهنمای راه‌اندازی سریع (Quick Start Guide)

### پیش‌نیازها
- نصب [Docker](https://www.docker.com/) و Docker Compose روی سرور یا رایانه محلی.
- ابزار `git`

### مراحل اجرا:

۱. کلون کردن ریپازیتوری:
```bash
git clone https://github.com/mehdinikzad68/OMP-Persian-Academic.git
cd OMP-Persian-Academic
```

۲. راه‌اندازی کانتینرهای OMP و MariaDB:
```bash
docker compose up -d
```

۳. دسترسی به سامانه:
مرورگر خود را باز کرده و به آدرس زیر مراجعه فرمایید:
```
http://localhost:8080
```

> **نکته**: اطلاعات پیش‌فرض اتصال پایگاه داده در `docker-compose.yml` و `config.inc.php` تعریف شده است:
> - نام پایگاه‌داده: `omp_db`
> - نام کاربری: `omp_user`
> - رمز عبور: `omp_password`

---

## 📁 ساختار مخزن (Repository Structure)

```text
├── docker-compose.yml          # فایل پیکربندی کانتینرهای OMP و MariaDB
├── config.inc.php              # تنظیمات اصلی پیکربندی OMP 3.5
├── ARCHITECTURE_PLAN.md        # نقشه استراتژی و مستند معماری پروژه
├── DIRECTORY_STRUCTURE.md      # راهنمای جامع ساختار فایل‌ها
├── Local_Overrides/
│   ├── OMP_Locales/            # فایل‌های ترجمه فارسی (PO و MO)
│   │   ├── core/fa/            # ترجمه هسته سیستم
│   │   ├── lib/fa/             # ترجمه کتابخانه‌های فرآیند نشر و داوری
│   │   └── plugins/            # ترجمه تک‌تک افزونه‌های رسمی
│   └── nigebTheme/             # تم اختصاصی راست‌چین دانشگاهی
├── tools/                      # اسکریپت‌های پایتون آدیت و مدیریت ترجمه
└── Archive_May2026/            # مستندات و اسکریپت‌های توسعه
```

---

## 🤝 مشارکت و توسعه (Contributing)

از هرگونه مشارکت در بهبود ترجمه‌ها، گزارش مغایرت‌های زبانی یا بهینه‌سازی تم‌ها استقبال می‌شود. لطفاً نظرات و اصلاحات خود را از طریق **Issue** یا **Pull Request** ارسال نمایید.

---

## 📄 مجوز (License)

این پروژه بر اساس مجوز **GNU General Public License v3.0 (GPLv3)** منتشر شده است و از شرایط نرم‌افزارهای متن‌باز Public Knowledge Project (PKP) پیروی می‌کند.
