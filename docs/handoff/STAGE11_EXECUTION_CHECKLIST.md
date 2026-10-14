# Checklist Eksekusi Tahap 11

## A. Primary robustness analysis

- [ ] Pastikan prediction files Tahap 10 tersedia untuk tiga model × NORMAL dan delapan kondisi.
- [ ] Jalankan `python scripts/analysis/stage11_robustness_analysis.py`.
- [ ] Periksa `reports/stage11/primary/analysis_snapshot_manifest.json` dan pastikan tiap input hash tercatat.
- [ ] Verifikasi 3 baris absolute performance, 24 baris condition-level metrics, 12 baris severity analysis, dan CI bootstrap 95%.
- [ ] Laporkan clean-test F1 terpisah dari mean paired F1 drop / retention; jangan buat skor gabungan atau ranking tunggal.
- [ ] Review contoh error yang dipilih secara deterministik; isi kategori semantik, hipotesis representasi, catatan, dan status reviewer. Jangan menganggap antrean kandidat sebagai anotasi final.

## B. OOD / external-source evaluation

- [ ] Verifikasi SHA-256 dataset DS3 dan DS5 dengan `data/processed/stage11/manifest_v1.json`.
- [ ] DS3 OOD target: 2.689 baris, 2.653 Non-Promotion, 36 Promotion.
- [ ] DS5 external target: 3.999 baris, 1.167 Non-Promotion, 2.832 Promotion.
- [ ] Jangan rebuild DS5 dari raw input saat ini sebelum sumber resmi dipulihkan: hash file saat ini tidak sama dengan hash resmi dalam manifest.
- [ ] Jalankan SVM di local: `python scripts/evaluation/stage11_domain_shift.py --dataset both --models linear_svm --device cpu`.
- [ ] Jalankan Char-CNN di lingkungan yang artefaknya tersedia: `python scripts/evaluation/stage11_domain_shift.py --dataset both --models char_cnn --device cuda` (gunakan `cpu` jika CUDA tidak tersedia).
- [ ] Pulihkan bobot IndoBERT, verifikasi SHA-256 yang dikunci di `configs/evaluation/stage10_robustness.json`, lalu jalankan `python scripts/evaluation/stage11_domain_shift.py --dataset both --models indobert --device cuda`.
- [ ] Periksa `reports/stage11/domain_shift/domain_shift_metrics.csv` dan `run_status.json`. File metrics menggabungkan hasil antar-run lokal/cloud berdasarkan dataset dan model.
- [ ] Pastikan DS3/DS5 hanya untuk inference/evaluasi: jangan training, fine-tune, memilih threshold, atau tuning pada dua set tersebut.

## C. Integritas dan pelaporan

- [ ] Jangan ubah hash manifest train/validation untuk menghilangkan mismatch. Pulihkan snapshot beku dahulu.
- [ ] Jalankan `python scripts/evaluation/robustness.py --mode preflight`, `python scripts/evaluation/validate_results.py`, dan `pytest tests/` di checkout terbaru.
- [ ] Tandai tahap selesai hanya saat output analisis, review manual, domain inference yang memang dikerjakan, integrity checks, dan status tes terdokumentasi. Inference IndoBERT yang belum dijalankan tidak boleh dilaporkan sebagai hasil.
