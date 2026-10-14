#!/usr/bin/env python3
"""Rebuild frozen Stage 11 DS3 OOD and DS5 external candidate sets."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed" / "stage11"
MANIFEST = OUT / "manifest_v1.json"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def build(raw_path: Path, exclusion_path: Path, text_col: str, label_col: str,
          prefix: str, source_name: str):
    raw = pd.read_csv(raw_path, encoding="utf-8")
    if text_col not in raw or label_col not in raw:
        raise ValueError(f"Missing required columns in {raw_path}")
    raw = raw.copy()
    raw["source_row_id"] = range(1, len(raw) + 1)
    raw["record_id"] = raw["source_row_id"].map(lambda n: f"{prefix}_{n:06d}")
    raw["text_raw"] = raw[text_col]
    raw["canonical_label"] = pd.to_numeric(raw[label_col], errors="coerce")
    raw = raw[raw["text_raw"].map(lambda x: isinstance(x, str) and bool(x.strip())) &
              raw["canonical_label"].isin([0, 1])].copy()
    raw = raw.drop_duplicates(subset=["text_raw"], keep="first")
    exclusion = pd.read_csv(exclusion_path, encoding="utf-8")
    excluded_ids = set(exclusion["record_id"].dropna().astype(str))
    unique_before = len(raw)
    raw = raw[~raw["record_id"].isin(excluded_ids)].copy()
    raw["source_dataset"] = source_name
    raw["canonical_label"] = raw["canonical_label"].astype(int)
    out = raw[["record_id", "source_dataset", "source_row_id", "text_raw", "canonical_label"]].reset_index(drop=True)
    audit = {"raw_rows": int(len(pd.read_csv(raw_path, encoding="utf-8")),
              "unique_valid_before_overlap_removal": int(unique_before),
              "excluded_overlap_ids": len(excluded_ids), "rows": len(out),
              "non_promotion": int((out.canonical_label == 0).sum()),
              "promotion": int((out.canonical_label == 1).sum())}
    return out, audit

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    d3, a3 = build(ROOT/"data/raw/ds3_yaemico/youtube_chat_jogja_clean.csv",
                   ROOT/"data/audit/ood_ds3_overlap_examples_v2.csv",
                   "message", "label", "DS3", "DS3_yaemico")
    d5, a5 = build(ROOT/"data/raw/ds5_ferdiansakti/rawdata.csv",
                   ROOT/"data/audit/ds5_overlap_examples_v2.csv",
                   "Comments", "Label", "DS5", "DS5_ferdiansakti")
    expected = {"ds3": (2689, 2653, 36), "ds5": (3999, 1167, 2832)}
    actual = {"ds3": (len(d3), int((d3.canonical_label == 0).sum()), int((d3.canonical_label == 1).sum())),
              "ds5": (len(d5), int((d5.canonical_label == 0).sum()), int((d5.canonical_label == 1).sum()))}
    if actual != expected:
        raise RuntimeError(f"Frozen candidate validation failed; expected {expected}, got {actual}")
    p3, p5 = OUT/"ds3_ood_v1.csv", OUT/"ds5_external_v1.csv"
    d3.to_csv(p3, index=False, encoding="utf-8", lineterminator="\n")
    d5.to_csv(p5, index=False, encoding="utf-8", lineterminator="\n")
    old = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    old["status"] = "PREPARED_NOT_EVALUATED"
    old["sources"] = {
      "ds3_raw_path":"data/raw/ds3_yaemico/youtube_chat_jogja_clean.csv",
      "ds3_raw_sha256":sha256(ROOT/"data/raw/ds3_yaemico/youtube_chat_jogja_clean.csv"),
      "ds3_exclusions_path":"data/audit/ood_ds3_overlap_examples_v2.csv",
      "ds3_exclusions_sha256":sha256(ROOT/"data/audit/ood_ds3_overlap_examples_v2.csv"),
      "ds5_raw_path":"data/raw/ds5_ferdiansakti/rawdata.csv",
      "ds5_raw_sha256":sha256(ROOT/"data/raw/ds5_ferdiansakti/rawdata.csv"),
      "ds5_exclusions_path":"data/audit/ds5_overlap_examples_v2.csv",
      "ds5_exclusions_sha256":sha256(ROOT/"data/audit/ds5_overlap_examples_v2.csv")}
    old["datasets"] = {
      "ds3_ood_v1":{"path":"data/processed/stage11/ds3_ood_v1.csv","sha256":sha256(p3),**a3},
      "ds5_external_v1":{"path":"data/processed/stage11/ds5_external_v1.csv","sha256":sha256(p5),**a5}}
    MANIFEST.write_text(json.dumps(old, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status":old["status"],"actual":actual,"manifest":str(MANIFEST.relative_to(ROOT))},ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
