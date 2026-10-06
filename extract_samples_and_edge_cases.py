import sys
import json
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

DATASETS = [
    {
        "id": "DS1_fahruu",
        "name": "fahruu/komentar-judi-online",
        "file": "datasets/fahruu_komentar-judi-online/judi_online.csv",
        "raw_col": "comment",
        "clean_col": "final_comment",
        "label_col": "label"
    },
    {
        "id": "DS2_kyyyy8_all",
        "name": "kyyyy8/dataset-komentar-judi-online-di-youtube",
        "file": "datasets/kyyyy8_dataset-komentar-judi-online-di-youtube/dataset.csv",
        "raw_col": "text",
        "clean_col": "text_preprocessed",
        "label_col": "label"
    },
    {
        "id": "DS3_yaemico",
        "name": "yaemico/deteksi-judi-online",
        "file": "datasets/yaemico_deteksi-judi-online/youtube_chat_jogja_clean.csv",
        "raw_col": "message",
        "clean_col": "cleaned_message",
        "label_col": "label"
    },
    {
        "id": "DS4_kyyyy8_plat",
        "name": "kyyyy8/dataset-komentar-judi-online-platform-youtube",
        "file": "datasets/kyyyy8_dataset-komentar-judi-online-platform-youtube/dataset_komentarJudol_preprocessed_nonAnom.csv",
        "raw_col": "text",
        "clean_col": "text_preprocessed",
        "label_col": "label"
    },
    {
        "id": "DS5_ferdiansakti",
        "name": "ferdiansakti/gambling-comments-from-youtube-platform",
        "file": "datasets/ferdiansakti_gambling-comments-from-youtube-platform/rawdata.csv",
        "raw_col": "Comments",
        "clean_col": None,
        "label_col": "Label"
    }
]

def get_samples(df, raw_col, label_col, label_val, n=25):
    sub = df[df[label_col] == label_val].dropna(subset=[raw_col]).copy()
    # remove duplicate texts for diverse samples
    sub = sub.drop_duplicates(subset=[raw_col])
    # pick evenly spaced samples across the dataset
    total = len(sub)
    if total <= n:
        indices = list(range(total))
    else:
        indices = np.linspace(0, total - 1, n, dtype=int)
    samples = []
    for idx in indices:
        row = sub.iloc[idx]
        t = str(row[raw_col]).replace('\r', ' ').replace('\n', ' ').strip()
        samples.append(t)
    return samples

def find_borderline_cases(df, raw_col, label_col):
    sub = df.dropna(subset=[raw_col]).drop_duplicates(subset=[raw_col]).copy()
    sub["text_str"] = sub[raw_col].astype(str)
    
    # Borderline 0: contains keywords like 'judi', 'slot', 'bandar', 'zeus', 'tikus', 'polisi', 'korban' but labeled 0
    kw_judi = r'judi|judol|slot|bandar|zeus|taruhan|hoki|depo|wd|scatter|pragmatic'
    b0 = sub[(sub[label_col] == 0) & (sub["text_str"].str.contains(kw_judi, case=False, regex=True))]
    b0_samples = b0["text_str"].head(10).tolist()
    
    # Borderline 1: labeled 1, but doesn't explicitly have clear gambling words or looks like normal comment / stealth spam
    # or very short
    b1_short = sub[(sub[label_col] == 1) & (sub["text_str"].str.len() < 30)]
    b1_samples = b1_short["text_str"].head(10).tolist()
    
    return {
        "borderline_label_0": b0_samples,
        "borderline_label_1": b1_samples
    }

results = {}
for item in DATASETS:
    df = pd.read_csv(item["file"])
    r_col = item["raw_col"]
    l_col = item["label_col"]
    
    s0 = get_samples(df, r_col, l_col, 0, n=25)
    s1 = get_samples(df, r_col, l_col, 1, n=25)
    bl = find_borderline_cases(df, r_col, l_col)
    
    # Check what preprocessing does if clean_col exists
    clean_diff_sample = []
    if item["clean_col"] and item["clean_col"] in df.columns:
        valid_pairs = df.dropna(subset=[r_col, item["clean_col"]]).head(5)
        for _, row in valid_pairs.iterrows():
            clean_diff_sample.append({
                "raw": str(row[r_col])[:120],
                "clean": str(row[item["clean_col"]])[:120]
            })
            
    # Check top duplicate texts in dataset
    top_dups = df[r_col].value_counts().head(5).to_dict()
    
    results[item["id"]] = {
        "samples_0": s0,
        "samples_1": s1,
        "borderline": bl,
        "clean_diff": clean_diff_sample,
        "top_duplicates": top_dups
    }

with open("datasets_samples_and_edge_cases.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Saved samples and edge cases successfully.")
