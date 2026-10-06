import os
import sys
import re
import json
import unicodedata
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
        "name": "kyyyy8/dataset-komentar-judi-online-di-youtube (dataset.csv)",
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

def has_unicode_math_or_special(text):
    if not isinstance(text, str): return False
    for char in text:
        # Check if character is mathematical alphanumeric symbols or unusual symbols
        cp = ord(char)
        if (0x1D400 <= cp <= 0x1D7FF) or (0x2460 <= cp <= 0x24FF) or (0x2100 <= cp <= 0x214F):
            return True
    return False

def has_emoji(text):
    if not isinstance(text, str): return False
    for char in text:
        cat = unicodedata.category(char)
        # So: Symbol other (most emojis), or specific ranges
        if cat in ('So', 'Sk') or ord(char) > 0x1F000:
            return True
    return False

def text_stats(df, raw_col):
    s = df[raw_col].fillna("").astype(str)
    
    char_lens = s.apply(len)
    word_lens = s.apply(lambda x: len(x.split()))
    
    url_pattern = re.compile(r'https?://|www\.|\.com|\.id|\.net|\.xyz|\.vip|\.link|\.top|\.club|\.online', re.IGNORECASE)
    has_url = s.apply(lambda x: bool(url_pattern.search(x)))
    
    has_digits = s.apply(lambda x: bool(re.search(r'\d', x)))
    has_emojis = s.apply(has_emoji)
    has_special_unicode = s.apply(has_unicode_math_or_special)
    
    # whitespace anomaly: multiple spaces, newline, carriage return, non-breaking space
    whitespace_anomaly = s.apply(lambda x: bool(re.search(r'[\r\n\t]| {2,}|\u00a0|\u200b', x)))
    
    # symbols / punctuation heavy (> 10% characters are non-alphanumeric and non-space)
    def is_symbol_heavy(x):
        if not x: return False
        syms = sum(1 for c in x if not c.isalnum() and not c.isspace())
        return (syms / len(x)) > 0.15
    symbol_heavy = s.apply(is_symbol_heavy)
    
    return {
        "char_len": {
            "min": int(char_lens.min()),
            "max": int(char_lens.max()),
            "mean": round(float(char_lens.mean()), 2),
            "median": float(char_lens.median()),
            "std": round(float(char_lens.std()), 2)
        },
        "word_len": {
            "min": int(word_lens.min()),
            "max": int(word_lens.max()),
            "mean": round(float(word_lens.mean()), 2),
            "median": float(word_lens.median()),
            "std": round(float(word_lens.std()), 2)
        },
        "has_url": {"count": int(has_url.sum()), "pct": round(float(has_url.mean()*100), 2)},
        "has_digits": {"count": int(has_digits.sum()), "pct": round(float(has_digits.mean()*100), 2)},
        "has_emojis": {"count": int(has_emojis.sum()), "pct": round(float(has_emojis.mean()*100), 2)},
        "has_special_unicode": {"count": int(has_special_unicode.sum()), "pct": round(float(has_special_unicode.mean()*100), 2)},
        "whitespace_anomaly": {"count": int(whitespace_anomaly.sum()), "pct": round(float(whitespace_anomaly.mean()*100), 2)},
        "symbol_heavy": {"count": int(symbol_heavy.sum()), "pct": round(float(symbol_heavy.mean()*100), 2)},
    }

def main():
    dfs = {}
    analysis = {}
    
    for item in DATASETS:
        ds_id = item["id"]
        df = pd.read_csv(item["file"])
        dfs[ds_id] = df
        
        raw_col = item["raw_col"]
        clean_col = item["clean_col"]
        label_col = item["label_col"]
        
        # basic info
        n_rows, n_cols = df.shape
        col_names = df.columns.tolist()
        col_dtypes = {c: str(df[c].dtype) for c in col_names}
        missing_per_col = df.isnull().sum().to_dict()
        exact_dups = int(df.duplicated().sum())
        text_dups = int(df.duplicated(subset=[raw_col]).sum())
        
        # label distribution
        label_dist = df[label_col].value_counts(dropna=False).to_dict()
        label_dist_pct = (df[label_col].value_counts(normalize=True, dropna=False)*100).round(2).to_dict()
        
        # text characteristics
        stats = text_stats(df, raw_col)
        
        analysis[ds_id] = {
            "name": item["name"],
            "file": item["file"],
            "rows": n_rows,
            "cols": n_cols,
            "col_names": col_names,
            "col_dtypes": col_dtypes,
            "missing": missing_per_col,
            "exact_duplicates": exact_dups,
            "text_duplicates": text_dups,
            "raw_col": raw_col,
            "clean_col": clean_col,
            "label_col": label_col,
            "label_dist": {str(k): int(v) for k, v in label_dist.items()},
            "label_dist_pct": {str(k): float(v) for k, v in label_dist_pct.items()},
            "stats": stats
        }
    
    # Cross dataset overlap
    overlap = {}
    for i in range(len(DATASETS)):
        id_i = DATASETS[i]["id"]
        col_i = DATASETS[i]["raw_col"]
        df_i = dfs[id_i]
        # clean stripped lowercase text set
        s_i = df_i[[col_i, DATASETS[i]["label_col"]]].dropna().copy()
        s_i["norm_text"] = s_i[col_i].astype(str).str.strip().str.lower()
        s_i["label_val"] = s_i[DATASETS[i]["label_col"]]
        s_i = s_i[["norm_text", "label_val"]].drop_duplicates()
        
        for j in range(i+1, len(DATASETS)):
            id_j = DATASETS[j]["id"]
            col_j = DATASETS[j]["raw_col"]
            df_j = dfs[id_j]
            s_j = df_j[[col_j, DATASETS[j]["label_col"]]].dropna().copy()
            s_j["norm_text"] = s_j[col_j].astype(str).str.strip().str.lower()
            s_j["label_val"] = s_j[DATASETS[j]["label_col"]]
            s_j = s_j[["norm_text", "label_val"]].drop_duplicates()
            
            merged = pd.merge(s_i, s_j, on="norm_text", suffixes=("_i", "_j"))
            n_shared = len(merged["norm_text"].unique())
            
            # check label conflict
            conflicts = merged[merged["label_val_i"] != merged["label_val_j"]]
            n_conflicts = len(conflicts["norm_text"].unique())
            
            key = f"{id_i} vs {id_j}"
            overlap[key] = {
                "shared_unique_texts": n_shared,
                "label_conflicts": n_conflicts,
                "conflict_samples": conflicts[["norm_text", "label_val_i", "label_val_j"]].drop_duplicates("norm_text").head(5).to_dict(orient="records")
            }
            
    with open("datasets_analysis_summary.json", "w", encoding="utf-8") as f:
        json.dump({"datasets": analysis, "overlap": overlap}, f, indent=2, ensure_ascii=False)
    print("Analysis saved to datasets_analysis_summary.json")

if __name__ == "__main__":
    main()
