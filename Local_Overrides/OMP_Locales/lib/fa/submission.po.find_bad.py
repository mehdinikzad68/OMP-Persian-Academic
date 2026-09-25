
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'c:\omp-server\OMP_Locales\lib\fa\submission.po'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

terms = ["نویسنده", "نویسندگان", "دست نوشته", "دست‌نوشته", "دانلود", "مجله", "نشریه", "آپلود"]

found = []
for i, line in enumerate(lines):
    if line.startswith('#~'): continue # Skip obsolete
    
    # Skip already fixed ones
    skip_contents = [
        "آیا از حذف سوابق مکاتبات ایمیلی مربوط به این اثر ارسالی اطمینان دارید؟",
        "مراحل ارسال اولیه اثر با موفقیت تکمیل شد.",
        "اطلاعات اثر ارسالی",
        "فراداده اثر ارسالی",
        "هیچ دبیری برای این اثر ارسالی تعیین نشده است (در انتظار انتساب).",
        "فایل اصل اثر ارسالی",
        "کلیه فایل‌های مورد نیاز تیم تحریریه جهت ارزیابی اثر خود را بارگذاری نمایید.",
        "بارگذاری فایل اصل اثر",
        "اثر باید جهت بررسی مجدد در دور جدید داوری ارسال گردد.",
        "اثر جهت بررسی در دور جدید داوری، مجدداً ارسال گردید.",
        "نسخه اصلاحی «{$filename}» برای فایل {$submissionFileId} بارگذاری شد.",
        "فایل شما با موفقیت بارگذاری شد.",
        "1. بارگذاری فایل",
        "اثر ارسالی پذیرفته شد.",
        "اثر ارسالی رد شد.",
        "برای پدیدآورندگان ایمیلی ارسال نمایید تا از انتقال اثر به مرحله تولید و نشر مطلع گردند.",
        "بازگرداندن اثر از مرحله ویراستاری به مرحله پیشین.",
        "پذیرش و عبور از داوری",
        "پذیرش اثر جهت انتشار و عبور از مرحله داوری.",
        "اثر {$title} از مرحله داوری عبور کرده و به مرحله ویراستاری منتقل شد."
    ]
    if any(skip in line for skip in skip_contents):
        continue

    for term in terms:
        if term in line:
            found.append((i + 1, line.strip()))
            break
    if len(found) >= 20:
        break

for line_no, content in found:
    print(f"Line {line_no}: {content}")
