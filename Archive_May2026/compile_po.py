#!/usr/bin/env python3
"""
OMP Localization Compiler
Compiles all .po files in OMP_Locales/ to .mo using msgfmt
Requirements: msgfmt must be in system PATH
Compatible: Python 3.11+, Windows/Linux/macOS
"""

import subprocess
import shutil
import sys
from pathlib import Path

# ── تنظیمات ──────────────────────────────────────────────────────────────────
LOCALES_DIR = Path(__file__).parent / "OMP_Locales"
# ─────────────────────────────────────────────────────────────────────────────


def check_msgfmt() -> Path:
    """بررسی وجود msgfmt در PATH سیستم"""
    found = shutil.which("msgfmt")
    if not found:
        print("❌ خطا: ابزار 'msgfmt' در PATH سیستم یافت نشد.")
        print("   راه‌حل (Windows): نصب gettext via https://mlocati.github.io/articles/gettext-iconv-windows.html")
        print("   راه‌حل (Ubuntu/WSL): sudo apt-get install gettext")
        sys.exit(1)
    return Path(found)


def verify_utf8_no_bom(filepath: Path) -> bool:
    """بررسی encoding UTF-8 بدون BOM"""
    with open(filepath, "rb") as f:
        raw = f.read(3)
    if raw.startswith(b"\xef\xbb\xbf"):
        return False
    return True


def compile_po_file(po_path: Path, msgfmt_path: Path) -> bool:
    """کامپایل یک فایل .po به .mo در همان مسیر"""
    mo_path = po_path.with_suffix(".mo")

    # بررسی encoding پیش از کامپایل
    if not verify_utf8_no_bom(po_path):
        print(f"⛔ توقف — BOM شناسایی شد: {po_path}")
        print(f"   فایل دارای UTF-8 with BOM است. قبل از ادامه این فایل را fix کنید.")
        print(f"   دستور fix در WSL: sed -i 's/\\xef\\xbb\\xbf//' \"{po_path}\"")
        sys.exit(2)

    result = subprocess.run(
        [str(msgfmt_path), "-o", str(mo_path), str(po_path)],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    if result.returncode != 0:
        print(f"❌ خطای msgfmt برای فایل: {po_path}")
        print(f"   stderr: {result.stderr.strip()}")
        sys.exit(3)

    return True


def main():
    if not LOCALES_DIR.exists():
        print(f"❌ پوشه '{LOCALES_DIR}' یافت نشد. مسیر LOCALES_DIR را بررسی کنید.")
        sys.exit(4)

    msgfmt_path = check_msgfmt()
    print(f"✅ msgfmt پیدا شد: {msgfmt_path}")
    print(f"🔍 اسکن پوشه: {LOCALES_DIR}\n")

    po_files = sorted(LOCALES_DIR.rglob("*.po"))

    if not po_files:
        print("⚠️ هیچ فایل .po یافت نشد.")
        sys.exit(0)

    success_count = 0
    for po_file in po_files:
        print(f"⚙️  کامپایل: {po_file.relative_to(LOCALES_DIR.parent)}")
        compile_po_file(po_file, msgfmt_path)
        print(f"   ✅ → {po_file.with_suffix('.mo').name}")
        success_count += 1

    print(f"\n🎉 کامپایل کامل شد — {success_count} فایل با موفقیت پردازش شدند.")


if __name__ == "__main__":
    main()