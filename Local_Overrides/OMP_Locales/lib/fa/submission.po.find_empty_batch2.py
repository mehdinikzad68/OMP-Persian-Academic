
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'c:\omp-server\OMP_Locales\lib\fa\submission.po'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

already_fixed = [
    "editor.submission.recommendation.noDecidingEditors",
    "log.review.reviewerResendRequest",
    "publication.wordCountLong"
]

count = 0
for i, line in enumerate(lines):
    if line.strip().startswith('msgstr ""'):
        has_text = False
        if i + 1 < len(lines) and lines[i+1].strip().startswith('"'):
            has_text = True
        
        if not has_text:
            msgid = ""
            for j in range(i-1, -1, -1):
                if lines[j].startswith('msgid'):
                    msgid = re.search(r'msgid "(.*)"', lines[j]).group(1)
                    break
            
            if msgid and msgid != "" and msgid not in already_fixed:
                print(f"Empty entry: {msgid}")
                count += 1
                if count >= 10:
                    break
