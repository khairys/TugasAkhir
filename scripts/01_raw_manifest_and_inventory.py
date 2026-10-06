import os
import sys
import shutil
import hashlib
import logging
from pathlib import Path
import pandas as pd

# Setup logging
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/01_raw_manifest.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

RAW_SOURCES = [
    {
        "source_id": "DS1_fahruu",
        "source_name": "fahruu/komentar-judi-online",
        "src_path": "datasets/fahruu_komentar-judi-online/judi_online.csv",
        "dest_dir": "data/raw/ds1_fahruu",
        "filename": "judi_online.csv",
        "raw_text_col": "comment",
        "label_col": "label",
        "notes": "Dataset YouTube investigasi judol (Ferry Irwandi, Gunawan Sadbor, Budi Arie)"
    },
    {
        "source_id": "DS2_kyyyy8_all",
        "source_name": "kyyyy8/dataset-komentar-judi-online-di-youtube",
        "src_path": "datasets/kyyyy8_dataset-komentar-judi-online-di-youtube/dataset.csv",
        "dest_dir": "data/raw/ds2_kyyyy8_all",
        "filename": "dataset.csv",
        "raw_text_col": "text",
        "label_col": "label",
        "notes": "Dataset komentar YouTube skala besar (esports MPL, gadget, video umum)"
    },
    {
        "source_id": "DS3_yaemico",
        "source_name": "yaemico/deteksi-judi-online",
        "src_path": "datasets/yaemico_deteksi-judi-online/youtube_chat_jogja_clean.csv",
        "dest_dir": "data/raw/ds3_yaemico",
        "filename": "youtube_chat_jogja_clean.csv",
        "raw_text_col": "message",
        "label_col": "label",
        "notes": "Live chat YouTube CCTV Jogja, burst spamming ekstrem"
    },
    {
        "source_id": "DS4_kyyyy8_platform",
        "source_name": "kyyyy8/dataset-komentar-judi-online-platform-youtube",
        "src_path": "datasets/kyyyy8_dataset-komentar-judi-online-platform-youtube/dataset_komentarJudol_preprocessed_nonAnom.csv",
        "dest_dir": "data/raw/ds4_kyyyy8_platform",
        "filename": "dataset_komentarJudol_preprocessed_nonAnom.csv",
        "raw_text_col": "text",
        "label_col": "label",
        "notes": "Dataset YouTube dengan metadata resmi (comment_id, author, time_parsed)"
    },
    {
        "source_id": "DS5_ferdiansakti",
        "source_name": "ferdiansakti/gambling-comments-from-youtube-platform",
        "src_path": "datasets/ferdiansakti_gambling-comments-from-youtube-platform/rawdata.csv",
        "dest_dir": "data/raw/ds5_ferdiansakti",
        "filename": "rawdata.csv",
        "raw_text_col": "Comments",
        "label_col": "Label",
        "notes": "Dataset YouTube invasi kampanye bot ambil4d (imbalanced 74.8% judol)"
    }
]

def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()

def main():
    logging.info("Memulai Phase 1: Raw Data Immutability & Inventory Setup")
    manifest_rows = []
    inventory_rows = []

    for item in RAW_SOURCES:
        src = Path(item["src_path"])
        dest_dir = Path(item["dest_dir"])
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / item["filename"]

        if not src.exists():
            logging.error(f"File sumber tidak ditemukan: {src}")
            continue

        # Copy to data/raw preserving metadata
        shutil.copy2(src, dest)
        checksum = compute_sha256(dest)
        file_size_bytes = dest.stat().st_size

        # Read CSV to check rows, columns, dtypes
        df = pd.read_csv(dest)
        n_rows, n_cols = df.shape
        col_names = ";".join(df.columns.tolist())
        col_dtypes = ";".join([f"{c}:{df[c].dtype}" for c in df.columns])

        logging.info(f"[{item['source_id']}] File: {item['filename']} | Rows: {n_rows:,} | Cols: {n_cols} | SHA256: {checksum[:12]}...")

        manifest_rows.append({
            "source_id": item["source_id"],
            "dataset_name": item["source_name"],
            "original_path": str(src),
            "raw_storage_path": str(dest),
            "filename": item["filename"],
            "file_size_bytes": file_size_bytes,
            "sha256_checksum": checksum,
            "encoding": "utf-8",
            "row_count": n_rows,
            "column_count": n_cols
        })

        inventory_rows.append({
            "source_id": item["source_id"],
            "dataset_name": item["source_name"],
            "raw_file": str(dest),
            "row_count": n_rows,
            "column_count": n_cols,
            "column_names": col_names,
            "column_dtypes": col_dtypes,
            "raw_text_column": item["raw_text_col"],
            "source_label_column": item["label_col"],
            "notes": item["notes"]
        })

    # Save manifests
    manifest_df = pd.DataFrame(manifest_rows)
    manifest_df.to_csv("data/manifests/raw_file_manifest.csv", index=False, encoding="utf-8")
    logging.info("Saved data/manifests/raw_file_manifest.csv")

    inventory_df = pd.DataFrame(inventory_rows)
    inventory_df.to_csv("data/audit/dataset_inventory.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/dataset_inventory.csv")

    total_rows = manifest_df["row_count"].sum()
    logging.info(f"Total Raw Records across all 5 datasets: {total_rows:,} rows.")

if __name__ == "__main__":
    main()
