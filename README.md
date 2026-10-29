# [ARSIP] Tugas Akhir — Riwayat Lengkap Penelitian

> **Repositori ini adalah arsip.** Versi final penelitian ada di **[khairys/TugasAkhir-Robustness](https://github.com/khairys/TugasAkhir-Robustness)** (tag `v1.0-thesis-freeze`). Gunakan repositori final itu untuk kode, data, dan hasil yang dipakai di skripsi.

**Penelitian:** Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Penyamaran Teks pada Komentar YouTube  
**Peneliti:** Gathan Khairy (Universitas Diponegoro)

## Isi arsip

Repositori ini menyimpan seluruh jejak pengerjaan, termasuk bagian yang tidak masuk ke versi final:

| Branch | Isi |
|---|---|
| `main` | Kondisi per 13 Oktober 2026, termasuk percobaan IndoBERT v2 |
| `stage10-supervisor-handoff` | Handoff evaluasi ketahanan (Stage 10) |
| `stage11-robustness-analysis` | Analisis statistik dan evaluasi pergeseran domain (Stage 11) — kondisi paling lengkap |
| `literature-extraction` | Ekstraksi 21 publikasi referensi |

Yang hanya ada di arsip ini:

- **Evaluasi pergeseran domain** pada dataset Yaemico (live chat, "DS3") dan Ferdiansakti ("DS5"): di luar cakupan versi final (Master Research Blueprint V5).
- **IndoBERT v2** (percobaan pelatihan kedua dengan epoch lebih banyak): tidak dipakai di versi final.

## Catatan penting: IndoBERT v2

Skor validasi IndoBERT v2 yang tercatat di notebook Colab (F1 ≈ 0,118) **tidak valid**. Notebook itu memakai `group_by_length=True`, sehingga urutan prediksi validasi tidak sama dengan urutan label. Bila dinilai ulang dengan urutan yang benar, F1 validasi v2 adalah 0,9624. Akibatnya, pemilihan kandidat v2 tidak bisa dipakai. Model IndoBERT di versi final adalah checkpoint pertama (SHA-256 bobot `890dd84c…`), yang tidak terkena bug ini.

## Penamaan

Arsip ini memakai penomoran lama ("Stage 7–11", DS1–DS5). Pemetaan ke nama di versi final ada di [`docs/GLOSARIUM_DAN_PEMETAAN_NAMA.md`](https://github.com/khairys/TugasAkhir-Robustness/blob/main/docs/GLOSARIUM_DAN_PEMETAAN_NAMA.md) pada repositori final.
