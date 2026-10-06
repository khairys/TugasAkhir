import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
with open('data/interim/all_51_conflicts.json', encoding='utf-8') as f:
    items = json.load(f)

for idx, it in enumerate(items, 1):
    src = it['sources_str']
    txt = it['text'].replace('\n', ' ')
    print(f"[{idx:02d}] {src}")
    print(f"     \"{txt}\"\n")
