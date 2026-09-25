import os
import sys
import re

def find_fuzzy(files, limit=10):
    fuzzy_blocks = []
    
    for filename in files:
        if not filename.endswith('.po'):
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find blocks starting with #, fuzzy
        # We want to capture the msgid and the msgstr
        # Pattern: #, fuzzy\nmsgid "(.*?)"\nmsgstr "(.*?)"
        # Note: msgstr might be multiline
        
        pattern = re.compile(r'#, fuzzy\nmsgid "(.*?)"\nmsgstr "(.*?)"', re.DOTALL)
        
        matches = re.finditer(pattern, content)
        for match in matches:
            msgid = match.group(1)
            msgstr = match.group(2)
            fuzzy_blocks.append({
                'file': filename,
                'msgid': msgid,
                'msgstr': msgstr
            })
            if len(fuzzy_blocks) >= limit:
                return fuzzy_blocks
                
    return fuzzy_blocks

if __name__ == "__main__":
    po_files = [f for f in os.listdir('.') if f.endswith('.po')]
    fuzzy_found = find_fuzzy(po_files)
    
    for i, item in enumerate(fuzzy_found, 1):
        print(f"{i}. {item['file']} | {item['msgid']}")
