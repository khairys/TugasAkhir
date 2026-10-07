# STAGE 8 FINAL READINESS REPORT: FINAL EXPERIMENTAL LOCK v1

**Judul Penelitian:**  
*Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Penyamaran Teks pada Komentar YouTube*

- **Tanggal Pelaksanaan**: `2026-10-07 15:51:31`
- **Repositori**: `https://github.com/khairys/TugasAkhir`
- **Branch**: `main`
- **Git Commit SHA**: `4b78b36e6d3d4d42fa21b32c9d3b4782e5858522`
- **Python Version**: `3.13.0`
- **Pandas Version**: `3.0.5`
- **Scikit-Learn Version**: `1.9.1`
- **Status Metodologi**: `STAGE 8 — FINAL EXPERIMENTAL LOCK COMPLETED`

---

## A. Dataset Master & Pool Utama
- **Sumber Data Eksperimen**: `data/processed/main_pool_candidate_v2.csv`
- **Total Baris**: `41,152` records
- **Distribusi Kelas**:
  - Promotion (`1`): `4,950` records (12.03%)
  - Non-Promotion (`0`): `36,202` records (87.97%)
- **Sumber Crawl**: `DS1_fahruu` (6,602), `DS2_kyyyy8_all` (23,894), `DS4_kyyyy8_platform` (10,656)
- **Isolasi External & OOD**: DS3 dan DS5 terbukti 100% terisolasi (0 baris di main pool)
- **SHA-256 Main Pool**: `0f07bc2e11a61804d5b46b2e6eb1e80c2f1ce3de4ce50cffaf5b67bfc1fde6ec`

---

## B. Partisi Eksperimental (Group-Aware Stratified Split)
- **Metode Pembagian**: `StratifiedGroupKFold`
- **Parameter**: `n_splits = 10`, `shuffle = True`, `random_state = 42`
- **Variabel Pengelompokan (Group)**: `leakage_group_id` (40,091 kelompok unik)
- **Variabel Stratifikasi (Target)**: `canonical_label`
- **Penetapan Fold Deterministik**:
  - Fold 0 $\rightarrow$ **TEST** (`4,116` baris, 10.00%)
  - Fold 1 $\rightarrow$ **VALIDATION** (`4,116` baris, 10.00%)
  - Fold 2–9 $\rightarrow$ **TRAIN** (`32,920` baris, 80.00%)

### Distribusi Partisi & Label:
| Partisi | Total Baris | Persentase | Promosi (1) | Non-Promosi (0) | Rasio Promosi | Leakage Groups |
| --- | --- | --- | --- | --- | --- | --- |
| **TRAIN** | 32,920 | 80.00% | 3,960 | 28,960 | 12.03% | 32,087 |
| **VALIDATION** | 4,116 | 10.00% | 495 | 3,621 | 12.03% | 4,004 |
| **TEST** | 4,116 | 10.00% | 495 | 3,621 | 12.03% | 4,000 |
| **TOTAL** | **41,152** | **100.00%** | **4,950** | **36,202** | **12.03%** | **40,091** |

### Distribusi Sumber per Partisi:
- **Train**: DS2: 19,148 (58.17%), DS4: 8,492 (25.80%), DS1: 5,280 (16.04%)
- **Validation**: DS2: 2,355 (57.22%), DS4: 1,068 (25.95%), DS1: 693 (16.84%)
- **Test**: DS2: 2,391 (58.09%), DS4: 1,096 (26.63%), DS1: 629 (15.28%)

---

## C. Pencegahan Data Leakage
1. **Record ID Overlap**: `0` (Disjoint 100% across all 3 partitions)
2. **Leakage Group Overlap**: `0` (Disjoint 100% across all 3 partitions)
3. **Review Records Leaked**: `0` (Zero records from `data/review/label_review_queue_v2.csv` enter train, val, or test)
4. **Author Overlap Diagnostic**:
   - Train ∩ Validation: 1,475 authors (terdokumentasi di `data/audit/author_overlap_diagnostic_v1.md`)
   - Train ∩ Test: 1,475 authors
   - Validation ∩ Test: 357 authors
   - *Catatan Metodologis*: Author bukan primary constraint karena identitas bot burner accounts berganti-ganti di YouTube; mitigasi primer dijamin oleh `leakage_group_id` yang 100% saling lepas (*disjoint*).

---

## D. Pembekuan Test Normal (Test Set Anchor Freeze)
- **File Anchor**: `data/processed/test_normal_v1.csv`
- **Total Baris**: `4,116` records (495 Promotion, 3,621 Non-Promotion)
- **Status**: **FROZEN & IMMUTABLE** (Dilarang dimodifikasi pada tahap pelatihan model)
- **SHA-256 Test Normal**: `6d5a2c8b386193147013fb7a6002e4fa0375969f00d46a0cc86eea674e8c3780`

---

## E. Generasi Test Set Terobfuscasi Berpasangan (Paired Obfuscated Test Sets)
Generasi resmi dilakukan menggunakan generator Stage 7 yang telah dibekukan (`FROZEN_V1`) dengan parameter global `seed = 42`.

### Statistik Kondisi & Success Rate:
| Kondisi | Famili Perturbasi | Tingkat Keparahan | Total Uji | Berhasil Tertransformasi | No Target | Success Rate | Status Ambang (>=90%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `O1_MILD` | O1_CHAR_SUBSTITUTION | MILD | 4,116 | 3,973 | 143 | 96.53% | **READY** |
| `O1_STRONG` | O1_CHAR_SUBSTITUTION | STRONG | 4,116 | 3,973 | 143 | 96.53% | **READY** |
| `O2_MILD` | O2_CHAR_INSERT_DELETE | MILD | 4,116 | 3,982 | 134 | 96.74% | **READY** |
| `O2_STRONG` | O2_CHAR_INSERT_DELETE | STRONG | 4,116 | 3,992 | 124 | 96.99% | **READY** |
| `O3_MILD` | O3_WHITESPACE | MILD | 4,116 | 3,985 | 131 | 96.82% | **READY** |
| `O3_STRONG` | O3_WHITESPACE | STRONG | 4,116 | 3,992 | 124 | 96.99% | **READY** |
| `O4_MILD` | O4_UNICODE_ORTHOGRAPHIC | MILD | 4,116 | 3,992 | 124 | 96.99% | **READY** |
| `O4_STRONG` | O4_UNICODE_ORTHOGRAPHIC | STRONG | 4,116 | 3,992 | 124 | 96.99% | **READY** |

- **Total Pasangan dalam Manifest**: `32,928` baris (`data/processed/obfuscated_test_v1/condition_manifest.csv`)
- **Status Evaluasi Terpasang**: Seluruh 8 kondisi memenuhi ambang batas kualitas metodologis $\ge 90.0\%$ (96.53% – 96.99%).

---

## F. Verifikasi Pairing & Integritas Semantik
- **Invarian Pairing**:
  - `original.record_id == obfuscated.source_record_id` $\rightarrow$ **100% IDENTIK**
  - `original.canonical_label == obfuscated.canonical_label` $\rightarrow$ **100% IDENTIK (Preservasi Label Sempurna)**
  - `original.text_raw == obfuscated.text_original` $\rightarrow$ **100% BYTE-FOR-BYTE IDENTIK**
- **Konsistensi Perubahan**:
  - `changed == True` $\rightarrow$ `text_obfuscated != text_original` (100% terbukti)
  - `changed == False` $\rightarrow$ `text_obfuscated == text_original` (100% terbukti dengan status `NO_CHANGE` / `NO_ELIGIBLE_TARGET`)
- **Evaluasi Berpasangan (Paired Evaluation Protocol)**:
  - Degradasi model pada tiap kondisi hanya dihitung terhadap pasangan yang berhasil diubah (`is_evaluable_pair == True`), dibandingkan langsung dengan inferensi baseline normal pada subset `source_record_id` yang identik.

---

## G. Reproducibility & Integritas Hash SHA-256
| Berkas Artefak | Lokasi Berkas | SHA-256 Checksum |
| --- | --- | --- |
| Main Pool | `data/processed/main_pool_candidate_v2.csv` | `0f07bc2e11a61804d5b46b2e6eb1e80c2f1ce3de4ce50cffaf5b67bfc1fde6ec` |
| Train v1 | `data/splits/v1/train_v1.csv` | `65a10e93713586e20ebb9a3a0c0694d860a6d9d5541e84000713f2918d595cf3` |
| Validation v1 | `data/splits/v1/validation_v1.csv` | `7753fb36275d36a2367e15d28de3f52f06e0f33a4f666d81d7dd95c5a9d87038` |
| Test v1 | `data/splits/v1/test_v1.csv` | `4e544147a29cdcdc8523d058cc9fb9790b44c38388e92bdf60a72fb7feff684f` |
| Test Normal Anchor | `data/processed/test_normal_v1.csv` | `6d5a2c8b386193147013fb7a6002e4fa0375969f00d46a0cc86eea674e8c3780` |
| Split Manifest | `data/splits/v1/split_manifest_v1.json` | `dda63d77aaa45ae3ec1e4005e3e32e3e03ae80400a5bbb915b07c496247f4965` |
| Obfuscation Spec | `docs/OBFUSCATION_SPECIFICATION_V1.md` | `421f9f087dbd2df75e576cd64a27274c93f9ee29431c16b33bdc2f83b7164ee8` |
| O1 MILD Test | `data/processed/obfuscated_test_v1/O1_MILD.csv` | `a455e6224a37c826cefe3c19a7aa1966feb11fa93eca266ae14479a8fea1fb6e` |
| O1 STRONG Test | `data/processed/obfuscated_test_v1/O1_STRONG.csv` | `79dff505fe3d121dbe187cce2e41bdcc228b959767e7e9b2556c76ed83a8dd98` |
| O2 MILD Test | `data/processed/obfuscated_test_v1/O2_MILD.csv` | `5357596408b1d5fc3354a53fee1fd957808bd517e4055966d2c4ab59d3886584` |
| O2 STRONG Test | `data/processed/obfuscated_test_v1/O2_STRONG.csv` | `b6eb5c853777094f850a9b1ac112ea19f9e71a27d5a66e58c6444dcf07456174` |
| O3 MILD Test | `data/processed/obfuscated_test_v1/O3_MILD.csv` | `75b70109d5c33308f48146e5ad5e21e693086d8c004c724705737e8aa16386cc` |
| O3 STRONG Test | `data/processed/obfuscated_test_v1/O3_STRONG.csv` | `6a0016fb564e65ac0443ac28232f9bc5012eaade2a6d76863a8e00cbd1191764` |
| O4 MILD Test | `data/processed/obfuscated_test_v1/O4_MILD.csv` | `89e5402a5050252ca555c49266cd92f2cffa1f0e027b0e2d8ccec326139e264c` |
| O4 STRONG Test | `data/processed/obfuscated_test_v1/O4_STRONG.csv` | `466c428ef5f1515823ccfaf53c4911c599d1f6dc36ee7a596a67685ac84a1607` |

---

## H. Status Akhir Kesiapan Eksperimen

Seluruh 16 kriteria keberhasilan Stage 8 (Section 32) telah terpenuhi secara penuh:
- [x] Stage 7 Prerequisite = `FROZEN_V1`
- [x] Main Pool unchanged (`0f07bc2e11a61804d5b46b2e6eb1e80c2f1ce3de4ce50cffaf5b67bfc1fde6ec`)
- [x] StratifiedGroupKFold completed (seed = 42)
- [x] Train/Validation/Test generated
- [x] 41,152 records fully reconciled across partitions
- [x] Zero record_id overlap
- [x] Zero leakage_group_id overlap
- [x] Zero review records leaked
- [x] Test set frozen (`test_normal_v1.csv`)
- [x] Official obfuscation generated only from frozen test
- [x] Every transformed sample paired with original
- [x] Label preserved 100%
- [x] Original text preserved 100%
- [x] Deterministic regeneration verified
- [x] Obfuscation condition statistics generated
- [x] All 8 conditions meet $\ge 90\%$ success rate (96.53% - 96.99%)
- [x] SHA256 manifests generated
- [x] 47/47 automated tests passed

**FINAL STATUS: `READY_FOR_STAGE_9`**
