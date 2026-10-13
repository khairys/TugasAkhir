# Stage 10 — Artifact & Input Data Validation Report
**Penelitian Skripsi:** Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Penyamaran Teks pada Komentar YouTube  
**Status Verifikasi:** PASSED (Seluruh Prasyarat Terpenuhi)  
**Tanggal Verifikasi:** 12 Oktober 2026  

---

## 1. Verifikasi Integritas Dataset Test Stage 8 (Frozen Data)

Seluruh file data test resmi Stage 8 diverifikasi menggunakan SHA-256 dan terbukti cocok 100% dengan hash resmi yang tercatat:

| Kondisi Test | Path File | SHA-256 Resmi / Aktual | Jumlah Baris | Status |
|---|---|---|---|---|
| **Normal Test** | `data/processed/test_normal_v1.csv` | `6d5a2c8b386193147013fb7a6002e4fa0375969f00d46a0cc86eea674e8c3780` | 4.116 | **MATCH (PASS)** |
| **O1_MILD** | `data/processed/obfuscated_test_v1/O1_MILD.csv` | `a455e6224a37c826cefe3c19a7aa1966feb11fa93eca266ae14479a8fea1fb6e` | 4.116 | **MATCH (PASS)** |
| **O1_STRONG** | `data/processed/obfuscated_test_v1/O1_STRONG.csv` | `79dff505fe3d121dbe187cce2e41bdcc228b959767e7e9b2556c76ed83a8dd98` | 4.116 | **MATCH (PASS)** |
| **O2_MILD** | `data/processed/obfuscated_test_v1/O2_MILD.csv` | `5357596408b1d5fc3354a53fee1fd957808bd517e4055966d2c4ab59d3886584` | 4.116 | **MATCH (PASS)** |
| **O2_STRONG** | `data/processed/obfuscated_test_v1/O2_STRONG.csv` | `b6eb5c853777094f850a9b1ac112ea19f9e71a27d5a66e58c6444dcf07456174` | 4.116 | **MATCH (PASS)** |
| **O3_MILD** | `data/processed/obfuscated_test_v1/O3_MILD.csv` | `75b70109d5c33308f48146e5ad5e21e693086d8c004c724705737e8aa16386cc` | 4.116 | **MATCH (PASS)** |
| **O3_STRONG** | `data/processed/obfuscated_test_v1/O3_STRONG.csv` | `6a0016fb564e65ac0443ac28232f9bc5012eaade2a6d76863a8e00cbd1191764` | 4.116 | **MATCH (PASS)** |
| **O4_MILD** | `data/processed/obfuscated_test_v1/O4_MILD.csv` | `89e5402a5050252ca555c49266cd92f2cffa1f0e027b0e2d8ccec326139e264c` | 4.116 | **MATCH (PASS)** |
| **O4_STRONG** | `data/processed/obfuscated_test_v1/O4_STRONG.csv` | `466c428ef5f1515823ccfaf53c4911c599d1f6dc36ee7a596a67685ac84a1607` | 4.116 | **MATCH (PASS)** |

---

## 2. Invarian Pairing & Transformasi

Uji pairing membuktikan:
- Seluruh 4.116 record ID pada setiap kondisi berkorespondensi 1-ke-1 secara sempurna dengan `test_normal_v1.csv`.
- Tidak ada pergeseran label (label konsisten 100%).
- Kolom `text_original` identik 100% dengan teks pada `test_normal_v1.csv`.
- Flag `changed == True` konsisten 100% dengan kondisi `text_obfuscated != text_original`.
- Jumlah pasangan yang berhasil ditransformasikan (`changed == True`):
  - O1_MILD: 3.973 baris (96,53%)
  - O1_STRONG: 3.973 baris (96,53%)
  - O2_MILD: 3.982 baris (96,74%)
  - O2_STRONG: 3.992 baris (96,99%)
  - O3_MILD: 3.985 baris (96,82%)
  - O3_STRONG: 3.992 baris (96,99%)
  - O4_MILD: 3.992 baris (96,99%)
  - O4_STRONG: 3.992 baris (96,99%)

---

## 3. Verifikasi Artefak Tiga Model Stage 9

Ketiga model final yang dipilih berdasarkan performa validasi Stage 9 hadir lengkap:

1. **Linear SVM Baseline v1:**
   - Path: `models/linear_svm/model/model.joblib`
   - Ukuran: 8.393.329 bytes (~8,39 MB)
   - SHA-256: `d1708afd513c7f276aa9df75a13ecef92a2204587f8365c0d93fb249bb13d0d9`
   - Konfigurasi: TF-IDF word unigram + bigram, C = 10, balanced class weight.
2. **Character-level CNN v1:**
   - Bobot Model: `models/char_cnn/artifacts/final_model/charcnn_model.pt` (450.342 bytes)
   - SHA-256: `9d0c5caaa3b2e316ab9131df09e2377467966c3d3a3f6fcc6a1c46d9ff8236b8`
   - Kamus Karakter: `models/char_cnn/artifacts/final_model/vocab.json` (1.727 karakter, SHA-256: `d156b5a5...`)
   - Konfigurasi: Multi-scale kernel [3, 5, 7], 64 channels, hidden dim 128, max_length 576.
3. **IndoBERT v1:**
   - Direktori Model: `models/indobert/artifacts/final_model/`
   - Bobot Safetensors: `model.safetensors` (497.795.072 bytes, SHA-256: `890dd84c...`)
   - Tokenizer & Config: `tokenizer.json`, `config.json`, `vocab.txt`
   - Konfigurasi: `indobenchmark/indobert-base-p2`, max_length 128, class weights (0,568 : 4,157).

---

## 4. Hasil Preflight Smoke Test

- Linear SVM smoke test: **PASS**
- Char-CNN smoke test: **PASS**
- IndoBERT smoke test: **PASS**
- Total 36 unit test pytest: **100% PASS**
