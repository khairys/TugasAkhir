import sys
import json
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

with open('datasets_analysis_summary.json', encoding='utf-8') as f:
    d = json.load(f)

for k, v in d['overlap'].items():
    if v['label_conflicts'] > 0:
        print(f"=== Conflicts in {k} (total: {v['label_conflicts']}) ===")
        for sample in v['conflict_samples']:
            print(f"Text: {sample['norm_text']}")
            print(f"  label_i: {sample['label_val_i']} vs label_j: {sample['label_val_j']}")
