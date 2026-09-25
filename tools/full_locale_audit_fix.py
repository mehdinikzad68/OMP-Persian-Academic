import re, os, shutil, datetime

def parse_po_entries(filepath):
    """Returns dict of {msgid: full_block_string}"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except FileNotFoundError:
        return {}

    entries = {}
    blocks = re.split(r'\n(?=msgid )', content)
    for block in blocks:
        block = block.strip()
        if not block.startswith('msgid '):
            continue
        m = re.match(r'^msgid\s+"((?:[^"\\]|\\.)*)"\s*\n', block)
        if not m or m.group(1) == '':
            continue
        entries[m.group(1)] = block
    return entries

def get_header(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        parts = re.split(r'\n(?=msgid )', content)
        if parts and 'msgid ""' in parts:
            return parts.strip()
    except:
        pass
    return ''

def make_untranslated_block(en_block):
    """Convert English block to empty-msgstr Persian-ready block"""
    lines = en_block.split('\n')
    result = []
    in_msgstr = False
    for line in lines:
        if line.startswith('msgstr '):
            result.append('msgstr ""')
            in_msgstr = True
        elif in_msgstr and (line.startswith('"') or line == ''):
            if line == '':
                in_msgstr = False
                result.append(line)
        else:
            in_msgstr = False
            result.append(line)
    return '\n'.join(result)

def append_missing_keys(fa_path, en_path, label):
    fa_entries = parse_po_entries(fa_path)
    en_entries = parse_po_entries(en_path)
    missing = [k for k in en_entries if k not in fa_entries]

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  FA: {len(fa_entries)} keys | EN: {len(en_entries)} keys | Missing: {len(missing)}")

    if not missing:
        print("  ✅ No missing keys.")
        return 0

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = fa_path + f".bak_{ts}"
    shutil.copy2(fa_path, bak)

    with open(fa_path, 'r', encoding='utf-8', errors='replace') as f:
        existing = f.read()

    append_lines = ["\n\n# === Auto-appended missing keys (needs Persian translation) ===\n"]
    for key in missing:
        append_lines.append(make_untranslated_block(en_entries[key]))
        append_lines.append('')

    with open(fa_path, 'w', encoding='utf-8') as f:
        f.write(existing.rstrip() + '\n' + '\n'.join(append_lines))

    print(f"  ✅ Appended {len(missing)} keys:")
    for k in missing:
        print(f"     + {k}")
    return len(missing)

def create_plugin_fa_locale(en_path, fa_path, plugin_name):
    """Create a new fa locale.po from English source with empty msgstr"""
    en_entries = parse_po_entries(en_path)
    header = get_header(en_path)

    print(f"\n{'='*60}")
    print(f"  Plugin: {plugin_name}")
    print(f"  Creating new FA locale: {fa_path}")
    print(f"  EN keys: {len(en_entries)}")

    os.makedirs(os.path.dirname(fa_path), exist_ok=True)

    lines = []
    if header:
        lines.append(header)
        lines.append('')

    lines.append("# === Plugin locale — needs Persian translation ===")
    lines.append('')

    for key, block in en_entries.items():
        lines.append(make_untranslated_block(block))
        lines.append('')

    with open(fa_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"  ✅ Created with {len(en_entries)} keys (empty msgstr — needs translation)")
    return len(en_entries)

# ──────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────
BASE      = r"C:\omp-server"
FA_CORE   = os.path.join(BASE, r"OMP_Locales\core\fa")
FA_LIB    = os.path.join(BASE, r"OMP_Locales\lib\fa")
EN_CORE   = os.path.join(BASE, r"tools\en_source\core")
EN_LIB    = os.path.join(BASE, r"tools\en_source\lib")
EN_PLUGIN = os.path.join(BASE, r"tools\en_source")

# ──────────────────────────────────────────────────────────────────
# FILE MAPPING: (fa_file, en_file, label)
# ──────────────────────────────────────────────────────────────────
file_pairs = [
    # Core OMP (locale/fa/)
    (f"{FA_CORE}\\admin.po",      f"{EN_CORE}\\admin.po",      "core/fa/admin.po"),
    (f"{FA_CORE}\\author.po",     f"{EN_CORE}\\author.po",     "core/fa/author.po"),
    (f"{FA_CORE}\\default.po",    f"{EN_CORE}\\default.po",    "core/fa/default.po"),
    (f"{FA_CORE}\\editor.po",     f"{EN_CORE}\\editor.po",     "core/fa/editor.po"),
    (f"{FA_CORE}\\emails.po",     f"{EN_CORE}\\emails.po",     "core/fa/emails.po"),
    (f"{FA_CORE}\\invitation.po", f"{EN_CORE}\\invitation.po", "core/fa/invitation.po"),
    (f"{FA_CORE}\\locale.po",     f"{EN_CORE}\\locale.po",     "core/fa/locale.po"),
    (f"{FA_CORE}\\manager.po",    f"{EN_CORE}\\manager.po",    "core/fa/manager.po"),
    (f"{FA_CORE}\\submission.po", f"{EN_CORE}\\submission.po", "core/fa/submission.po"),
    # Lib PKP (lib/pkp/locale/fa/)
    (f"{FA_LIB}\\admin.po",       f"{EN_LIB}\\admin.po",       "lib/fa/admin.po"),
    (f"{FA_LIB}\\api.po",         f"{EN_LIB}\\api.po",         "lib/fa/api.po"),
    (f"{FA_LIB}\\common.po",      f"{EN_LIB}\\common.po",      "lib/fa/common.po"),
    (f"{FA_LIB}\\default.po",     f"{EN_LIB}\\default.po",     "lib/fa/default.po"),
    (f"{FA_LIB}\\editor.po",      f"{EN_LIB}\\editor.po",      "lib/fa/editor.po"),
    (f"{FA_LIB}\\emails.po",      f"{EN_LIB}\\emails.po",      "lib/fa/emails.po"),
    (f"{FA_LIB}\\grid.po",        f"{EN_LIB}\\grid.po",        "lib/fa/grid.po"),
    (f"{FA_LIB}\\installer.po",   f"{EN_LIB}\\installer.po",   "lib/fa/installer.po"),
    (f"{FA_LIB}\\invitation.po",  f"{EN_LIB}\\invitation.po",  "lib/fa/invitation.po"),
    (f"{FA_LIB}\\manager.po",     f"{EN_LIB}\\manager.po",     "lib/fa/manager.po"),
    (f"{FA_LIB}\\reader.po",      f"{EN_LIB}\\reader.po",      "lib/fa/reader.po"),
    (f"{FA_LIB}\\reviewer.po",    f"{EN_LIB}\\reviewer.po",    "lib/fa/reviewer.po"),
    (f"{FA_LIB}\\submission.po",  f"{EN_LIB}\\submission.po",  "lib/fa/submission.po"),
    (f"{FA_LIB}\\user.po",        f"{EN_LIB}\\user.po",        "lib/fa/user.po"),
]

# ──────────────────────────────────────────────────────────────────
# PLUGIN FILES TO CREATE
# ──────────────────────────────────────────────────────────────────
plugin_tasks = [
    (
        f"{EN_PLUGIN}\\plugin_csv_locale.po",
        os.path.join(BASE, r"OMP_Locales\plugins\importexport\csv\locale\fa\locale.po"),
        "importexport/csv"
    ),
    (
        f"{EN_PLUGIN}\\plugin_native_locale.po",
        os.path.join(BASE, r"OMP_Locales\plugins\importexport\native\locale\fa\locale.po"),
        "importexport/native"
    ),
    (
        f"{EN_PLUGIN}\\plugin_onix30_locale.po",
        os.path.join(BASE, r"OMP_Locales\plugins\importexport\onix30\locale\fa\locale.po"),
        "importexport/onix30"
    ),
]

# ──────────────────────────────────────────────────────────────────
# RUN
# ──────────────────────────────────────────────────────────────────
total_missing = 0
print("=== FULL LOCALE AUDIT & FIX ===")

for fa, en, label in file_pairs:
    if not os.path.exists(en):
        print(f"\n⚠️  EN file not found, skipping: {en}")
        continue
    if not os.path.exists(fa):
        print(f"\n⚠️  FA file not found, skipping: {fa}")
        continue
    total_missing += append_missing_keys(fa, en, label)

print(f"\n{'='*60}")
print(f"TOTAL MISSING KEYS APPENDED: {total_missing}")

print("\n=== PLUGIN LOCALE CREATION ===")
for en_p, fa_p, name in plugin_tasks:
    if not os.path.exists(en_p):
        print(f"\n⚠️  EN plugin file not found: {en_p}")
        continue
    create_plugin_fa_locale(en_p, fa_p, name)

print("\n✅ ALL DONE.")
