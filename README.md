# Online Gambling Promotion Detection — Robustness Study

Repositori penelitian ini mengevaluasi ketahanan model klasifikasi komentar YouTube berbahasa Indonesia terhadap penyamaran teks terkontrol.

## Model utama

Perbandingan utama dikunci pada tiga sistem model: Linear SVM dengan word-level TF-IDF, Char-CNN berbasis karakter, dan baseline IndoBERT fine-tuned yang terpilih. Versi pelatihan IndoBERT lain tidak dihitung sebagai model utama keempat.

## Mulai dari sini

1. [Keputusan pemilihan model](docs/research/MODEL_SELECTION_DECISION.md)
2. [Hasil utama Tahap 10](docs/research/FINAL_RESULTS.md)
3. [Analisis robustness Tahap 11](docs/research/STAGE11_ROBUSTNESS_ANALYSIS.md)
4. [Rencana analisis lanjutan](docs/research/FUTURE_ANALYSIS_PLAN.md)
5. [Checklist eksekusi Tahap 11](docs/handoff/STAGE11_EXECUTION_CHECKLIST.md)
6. [Handoff pembimbing](docs/handoff/SUPERVISOR_HANDOFF.md)
7. [Panduan reproduksibilitas](docs/handoff/REPRODUCIBILITY_GUIDE.md)
8. [Spesifikasi obfuscation](docs/research/OBFUSCATION_SPECIFICATION_V1.md)
9. [Audit dataset dan pedoman label](docs/data/DATASET_AUDIT_REPORT.md)

## Struktur riset

- `configs/`: registry tiga model dan kontrak evaluasi beku.
- `data/raw/`: sumber dataset asli untuk provenance.
- `data/audit/`: laporan kualitas, overlap, dan integritas sumber.
- `data/splits/v1/`: split train/validation/test dan manifest beku.
- `data/processed/`: test normal, delapan kondisi obfuscation, dan kandidat evaluasi domain-shift Tahap 11.
- `models/`: konfigurasi dan artefak model terpilih.
- `scripts/training/`: entrypoint pelatihan model utama.
- `scripts/evaluation/`: evaluasi Stage 10 dan inference-only untuk DS3 OOD / DS5 external.
- `scripts/analysis/`: analisis robustness serta persiapan dataset domain-shift.
- `reports/stage10/`: prediksi dan hasil evaluasi utama yang telah disimpan.
- `reports/stage11/`: hasil analisis utama dan evaluasi domain-shift ketika skrip dijalankan.
- `docs/`: metode, hasil riset, audit, dan handoff.

## Analisis utama Tahap 11

Jalankan dari root repositori: `python scripts/analysis/stage11_robustness_analysis.py`. Skrip ini tidak melatih ulang model; skrip menggunakan prediksi Tahap 10 yang tersimpan, memasangkan baris berdasarkan ID, menghitung metrik hanya pada pasangan `changed == True`, melakukan 10.000 stratified paired bootstrap resamples, menulis matriks keluarga obfuscation dan analisis severity, serta membuat antrean contoh error yang belum direview manual.

Evaluasi domain-shift bersifat sekunder dan inference-only. Contoh menjalankan model yang artefaknya tersedia pada kedua dataset: `python scripts/evaluation/stage11_domain_shift.py --dataset both --models linear_svm char_cnn --device auto`. Runner menggabungkan hasil per model secara aman agar evaluasi lokal SVM tidak tertimpa ketika model neural dijalankan di GPU terpisah. Jalankan IndoBERT setelah bobot terpilih tersedia dan lolos SHA-256 verification.

## Temuan utama saat ini

Pada clean test, F1 Promotion adalah 0,9428 untuk Linear SVM, 0,9786 untuk Char-CNN, dan 0,9605 untuk IndoBERT. Dari delapan kondisi obfuscation, rata-rata F1 drop (ΔF1 bertanda) pada pasangan adalah 0,0569 untuk Linear SVM, 0,0037 untuk Char-CNN, dan 0,0839 untuk IndoBERT. Dua konsep ini dilaporkan terpisah; tidak ada satu ranking gabungan.

## Batasan reproduksibilitas

- File train/validation yang sedang dilacak Git belum cocok dengan hash manifest split yang dibekukan.
- Bobot IndoBERT `model.safetensors` yang diharapkan belum tersedia di Git.
- Hash sumber DS5 raw yang sekarang tercatat berbeda dari hash resmi sumber DS5 pada manifest Tahap 11. Skrip rebuild sekarang berhenti sebelum menulis ulang kandidat dataset jika hash sumber tidak cocok.
- Analisis utama dan evaluasi domain-shift belum dijalankan kembali secara lokal pada checkout setelah perubahan kode ini. Jangan menyatakan seluruh tahap selesai sebelum output, hash, dan tests diverifikasi.
