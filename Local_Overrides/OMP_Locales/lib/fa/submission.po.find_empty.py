
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'c:\omp-server\OMP_Locales\lib\fa\submission.po'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines):
    if line.strip().startswith('msgstr ""'):
        # Check if next line exists and starts with "
        has_text = False
        if i + 1 < len(lines) and lines[i+1].strip().startswith('"'):
            has_text = True
        
        if not has_text:
            # Find the msgid before it
            msgid = ""
            for j in range(i-1, -1, -1):
                if lines[j].startswith('msgid'):
                    msgid = lines[j].strip()
                    break
            
            if msgid and msgid != 'msgid ""':
                print(f"Line {i+1}: {msgid}")
                count += 1
                if count >= 10:
                    break
