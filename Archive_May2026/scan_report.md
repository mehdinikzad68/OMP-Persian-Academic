# گزارش اسکن و اعتبارسنجی ترجمه‌ها (Phase A)

**نسخه ابزار محیطی**: `Python/PowerShell 5.1.26100.8457`
**انکودینگ (Encoding) بررسی‌شده**: `UTF-8`

## فهرست موارد شناسایی‌شده

| File | msgid | Category | Current msgstr | Proposed Translation | Status | Action |
|------|-------|----------|----------------|----------------------|--------|--------|
| `lib/fa/manager.po` | `manager.navigationMenus.form.viewInstructions` | `EMPTY_MSGSTR` | `(خالی)` | `<p>این صفحه در نشانی زیر در دسترس خواهد بود: <blockquote>{$pagesPath}</blockquote>... که در آن %PATH% مسیری است که در بالا وارد کرده‌اید. <strong>توجه:</strong> هیچ دو صفحه‌ای نمی‌توانند مسیر یکسانی داشته باشند. استفاده از مسیرهایی که در سامانه تعبیه شده‌اند ممکن است باعث از دست دادن دسترسی به عملکردهای مهم شود.</p>` | `READY_FOR_REVIEW` | در انتظار تأیید |
| `lib/fa/manager.po` | `manager.navigationMenus.form.pathRegEx` | `EMPTY_MSGSTR` | `(خالی)` | `فیلد مسیر باید تنها شامل نویسه‌های الفبایی-عددی و '.', '/', '-' و '_' باشد.` | `READY_FOR_REVIEW` | در انتظار تأیید |
| `lib/fa/manager.po` | `manager.navigationMenus.form.submenuWarning` | `EMPTY_MSGSTR` | `(خالی)` | `هنگامی که یک قلم منو زیرمنویی را باز می‌کند، پیوند آن در همه دستگاه‌ها قابل دنبال کردن نیست. برای مثال، اگر یک قلم «درباره ما» داشته باشید که زیرمنویی با «تماس» و «سربرگ تحریریه» را باز می‌کند، ممکن است پیوند «درباره ما» در همه دستگاه‌ها در دسترس نباشد. در منوی پیش‌فرض، این مسئله با ایجاد دومین قلم منو، «درباره انتشارات»، که در زیرمنو ظاهر می‌شود، مدیریت می‌شود.` | `READY_FOR_REVIEW` | در انتظار تأیید |
| `lib/fa/manager.po` | `manager.navigationMenus.remoteUrl.description` | `POSSIBLE_ENGLISH_ONLY` | (نیازمند اصلاح نگارشی/انگلیسی) | `پیوند به هر نشانی وب در یک پایگاه دیگر، مانند https://pkp.sfu.ca.` | `READY_FOR_REVIEW` | در انتظار تأیید |
| `lib/fa/manager.po` | `manager.navigationMenus.about.conditionalWarning` | `EMPTY_MSGSTR` | `(خالی)` | `این پیوند تنها در صورتی نمایش داده می‌شود که بخش درباره انتشارات را در تنظیمات > انتشارات تکمیل کرده باشید.` | `READY_FOR_REVIEW` | در انتظار تأیید |
| `lib/fa/manager.po` | `manager.navigationMenus.announcements.conditionalWarning` | `EMPTY_MSGSTR` | `(خالی)` | `این پیوند تنها در صورتی نمایش داده می‌شود که اطلاعیه‌ها را در تنظیمات > پایگاه وب فعال کرده باشید.` | `READY_FOR_REVIEW` | در انتظار تأیید |

---

## خلاصه گزارش

- **تعداد کل فایل‌های اسکن‌شده**: ۴۶ فایل انگلیسی و متناظرهای فارسی آن‌ها.
- **تعداد کل کلیدهای مشکل‌دار**: ۶ مورد
- **تعداد موارد به تفکیک دسته**:
  - `EMPTY_MSGSTR`: ۵ مورد
  - `POSSIBLE_ENGLISH_ONLY`: ۱ مورد
  - `MISSING_COUNTERPART`: ۰ مورد
  - `FUZZY`: ۰ مورد
  - `MISSING_MSGID`: ۰ مورد

- **فهرست فایل‌های قابل اعمال**:
  - `OMP_Locales/lib/fa/manager.po`

- **فهرست فایل‌های پرریسک یا نامعتبر**:
  - هیچ فایلی پرریسک یا نامعتبر (SKIPPED_ENV_RISK / SKIPPED_NO_COUNTERPART) گزارش نشده است.

> [!IMPORTANT]
> با توجه به ضوابط اجرایی، این عملیات منحصراً **Scan + Dry Run + Report (Phase A)** است. تمام ۶ ترجمه پیشنهادی مطابق با «واژه‌نامه سازمانی» استخراج شده‌اند و ملاحظاتی نظیر نگهداری تگ‌های HTML (`<strong>`, `<blockquote>`) و متغیرها (`{$pagesPath}`) رعایت گردیده است. 
> هیچ‌گونه تغییری (Write) روی فایل‌ها اعمال نشده است. در صورت تأیید، **فاز دوم (Phase B: Backup -> Apply -> Validate)** اجرا خواهد شد.
