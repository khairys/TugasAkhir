# LAPORAN KONTROL KUALITAS DATA (DATA QUALITY REPORT)

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

## 2. Tabel Rekonsiliasi Dataset

| source_dataset | raw_rows | invalid_rows | exact_duplicate_rows | cross_dataset_duplicate_rows | conflict_rows | review_rows | accepted_rows | excluded_rows | final_unique_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS1_fahruu | 8440 | 0 | 2443 | 112 | 1 | 0 | 8440 | 0 | 6602 |
| DS2_kyyyy8_all | 45592 | 0 | 13473 | 19549 | 87 | 3 | 45589 | 0 | 23894 |
| DS3_yaemico | 6350 | 2 | 3746 | 57 | 0 | 0 | 6348 | 2 | 2718 |
| DS4_kyyyy8_platform | 18902 | 0 | 9889 | 18902 | 81 | 3 | 18899 | 0 | 10656 |
| DS5_ferdiansakti | 4720 | 0 | 797 | 31 | 12 | 0 | 4720 | 0 | 4181 |
| TOTAL_POOL | 84004 | 2 | 48405 | 38651 | 181 | 6 | 83996 | 2 | 48051 |


## 3. Matriks Irisan Teks Antar Dataset

| dataset_a | dataset_b | shared_exact_texts | shared_whitespace_texts | shared_normalized_variants | label_conflicts | notes |
| --- | --- | --- | --- | --- | --- | --- |
| DS1_fahruu | DS2_kyyyy8_all | 51 | 51 | 57 | 0 | Shared 51 teks persis |
| DS1_fahruu | DS3_yaemico | 6 | 6 | 9 | 0 | Shared 6 teks persis |
| DS1_fahruu | DS4_kyyyy8_platform | 25 | 25 | 31 | 1 | Terdapat 1 konflik label (telah diadjudikasi); Shared 25 teks persis |
| DS1_fahruu | DS5_ferdiansakti | 14 | 14 | 15 | 0 | Shared 14 teks persis |
| DS2_kyyyy8_all | DS3_yaemico | 25 | 25 | 41 | 0 | Shared 25 teks persis |
| DS2_kyyyy8_all | DS4_kyyyy8_platform | 10659 | 10658 | 10539 | 48 | Terdapat 48 konflik label (telah diadjudikasi); Kyyyy8 Lineage (overlap masif ~10.5k teks, metadata DS4 diprioritaskan) |
| DS2_kyyyy8_all | DS5_ferdiansakti | 9 | 9 | 9 | 0 | Shared 9 teks persis |
| DS3_yaemico | DS4_kyyyy8_platform | 10 | 10 | 16 | 0 | Shared 10 teks persis |
| DS3_yaemico | DS5_ferdiansakti | 0 | 0 | 2 | 0 | Tidak ada irisan teks |
| DS4_kyyyy8_platform | DS5_ferdiansakti | 6 | 6 | 6 | 0 | Shared 6 teks persis |


## 4. Distribusi Kelas (Label Distribution)

- **Distribusi Raw Source Label**: 0 = 52,568 | 1 = 31,436
- **Distribusi Final Canonical Label**: 0 = 40,052 (83.35%) | 1 = 7,999 (16.65%)

## 5. Distribusi Tipe Promosi (Promotion Types in Canonical Dataset)

- `non_gambling`: 35,182 (73.22%)
- `obfuscated_promotion`: 4,657 (9.69%)
- `ambiguous`: 2,718 (5.66%)
- `site_endorsement`: 2,108 (4.39%)
- `neutral_gambling_discussion`: 964 (2.01%)
- `criticism`: 833 (1.73%)
- `testimonial`: 668 (1.39%)
- `spam_complaint`: 378 (0.79%)
- `promotional_claim`: 287 (0.6%)
- `explicit_ad`: 139 (0.29%)
- `call_to_action`: 104 (0.22%)
- `anti_gambling`: 13 (0.03%)

## 6. Konsentrasi Entitas / Kampanye Judi (Campaign Frequency Report)

| entity | frequency | pct_of_total_raw |
| --- | --- | --- |
| pulauwin | 3781 | 4.5 |
| wisdomtoto | 2923 | 3.48 |
| zeus_olympus | 1573 | 1.87 |
| timo4d | 963 | 1.15 |
| alexis17 | 930 | 1.11 |
| gunungwin | 489 | 0.58 |
| garudahoki | 419 | 0.5 |
| ambil4d | 402 | 0.48 |
| weton88 | 233 | 0.28 |
| berkah99 | 174 | 0.21 |
| pas4d | 129 | 0.15 |
| toke69 | 31 | 0.04 |
| bardi4d | 29 | 0.03 |
| sendal4d | 16 | 0.02 |
| wifi4d | 8 | 0.01 |