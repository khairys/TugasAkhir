# OBFUSCATION PILOT VALIDATION REPORT v1

**Stage 7: Text Obfuscation Design, Generator, and Pilot Validation**

- **Timestamp**: `2026-10-07 15:38:37`
- **Pipeline Version**: `obfuscation_pilot_v1`
- **Global Seed**: `42`
- **Source Dataset**: `data/processed/main_pool_candidate_v2.csv`
- **Pilot Source Records**: `200` (100 Promotion, 100 Non-Promotion)
- **Total Pilot Rows Generated**: `1,800` rows (200 source × 9 conditions)
- **Human Audit Queue Size**: `320` samples (balanced across 4 families × 2 severities × 2 labels)
- **Python Version**: `3.13.0`
- **Pandas Version**: `3.0.5`
- **NumPy Version**: `2.5.3`

---

## 1. Automated Integrity Assertions Summary
| Assertion | Rule | Status |
| --- | --- | --- |
| Check A: Determinism | Rerun on 1,800 records produces 100% byte-exact output | PASS |
| Check B: Original Text Match | text_original strictly matches main pool byte-for-byte | PASS |
| Check C: Label Preservation | canonical_label is identical to main pool label | PASS |
| Check D: Protected Spans | URLs, emails, mentions, hashtags remain completely intact | PASS |
| Check E: Normal Control | All 200 normal controls strictly unchanged (0 edits) | PASS |
| Check F: Human Review Verified | 320 review samples audited with 100% label and meaning preserved | PASS |


---

## 2. Generation & Change Rate Statistics
| family | severity | number_generated | number_changed | number_no_eligible_target | change_rate_pct |
| --- | --- | --- | --- | --- | --- |
| NORMAL | NORMAL | 200 | 0 | 0 | 0.0 |
| O1_CHAR_SUBSTITUTION | MILD | 200 | 197 | 3 | 98.5 |
| O1_CHAR_SUBSTITUTION | STRONG | 200 | 197 | 3 | 98.5 |
| O2_CHAR_INSERT_DELETE | MILD | 200 | 196 | 4 | 98.0 |
| O2_CHAR_INSERT_DELETE | STRONG | 200 | 198 | 2 | 99.0 |
| O3_WHITESPACE | MILD | 200 | 198 | 2 | 99.0 |
| O3_WHITESPACE | STRONG | 200 | 198 | 2 | 99.0 |
| O4_UNICODE_ORTHOGRAPHIC | MILD | 200 | 198 | 2 | 99.0 |
| O4_UNICODE_ORTHOGRAPHIC | STRONG | 200 | 198 | 2 | 99.0 |


---

## 3. Modification & Diagnostic Statistics (Changed Records)
| family | severity | changed_count | mean_mod_chars | median_mod_chars | max_mod_chars | mean_mod_ratio | median_mod_ratio | excessive_ratio_flags | length_anomaly_flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O1_CHAR_SUBSTITUTION | MILD | 197 | 1.0 | 1.0 | 1 | 0.0257 | 0.0182 | 0 | 0 |
| O1_CHAR_SUBSTITUTION | STRONG | 197 | 3.82 | 4.0 | 4 | 0.0899 | 0.0714 | 1 | 0 |
| O2_CHAR_INSERT_DELETE | MILD | 196 | 1.0 | 1.0 | 1 | 0.0258 | 0.0182 | 0 | 0 |
| O2_CHAR_INSERT_DELETE | STRONG | 198 | 1.95 | 2.0 | 2 | 0.047 | 0.0364 | 0 | 0 |
| O3_WHITESPACE | MILD | 198 | 1.0 | 1.0 | 1 | 0.0258 | 0.0182 | 0 | 0 |
| O3_WHITESPACE | STRONG | 198 | 1.95 | 2.0 | 2 | 0.0471 | 0.0364 | 0 | 0 |
| O4_UNICODE_ORTHOGRAPHIC | MILD | 198 | 1.0 | 1.0 | 1 | 0.0258 | 0.0182 | 0 | 0 |
| O4_UNICODE_ORTHOGRAPHIC | STRONG | 198 | 1.96 | 2.0 | 2 | 0.0472 | 0.0364 | 0 | 0 |

- **Total Excessive Ratio Flags**: `1` (Diagnostic flags for human inspection)
- **Total Length Anomaly Flags**: `0`

---

## 4. Human Review Audit Status
- **Review Queue Path**: `data/review/obfuscation_pilot_review_v1.csv`
- **Total Review Samples**: `320` samples (4 families × 2 severities × 2 labels × 20 samples)
- **Audit State**: **`AUDIT_COMPLETED_AND_APPROVED`**
- **Audit Summary**: 320 dari 320 sampel (100%) diverifikasi secara kontekstual:
  1. `human_meaning_preserved`: 320/320 (100% YES)
  2. `human_label_preserved`: 320/320 (100% YES)
  3. `human_transformation_valid`: 320/320 (100% YES)
  4. Komentar Non-Promosi (160 sampel): Terverifikasi murni komentar YouTube organik non-judi.
  5. Komentar Promosi (160 sampel): Terverifikasi promosi situs/platform judi online.
- **Keputusan Audit**: Preservasi semantik dan validitas fungsi komunikasi terbukti valid.

---

## 5. Stage 7 Final Decision
### OBFUSCATION_STATUS: `FROZEN_V1`

- Generator implementasi: **SELESAI & VALID ✅**
- Validasi integritas otomatis: **100% PASS ✅**
- Audit semantik & label manusia: **100% VERIFIED & APPROVED ✅**
- Pembekuan spesifikasi formal: **RESMI FROZEN_V1 (Siap masuk Stage 8) ✅**
