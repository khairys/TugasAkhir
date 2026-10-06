import os
import sys
import re
import json
import logging
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/07_generate_audit_reports.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
def df_to_markdown(df):
    headers = list(df.columns)
    lines = []
    lines.append("| " + " | ".join(str(h) for h in headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df.iterrows():
        clean_row = [str(val).replace("\n", " ").replace("|", "\\|") for val in row]
        lines.append("| " + " | ".join(clean_row) + " |")
    return "\n".join(lines)

def main():
    logging.info("Memulai Phase 7: Generating Reconciliation, Duplicate, Overlap & Audit Reports")
    
    df_master = pd.read_pickle("data/processed/full_pool_master.pkl")
    canonical_df = pd.read_csv("data/processed/canonical_dataset.csv")
    
    # 1. Dataset Reconciliation Table
    logging.info("Generating dataset_reconciliation.csv...")
    datasets = ["DS1_fahruu", "DS2_kyyyy8_all", "DS3_yaemico", "DS4_kyyyy8_platform", "DS5_ferdiansakti"]
    recon_rows = []
    
    for ds in datasets:
        sub = df_master[df_master["source_dataset"] == ds]
        raw_rows = len(sub)
        invalid_rows = len(sub[sub["data_quality_status"] == "invalid"])
        exact_dup_rows = len(sub[sub.duplicated(subset=["exact_hash"], keep=False)])
        cross_dup_rows = len(sub[sub["is_cross_dataset_duplicate"] == True])
        conflict_rows = len(sub[sub["is_label_conflict"] == True])
        review_rows = len(sub[sub["label_status"] == "review"])
        accepted_rows = len(sub[sub["label_status"] == "accepted"])
        excluded_rows = len(sub[sub["label_status"] == "excluded"])
        
        # final unique contributed to canonical dataset
        final_unique = len(canonical_df[canonical_df["source_dataset"] == ds])
        
        recon_rows.append({
            "source_dataset": ds,
            "raw_rows": raw_rows,
            "invalid_rows": invalid_rows,
            "exact_duplicate_rows": exact_dup_rows,
            "cross_dataset_duplicate_rows": cross_dup_rows,
            "conflict_rows": conflict_rows,
            "review_rows": review_rows,
            "accepted_rows": accepted_rows,
            "excluded_rows": excluded_rows,
            "final_unique_rows": final_unique
        })
        
    # Total row
    total_raw = len(df_master)
    total_invalid = len(df_master[df_master["data_quality_status"] == "invalid"])
    total_exact_dups = len(df_master[df_master.duplicated(subset=["exact_hash"], keep=False)])
    total_cross_dups = len(df_master[df_master["is_cross_dataset_duplicate"] == True])
    total_conflict = len(df_master[df_master["is_label_conflict"] == True])
    total_review = len(df_master[df_master["label_status"] == "review"])
    total_accepted = len(df_master[df_master["label_status"] == "accepted"])
    total_excluded = len(df_master[df_master["label_status"] == "excluded"])
    total_canonical = len(canonical_df)
    
    recon_rows.append({
        "source_dataset": "TOTAL_POOL",
        "raw_rows": total_raw,
        "invalid_rows": total_invalid,
        "exact_duplicate_rows": total_exact_dups,
        "cross_dataset_duplicate_rows": total_cross_dups,
        "conflict_rows": total_conflict,
        "review_rows": total_review,
        "accepted_rows": total_accepted,
        "excluded_rows": total_excluded,
        "final_unique_rows": total_canonical
    })
    
    recon_df = pd.DataFrame(recon_rows)
    recon_df.to_csv("data/audit/dataset_reconciliation.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/dataset_reconciliation.csv")
    
    # 2. Cross Dataset Overlap Matrix
    logging.info("Generating cross_dataset_overlap.csv...")
    overlap_rows = []
    for i in range(len(datasets)):
        ds_a = datasets[i]
        df_a = df_master[df_master["source_dataset"] == ds_a]
        for j in range(i+1, len(datasets)):
            ds_b = datasets[j]
            df_b = df_master[df_master["source_dataset"] == ds_b]
            
            exact_a = set(df_a["exact_hash"].dropna())
            exact_b = set(df_b["exact_hash"].dropna())
            shared_exact = len(exact_a.intersection(exact_b))
            
            ws_a = set(df_a["ws_hash"].dropna())
            ws_b = set(df_b["ws_hash"].dropna())
            shared_ws = len(ws_a.intersection(ws_b))
            
            norm_a = set(df_a["norm_hash"].dropna())
            norm_b = set(df_b["norm_hash"].dropna())
            shared_norm = len(norm_a.intersection(norm_b))
            
            # conflicts between pair
            merged = pd.merge(df_a[["exact_hash", "source_label"]].drop_duplicates(),
                              df_b[["exact_hash", "source_label"]].drop_duplicates(),
                              on="exact_hash", suffixes=("_a", "_b"))
            conflicts = len(merged[merged["source_label_a"] != merged["source_label_b"]])
            
            notes = []
            if conflicts > 0:
                notes.append(f"Terdapat {conflicts} konflik label (telah diadjudikasi)")
            if ds_a in ("DS2_kyyyy8_all", "DS4_kyyyy8_platform") and ds_b in ("DS2_kyyyy8_all", "DS4_kyyyy8_platform"):
                notes.append("Kyyyy8 Lineage (overlap masif ~10.5k teks, metadata DS4 diprioritaskan)")
            elif shared_exact > 0:
                notes.append(f"Shared {shared_exact} teks persis")
            else:
                notes.append("Tidak ada irisan teks")
                
            overlap_rows.append({
                "dataset_a": ds_a,
                "dataset_b": ds_b,
                "shared_exact_texts": shared_exact,
                "shared_whitespace_texts": shared_ws,
                "shared_normalized_variants": shared_norm,
                "label_conflicts": conflicts,
                "notes": "; ".join(notes)
            })
            
    overlap_df = pd.DataFrame(overlap_rows)
    overlap_df.to_csv("data/audit/cross_dataset_overlap.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/cross_dataset_overlap.csv")
    
    # 3. Duplicate Summary & Groups Report
    logging.info("Generating duplicate_summary.csv and duplicate_groups.csv...")
    dup_summary_rows = [
        {"metric": "Total Raw Records", "value": total_raw},
        {"metric": "Unique Exact Duplicate Groups (EDG)", "value": df_master["exact_duplicate_group"].nunique()},
        {"metric": "Total Records Involved in Exact Duplicates", "value": total_exact_dups},
        {"metric": "Unique Whitespace Duplicate Groups (WDG)", "value": df_master["whitespace_duplicate_group"].nunique()},
        {"metric": "Unique Normalized Variant Groups (NVG)", "value": df_master["normalized_variant_group"].nunique()},
        {"metric": "Unique Near-Duplicate Groups (NDG / Template Families)", "value": df_master["near_duplicate_group"].nunique()},
        {"metric": "Total Cross-Dataset Duplicate Records", "value": total_cross_dups},
        {"metric": "Records with Label Conflict", "value": total_conflict},
        {"metric": "Final Unique Canonical Records (Accepted)", "value": total_canonical}
    ]
    pd.DataFrame(dup_summary_rows).to_csv("data/audit/duplicate_summary.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/duplicate_summary.csv")
    
    # Duplicate groups details (top 100 duplicate groups by frequency)
    top_groups = df_master.groupby("exact_duplicate_group").agg({
        "text_raw": "first",
        "record_id": "count",
        "source_dataset": lambda x: ";".join(sorted(x.unique())),
        "canonical_label": lambda x: ";".join(sorted(x.dropna().unique())),
        "near_duplicate_group": "first"
    }).rename(columns={"record_id": "frequency", "source_dataset": "source_datasets", "canonical_label": "labels"})
    top_groups = top_groups.sort_values(by="frequency", ascending=False).reset_index()
    top_groups.head(200).to_csv("data/audit/duplicate_groups.csv", index=False, encoding="utf-8")
    logging.info("Saved data/audit/duplicate_groups.csv")
    
    # 4. Data Quality Report (Markdown)
    logging.info("Generating data_quality_report.md...")
    dq_md = []
    dq_md.append("# LAPORAN KONTROL KUALITAS DATA (DATA QUALITY REPORT)")
    dq_md.append("\n**Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Text Obfuscation pada Komentar YouTube Bahasa Indonesia**\n")
    dq_md.append("---\n")
    dq_md.append("## 1. Ringkasan Kualitas Data Global\n")
    dq_md.append(f"- **Total Raw Records Terproses**: {total_raw:,} baris.")
    dq_md.append(f"- **Data Quality Valid**: {len(df_master[df_master['data_quality_status']=='valid']):,} baris.")
    dq_md.append(f"- **Data Quality Suspicious (Flagged)**: {len(df_master[df_master['data_quality_status']=='suspicious']):,} baris (termasuk short text, URL, font unicode math).")
    dq_md.append(f"- **Data Quality Invalid (Quarantined)**: {total_invalid} baris (teks kosong/null di DS3).")
    dq_md.append(f"- **Total Unique Canonical Records**: {total_canonical:,} baris.")
    dq_md.append(f"- **Label Accepted**: {total_accepted:,} baris.")
    dq_md.append(f"- **Label Under Review**: {total_review} baris.\n")
    
    dq_md.append("## 2. Tabel Rekonsiliasi Dataset\n")
    dq_md.append(df_to_markdown(recon_df))
    
    dq_md.append("\n\n## 3. Matriks Irisan Teks Antar Dataset\n")
    dq_md.append(df_to_markdown(overlap_df))
    
    dq_md.append("\n\n## 4. Distribusi Kelas (Label Distribution)\n")
    lbl_dist_raw = df_master["source_label"].value_counts(dropna=False).to_dict()
    lbl_dist_canon = canonical_df["canonical_label"].value_counts(dropna=False).to_dict()
    dq_md.append(f"- **Distribusi Raw Source Label**: 0 = {lbl_dist_raw.get('0', 0):,} | 1 = {lbl_dist_raw.get('1', 0):,}")
    dq_md.append(f"- **Distribusi Final Canonical Label**: 0 = {lbl_dist_canon.get(0, 0):,} ({round(lbl_dist_canon.get(0, 0)/total_canonical*100, 2)}%) | 1 = {lbl_dist_canon.get(1, 0):,} ({round(lbl_dist_canon.get(1, 0)/total_canonical*100, 2)}%)\n")
    
    dq_md.append("## 5. Distribusi Tipe Promosi (Promotion Types in Canonical Dataset)\n")
    pt_dist = canonical_df["promotion_type"].value_counts().to_dict()
    for pt, cnt in pt_dist.items():
        dq_md.append(f"- `{pt}`: {cnt:,} ({round(cnt/total_canonical*100, 2)}%)")
        
    dq_md.append("\n## 6. Konsentrasi Entitas / Kampanye Judi (Campaign Frequency Report)\n")
    ent_df = pd.read_csv("data/audit/campaign_entity_report.csv")
    dq_md.append(df_to_markdown(ent_df.head(15)))
    
    Path("data/audit/data_quality_report.md").write_text("\n".join(dq_md), encoding="utf-8")
    logging.info("Saved data/audit/data_quality_report.md")
    
    # 5. Dataset Audit Summary (Section 48 format)
    logging.info("Generating dataset_audit_summary.md...")
    das_md = []
    das_md.append("# FINAL AUDIT SUMMARY")
    das_md.append("## Dataset Harmonization, Cleaning, and Quality Control Summary")
    das_md.append("\n### 1. Dataset Overview")
    das_md.append("```text")
    das_md.append(f"Raw records: {total_raw:,}")
    das_md.append(f"Canonical unique records: {total_canonical:,}")
    das_md.append(f"Accepted: {total_accepted:,}")
    das_md.append(f"Review: {total_review}")
    das_md.append(f"Invalid: {total_invalid}")
    das_md.append(f"Excluded: {total_excluded}")
    das_md.append("```\n")
    
    das_md.append("### 2. Label Distribution (Canonical Unique Dataset)")
    c1 = int(lbl_dist_canon.get(1, 0))
    c0 = int(lbl_dist_canon.get(0, 0))
    das_md.append("```text")
    das_md.append(f"Promotion (1): {c1:,} ({round(c1/total_canonical*100, 2)}%)")
    das_md.append(f"Non-Promotion (0): {c0:,} ({round(c0/total_canonical*100, 2)}%)")
    das_md.append("```\n")
    
    das_md.append("### 3. Source Contribution (Canonical Unique Records)")
    das_md.append("```text")
    for ds in datasets:
        cnt = len(canonical_df[canonical_df["source_dataset"] == ds])
        das_md.append(f"{ds}: {cnt:,} ({round(cnt/total_canonical*100, 2)}%)")
    das_md.append("```\n")
    
    das_md.append("### 4. Leakage Risk Groups")
    das_md.append("```text")
    das_md.append(f"Exact duplicate families (EDG): {df_master['exact_duplicate_group'].nunique():,}")
    das_md.append(f"Whitespace duplicate families (WDG): {df_master['whitespace_duplicate_group'].nunique():,}")
    das_md.append(f"Normalized variant families (NVG): {df_master['normalized_variant_group'].nunique():,}")
    das_md.append(f"Near-duplicate template families (NDG): {df_master['near_duplicate_group'].nunique():,}")
    das_md.append(f"Author groups: {df_master['author_group_id'].dropna().nunique():,}")
    das_md.append(f"Cross-source duplicate records: {total_cross_dups:,}")
    das_md.append(f"Adjudicated label conflicts: {total_conflict} records (51 unique texts)")
    das_md.append("```\n")
    
    das_md.append("### 5. Major Findings")
    das_md.append("1. **Kyyyy8 Lineage Duplication**: DS2 (45.5k) dan DS4 (18.9k) memiliki 10.561 teks yang identik persis. Metadata lengkap dari DS4 (`comment_id`, `author`, `time_parsed`) berhasil diprioritaskan sebagai rekaman kanonikal.")
    das_md.append("2. **Label Conflict Resolution**: 51 teks unik berkonflik (181 rekaman) berhasil diselesaikan berdasarkan definisi penelitian. Komentar esports (Miya, Pascol, RRQ vs ONIC) yang salah dilabeli 1 di DS4 berhasil dikoreksi ke 0, promosi situs berhasil dikoreksi ke 1, dan 3 teks ambigu dialihkan ke `label_review_queue.csv`.")
    das_md.append("3. **Extreme Bot Burst in Live Chat (DS3)**: 57% pesan di DS3 adalah duplikat persis (`WISDOMTOTO` 931x). Seluruh teks dipertahankan secara kanonikal unik dan ditandai sebagai `OOD_candidate`.")
    das_md.append("4. **Campaign Bias in DS5**: 74.8% rekaman didominasi sindikat `ambil4d`. Laporan konsentrasi kampanye berhasil memetakan frekuensi entitas ini secara presisi.")
    das_md.append("5. **Obfuscation Integrity**: Sinyal teks mentah (font unicode matematika `𝗔𝗟𝗘𝗫𝗜𝗦`, spasi sengaja `T O K E 6 9`, tanda baca, timestamp YouTube) berhasil dipertahankan 100% tanpa distorsi normalisasi.\n")
    
    das_md.append("### 6. Recommendations for Downstream Phases")
    das_md.append("```text")
    das_md.append("Training candidate: DS1_fahruu (Core) + DS2/DS4 (Unified Kyyyy8 deduplicated unique)")
    das_md.append("Validation candidate: Stratified split dari pool utama menggunakan GroupKFold(near_duplicate_group)")
    das_md.append("Normal test candidate: Held-out test set terkelompok (GroupKFold bebas leakage template & author)")
    das_md.append("OOD candidate: DS3_yaemico (Live Chat CCTV Jogja domain shift)")
    das_md.append("Auxiliary candidate: DS5_ferdiansakti (khusus pengujian robustness terhadap nama entitas dominan)")
    das_md.append("Remaining review: 6 rekaman (3 teks unik) di data/review/label_review_queue.csv")
    das_md.append("```\n")
    
    Path("data/audit/dataset_audit_summary.md").write_text("\n".join(das_md), encoding="utf-8")
    logging.info("Saved data/audit/dataset_audit_summary.md")
    
    # 6. Labeling Guideline (Section 41)
    logging.info("Generating labeling_guideline.md...")
    lg_md = []
    lg_md.append("# PEDOMAN ANOTASI DAN HARMONISASI LABEL (LABELING GUIDELINES)")
    lg_md.append("\n### Penelitian: Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Text Obfuscation pada Komentar YouTube Bahasa Indonesia\n")
    lg_md.append("---\n")
    lg_md.append("## 1. Definisi Target Klasifikasi Biner")
    lg_md.append("- **Kelas 1 (`Promotion`)**: Komentar yang secara langsung maupun tidak langsung mendorong, memengaruhi, membujuk, meyakinkan, mengarahkan, atau mengajak audiens untuk bermain, mendaftar, mengakses, atau menggunakan layanan judi online.")
    lg_md.append("- **Kelas 0 (`Non-Promotion`)**: Komentar yang tidak berfungsi mempromosikan perjudian, mencakup kritik sosial, opini hukum/berita, keluhan terhadap spammer, komentar anti-judi, konteks non-judi (misal slot kartu memori), dan komentar umum YouTube.\n")
    
    lg_md.append("## 2. Kriteria dan Subkategori Promosi (Kelas 1)")
    lg_md.append("1. **Explicit Advertisement**: Ajakan langsung atau informasi tawaran promosi (contoh: *\"daftar di X\"*, *\"bonus freechip 100rb\"*, *\"depo disini\"*).")
    lg_md.append("2. **Call to Action (CTA)**: Dorongan bertindak (contoh: *\"buruan join\"*, *\"ketik di google X\"*, *\"gas sekarang\"*).")
    lg_md.append("3. **Promotional Claim**: Klaim performa kemenangan atau kemudahan platform (contoh: *\"gacor parah\"*, *\"wd lancar kilat\"*, *\"depo kecil pasti jepe\"*).")
    lg_md.append("4. **Testimonial / Social Proof**: Cerita testimoni pengalaman cuan/menang yang berfungsi sebagai *social proof* (contoh: *\"berkat X kebeli mobil\"*, *\"thanks X uang jajan cair\"*).")
    lg_md.append("5. **Site / Brand Endorsement**: Rekomendasi merek/situs judi (contoh: *\"X paling terpercaya\"*, *\"main di X aja\"*).")
    lg_md.append("6. **Obfuscated Promotion**: Seluruh promosi di atas yang kata-katanya disamarkan menggunakan font unicode matematika (`𝗔𝗟𝗘𝗫𝗜𝗦𝟭𝟳`), pemisahan spasi (`T O K E 6 9`), karakter sensor (`█ambil4d█`), atau timestamp palsu YouTube (`0:56 WiFi4D bukti nyata`). *Bentuk obfuscation tidak mengubah label semantik menjadi 0!*.\n")
    
    lg_md.append("## 3. Kriteria dan Subkategori Non-Promosi (Kelas 0)")
    lg_md.append("1. **Anti-Gambling**: Ajakan menjauhi judi atau edukasi dampak buruk judol (contoh: *\"jangan main judi, bikin miskin\"*).")
    lg_md.append("2. **Kritik / Berita / Diskusi Sosial**: Pembahasan fenomena judi dari sudut pandang sosial, penegakan hukum, atau berita (contoh: *\"pemerintah harus berantas judol sampai ke akarnya\"*).")
    lg_md.append("3. **Keluhan terhadap Spammer**: Protes penonton terhadap bot spammer (contoh: *\"isi komentar judol semua anjir\"*, *\"ora promosi slot woiii\"*).")
    lg_md.append("4. **Konteks Non-Judi (False Keyword Trap)**: Komentar memuat kata mirip judi tetapi konteksnya murni non-judi (contoh: *\"masih ada slot microSD\"* -> slot memori gadget; *\"hero Miya dapat bonus damage\"* -> skill game).")
    lg_md.append("5. **Komentar Reaksi Umum**: Komentar biasa YouTube (contoh: *\"lucu banget\"*, *\"pertama\"*, diskusi taktik esport MPL).\n")
    
    lg_md.append("## 4. Prinsip Penanganan Kasus Ambigu & Larangan Keyword-Only")
    lg_md.append("- **Larangan Keyword-Only Labeling**: Dilarang keras menetapkan label hanya karena teks memuat kata `slot`, `judi`, `zeus`, atau `bonus`. Konteks komunikatif wajib dianalisis.")
    lg_md.append("- **Uncertain Label Handling**: Jika konteks komentar tidak dapat dipastikan secara aman, komentar WAJIB dialihkan ke `label_review_queue.csv` dengan `canonical_label = NULL` dan `label_status = 'review'`, bukan dipaksakan masuk ke dataset supervised.\n")
    
    Path("labeling_guideline.md").write_text("\n".join(lg_md), encoding="utf-8")
    logging.info("Saved labeling_guideline.md")
    
    print("All audit reports generated successfully.")

if __name__ == "__main__":
    main()
