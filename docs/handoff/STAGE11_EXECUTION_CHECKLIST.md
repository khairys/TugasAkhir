# Checklist Validasi dan Penutupan Tahap 11

Tanggal pembaruan: 17 Oktober 2026  
Branch sasaran: stage11-robustness-analysis

## A. Primary robustness analysis

- [x] Prediksi Tahap 10 yang tersimpan digunakan untuk tiga model dan delapan kondisi; tidak ada training ulang atau tuning terhadap frozen test.
- [x] Artefak utama tersedia: absolute performance (3 model), condition-level metrics (24 pasangan), robustness summary (3 model), family matrix (3 model), severity analysis (12 pasangan), dan paired bootstrap intervals (24 pasangan).
- [x] Review awal berbantuan AI terhadap 113 kandidat dilengkapi kategori semantik usulan, hipotesis representasi, catatan batas konteks, dan status AI_ASSISTED_REVIEWED.
- [x] Skrip analisis mempertahankan kolom review ketika laporan numerik dibuat ulang.
- [x] Gold label dan prediksi frozen tidak diubah oleh review.

## B. OOD / external-source evaluation

- [x] Kandidat DS3 OOD dan DS5 external tetap frozen; hash, jumlah baris, dan distribusi label tercatat dalam manifest.
- [x] Artefak prediksi/metrik tersimpan untuk seluruh enam kombinasi model-dataset (3 model × 2 dataset).
- [x] Confusion-matrix counts, precision, recall, F1, dan hash kandidat diperiksa oleh validator.
- [x] DS3/DS5 tetap evaluasi sekunder; tidak digunakan untuk training, fine-tuning, threshold selection, atau tuning.
- [x] Perbedaan hash raw-source DS5 dengan hash resmi dicatat sebagai caveat provenance; kandidat frozen tidak boleh dibangun ulang atau ditimpa sebelum provenance direkonsiliasi.

## C. Verifikasi artefak dan tes

- [x] Ditambahkan scripts/validation/validate_stage11_artifacts.py untuk memeriksa hash kandidat, row count, distribusi label, unique IDs, metrik, prediction files, dan kolom review.
- [x] Ditambahkan tests/stage11/test_stage11_artifacts_validator.py.
- [x] Ditambahkan workflow GitHub Actions untuk menjalankan validator dan tes fokus pada branch Tahap 11.
- [ ] Periksa hasil run GitHub Actions setelah commit ini; tandai tes lulus hanya jika run aktual berstatus sukses.
- [ ] Jika validator menemukan error, perbaiki akar masalah pada artefak/skrip terkait; jangan melonggarkan hash atau assertion agar tes terlihat hijau.

## D. Caveat yang dipertahankan secara eksplisit

- Bobot IndoBERT sengaja tidak masuk Git karena ukuran file. Ini bukan blocker untuk memeriksa hasil prediksi/metrik tersimpan; inference baru membutuhkan artefak eksternal dengan SHA-256 sesuai konfigurasi.
- Hash train/validation pada checkout belum sama dengan hash di split manifest resmi. Ini caveat reproduksibilitas training/validation Tahap 8–10, bukan bukti otomatis bahwa tabel hasil tersimpan salah. Pulihkan snapshot resmi sebelum mengklaim reproduksi training end-to-end.
- Hash raw DS5 belum cocok dengan hash resmi. Validasi kandidat DS5 frozen terpisah dari validasi sumber mentah; jangan rebuild dataset dari sumber yang belum direkonsiliasi.
- Review 113 kandidat adalah review awal berbantuan AI yang hanya menggunakan teks dalam file; bukan adjudikasi manusia independen atau bukti kausal. Konfirmasikan contoh yang dipakai dalam pembahasan skripsi dengan pedoman label dan konteks sumber jika tersedia.

## Status penutupan

Tahap 11 dapat dinyatakan selesai untuk **analisis dan pelaporan berbasis artefak tersimpan** setelah validator dan tes fokus pada branch ini sukses. Hal itu tidak menyatakan inference baru, training ulang, atau reproduksi end-to-end dari clone bersih telah dilakukan.
