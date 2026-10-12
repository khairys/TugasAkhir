# LAPORAN RESMI EVALUASI KETAHANAN MODEL (STAGE 10)
## Evaluasi Komparatif Ketahanan Linear SVM vs Character-level CNN vs IndoBERT terhadap Penyamaran Teks pada Komentar YouTube

---

## 1. TUJUAN EKSPERIMEN

Penelitian skripsi ini bertujuan untuk mengevaluasi dan membandingkan ketahanan (*robustness*) tiga arsitektur model deteksi promosi judi online pada komentar YouTube berbahasa Indonesia:
1. **Linear SVM** dengan representasi *word-level* TF-IDF (unigram + bigram, C = 10.0).
2. **Character-level CNN (Char-CNN)** dengan representasi karakter, multi-scale 1D convolution (kernel 3, 5, 7), dan masked global max pooling.
3. **IndoBERT** (`indobenchmark/indobert-base-p2`) yang telah di-*fine-tune* menggunakan representasi subword WordPiece kontekstual.

Fokus pengujian Stage 10 adalah mengukur stabilitas performa klasifikasi ketiga model ketika dihadapkan pada 4 keluarga penyamaran teks (*text obfuscation*) lintas 2 tingkat keparahan (MILD dan STRONG), dengan total 8 kondisi manipulasi teks adversarial. Evaluasi ini berpedoman pada prinsip ilmiah ketat: **tanpa retraining**, **tanpa threshold tuning**, **tanpa data leakage**, dan **menggunakan test set yang telah dibekukan sejak Stage 8**.

---

## 2. DATASET DAN INTEGRITAS TEST SET

Test set resmi yang dibekukan terdiri dari 1 kondisi normal baseline dan 8 kondisi penyamaran teks. Setiap berkas memiliki ukuran persis 4.116 baris dengan distribusi label biner:
- **Non-Promotion (`canonical_label = 0`)**: 3.621 baris (87,97%)
- **Promotion (`canonical_label = 1`)**: 495 baris (12,03%)
- **Total Sampel per Kondisi**: 4.116 baris

Seluruh berkas data telah lolos verifikasi kriptografis SHA-256 sebelum dan sesudah evaluasi:

| Kondisi | Path Dataset | SHA-256 Aktual | Status |
|---|---|---|---|
| NORMAL | `data/processed/test_normal_v1.csv` | `6d5a2c8b386193147013fb7a6002e4fa0375969f00d46a0cc86eea674e8c3780` | MATCH |
| O1_MILD | `data/processed/obfuscated_test_v1/O1_MILD.csv` | `a455e6224a37c826cefe3c19a7aa1966feb11fa93eca266ae14479a8fea1fb6e` | MATCH |
| O1_STRONG | `data/processed/obfuscated_test_v1/O1_STRONG.csv` | `79dff505fe3d121dbe187cce2e41bdcc228b959767e7e9b2556c76ed83a8dd98` | MATCH |
| O2_MILD | `data/processed/obfuscated_test_v1/O2_MILD.csv` | `5357596408b1d5fc3354a53fee1fd957808bd517e4055966d2c4ab59d3886584` | MATCH |
| O2_STRONG | `data/processed/obfuscated_test_v1/O2_STRONG.csv` | `b6eb5c853777094f850a9b1ac112ea19f9e71a27d5a66e58c6444dcf07456174` | MATCH |
| O3_MILD | `data/processed/obfuscated_test_v1/O3_MILD.csv` | `75b70109d5c33308f48146e5ad5e21e693086d8c004c724705737e8aa16386cc` | MATCH |
| O3_STRONG | `data/processed/obfuscated_test_v1/O3_STRONG.csv` | `6a0016fb564e65ac0443ac28232f9bc5012eaade2a6d76863a8e00cbd1191764` | MATCH |
| O4_MILD | `data/processed/obfuscated_test_v1/O4_MILD.csv` | `89e5402a5050252ca555c49266cd92f2cffa1f0e027b0e2d8ccec326139e264c` | MATCH |
| O4_STRONG | `data/processed/obfuscated_test_v1/O4_STRONG.csv` | `466c428ef5f1515823ccfaf53c4911c599d1f6dc36ee7a596a67685ac84a1607` | MATCH |

Invarian integritas:
- `source_record_id` 100% selaras antara baseline normal dan 8 file obfuscation.
- `canonical_label` pada file obfuscation terverifikasi 100% identik dengan baseline normal.
- Seluruh 3.973 s.d. 3.992 pasangan yang ditandai `changed == True` terverifikasi mengalami perubahan string antara `text_original` dan `text_obfuscated`.

---

## 3. MODEL FINAL YANG DIEVALUASI

Ketiga artefak model yang dievaluasi merupakan artefak beku hasil Stage 9 tanpa modifikasi bobot atau arsitektur:

1. **Linear SVM Pipeline**:
   - Berkas: `artifacts/stage9/svm_v1/linear_svm_pipeline.joblib`
   - SHA-256: `d1708afd513c7f276aa9df75a13ecef92a2204587f8365c0d93fb249bb13d0d9`
   - Komponen: Word TfidfVectorizer (ngram_range=(1,2), sublinear_tf=True, min_df=2) + LinearSVC (C=10.0, loss='squared_hinge').
2. **Character-level CNN (Char-CNN)**:
   - Bobot Model: `charcnn_v1_results/artifacts/final_model/charcnn_model.pt`
   - SHA-256 Bobot: `9d0c5caaa3b2e316ab9131df09e2377467966c3d3a3f6fcc6a1c46d9ff8236b8`
   - Kosakata: `charcnn_v1_results/artifacts/final_model/vocab.json` (SHA-256: `d156b5a5...`, ukuran: 1.727 karakter).
   - Arsitektur: Embedding(1727, 32), Conv1D(kernel 3, 5, 7, channel 64 each, total 192 filters), Masked Global Max Pooling, Dense(192 → 128, ReLU, Dropout 0.3), Output Dense(128 → 2).
3. **IndoBERT (Fine-tuned)**:
   - Bobot Model: `indobert_v1_results/artifacts/final_model/model.safetensors`
   - SHA-256 Bobot: `890dd84c8f25f2d0761959335c5bc00c76b396cf6065317d7589ee84d3ddafbd`
   - Tokenizer: WordPiece (`vocab.txt`, 30.521 subwords), konfigurasi arsitektur bert-base (12 layers, 768 hidden, 12 heads).
   - Mapping Label: index 0 = Non-Promotion, index 1 = Promotion.

---

## 4. KONFIGURASI INFERENCE

- **Linear SVM**: Prediksi kelas menggunakan `pipeline.predict(X)`, decision score diekstrak menggunakan `pipeline.decision_function(X)`.
- **Char-CNN**: Mode inferensi `model.eval()` dan `torch.inference_mode()`, truncation pada `max_length = 576` karakter dengan padding kanan, keputusan label biner menggunakan `argmax(logits, dim=1)`. Probabilitas dihitung via `softmax(logits)`.
- **IndoBERT**: Mode inferensi `model.eval()` dan `torch.inference_mode()`, tokenisasi batch `truncation=True, max_length=128`, klasifikasi menggunakan `argmax(logits, dim=1)`. Logits dan probabilitas diekstrak secara deterministik.
- **Perangkat**: CPU (8 thread deterministik).

---

## 5. DEFINISI KELUARGA OBFUSCATION DAN SUCCESS RATE

Penelitian menguji 4 keluarga penyamaran teks yang diimplementasikan pada Stage 8:
- **O1: Character Substitution**: Penggantian karakter huruf dengan angka leetspeak (misal: 'e' → '3', 'a' → '4', 'i' → '1').
  - Tingkat transformasi: 3.973 / 4.116 (96,53%).
- **O2: Character Insertion / Deletion**: Penambahan karakter acak atau penghapusan karakter ganda.
  - O2_MILD: 3.982 / 4.116 (96,74%), O2_STRONG: 3.992 / 4.116 (96,99%).
- **O3: Whitespace Manipulation**: Penambahan spasi antarkarakter (*spacing*) atau penghapusan spasi pemisah kata (*zero-width spacing / concatenation*).
  - O3_MILD: 3.985 / 4.116 (96,82%), O3_STRONG: 3.992 / 4.116 (96,99%).
- **O4: Unicode / Orthographic Manipulation**: Penggantian karakter Latin dengan homoglyph Unicode (Cyrillic, Greek, Math Alphanumeric Symbols).
  - Tingkat transformasi: 3.992 / 4.116 (96,99%).

---

## 6. PROTOKOL EVALUASI FULL-SET DAN PAIRED

Untuk mencegah bias metodologis, evaluasi dibagi menjadi dua tingkat:
1. **Full-Set Evaluation**: Menggunakan seluruh 4.116 sampel pada berkas pengujian. Menghitung Precision, Recall, F1 Promotion, Accuracy, Macro-F1, dan Confusion Matrix.
2. **Paired Robustness Evaluation**: Menggunakan hanya sampel yang berhasil mengalami manipulasi teks (`changed == True`, N = 3.973 s.d. 3.992 pasang).
   - **F1 Drop**: F1 Normal (Paired) - F1 Obfuscated (Paired)
   - **Relative Drop (%)**: (F1 Drop / F1 Normal (Paired)) × 100
   - **F1 Retention (%)**: (F1 Obfuscated (Paired) / F1 Normal (Paired)) × 100
   - **95% Confidence Interval**: Dihitung menggunakan **10.000 replikasi Paired Stratified Bootstrap** dengan seed tetap 42.

---

## 7. HASIL PENGUJIAN TEST NORMAL (BASELINE)

Pada kondisi teks bersih tanpa penyamaran (`test_normal_v1.csv`, N = 4.116), performa ketiga model tercatat sebagai berikut:

| Model | F1 Promotion | Precision | Recall | Accuracy | Macro-F1 | TN | FP | FN | TP |
|---|---|---|---|---|---|---|---|---|---|
| **Character-level CNN** | **0.9786** | **0.9877** | **0.9697** | **0.9949** | **0.9878** | 3.615 | 6 | 15 | 480 |
| **IndoBERT (Fine-tuned)** | 0.9605 | 0.9634 | 0.9576 | 0.9905 | 0.9776 | 3.603 | 18 | 21 | 474 |
| **Linear SVM (TF-IDF)** | 0.9428 | 0.9721 | 0.9152 | 0.9866 | 0.9676 | 3.608 | 13 | 42 | 453 |

*Temuan Baseline:*
Char-CNN mencapai F1 Promotion tertinggi (0.9786) dengan Recall tertinggi (0.9697) dan False Positive terendah (hanya 6 kasus), diikuti oleh IndoBERT (F1 0.9605), dan Linear SVM (F1 0.9428).

---

## 8. HASIL TIAP MODEL PADA DELAPAN KONDISI (FULL-SET METRICS)

Tabel berikut menyajikan metrik F1 Promotion pada seluruh 4.116 sampel untuk setiap model dan kondisi:

| Kondisi | Keluarga | Severity | Linear SVM F1 | Char-CNN F1 | IndoBERT F1 |
|---|---|---|---|---|---|
| **NORMAL (Baseline)** | Baseline | Normal | 0.9428 | **0.9786** | 0.9605 |
| **O1_MILD** | O1 (Char Substitution) | MILD | 0.9137 | **0.9756** | 0.9386 |
| **O1_STRONG** | O1 (Char Substitution) | STRONG | 0.8749 | **0.9608** | 0.8617 |
| **O2_MILD** | O2 (Insertion/Deletion) | MILD | 0.9154 | **0.9792** | 0.9558 |
| **O2_STRONG** | O2 (Insertion/Deletion) | STRONG | 0.8734 | **0.9785** | 0.9424 |
| **O3_MILD** | O3 (Whitespace) | MILD | 0.9099 | **0.9782** | 0.9588 |
| **O3_STRONG** | O3 (Whitespace) | STRONG | 0.8498 | **0.9806** | 0.9396 |
| **O4_MILD** | O4 (Unicode/Homoglyph) | MILD | 0.9039 | **0.9776** | 0.7878 |
| **O4_STRONG** | O4 (Unicode/Homoglyph) | STRONG | 0.8596 | **0.9786** | 0.6323 |

---

## 9. PERUBAHAN F1 DAN PAIRED BOOTSTRAP CONFIDENCE INTERVAL (95% CI)

Metrik paired robustness dievaluasi secara ketat pada pasangan komentar yang berhasil disamarkan (`changed == True`). Estimasi ketidakpastian dihitung menggunakan 10.000 replikasi paired stratified bootstrap.

| Model | Kondisi | F1 Normal (Paired) | F1 Obf (Paired) | F1 Drop | Relative Drop (%) | Retention (%) | 95% Bootstrap CI |
|---|---|---|---|---|---|---|---|
| **Char-CNN** | O1_MILD | 0.9806 | 0.9766 | **0.0040** | 0.40% | 99.60% | [-0.0011, 0.0099] |
| **Char-CNN** | O1_STRONG | 0.9806 | 0.9608 | **0.0197** | 2.01% | 97.99% | [0.0097, 0.0306] |
| **Char-CNN** | O2_MILD | 0.9802 | 0.9792 | **0.0011** | 0.11% | 99.89% | [0.0000, 0.0032] |
| **Char-CNN** | O2_STRONG | 0.9796 | 0.9785 | **0.0011** | 0.11% | 99.89% | [-0.0030, 0.0053] |
| **Char-CNN** | O3_MILD | 0.9804 | 0.9782 | **0.0021** | 0.22% | 99.78% | [0.0000, 0.0053] |
| **Char-CNN** | O3_STRONG | 0.9796 | 0.9806 | **-0.0010** | -0.11% | 100.11% | [-0.0032, 0.0000] |
| **Char-CNN** | O4_MILD | 0.9796 | 0.9776 | **0.0020** | 0.21% | 99.79% | [0.0000, 0.0051] |
| **Char-CNN** | O4_STRONG | 0.9796 | 0.9786 | **0.0010** | 0.10% | 99.90% | [-0.0021, 0.0042] |
| **Linear SVM** | O1_MILD | 0.9447 | 0.9137 | **0.0310** | 3.29% | 96.71% | [0.0192, 0.0445] |
| **Linear SVM** | O1_STRONG | 0.9447 | 0.8749 | **0.0699** | 7.40% | 92.60% | [0.0524, 0.0887] |
| **Linear SVM** | O2_MILD | 0.9448 | 0.9154 | **0.0294** | 3.11% | 96.89% | [0.0165, 0.0434] |
| **Linear SVM** | O2_STRONG | 0.9438 | 0.8734 | **0.0704** | 7.46% | 92.54% | [0.0519, 0.0903] |
| **Linear SVM** | O3_MILD | 0.9463 | 0.9099 | **0.0364** | 3.85% | 96.15% | [0.0230, 0.0512] |
| **Linear SVM** | O3_STRONG | 0.9438 | 0.8498 | **0.0940** | 9.96% | 90.04% | [0.0724, 0.1163] |
| **Linear SVM** | O4_MILD | 0.9438 | 0.9039 | **0.0398** | 4.22% | 95.78% | [0.0259, 0.0549] |
| **Linear SVM** | O4_STRONG | 0.9438 | 0.8596 | **0.0841** | 8.91% | 91.09% | [0.0653, 0.1046] |
| **IndoBERT** | O1_MILD | 0.9624 | 0.9386 | **0.0237** | 2.47% | 97.53% | [0.0120, 0.0360] |
| **IndoBERT** | O1_STRONG | 0.9624 | 0.8617 | **0.1006** | 10.46% | 89.54% | [0.0809, 0.1216] |
| **IndoBERT** | O2_MILD | 0.9607 | 0.9558 | **0.0050** | 0.52% | 99.48% | [-0.0045, 0.0149] |
| **IndoBERT** | O2_STRONG | 0.9605 | 0.9424 | **0.0181** | 1.88% | 98.12% | [0.0056, 0.0316] |
| **IndoBERT** | O3_MILD | 0.9610 | 0.9588 | **0.0022** | 0.23% | 99.77% | [-0.0090, 0.0135] |
| **IndoBERT** | O3_STRONG | 0.9605 | 0.9396 | **0.0209** | 2.18% | 97.82% | [0.0070, 0.0354] |
| **IndoBERT** | O4_MILD | 0.9605 | 0.7878 | **0.1727** | 17.98% | 82.02% | [0.1519, 0.1927] |
| **IndoBERT** | O4_STRONG | 0.9605 | 0.6323 | **0.3282** | 34.17% | 65.83% | [0.3077, 0.3478] |

---

## 10. ANALISIS EVASION DAN FALSE-NEGATIVE FLIP

Analisis ini mengukur sejauh mana penyamaran teks berhasil mengecoh model sehingga komentar promosi yang sebelumnya terdeteksi (*True Positive*) berubah menjadi tidak terdeteksi (*False Negative / Evasion*). Denominator adalah jumlah True Positive normal pada paired subset.

| Model | Kondisi | TP Normal | Evasion Flips | Evasion Flip Rate (%) | New FP Flips | Total Pred Flips |
|---|---|---|---|---|---|---|
| **Char-CNN** | O1_MILD | 479 | 0 | **0,00%** | 6 | 8 |
| **Char-CNN** | O1_STRONG | 479 | 3 | **0,63%** | 22 | 30 |
| **Char-CNN** | O2_MILD | 471 | 1 | **0,21%** | 0 | 1 |
| **Char-CNN** | O2_STRONG | 480 | 2 | **0,42%** | 1 | 5 |
| **Char-CNN** | O3_MILD | 474 | 2 | **0,42%** | 0 | 2 |
| **Char-CNN** | O3_STRONG | 480 | 0 | **0,00%** | 0 | 1 |
| **Char-CNN** | O4_MILD | 480 | 1 | **0,21%** | 1 | 2 |
| **Char-CNN** | O4_STRONG | 480 | 1 | **0,21%** | 1 | 3 |
| **Linear SVM** | O1_MILD | 453 | 20 | **4,42%** | 13 | 37 |
| **Linear SVM** | O1_STRONG | 453 | 46 | **10,15%** | 23 | 74 |
| **Linear SVM** | O2_MILD | 445 | 25 | **5,62%** | 7 | 38 |
| **Linear SVM** | O2_STRONG | 453 | 56 | **12,36%** | 13 | 76 |
| **Linear SVM** | O3_MILD | 449 | 26 | **5,79%** | 13 | 45 |
| **Linear SVM** | O3_STRONG | 453 | 75 | **16,56%** | 12 | 94 |
| **Linear SVM** | O4_MILD | 453 | 28 | **6,18%** | 14 | 47 |
| **Linear SVM** | O4_STRONG | 453 | 58 | **12,80%** | 20 | 81 |
| **IndoBERT** | O1_MILD | 473 | 3 | **0,63%** | 30 | 41 |
| **IndoBERT** | O1_STRONG | 473 | 23 | **4,86%** | 100 | 137 |
| **IndoBERT** | O2_MILD | 465 | 12 | **2,58%** | 1 | 22 |
| **IndoBERT** | O2_STRONG | 474 | 25 | **5,27%** | 3 | 40 |
| **IndoBERT** | O3_MILD | 468 | 8 | **1,71%** | 9 | 32 |
| **IndoBERT** | O3_STRONG | 474 | 25 | **5,27%** | 9 | 49 |
| **IndoBERT** | O4_MILD | 474 | 4 | **0,84%** | 226 | 241 |
| **IndoBERT** | O4_STRONG | 474 | 7 | **1,48%** | **523** | **543** |

*Temuan Evasion dan Pola Kerusakan:*
1. **Linear SVM menderita kerentanan Evasion sistemik**: Rata-rata evasion rate mencapai 9,24% (puncaknya pada O3_STRONG dengan 16,56% atau 75 komentar promosi lolos deteksi).
2. **Char-CNN hampir kebal terhadap Evasion**: Rata-rata evasion rate hanya 0,26% (total hanya 10 kasus evasion lintas seluruh 8 kondisi).
3. **IndoBERT mengalami kolaps tipe False Positive pada O4**: Meskipun evasion rate-nya rendah pada O4 (0,84% s.d. 1,48%), IndoBERT mengalami ledakan False Positive yang masif: **226 komentar non-promosi pada O4_MILD dan 523 komentar non-promosi pada O4_STRONG keliru diprediksi sebagai Promosi!** Hal ini menyebabkan precision IndoBERT anjlok drastis ke 47,00%.

---

## 11. ANALISIS BERDASARKAN SUMBER DATASET

Dataset pengujian berasal dari 4 korpus sumber:
- `DS1_fahruu`: 629 sampel (142 Promotion, 487 Non-Promotion)
- `DS2_prabowo`: 2.290 sampel (35 Promotion, 2.255 Non-Promotion)
- `DS3_judol`: 134 sampel (134 Promotion, 0 Non-Promotion)
- `DS4_tambahan`: 1.063 sampel (184 Promotion, 879 Non-Promotion)

*Observasi Stratifikasi:*
- Pada sumber yang didominasi komentar normal umum (`DS2_prabowo`), penurunan presisi IndoBERT pada kondisi O4 terlihat sangat parah karena komentar umum yang disisipi karakter homoglyph memicu model secara agresif untuk memprediksinya sebagai promosi.
- Char-CNN menunjukkan ketahanan yang merata di keempat korpus sumber tanpa penurunan tajam pada subset mana pun.
- Rincian lengkap metrik stratifikasi tersimpan pada `reports/stage10/source_stratified_metrics.csv`.

---

## 12. PERBANDINGAN KOMPARATIF KETAHANAN KETIGA MODEL

Ringkasan komparatif lintas seluruh kondisi:

| Parameter Evaluasi | Character-level CNN | Linear SVM (TF-IDF) | IndoBERT (Fine-tuned) |
|---|---|---|---|
| **F1 Normal Test** | **0.9786** | 0.9428 | 0.9605 |
| **Rata-rata F1 Drop (8 Kondisi)** | **0.0037** | 0.0569 | 0.0839 |
| **Rata-rata F1 Retention (%)** | **99.62%** | 93.98% | 91.27% |
| **Rata-rata Evasion Flip Rate** | **0.26%** | 9.24% | 2.83% |
| **Keluarga Paling Rentan** | O1 (Drop: 0.0118) | O3 (Drop: 0.0652) | O4 (Drop: 0.2504) |
| **Keluarga Paling Tahan** | O3 (Drop: 0.0005) | O2 (Drop: 0.0499) | O2 & O3 (Drop: ~0.0115) |
| **Tingkat Degradasi Severity** | MILD: 0.0023 / STRONG: 0.0052 | MILD: 0.0342 / STRONG: 0.0796 | MILD: 0.0509 / STRONG: 0.1170 |

---

## 13. ERROR ANALYSIS DENGAN CONTOH AKTUAL

Berdasarkan inspeksi terhadap 2.385 baris pada `reports/stage10/paired_error_analysis.csv`, ditemukan perbedaan mendasar mekanisme kegagalan ketiga model:

### A. Kegagalan Linear SVM: Token Fragmentation & Evasion
- **Contoh O3_STRONG (Spasi Karakter)**:
  - Teks Asli: `"P U L A U W I N agen terpercaya langsung cair"`
  - Teks Obfuscated: `"P  U  L  A  U  W  I  N  agen terpercaya langsung cair"` (atau pemisahan kata kunci promosi)
  - Perilaku: Token unigram dan bigram kata kunci promosi pecah menjadi unigram satu huruf yang tidak terdaftar dalam bobot TF-IDF model. Bobot score SVM turun di bawah hyperplane threshold (0.0), sehingga model memprediksi Non-Promotion (Evasion / False Negative).
- **Contoh O1_STRONG (Substitusi Angka)**:
  - Teks Asli: `cuman di HBC MANTUL hidup gue langsung berubah jadi makin keren 😎`
  - Teks Obfuscated: `cuman di HBC MANTUL hidup gue langsun9 berubah jadi makin keren 😎`
  - Perilaku: Kata `langsun9` menjadi token Out-of-Vocabulary (OOV), menghilangkan fitur kontekstual penting.

### B. Kegagalan IndoBERT: Overfitting Representasi Homoglyph (False Positive Spikes)
- **Contoh O4_STRONG (Unicode Homoglyph pada Komentar Non-Promosi)**:
  - Teks Asli: `'Kamari punya ekspresi yang lucu dan natural 😂😂😂😂❤🎉'` (Non-Promotion, label 0)
  - Teks Obfuscated: `'Kаmari punya ekspresi yang lucu dan naturаl 😂😂😂😂❤🎉'` (Karakter 'а' diganti Cyrillic U+0430)
  - Prediksi Normal: Non-Promotion (Label 0, Benar)
  - Prediksi Obfuscated: **Promotion (Label 1, SALAH - False Positive)**
  - Teks Asli: `'pandu cringe banget'` (Non-Promotion, label 0)
  - Teks Obfuscated: `'pаndu сringe banget'` (Cyrillic 'а' dan 'с')
  - Prediksi Normal: Non-Promotion (Label 0, Benar)
  - Prediksi Obfuscated: **Promotion (Label 1, SALAH - False Positive)**
- **Analisis Mekanisme**:
  Tokenizer WordPiece IndoBERT memecah karakter Cyrillic menjadi token terpisah atau `[UNK]`. Karena pada dataset training promosi judi YouTube banyak pelaku spam menggunakan huruf dekoratif/Unicode, self-attention layer IndoBERT mempelajari asosiasi semu (*spurious correlation*) bahwa kehadiran karakter non-ASCII/homoglyph berkorelasi sangat kuat dengan promosi judi. Akibatnya, ketika teks netral non-promosi disamarkan dengan homoglyph, IndoBERT mengalami halusinasi klasifikasi dan salah melabelinya sebagai promosi.

### C. Keberhasilan Mekanistik Character-level CNN
- Char-CNN memproses teks pada granularitas karakter individu dengan representasi embedding dense (32 dimensi) dan filter konvolusi berukuran 3, 5, dan 7 karakter yang dilanjutkan dengan masked global max pooling.
- Meskipun sebuah kata kunci disisipi spasi (O3), angka (O1), atau karakter Unicode (O4), filter konvolusi tetap mampu menangkap n-gram karakter yang tersisa di sekitarnya. Penggunaan global max pooling memastikan bahwa sinyal fitur paling representatif tetap terdeteksi tanpa terpengaruh oleh posisi padding atau token OOV.
- Akibatnya, Char-CNN mempertahankan retensi F1 rata-rata sebesar **99,62%**, menjadikannya arsitektur yang paling tahan terhadap manipulasi teks adversarial.

---

## 14. KETERBATASAN DAN ANCAMAN VALIDITAS

1. **Lingkup Obfuscation Terisolasi**: Pengujian mengevaluasi 4 keluarga transformasi secara terpisah (O1 s.d. O4) dan belum menguji kombinasi simultan (misalnya kombinasi substitusi leetspeak sekaligus homoglyph dan zero-width spacing).
2. **Ketergantungan Kosakata Karakter Char-CNN**: Char-CNN sangat kuat dalam penelitian ini karena kosakata karakternya (1.727 karakter) mencakup hampir seluruh variasi Unicode yang ada di korpus YouTube Indonesia. Jika penyerang menggunakan karakter Unicode dari blok skrip yang belum pernah ada di kosakata, embedding karakter tersebut akan dipetakan ke `<UNK>`.
3. **Perbedaan Indeks Tokenizer Transformer**: IndoBERT tidak menggunakan karakter-level tokenizer melainkan WordPiece 32k. Kerentanan IndoBERT terhadap homoglyph merupakan konsekuensi inheren dari subword tokenization yang tidak terlatih pada korpus noisy/adversarial.
4. **Generalisasi Domain**: Korpus pengujian terfokus pada komentar YouTube Indonesia. Pola penyamaran di platform lain (seperti Twitter/X atau Telegram) mungkin memiliki distribusi leetspeak dan emoji yang berbeda.

---

## 15. KESIMPULAN PENELITIAN

1. **Character-level CNN Terbukti Sebagai Model Paling Robust**:
   Char-CNN tidak hanya memiliki F1 baseline tertinggi pada teks normal (0.9786), tetapi juga menunjukkan ketahanan yang superior dengan rata-rata F1 drop hanya **0.0037** (retensi 99,62%) dan rata-rata evasion flip rate hanya **0.26%**. Pada kondisi manipulasi spasi ekstrem (O3_STRONG), F1 Char-CNN bahkan praktis tidak mengalami penurunan (-0.0010 ΔF1).
2. **Linear SVM Mengalami Kerentanan Evasion Sistemik**:
   Linear SVM dengan word-level TF-IDF mengalami degradasi signifikan dengan rata-rata F1 drop **0.0569** (retensi 93,98%). Kelemahan utamanya adalah tingginya *evasion flip rate* (mencapai 16,56% pada manipulasi spasi O3_STRONG) akibat terpecahnya token kata kunci menjadi OOV.
3. **IndoBERT Mengalami Kerentanan Homoglyph Catastrophic (False Positive Surge)**:
   Meskipun IndoBERT cukup tahan terhadap variasi spasi dan penambahan karakter (O2 dan O3 drop ~0.011), model ini mengalami kegagalan fatal pada manipulasi Unicode homoglyph (O4_STRONG drop **0.3282**, retensi anjlok ke 65,83%). Kerentanan ini termanifestasi dalam bentuk lonjakan False Positive (+523 kasus) akibat bias atensi terhadap karakter homoglyph.
4. **Implikasi untuk Praktik dan Penelitian Skripsi**:
   Untuk sistem moderasi konten dan deteksi promosi judi online real-world yang menghadapi teks adversarial, arsitektur berbasis karakter (Character-level CNN) terbukti secara empiris jauh lebih reliabel dan tahan banting dibandingkan model representasi kata (Linear SVM) maupun model bahasa subword (IndoBERT).

---

## 16. DAFTAR FILE DAN MANIFEST ARTEFAK

Seluruh artefak hasil evaluasi resmi Stage 10 telah diproduksi dan divalidasi:

| Berkas | Deskripsi |
|---|---|
| `configs/stage10/robustness_evaluation_v1.json` | Konfigurasi evaluasi beku Stage 10 |
| `reports/stage10/evaluation_plan_v1.json` | Rencana dan protokol evaluasi resmi |
| `reports/stage10/artifact_validation_report.md` | Laporan audit integritas artefak Stage 8 & 9 |
| `reports/stage10/test_normal_metrics.csv` | Hasil evaluasi baseline normal (3 model) |
| `reports/stage10/obfuscation_metrics_full.csv` | Hasil evaluasi full-set 8 kondisi (24 baris) |
| `reports/stage10/paired_robustness_metrics.csv` | Hasil paired robustness + 10.000 bootstrap CI (24 baris) |
| `reports/stage10/prediction_flip_summary.csv` | Ringkasan evasion flips dan label shifts (24 baris) |
| `reports/stage10/paired_error_analysis.csv` | Audit baris per baris kegagalan klasifikasi (2.385 baris) |
| `reports/stage10/source_stratified_metrics.csv` | Metrik terstratifikasi berdasarkan sumber dataset (81 baris) |
| `reports/stage10/robustness_summary.json` | Ringkasan metrik dan peringkat model resmi |
| `reports/stage10/manifest_v1.json` | Manifest run lengkap berisi hash, runtime, dan environment |
| `reports/stage10/predictions/` | 27 file CSV berisi 111.132 prediksi resmi |
| `scripts/22_run_stage10_robustness.py` | Pipeline runner evaluasi deterministik |
| `scripts/23_validate_stage10_results.py` | Validator komprehensif artefak output Stage 10 |
| `tests/stage10/` | 36 unit tests verifikasi dataset, pairing, dan metrik |
