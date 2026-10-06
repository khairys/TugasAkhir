# FINAL AUDIT SUMMARY
## Dataset Harmonization, Cleaning, and Quality Control Summary

### 1. Dataset Overview
```text
Raw records: 84,004
Canonical unique records: 48,051
Accepted: 83,996
Review: 6
Invalid: 2
Excluded: 2
```

### 2. Label Distribution (Canonical Unique Dataset)
```text
Promotion (1): 7,999 (16.65%)
Non-Promotion (0): 40,052 (83.35%)
```

### 3. Source Contribution (Canonical Unique Records)
```text
DS1_fahruu: 6,602 (13.74%)
DS2_kyyyy8_all: 23,894 (49.73%)
DS3_yaemico: 2,718 (5.66%)
DS4_kyyyy8_platform: 10,656 (22.18%)
DS5_ferdiansakti: 4,181 (8.7%)
```

### 4. Leakage Risk Groups
```text
Exact duplicate families (EDG): 48,054
Whitespace duplicate families (WDG): 48,041
Normalized variant families (NVG): 47,645
Near-duplicate template families (NDG): 46,469
Author groups: 18,968
Cross-source duplicate records: 38,651
Adjudicated label conflicts: 181 records (51 unique texts)
```

### 5. Major Findings
1. **Kyyyy8 Lineage Duplication**: DS2 (45.5k) dan DS4 (18.9k) memiliki 10.561 teks yang identik persis. Metadata lengkap dari DS4 (`comment_id`, `author`, `time_parsed`) berhasil diprioritaskan sebagai rekaman kanonikal.
2. **Label Conflict Resolution**: 51 teks unik berkonflik (181 rekaman) berhasil diselesaikan berdasarkan definisi penelitian. Komentar esports (Miya, Pascol, RRQ vs ONIC) yang salah dilabeli 1 di DS4 berhasil dikoreksi ke 0, promosi situs berhasil dikoreksi ke 1, dan 3 teks ambigu dialihkan ke `label_review_queue.csv`.
3. **Extreme Bot Burst in Live Chat (DS3)**: 57% pesan di DS3 adalah duplikat persis (`WISDOMTOTO` 931x). Seluruh teks dipertahankan secara kanonikal unik dan ditandai sebagai `OOD_candidate`.
4. **Campaign Bias in DS5**: 74.8% rekaman didominasi sindikat `ambil4d`. Laporan konsentrasi kampanye berhasil memetakan frekuensi entitas ini secara presisi.
5. **Obfuscation Integrity**: Sinyal teks mentah (font unicode matematika `𝗔𝗟𝗘𝗫𝗜𝗦`, spasi sengaja `T O K E 6 9`, tanda baca, timestamp YouTube) berhasil dipertahankan 100% tanpa distorsi normalisasi.

### 6. Recommendations for Downstream Phases
```text
Training candidate: DS1_fahruu (Core) + DS2/DS4 (Unified Kyyyy8 deduplicated unique)
Validation candidate: Stratified split dari pool utama menggunakan GroupKFold(near_duplicate_group)
Normal test candidate: Held-out test set terkelompok (GroupKFold bebas leakage template & author)
OOD candidate: DS3_yaemico (Live Chat CCTV Jogja domain shift)
Auxiliary candidate: DS5_ferdiansakti (khusus pengujian robustness terhadap nama entitas dominan)
Remaining review: 6 rekaman (3 teks unik) di data/review/label_review_queue.csv
```
