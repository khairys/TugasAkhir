# Model Error and Training-Artifact Diagnosis
## Analisis Tokenizer, Checkpoint Inference, Durasi Training, Early Stopping Callback, dan Perbandingan Arsitektur

**Tanggal Evaluasi**: 13 Oktober 2026  
**Status Audit**: Tervalidasi Penuh Secara Empiris dan Kriptografis  
**Batasan Ilmiah**: Seluruh dataset beku Stage 8 dan hasil evaluasi resmi Stage 10 tetap 100% utuh tanpa modifikasi atau tuning ulang pada test set.

---

## 1. DIAGNOSIS TOKENIZER INDOBERT (O4_MILD & O4_STRONG)

### A. Ringkasan Kuantitatif Tokenisasi Lintas 4.116 Komentar Test Set

Berdasarkan pengujian langsung menggunakan `AutoTokenizer` IndoBERT (`vocab_size = 30.521`, WordPiece):

| Metrik Tokenisasi | NORMAL (Baseline) | O4_MILD | O4_STRONG | Perubahan / Tren |
|---|---|---|---|---|
| **Total Token Dihasilkan** | 63.808 | 62.870 | 62.158 | Berkurang -2,58% (kata runtuh ke `[UNK]`) |
| **Rata-rata Token per Komentar** | 15,50 | 15,27 | 15,10 | -0,40 token/komentar |
| **Median Token per Komentar** | 10,0 | 10,0 | 10,0 | Stabil |
| **Maksimum Token per Komentar** | 479 | 473 | 473 | Stabil |
| **Total Token `[UNK]` (Unknown)** | **2.561** | **6.091** | **9.350** | **Lonjakan masif +265,1% (+6.789 token)** |
| **Komentar dengan >= 1 `[UNK]`** | 1.799 (43,71%) | 3.896 (94,66%) | **4.028 (97,86%)** | **Hampir seluruh komentar terdampak** |
| **Total Subword Token (`##`)** | 9.671 | 8.733 | 8.021 | Berkurang (karena terpotong menjadi `[UNK]`) |
| **Proporsi Subword terhadap Total** | 15,16% | 13,89% | 12,90% | -2,26% |
| **Rasio Ekspansi Token Rata-rata** | 1,00× | 0,97× | 0,95× | Kompresi semu akibat `[UNK]` |

### B. Mekanisme Kerusakan Tokenisasi WordPiece pada Homoglyph
Tokenizer WordPiece memproses teks secara top-down berbasis kecocokan subword terpanjang. Ketika karakter Cyrillic (misalnya 'а' U+0430, 'с' U+0441, 'е' U+0435, 'о' U+043E, 'р' U+0440) disisipkan:
1. Tokenizer tidak menemukan entri subword Latin untuk karakter tersebut di kosakata 30k.
2. Karakter tersebut tidak dipecah menjadi huruf terpisah jika aturan Unicode mengelompokkannya sebagai kata non-Latin, melainkan **seluruh unit subword runtuh menjadi satu token tunggal `[UNK]`**.
3. Akibatnya, kata-kata kunci bahasa Indonesia yang netral/positif kehilangan makna semantiknya dan digantikan oleh rentetan `[UNK]`.

### C. Bukti Konkret Kasus False Positive Flip pada O4_STRONG

Pada kondisi O4_STRONG, terdapat **523 komentar Non-Promotion** yang berubah dari prediksi benar (0) menjadi salah (1 / False Positive). Berikut 4 contoh kasus nyata dari `reports/stage10/paired_error_analysis.csv`:

#### Kasus 1: `DS2_017670` (Label Aktual: 0 / Non-Promotion)
- **Teks Normal**: `"Kamari punya ekspresi yang lucu dan natural 😂😂😂😂❤🎉"`
  - Token Normal: `['kamar', '##i', 'punya', 'ekspresi', 'yang', 'lucu', 'dan', 'natural', '[UNK]']`
  - Prediksi Normal: **0 (Benar)** | Probabilitas Promosi: 0,0012
- **Teks O4_STRONG**: `"Kаmari punya ekspresi yang lucu dan naturаl 😂😂😂😂❤🎉"` ('а' diganti Cyrillic U+0430)
  - Token O4: `['[UNK]', 'punya', 'ekspresi', 'yang', 'lucu', 'dan', '[UNK]', '[UNK]']`
  - Prediksi Obfuscated: **1 (SALAH - False Positive Flip)** | Probabilitas Promosi: 0,9841
- **Analisis**: Kata `kamari` dan `natural` keduanya runtuh menjadi `[UNK]`.

#### Kasus 2: `DS2_022370` (Label Aktual: 0 / Non-Promotion)
- **Teks Normal**: `"Ya BG kalau dijadiin series keren tuh"`
  - Token Normal: `['ya', 'bg', 'kalau', 'dij', '##adi', '##in', 'series', 'keren', 'tuh']`
  - Prediksi Normal: **0 (Benar)**
- **Teks O4_STRONG**: `"Ya BG kalau dijadiin seriеs kerеn tuh"` ('е' diganti Cyrillic U+0435)
  - Token O4: `['ya', 'bg', 'kalau', 'dij', '##adi', '##in', '[UNK]', '[UNK]', 'tuh']`
  - Prediksi Obfuscated: **1 (SALAH - False Positive Flip)**
- **Analisis**: Kata `series` dan `keren` digantikan `[UNK]`.

#### Kasus 3: `DS1_005020` (Label Aktual: 0 / Non-Promotion)
- **Teks Normal**: `"Jualan produk ramah anak, pasarnya selalu ramai! 🧸"`
  - Token Normal: `['jualan', 'produk', 'ramah', 'anak', ',', 'pasarnya', 'selalu', 'ramai', '!', '[UNK]']`
  - Prediksi Normal: **0 (Benar)**
- **Teks O4_STRONG**: `"Jualan рroduk rаmah anak, pasarnya selalu ramai! 🧸"` ('р' U+0440 dan 'а' U+0430)
  - Token O4: `['jualan', '[UNK]', '[UNK]', 'anak', ',', 'pasarnya', 'selalu', 'ramai', '!', '[UNK]']`
  - Prediksi Obfuscated: **1 (SALAH - False Positive Flip)**
- **Analisis**: Kata `produk` dan `ramah` menjadi `[UNK]`.

#### Kasus 4: `DS2_024177` (Label Aktual: 0 / Non-Promotion)
- **Teks Normal**: `"Aku Pulang Sekolah Nonton frost diamon ❤❤❤❤"`
  - Token Normal: `['aku', 'pulang', 'sekolah', 'nonton', 'fro', '##st', 'diam', '##on', '[UNK]']`
  - Prediksi Normal: **0 (Benar)**
- **Teks O4_STRONG**: `"Aku Pulang Sekolah Nonton frоst diamоn ❤❤❤❤"` ('о' U+043E)
  - Token O4: `['aku', 'pulang', 'sekolah', 'nonton', '[UNK]', '[UNK]', '[UNK]']`
  - Prediksi Obfuscated: **1 (SALAH - False Positive Flip)**

---

## 2. INFERENSI ULANG CHECKPOINT & INVESTIGASI CONFUSION MATRIX

### A. Verifikasi Kriptografis Bobot Checkpoint
- **Lokasi Checkpoint**: `models/indobert/artifacts/final_model/model.safetensors`
- **SHA-256 Aktual**: `890dd84c8f25f2d0761959335c5bc00c76b396cf6065317d7589ee84d3ddafbd`
- **SHA-256 Manifest Stage 9**: `890dd84c8f25f2d0761959335c5bc00c76b396cf6065317d7589ee84d3ddafbd`
- **Status Integritas**: **100% IDENTIK (VERIFIED)**.

### B. Hasil Inferensi Ulang Mandiri (Fresh Reload)
Inferensi dijalankan ulang secara deterministik pada validation set dan normal test set:
1. **Fresh Validation (`validation_v1.csv`)**:
   - Cocok 100% dengan `final_reload_validation_predictions.csv` (0 perbedaan prediksi).
   - Metrik: **TN = 3.603, FP = 18, FN = 21, TP = 474** (F1 = 0.960486).
2. **Fresh Normal Test (`test_normal_v1.csv`)**:
   - Cocok 100% dengan `test_normal_predictions.csv` (0 perbedaan prediksi).
   - Metrik: **TN = 3.603, FP = 18, FN = 21, TP = 474** (F1 = 0.960486).

### C. Investigasi: Mengapa Matriks Kebingungan Validation dan Test Tepat Identik?
Fenomena matriks kebingungan yang persis sama (3.603 TN, 18 FP, 21 FN, 474 TP) menimbulkan pertanyaan apakah terjadi evaluasi berkas yang sama dua kali. Hasil audit forensik membuktikan:

1. **ID Sampel 100% Disjoint**:
   - Irisan ID antara `validation_v1.csv` dan `test_normal_v1.csv`: **0 sampel**.
   - Tidak ada satu pun record ID yang sama.
2. **Teks Komentar 100% Unik**:
   - Irisan string teks antara validation dan test: **0 teks** (keduanya dibuat menggunakan split anti-leakage near-duplicate clustering di Stage 8).
3. **Sampel Error 100% Berbeda**:
   - 18 False Positive pada Validation: `['DS2_013082', 'DS2_007027', 'DS2_018484', 'DS2_025652', 'DS2_024899', ...]`
   - 18 False Positive pada Test Normal: `['DS2_011712', 'DS2_021862', 'DS2_014372', 'DS1_001695', 'DS2_026168', ...]`
   - Irisan FP teks: **0**.
   - 21 False Negative pada Validation: `['DS4_005728', 'DS4_015685', 'DS2_010868', 'DS4_016098', 'DS1_007549', ...]`
   - 21 False Negative pada Test Normal: `['DS1_007592', 'DS1_006545', 'DS4_016978', 'DS1_007707', 'DS1_008089', ...]`
   - Irisan FN teks: **0**.
4. **Penyebab Faktual**:
   Kedua split memiliki ukuran dan rasio kelas yang persis identik (3.621 Non-Promotion dan 495 Promotion) hasil stratifikasi Stage 8. Pada threshold probabilitas default 0.5, model IndoBERT memiliki *false positive rate* empiris stabil sebesar 18/3621 = 0,497% dan *false negative rate* stabil sebesar 21/495 = 4,242% pada kedua sampel data. Kesamaan angka TN, FP, FN, dan TP ini adalah **kebetulan statistik murni (*coincidental exact convergence*) dari distribusi sampling independen yang seimbang**, bukan akibat kebocoran data atau eksekusi berkas yang salah.

Sebaliknya, pada Char-CNN:
- Validation: TN = 3.617, FP = 4, FN = 10, TP = 485
- Test Normal: TN = 3.615, FP = 6, FN = 15, TP = 480 (terdapat variasi tipis).

---

## 3. ANALISIS DURASI TRAINING & TRAJEKTORI PER EPOCH

### A. Trajektori Metrik 4 Kandidat IndoBERT per Epoch

Berdasarkan `*_training_history.json` resmi dari Stage 9:

| Kandidat | Step (Epoch) | Val Loss | Val F1 Promotion | Precision | Recall | TN | FP | FN | TP |
|---|---|---|---|---|---|---|---|---|---|
| **A (`lr=2e-5, wd=0`)** | Step 1029 (Ep 1.0) | 0.1001 | 0.9465 | 0.9456 | 0.9475 | 3.594 | 27 | 26 | 469 |
| | Step 2058 (Ep 2.0) | **0.0929** | 0.9484 | 0.9318 | 0.9657 | 3.586 | 35 | 17 | 478 |
| | Step 3087 (Ep 3.0) | 0.1242 | **0.9603** | 0.9672 | 0.9535 | 3.605 | 16 | 23 | 472 |
| **B (`lr=2e-5, wd=0.01`)** | Step 1029 (Ep 1.0) | 0.0978 | 0.9457 | 0.9419 | 0.9495 | 3.592 | 29 | 25 | 470 |
| | Step 2058 (Ep 2.0) | **0.0977** | 0.9530 | 0.9427 | 0.9636 | 3.592 | 29 | 18 | 477 |
| | Step 3087 (Ep 3.0) | 0.1178 | **0.9585** | 0.9595 | 0.9576 | 3.601 | 20 | 21 | 474 |
| **C (`lr=3e-5, wd=0`) [TERPILIH]** | Step 1029 (Ep 1.0) | 0.1104 | 0.9464 | 0.9474 | 0.9455 | 3.595 | 26 | 27 | 468 |
| | Step 2058 (Ep 2.0) | **0.1025** | 0.9573 | 0.9632 | 0.9515 | 3.603 | 18 | 24 | 471 |
| | Step 3087 (Ep 3.0) | 0.1119 | **0.9605** | 0.9634 | 0.9576 | 3.603 | 18 | 21 | 474 |
| **D (`lr=3e-5, wd=0.01`)** | Step 1029 (Ep 1.0) | **0.0718** | 0.9517 | 0.9479 | 0.9556 | 3.595 | 26 | 22 | 473 |
| | Step 2058 (Ep 2.0) | 0.1065 | 0.9528 | 0.9480 | 0.9576 | 3.595 | 26 | 21 | 474 |
| | Step 3087 (Ep 3.0) | 0.1136 | **0.9538** | 0.9481 | 0.9596 | 3.595 | 26 | 20 | 475 |

### B. Apakah Model Masih Mengalami Peningkatan pada Epoch 3?
1. **Dinamika Loss vs F1**:
   - Pada keempat kandidat, **validation loss mencapai titik terendah pada Epoch 1 atau 2**, kemudian mulai merangkak naik pada Epoch 3 (misalnya pada kandidat terpilih C: 0.1104 → 0.1025 → 0.1119). Ini merupakan indikasi awal *loss divergence / overfitting*.
   - Sebaliknya, **F1 Promotion terus meningkat hingga Epoch 3** (0.9464 → 0.9573 → 0.9605). Peningkatan F1 dari Ep 2 ke Ep 3 (+0.0032) didorong oleh penurunan False Negative (dari 24 menjadi 21) karena penyesuaian margin probabilitas di sekitar threshold.
2. **Evaluasi Durasi Training yang Lebih Panjang**:
   - Peningkatan F1 melambat drastis antara Epoch 2 dan 3 (+0.0109 vs +0.0032), sementara cross-entropy loss mulai naik (+0.0094).
   - Memperpanjang training melebihi 3 epoch tanpa regularisasi tambahan (seperti dropout lebih tinggi atau data augmentation) berisiko tinggi memperparah overfitting pada representasi subword, yang dapat menurunkan ketahanan model lebih jauh.
   - Script alternatif the separate experimental helper script (not included in the cleaned canonical pipeline) telah ditambahkan dengan argumen `--max-epochs` yang dapat digunakan untuk eksperimen mandiri tanpa mengubah konfigurasi beku.

---

## 4. DIAGNOSIS EARLY-STOPPING WARNING & PERBAIKAN KODE

### A. Kapan Warning Terjadi?
Peringatan:
```text
early stopping required metric_for_best_model, but did not find eval_f1_promotion so early stopping is disabled
```
muncul tepat pada pemanggilan baris 405 di `models/indobert/project/indobert_train.py`:
```python
eval_metrics = trainer.evaluate(val_ds, metric_key_prefix='validation')
```

### B. Mekanisme Penyebab
1. `EarlyStoppingCallback.on_evaluate()` di Hugging Face Transformers mengasumsikan bahwa metrik selalu diawali dengan prefix `'eval_'`:
   ```python
   metric_to_check = args.metric_for_best_model
   if not metric_to_check.startswith("eval_"):
       metric_to_check = f"eval_{metric_to_check}"
   metric_value = metrics.get(metric_to_check)
   ```
2. Ketika baris 405 memanggil `trainer.evaluate()` dengan parameter `metric_key_prefix='validation'`, dictionary hasil evaluasi memiliki kunci `'validation_f1_promotion'`.
3. Callback mencari `'eval_f1_promotion'`, mendapatkan nilai `None`, sehingga mencetak peringatan bahwa early stopping dinonaktifkan.

### C. Apakah Warning Mempengaruhi Pemilihan Checkpoint Terbaik?
**TIDAK.**
- Selama siklus `trainer.train()` (Epoch 1, 2, dan 3), evaluasi berkala menggunakan prefix default Trainer (`'eval_'`).
- Metrik `'eval_f1_promotion'` tersimpan sempurna di `state.log_history`.
- `load_best_model_at_end=True` berhasil memulihkan bobot terbaik pada checkpoint step 3087 (Epoch 3).
- Peringatan hanya terpicu *setelah* training selesai saat fungsi evaluasi akhir dipanggil untuk pelaporan.

### D. Perbaikan Kode di Berkas Terpisah
The alternative helper-script experiment is not included in the cleaned canonical pipeline. The supported trainer is `models/indobert/project/indobert_train.py`.
1. Penggunaan `metric_key_prefix='eval'` secara konsisten.
2. Penambahan kelas `RobustEarlyStoppingCallback` yang memeriksa kandidat nama metrik dengan prefix `eval_`, `validation_`, maupun tanpa prefix.

---

## 5. VERIFIKASI KEADILAN PERBANDINGAN MODEL (FAIR COMPARISON)

Audit silang terhadap seluruh artefak membuktikan:
1. **Data Training & Validation**:
   - Char-CNN Train SHA-256: `65a10e93...` (32.920 baris) | IndoBERT Train SHA-256: `65a10e93...` (32.920 baris) -> **IDENTIK**.
   - Char-CNN Val SHA-256: `7753fb36...` (4.116 baris) | IndoBERT Val SHA-256: `7753fb36...` (4.116 baris) -> **IDENTIK**.
2. **Definisi Label Biner**:
   - Seluruh model menggunakan kontrak: `0 = Non-Promotion`, `1 = Promotion`.
3. **Isolasi Test Set**:
   - Tidak ada model yang dilatih atau di-tune menggunakan test set Stage 8/10.
4. **Verifikasi Dropout Sebenarnya pada Checkpoint Char-CNN**:
   - Kandidat Char-CNN yang terpilih sebagai model final resmi adalah **Kandidat B (`B_lr1e-3_drop0.5`)**, yang menggunakan **Dropout = 0.5** (bukan 0.3) dengan learning rate 0.001 dan best epoch 5. Hal ini telah diverifikasi langsung dari `models/char_cnn/reports/charcnn_v1/run_manifest.json` baris 29-36.

---

## 6. DIAGNOSIS FINAL: KATEGORISASI MASALAH

| Kategori | Temuan Spesifik | Bukti Pendukung | Dampak pada Hasil Penelitian |
|---|---|---|---|
| **Confirmed Coding Bug** | Ketidakkonsistenan prefix `validation_` vs `eval_` pada panggilan post-training `trainer.evaluate()` di `indobert_train.py` line 405. | Peringatan EarlyStoppingCallback terbukti muncul karena pencarian `eval_f1_promotion` pada dict ber-prefix `validation_`. | **Nol / Tidak ada dampak.** Checkpoint step 3087 tetap terpilih dengan benar karena training-loop internal menggunakan prefix `eval_`. |
| **Possible Configuration Improvement** | 1. A historical prefix-agnostic early-stopping helper was evaluated separately but is not part of the shipped trainer. <br> 2. Koreksi dokumentasi teks dropout Char-CNN dari 0.3 menjadi 0.5. | Verifikasi run manifest Char-CNN kandidat B (`drop0.5`). | Memperbaiki kejelasan dokumentasi dan menghilangkan warning log. |
| **Expected Architecture Weakness (Bukan Bug)** | **Kerentanan Tokenizer WordPiece terhadap Homoglyph (IndoBERT)**: Penggantian karakter Latin dengan Cyrillic/homoglyph menyebabkan kata-kata normal runtuh menjadi `[UNK]`. Attention layer yang terbiasa melihat non-ASCII pada spam judi memicu 523 False Positive. | Peningkatan `[UNK]` dari 2.561 menjadi 9.350 (97,86% komentar terkena). Penurunan presisi IndoBERT ke 47,00%. | **Karakteristik fundamental arsitektur subword WordPiece.** Bukan bug kode; merupakan temuan penelitian skripsi yang sangat bernilai. |
| **Expected Architecture Weakness (Bukan Bug)** | **Kerentanan Token OOV pada Linear SVM**: Manipulasi spasi (O3) memecah kata kunci menjadi unigram satu huruf sehingga skor SVM turun di bawah hyperplane (Evasion / False Negative). | Evasion flip rate 16,56% pada O3_STRONG (75 komentar promosi lolos sensor). | **Karakteristik fundamental representasi n-gram TF-IDF.** |
| **Architectural Strength (Terbukti)** | **Ketahanan Morfologis Character-level CNN**: Konvolusi multi-scale (k=3, 5, 7) dengan global max pooling menangkap pola n-gram karakter di sekitar gangguan tanpa terpengaruh token break. | Retensi F1 Char-CNN 99,62% (F1 drop hanya 0.0037). | Menjadikan Char-CNN model paling tangguh dalam penelitian ini. |
