import re
import os
import sys

def parse_po_entries(filepath):
    """Parse a .po file and return dict of {msgid: (full_block_text, msgstr)}"""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    entries = {}
    # Split into blocks by double newline, find msgid/msgstr pairs
    blocks = re.split(r'\n(?=msgid )', content)
    for block in blocks:
        block = block.strip()
        if not block.startswith('msgid '):
            continue
        # Extract msgid
        msgid_match = re.match(r'^msgid\s+"((?:[^"\\]|\\.)*)"\s*\n', block)
        if not msgid_match:
            # Multi-line msgid — skip header
            continue
        msgid = msgid_match.group(1)
        if msgid == '':
            continue  # skip header
        entries[msgid] = block
    return entries

def extract_missing_and_append(fa_path, en_path, output_path):
    print(f"\nProcessing: {os.path.basename(fa_path)}")
    
    fa_entries = parse_po_entries(fa_path)
    en_entries = parse_po_entries(en_path)
    
    missing_keys = [k for k in en_entries if k not in fa_entries]
    print(f"  FA keys: {len(fa_entries)}")
    print(f"  EN keys: {len(en_entries)}")
    print(f"  Missing keys to append: {len(missing_keys)}")
    
    if not missing_keys:
        print("  ✅ No missing keys. Nothing to do.")
        return
    
    # Read original FA file content
    with open(fa_path, 'r', encoding='utf-8', errors='replace') as f:
        fa_content = f.read()
    
    # Build append block
    append_lines = ["\n\n# === Keys added from English source (needs Persian translation) ===\n"]
    for key in missing_keys:
        en_block = en_entries[key]
        # Convert English block to untranslated Persian entry
        # Keep msgid, set msgstr to "" (empty - needs translation)
        lines = en_block.split('\n')
        new_lines = []
        in_msgstr = False
        for line in lines:
            if line.startswith('msgstr '):
                new_lines.append('msgstr ""')
                in_msgstr = True
            elif in_msgstr and line.startswith('"'):
                pass  # skip multi-line msgstr continuation
            else:
                in_msgstr = False
                new_lines.append(line)
        append_lines.append('\n'.join(new_lines))
        append_lines.append('')
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(fa_content.rstrip() + '\n')
        f.write('\n'.join(append_lines))
    
    print(f"  ✅ Written to: {output_path}")
    print(f"  Missing keys appended:")
    for k in missing_keys:
        print(f"    - {k}")

# ─── Configuration ───────────────────────────────────────────────
BASE = r"C:\omp-server"
TOOLS = os.path.join(BASE, "tools")

tasks = [
    {
        "fa": os.path.join(BASE, r"OMP_Locales\lib\fa\submission.po"),
        "en": os.path.join(TOOLS, "submission_en.po"),
        "out": os.path.join(BASE, r"OMP_Locales\lib\fa\submission.po"),
    },
    {
        "fa": os.path.join(BASE, r"OMP_Locales\lib\fa\common.po"),
        "en": os.path.join(TOOLS, "common_en.po"),
        "out": os.path.join(BASE, r"OMP_Locales\lib\fa\common.po"),
    },
]

# ─── Safety backup ───────────────────────────────────────────────
import shutil, datetime
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
for task in tasks:
    src = task["fa"]
    bak = src + f".bak_{ts}"
    shutil.copy2(src, bak)
    print(f"Backup created: {bak}")

# ─── Process ─────────────────────────────────────────────────────
for task in tasks:
    extract_missing_and_append(task["fa"], task["en"], task["out"])

print("\n✅ All done.")
