# LAPORAN KONTROL KUALITAS DATA v2 (DATA QUALITY REPORT v2)

**Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Text Obfuscation pada Komentar YouTube Bahasa Indonesia**

---

## 1. Ringkasan Kualitas Data Global
- **Total Raw Records Terproses**: 84,004 baris.
- **Data Quality Valid**: 57,658 baris.
- **Data Quality Suspicious (Flagged)**: 26,344 baris (termasuk short text, URL, font unicode math).
- **Data Quality Invalid (Quarantined)**: 2 baris (teks kosong/null di DS3).
- **Total Unique Canonical Records**: 48,051 baris.
- **Label Accepted**: 83,996 baris.
- **Label Under Review**: 6 baris.

## 2. Tabel Rekonsiliasi Dataset v2

| source_dataset | raw_rows | invalid_rows | exact_duplicate_rows | cross_dataset_duplicate_rows | conflict_rows | review_rows | accepted_rows | excluded_rows | final_unique_canonical_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS1_fahruu | 8440 | 0 | 2443 | 0 | 0 | 0 | 8440 | 0 | 6602 |
| DS2_kyyyy8_all | 45592 | 0 | 13473 | 0 | 0 | 3 | 45589 | 0 | 23894 |
| DS3_yaemico | 6350 | 2 | 3746 | 0 | 0 | 0 | 6348 | 2 | 2718 |
| DS4_kyyyy8_platform | 18902 | 0 | 9889 | 0 | 0 | 3 | 18899 | 0 | 10656 |
| DS5_ferdiansakti | 4720 | 0 | 797 | 0 | 0 | 0 | 4720 | 0 | 4181 |
| TOTAL_POOL | 84004 | 2 | 48405 | 0 | 0 | 6 | 83996 | 2 | 48051 |


## 3. Matriks Irisan Teks Antar Dataset v2 (Monotonicity Recomputed)

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


## 4. Akuntansi Konflik Label v2

| conflicting_text_groups | conflicting_record_rows | cross_dataset_conflicting_text_groups | within_dataset_conflicting_text_groups | exclusively_cross_dataset_groups | exclusively_within_dataset_groups | both_cross_and_within_groups |
| --- | --- | --- | --- | --- | --- | --- |
| 51 | 181 | 48 | 6 | 45 | 3 | 3 |


## 5. Distribusi Kelas (Label Distribution)

- **Distribusi Raw Source Label**: 0 = 52,568 | 1 = 31,436
- **Distribusi Final Canonical Label**: 0 = 40,052 (83.35%) | 1 = 7,999 (16.65%)

## 6. Distribusi Subtipe Promosi Heuristik v2 (Bukan Anotasi Gold)

> *Catatan Penting*: Nilai pada kolom `promotion_type_heuristic` adalah metadata turunan berbasis aturan (rule-based) dan **bukan** anotasi manual manusia (gold annotation).

- `non_gambling`: 37,712 (78.48%)
- `obfuscated_promotion`: 4,660 (9.7%)
- `site_endorsement`: 2,119 (4.41%)
- `neutral_gambling_discussion`: 841 (1.75%)
- `criticism`: 786 (1.64%)
- `testimonial`: 672 (1.4%)
- `spam_complaint`: 447 (0.93%)
- `promotional_claim`: 292 (0.61%)
- `anti_gambling`: 266 (0.55%)
- `explicit_ad`: 145 (0.3%)
- `call_to_action`: 111 (0.23%)

## 7. Laporan Entitas Kampanye v2 (Brands vs Lexical Signals)

| entity_name | entity_type | frequency_raw | pct_of_total_raw |
| --- | --- | --- | --- |
| pulauwin | brand | 3781 | 4.5 |
| wisdomtoto | brand | 2923 | 3.48 |
| mona4d | brand | 1329 | 1.58 |
| timo4d | brand | 963 | 1.15 |
| alexis17 | brand | 930 | 1.11 |
| dora77 | brand | 869 | 1.03 |
| gunungwin | brand | 489 | 0.58 |
| garudahoki | brand | 419 | 0.5 |
| ambil4d | brand | 402 | 0.48 |
| weton88 | brand | 233 | 0.28 |
| poipet308 | brand | 205 | 0.24 |
| berkah99 | brand | 174 | 0.21 |
| pas4d | brand | 129 | 0.15 |
| mamajitu | brand | 48 | 0.06 |
| toke69 | brand | 31 | 0.04 |
| bardi4d | brand | 29 | 0.03 |
| sendal4d | brand | 16 | 0.02 |
| wifi4d | brand | 8 | 0.01 |
| kembar78 | brand | 5 | 0.01 |
| takjub4d | brand | 2 | 0.0 |


## 8. Laporan Isolasi Kandidat OOD DS3 terhadap Main Pool

| initial_ds3_unique_records | invalid_records_quarantined | exact_overlap_removed | whitespace_overlap_removed | normalized_overlap_removed | near_duplicate_overlap_removed | total_overlap_removed | remaining_isolated_ood_records | promotion_count | non_promotion_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2728 | 2 | 10 | 0 | 29 | 0 | 39 | 2689 | 36 | 2653 |