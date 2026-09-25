import os
import re

def find_empty_translations(directory):
    results = []
    # Order files logically or by name
    files = sorted([f for f in os.listdir(directory) if f.endswith('.po')])
    for filename in files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        pattern = r'msgid "(.*?)"\s*?\nmsgstr ""\s*?\n(?=\n|msgid|$)'
        matches = re.finditer(pattern, content, re.MULTILINE)
        
        for match in matches:
            results.append((filename, match.group(1)))
    return results

if __name__ == "__main__":
    locales_dir = r'c:\omp-server\OMP_Locales\lib\fa'
    empty_strings = find_empty_translations(locales_dir)
    # Skip the ones from admin.po and default.po that we already did
    # Actually, let's just print the first 10 remaining across all files
    for i, (filename, msgid) in enumerate(empty_strings[:10]):
        print(f"{i+1}. {filename} | {msgid}")
