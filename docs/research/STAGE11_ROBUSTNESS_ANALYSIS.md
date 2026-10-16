# Tahap 11 — Analisis Robustness

## Status dan batas eksperimen

Analisis ini memakai prediksi yang telah disimpan pada Tahap 10. Tiga model utama tetap Linear SVM, Char-CNN, dan IndoBERT baseline. Tidak ada pelatihan ulang atau tuning terhadap frozen test. Nilai yang ditampilkan di bawah diringkas dari artefak hasil Tahap 10 yang tersimpan; implementasi untuk menghitung ulang dari per-record predictions tersedia di `scripts/analysis/stage11_robustness_analysis.py`. Skrip tersebut telah dijalankan dan seluruh artefak metrik primer serta antrean review error telah diperbarui di `reports/stage11/primary/`.

Semua F1 merujuk pada kelas positif **Promotion (label 1)**. Untuk robustness, pasangan hanya mencakup record dengan `changed == True`, disejajarkan menggunakan `source_record_id`. F1 clean dalam tabel robustness adalah F1 pada subset pasangan yang sama; ini berbeda dari F1 clean-set penuh di bagian absolute performance.

## 11.1 Absolute performance — clean test

| Model | F1 normal | Precision | Recall | Accuracy | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| Linear SVM | 0,9428 | 0,9721 | 0,9152 | 0,9866 | 13 | 42 |
| Char-CNN | **0,9786** | 0,9877 | 0,9697 | **0,9949** | 6 | 15 |
| IndoBERT | 0,9605 | 0,9634 | 0,9576 | 0,9905 | 18 | 21 |

**Kesimpulan absolut:** Char-CNN memiliki F1 clean tertinggi. Ini adalah kesimpulan tentang performa pada data normal, bukan sendirinya kesimpulan robustness.

## 11.2 Robustness — degradasi pada pasangan yang sama

Rata-rata adalah rerata aritmetika tanpa bobot dari delapan kondisi; bukan F1 gabungan (*pooled F1*).

| Model | Mean F1 clean pada pasangan | Mean F1 obfuscated | Mean F1 drop (signed ΔF1) | Mean F1 retention |
|---|---:|---:|---:|---:|
| Linear SVM | 0,9444 | 0,8876 | 0,0569 | 93,98% |
| Char-CNN | 0,9800 | 0,9763 | **0,0037** | **99,62%** |
| IndoBERT | 0,9610 | 0,8771 | 0,0839 | 91,27% |

**Kesimpulan robustness:** Char-CNN menunjukkan degradasi rata-rata paling kecil. IndoBERT menunjukkan degradasi rata-rata terbesar; Linear SVM berada di antara keduanya. Ini tidak mengubah fakta bahwa F1 clean dan robustness adalah dua dimensi berbeda.

Definisi: `F1_drop = F1_normal_paired - F1_obfuscated_paired`. Retention adalah `100 × F1_obfuscated_paired / F1_normal_paired`.

## T. Matriks berdasarkan keluarga obfuscation

Angka adalah mean signed ΔF1 (F1 clean berpasangan dikurangi F1 obfuscated) dari kondisi MILD dan STRONG di dalam setiap keluarga. Nilai positif lebih besar berarti penurunan lebih besar; nilai negatif berarti F1 obfuscated sedikit melampaui F1 clean pada subset berpasangan tersebut.

| Model | Character substitution (O1) | Insertion/deletion (O2) | Whitespace (O3) | Unicode/orthographic (O4) |
|---|---:|---:|---:|---:|
| Linear SVM | 0,0505 | 0,0499 | 0,0652 | 0,0620 |
| Char-CNN | 0,0118 | 0,0011 | 0,0005 | 0,0015 |
| IndoBERT | 0,0622 | 0,0115 | 0,0116 | **0,2504** |

Pola ini memperjelas bahwa robustness bergantung pada jenis perturbasi. SVM paling terpengaruh rata-rata oleh whitespace (O3), IndoBERT sangat terpengaruh oleh Unicode/orthographic manipulation (O4), sedangkan Char-CNN mempertahankan F1 secara dekat pada keempat keluarga yang diuji.

## U. Severity analysis — MILD dibandingkan STRONG

`STRONG − MILD` pada tabel adalah selisih drop F1; nilai positif menunjukkan degradasi yang lebih tinggi pada STRONG.

| Model | Keluarga | ΔF1 MILD | ΔF1 STRONG | STRONG − MILD |
|---|---|---:|---:|---:|
| Linear SVM | O1 Character | 0,0310 | 0,0699 | +0,0388 |
| Linear SVM | O2 Insertion/deletion | 0,0294 | 0,0704 | +0,0410 |
| Linear SVM | O3 Whitespace | 0,0364 | 0,0940 | +0,0576 |
| Linear SVM | O4 Unicode | 0,0398 | 0,0841 | +0,0443 |
| Char-CNN | O1 Character | 0,0040 | 0,0197 | +0,0158 |
| Char-CNN | O2 Insertion/deletion | 0,0011 | 0,0011 | +0,0000 |
| Char-CNN | O3 Whitespace | 0,0021 | -0,0010 | -0,0032 |
| Char-CNN | O4 Unicode | 0,0020 | 0,0010 | -0,0010 |
| IndoBERT | O1 Character | 0,0237 | 0,1006 | +0,0769 |
| IndoBERT | O2 Insertion/deletion | 0,0050 | 0,0181 | +0,0131 |
| IndoBERT | O3 Whitespace | 0,0022 | 0,0209 | +0,0187 |
| IndoBERT | O4 Unicode | 0,1727 | 0,3282 | +0,1556 |

Pada 10 dari 12 pasangan model-keluarga, drop F1 lebih tinggi pada STRONG. Pengecualian berada pada Char-CNN untuk O3 dan O4, dengan perbedaan yang sangat kecil; ini lebih tepat dijelaskan sebagai performa yang stabil/tidak monoton daripada sebagai bukti bahwa STRONG secara umum lebih mudah. IndoBERT memperlihatkan kenaikan degradasi STRONG paling besar pada O4.

## V. Statistical / uncertainty analysis

Prosedur yang digunakan untuk tiap kondisi adalah **stratified paired bootstrap** dengan 10.000 resamples, confidence level 95%, dan seed 42. Record ID yang sama pada normal dan obfuscated diperlakukan sebagai satu pasangan; resampling distratifikasi menurut label gold (0/1). Interval untuk ΔF1 dihitung dari distribusi `F1_normal_paired − F1_obfuscated_paired`.

Contoh interval 95% dari artefak Tahap 10:

| Model | Kondisi | ΔF1 | CI 95% |
|---|---|---:|---:|
| Linear SVM | O3 STRONG | 0,0940 | [0,0724; 0,1163] |
| Char-CNN | O1 MILD | 0,0040 | [-0,0011; 0,0099] |
| Char-CNN | O4 STRONG | 0,0010 | [-0,0021; 0,0042] |
| IndoBERT | O4 MILD | 0,1727 | [0,1519; 0,1927] |
| IndoBERT | O4 STRONG | 0,3282 | [0,3077; 0,3478] |

CI Char-CNN yang mencakup nol konsisten dengan drop yang sangat kecil pada beberapa kondisi. CI IndoBERT O4 jauh dari nol dan menunjukkan degradasi besar pada subset uji ini. Interval di atas adalah ketidakpastian estimasi drop per model-kondisi; ini **bukan** pengujian statistik langsung bahwa satu model lebih baik daripada model lain. Belum ada uji perbedaan antar-model atau eksperimen multi-seed.

## W. Error analysis — AI-assisted text-only first pass

Artefak `reports/stage11/primary/error_review_candidates.csv` berisi 113 kandidat terpilih secara deterministik untuk dua transisi: *evasion false negative* dan *new false positive*. Semua kandidat kini memiliki `proposed_semantic_category`, `representation_failure_hypothesis`, `reviewer_notes`, dan status `AI_ASSISTED_REVIEWED`.

Kategori membedakan klaim winnings/withdrawal, offer/CTA, testimoni layanan, endorsement brand, penyebutan brand yang masih kontekstual, dan komentar non-promosi seperti game/esports, tanggapan video, salam, anti-judi, atau komentar singkat. **Gold label tidak diubah.** 

Ini adalah review awal berbantuan AI dan berbasis teks yang tersedia, bukan adjudikasi manusia independen: riwayat thread/video, pedoman anotasi per sumber, dan alasan label dataset asal tidak semuanya tersedia di antrean. Catatan setiap contoh menyatakan batas tersebut. Gunakan kategorisasi untuk memandu error analysis; konfirmasikan contoh penting terhadap pedoman pelabelan dan konteks sumber sebelum menggunakannya sebagai bukti semantik final pada skripsi.

Hipotesis representasi diperlakukan sebagai hipotesis, bukan penyebab kausal yang terbukti. Untuk SVM, periksa fitur unigram/bigram dan pengaruh spasi/Unicode; untuk Char-CNN, periksa pola n-gram karakter dan truncation; untuk IndoBERT, periksa token IDs/subword segmentation serta prediksi pasangan asli-obfuscated. Skrip analisis sekarang mempertahankan anotasi review ketika laporan numerik dihasilkan ulang.

Hipotesis yang sudah konsisten dengan pola agregat dan perlu diuji pada contoh nyata:
- **Linear SVM + word-level TF-IDF:** pemisahan token dan perubahan ejaan dapat merusak pencocokan unigram/bigram penting; O3 STRONG memiliki drop tertinggi SVM (0,0940).
- **Char-CNN + representasi karakter:** F1 tetap dekat dengan kondisi paired-clean pada semua keluarga; perlu memilih kasus error yang tersisa untuk memeriksa batas n-gram karakter, truncation, atau konteks yang lebih luas.
- **IndoBERT + subword tokenizer:** O4 memiliki drop sangat besar dan kenaikan false-positive; evaluasi contoh harus menguji fragmentasi token/Unicode, bukan sekadar menyatakan arsitektur sebagai penyebab tanpa memeriksa tokenisasi serta teks.

## X–Y. Evaluasi OOD dan external-source

Dataset kandidat pada manifest Stage 11 tercatat sebagai berikut:

| Set | Ukuran | Non-Promotion | Promotion | Peran |
|---|---:|---:|---:|---|
| DS3 OOD isolated | 2.689 | 2.653 | 36 | OOD / domain shift sekunder |
| DS5 external isolated | 3.999 | 1.167 | 2.832 | External-source supplementary |

Angka tersebut adalah nilai dalam manifest kandidat; skrip inference akan memeriksa hash, jumlah baris, serta distribusi label sebelum prediksi. Dataset tidak boleh dimasukkan ke primary training maupun dipakai untuk tuning. Teks `text_raw` diteruskan apa adanya, tanpa normalisasi tambahan.

Ada blocker provenance penting: manifest mencatat SHA-256 DS5 raw saat ini `06de9f634fca8690a9dcca74b7ffe1b67abdccbc7b15cf4795a9750c07767d72`, sedangkan hash sumber DS5 resmi yang tersimpan di manifest adalah `8e31db1a338cfb7ac1df69b67149af0a28796908691718ca6e1b7ce581412529`. Karena tidak sama, skrip persiapan sekarang harus menghentikan rebuild sebelum menimpa kandidat. Pulihkan sumber resmi terlebih dahulu dan validasi kandidat CSV terhadap hash manifest.

Artefak prediksi dan metrik domain-shift tersedia untuk ketiga model pada kedua dataset (DS3 OOD dan DS5 eksternal), dengan 6/6 kombinasi tercatat di `reports/stage11/domain_shift/`. Bobot `model.safetensors` IndoBERT sengaja tidak disimpan di Git karena ukurannya besar; bobot tersebut digunakan dari lingkungan eksekusi eksternal. SHA-256 konfigurasi tetap wajib diverifikasi sebelum inference baru. Validasi artefak tersimpan tidak mensyaratkan bobot model tersedia di clone.

### Hasil Evaluasi Domain-Shift Lengkap

| Dataset | Model | Precision | Recall | F1 Promotion | Macro F1 | Accuracy | TN | FP | FN | TP |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **DS3 OOD** (n=2.689) | Linear SVM | 0,1754 | 0,2778 | 0,2151 | 0,6006 | 0,9729 | 2.606 | 47 | 26 | 10 |
| | Char-CNN | 0,8333 | 0,2778 | 0,4167 | 0,7057 | 0,9896 | 2.651 | 2 | 26 | 10 |
| | IndoBERT | 0,6500 | 0,3611 | **0,4643** | **0,7293** | 0,9888 | 2.646 | 7 | 23 | 13 |
| **DS5 Eksternal** (n=3.999) | Linear SVM | 0,9911 | 0,7458 | 0,8511 | 0,8038 | 0,8152 | 1.148 | 19 | 720 | 2.112 |
| | Char-CNN | 0,9982 | 0,5812 | 0,7347 | 0,6983 | 0,7027 | 1.164 | 3 | 1.186 | 1.646 |
| | IndoBERT | 0,9924 | 0,9198 | **0,9547** | **0,9288** | **0,9382** | 1.147 | 20 | 227 | 2.605 |

**Temuan Domain Shift:**
- Pada **DS3 OOD** (distribusi sangat imbalanced, hanya 36 promosi dari 2.689 komentar live streaming YouTube): seluruh model mengalami drop recall yang signifikan. Namun, IndoBERT mempertahankan performa tertinggi (F1 = 0,4643), diikuti oleh Char-CNN (0,4167, dengan presisi tinggi 83,3%), sedangkan Linear SVM mengalami banyak false positive (F1 = 0,2151).
- Pada **DS5 Eksternal** (3.999 komentar YouTube dari domain berbeda dengan rasio promosi tinggi): IndoBERT menunjukkan kemampuan generalisasi lintas domain terbaik dengan F1 mencapai **0,9547** dan recall **0,9198**. Linear SVM mencapai F1 0,8511, sedangkan Char-CNN mengalami drop recall (58,12%, FN = 1.186) sehingga F1 berada pada 0,7347 meskipun presisinya sangat tinggi (99,82%).

## Kesimpulan Akhir Tahap 11

1. **Performa Absolut vs Robustness Perturbasi:**
   - Char-CNN unggul pada performa absolut clean-test (F1 = 0,9786) dan sangat tahan terhadap manipulasi level karakter/ortografi (mean retention 99,62%, mean F1 drop hanya 0,0037).
   - IndoBERT memiliki performa clean-test yang kuat (F1 = 0,9605), namun sangat rentan terhadap manipulasi ortografi Unicode O4 (drop hingga 0,3282 pada O4 STRONG).
   - Linear SVM mengalami degradasi terbesar pada pemisahan spasi/token O3 (drop 0,0940 pada O3 STRONG).

2. **Performa Generalisasi Domain Shift (OOD & Eksternal):**
   - Ketika berhadapan dengan pergeseran domain semantik (bukan sekadar perturbasi teks), IndoBERT terbukti paling tangguh dan adaptif, memimpin baik pada DS3 OOD (F1 = 0,4643) maupun DS5 eksternal (F1 = 0,9547).
   - Char-CNN memiliki presisi yang sangat konservatif/tinggi pada domain baru, namun mengalami penurunan recall yang tajam karena ketergantungan pada pola karakter in-domain.

3. **Status Penyelesaian:**
   - Output numerik primary robustness, paired bootstrap CI 95% (10.000 resamples), 113 anotasi awal error berbantuan AI, dan prediksi/metrik domain shift untuk 3 model × 2 dataset tersedia.
- Validator artefak Tahap 11 dan tes fokus telah ditambahkan. Status pass/fail harus diambil dari hasil workflow aktual; laporan historis 95 test passed tidak dianggap sebagai rerun independen oleh perubahan ini.
- Hash train/validation dan hash raw DS5 tetap menjadi caveat reproduksibilitas yang terdokumentasi; keduanya tidak boleh “diperbaiki” dengan mengganti hash atau menimpa data frozen. Bobot IndoBERT sengaja eksternal dan bukan blocker untuk validasi prediksi/metrik tersimpan.


### Automated validation record (17 October 2026)

The primary tables were regenerated from the committed Stage 10 prediction files using seed 42 and 10,000 paired-bootstrap resamples. GitHub Actions run [#38949243961](https://github.com/khairys/TugasAkhir/actions/runs/38949243961) completed successfully: the artifact validator returned `PASSED` with 0 errors, and all four tests in `tests/stage11` passed. This run validates saved Stage 11 artifacts; it does not represent fresh model inference, full-repository `pytest tests/`, or complete retraining reproducibility from a clean clone. DS5 source provenance and train/validation split hashes remain explicitly documented caveats.
