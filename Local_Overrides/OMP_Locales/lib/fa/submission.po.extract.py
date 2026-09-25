
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'c:\omp-server\OMP_Locales\lib\fa\submission.po'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_msgids = [
    "author.submission.roundStatus.reviewOverdue",
    "submission.submit.managerUserGroupsDescription",
    "metadata.filters.crossref.settings.email.validationMessage",
    "metadata.filters.settings.isOptional.validationMessage",
    "metadata.property.validationMessage.author",
    "metadata.property.validationMessage.editor",
    "metadata.property.validationMessage.publication-type",
    "metadata.property.validationMessage.title-type",
    "metadata.property.validationMessage.nonSort",
    "metadata.property.validationMessage.name-type"
]

for msgid in target_msgids:
    # Find the block for this msgid
    pattern = re.compile(rf'msgid "{msgid}"\s*msgstr\s+""(?!\s*")', re.DOTALL)
    # Actually some might be multiline msgid, but these look short.
    # Let's find them with context.
    
    # Better: find the line number and print 10 lines after.
    match = re.search(rf'msgid "{msgid}"', content)
    if match:
        start = match.start()
        # Find end of msgstr ""
        end_match = re.search(r'msgstr ""', content[start:])
        if end_match:
            block_end = start + end_match.end()
            print("---")
            print(content[start:block_end])
