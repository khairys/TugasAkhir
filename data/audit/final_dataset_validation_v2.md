# FINAL DATASET VALIDATION REPORT v2

**Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Text Obfuscation pada Komentar YouTube Bahasa Indonesia**

- **Pipeline Version**: `dataset_finalization_v2`
- **Random Seed**: 42
- **Python Version**: `3.13.0`
- **Pandas Version**: `3.0.5`
- **NumPy Version**: `2.5.3`

---

## A. Raw Integrity
Status: **PASS (100% Immutable)**

| source_dataset | path | expected_sha256 | actual_sha256 | status |
| --- | --- | --- | --- | --- |
| DS1_fahruu | data\raw\ds1_fahruu\judi_online.csv | 07e21ed85abeb668c9e9b89d7713f82354d02dd20ea32130584d3d9cd12a1d47 | 07e21ed85abeb668c9e9b89d7713f82354d02dd20ea32130584d3d9cd12a1d47 | PASS |
| DS2_kyyyy8_all | data\raw\ds2_kyyyy8_all\dataset.csv | a803346ea31c568e0fa678ef174ed997d4e867269b39901941081da0ac2c9711 | a803346ea31c568e0fa678ef174ed997d4e867269b39901941081da0ac2c9711 | PASS |
| DS3_yaemico | data\raw\ds3_yaemico\youtube_chat_jogja_clean.csv | b78e53a421d22a8221c40e76124edff5d27707b6620f81d86ec4ad1c8f5956e4 | b78e53a421d22a8221c40e76124edff5d27707b6620f81d86ec4ad1c8f5956e4 | PASS |
| DS4_kyyyy8_platform | data\raw\ds4_kyyyy8_platform\dataset_komentarJudol_preprocessed_nonAnom.csv | 83a82339957b94bb96c1379ac5d1defed1fe8509ec5deff0cb75800a62229696 | 83a82339957b94bb96c1379ac5d1defed1fe8509ec5deff0cb75800a62229696 | PASS |
| DS5_ferdiansakti | data\raw\ds5_ferdiansakti\rawdata.csv | 8e31db1a338cfb7ac1df69b67149af0a28796908691718ca6e1b7ce581412529 | 8e31db1a338cfb7ac1df69b67149af0a28796908691718ca6e1b7ce581412529 | PASS |


## B. Reconciliation
| source_dataset | raw_rows | invalid_rows | exact_duplicate_rows | cross_dataset_duplicate_rows | conflict_rows | review_rows | accepted_rows | excluded_rows | final_unique_canonical_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS1_fahruu | 8440 | 0 | 2443 | 0 | 0 | 0 | 8440 | 0 | 6602 |
| DS2_kyyyy8_all | 45592 | 0 | 13473 | 0 | 0 | 3 | 45589 | 0 | 23894 |
| DS3_yaemico | 6350 | 2 | 3746 | 0 | 0 | 0 | 6348 | 2 | 2718 |
| DS4_kyyyy8_platform | 18902 | 0 | 9889 | 0 | 0 | 3 | 18899 | 0 | 10656 |
| DS5_ferdiansakti | 4720 | 0 | 797 | 0 | 0 | 0 | 4720 | 0 | 4181 |
| TOTAL_POOL | 84004 | 2 | 48405 | 0 | 0 | 6 | 83996 | 2 | 48051 |


## C. Pairwise Overlap (All 10 Pairs)
| dataset_a | dataset_b | shared_exact_groups | shared_whitespace_groups | shared_normalized_groups | shared_alnum_groups | unique_ws_hashes_shared | unique_norm_hashes_shared | unique_alnum_hashes_shared | pair_label_conflicts | monotonicity_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS1_fahruu | DS2_kyyyy8_all | 51 | 51 | 83 | 173 | 51 | 57 | 64 | 0 | PASS | Shared 51 teks persis |
| DS1_fahruu | DS3_yaemico | 6 | 6 | 16 | 26 | 6 | 9 | 12 | 0 | PASS | Shared 6 teks persis |
| DS1_fahruu | DS4_kyyyy8_platform | 25 | 25 | 46 | 105 | 25 | 31 | 42 | 0 | PASS | Shared 25 teks persis |
| DS1_fahruu | DS5_ferdiansakti | 14 | 14 | 18 | 44 | 14 | 15 | 25 | 0 | PASS | Shared 14 teks persis |
| DS2_kyyyy8_all | DS3_yaemico | 25 | 25 | 77 | 130 | 25 | 41 | 47 | 0 | PASS | Shared 25 teks persis |
| DS2_kyyyy8_all | DS4_kyyyy8_platform | 10659 | 10660 | 10716 | 10721 | 10658 | 10539 | 10046 | 45 | PASS | Kyyyy8 Lineage (overlap masif 10,659 teks, 45 konflik label) |
| DS2_kyyyy8_all | DS5_ferdiansakti | 9 | 9 | 18 | 363 | 9 | 9 | 126 | 0 | PASS | Shared 9 teks persis |
| DS3_yaemico | DS4_kyyyy8_platform | 10 | 10 | 28 | 51 | 10 | 16 | 20 | 0 | PASS | Shared 10 teks persis |
| DS3_yaemico | DS5_ferdiansakti | 0 | 0 | 4 | 5 | 0 | 2 | 2 | 0 | PASS | Tidak ada irisan teks persis |
| DS4_kyyyy8_platform | DS5_ferdiansakti | 6 | 6 | 12 | 324 | 6 | 6 | 120 | 0 | PASS | Shared 6 teks persis |


## D. Conflict Accounting
| conflicting_text_groups | conflicting_record_rows | cross_dataset_conflicting_text_groups | within_dataset_conflicting_text_groups | exclusively_cross_dataset_groups | exclusively_within_dataset_groups | both_cross_and_within_groups |
| --- | --- | --- | --- | --- | --- | --- |
| 51 | 181 | 48 | 6 | 45 | 3 | 3 |


## E. Near Duplicate Clustering Summary
| metric | value |
| --- | --- |
| Unique Normalized Variant Groups (NVG) | 47645 |
| Near-Duplicate Groups / Template Families (NDG) | 46469 |
| Consolidated Leakage Groups (LG) | 46469 |
| Inspection Sample Pairs Verified | 300 |
| Recursive Sub-blocking Large Buckets (>=200) | HANDLED (No silent skips) |


## F. Canonical Dataset (Layer 1)
- **Total Canonical Records**: 48,051 rekaman.
- **Promotion (1)**: 7,999 (16.65%)
- **Non-Promotion (0)**: 40,052 (83.35%)

### Source Representative Attribution:
- `DS2_kyyyy8_all`: 23,894 (49.73%)
- `DS4_kyyyy8_platform`: 10,656 (22.18%)
- `DS1_fahruu`: 6,602 (13.74%)
- `DS5_ferdiansakti`: 4,181 (8.7%)
- `DS3_yaemico`: 2,718 (5.66%)


## G. Main Pool Candidate (Layer 2: DS1 + Unified Kyyyy8)
- **Total Main Pool Records**: 41,152 rekaman.
- **Promotion (1)**: 4,950 (12.03%)
- **Non-Promotion (0)**: 36,202 (87.97%)


## H. DS3 OOD Candidate (Layer 3: Live Chat CCTV Jogja Isolated)
| initial_ds3_unique_records | invalid_records_quarantined | exact_overlap_removed | whitespace_overlap_removed | normalized_overlap_removed | near_duplicate_overlap_removed | total_overlap_removed | remaining_isolated_ood_records | promotion_count | non_promotion_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2728 | 2 | 10 | 0 | 29 | 0 | 39 | 2689 | 36 | 2653 |


## I. DS5 External Candidate (Layer 3: Ambil4d Focused)
| initial_ds5_unique_records | exact_overlap_with_main_pool | whitespace_overlap_with_main_pool | normalized_overlap_with_main_pool | near_duplicate_overlap_with_main_pool | total_overlapping_records | strictly_non_overlapping_records | campaign_focus |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4202 | 21 | 0 | 3 | 179 | 203 | 3999 | ambil4d |


## J. Heuristic Metadata Clarification
- `promotion_type_heuristic`: Metadata turunan berbasis aturan (rule-based) untuk audit dan analisis, **BUKAN** anotasi gold manusia (`promotion_type_is_gold = False`).
- `known_brand_entity`: Entitas nama situs/platform perjudian resmi yang teridentifikasi.
- `gambling_signal_terms`: Istilah leksikal perjudian generik (misal `slot`, `gacor`, `maxwin`, `zeus`) yang sengaja dipisahkan agar tidak membingungkan pelaporan entitas kampanye.
- `obfuscation_candidate`: Flag keberadaan karakter font matematika unicode, pemisahan spasi, atau karakter pemblokir filter.


## K. Final Decision
### FINAL STATUS: `READY_FOR_SPLIT`

Seluruh 10 kriteria evaluasi telah tuntas terverifikasi dan memenuhi seluruh batasan metodologis.