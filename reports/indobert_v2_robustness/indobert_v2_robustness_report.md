# LAPORAN EVALUASI KETAHANAN INDOBERT V2 & KOMPARASI MULTI-MODEL
## Linear SVM vs Character-level CNN vs IndoBERT v1 vs IndoBERT v2

**Tanggal Pengujian**: 2026-10-13 19:19:13  
**Metodologi**: Protokol Resmi Stage 10 (Paired Robustness pada `changed == True`, 4.116 baris per kondisi)  

---

## 1. Perbandingan Performa Baseline (Normal Test Set Tanpa Penyamaran)

| Model | F1 Promosi | Precision | Recall | Accuracy | False Positives (FP) | False Negatives (FN) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **linear_svm** | **0.9428** | 0.9721 | 0.9152 | 0.9866 | 13 | 42 |
| **char_cnn** | **0.9786** | 0.9877 | 0.9697 | 0.9949 | 6 | 15 |
| **indobert** | **0.9605** | 0.9634 | 0.9576 | 0.9905 | 18 | 21 |
| **indobert_v2** | **0.9613** | 0.9692 | 0.9535 | 0.9908 | 15 | 23 |

---

## 2. Perbandingan Ketahanan Berpasangan Lintas 8 Kondisi Penyamaran (Paired F1 & Retensi)

| Kondisi | Linear SVM (F1 / Retensi) | Char-CNN (F1 / Retensi) | IndoBERT v1 (F1 / Retensi) | IndoBERT v2 (F1 / Retensi) | Pemenang Kondisi |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **O1_MILD** | 0.9137 (96.7%) | **0.9766 (99.6%)** | 0.9386 (97.5%) | 0.9350 (97.0%) | **Char-CNN** |
| **O1_STRONG** | 0.8749 (92.6%) | **0.9608 (98.0%)** | 0.8617 (89.5%) | 0.8441 (87.5%) | **Char-CNN** |
| **O2_MILD** | 0.9154 (96.9%) | **0.9792 (99.9%)** | 0.9558 (99.5%) | 0.9446 (98.3%) | **Char-CNN** |
| **O2_STRONG** | 0.8734 (92.5%) | **0.9785 (99.9%)** | 0.9424 (98.1%) | 0.9206 (95.8%) | **Char-CNN** |
| **O3_MILD** | 0.9099 (96.2%) | **0.9782 (99.8%)** | 0.9588 (99.8%) | 0.9404 (97.8%) | **Char-CNN** |
| **O3_STRONG** | 0.8498 (90.0%) | **0.9806 (100.1%)** | 0.9396 (97.8%) | 0.9093 (94.6%) | **Char-CNN** |
| **O4_MILD** | 0.9039 (95.8%) | **0.9776 (99.8%)** | 0.7878 (82.0%) | 0.8183 (85.1%) | **Char-CNN** |
| **O4_STRONG** | 0.8596 (91.1%) | **0.9786 (99.9%)** | 0.6323 (65.8%) | 0.6648 (69.2%) | **Char-CNN** |

---

## 3. Analisis Mendalam: IndoBERT v2 vs IndoBERT v1

| Kondisi | F1 IndoBERT v1 | F1 IndoBERT v2 | Perubahan F1 (ΔF1 v2 vs v1) | FP Flips v1 | FP Flips v2 | Evasion Flips v1 | Evasion Flips v2 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **O1_MILD** | 0.9386 | 0.9350 | **-0.0037** | 26 | 24 | 0 | 14 |
| **O1_STRONG** | 0.8617 | 0.8441 | **-0.0176** | 91 | 109 | 18 | 34 |
| **O2_MILD** | 0.9558 | 0.9446 | **-0.0112** | -7 | 1 | 11 | 20 |
| **O2_STRONG** | 0.9424 | 0.9206 | **-0.0218** | -8 | 1 | 24 | 43 |
| **O3_MILD** | 0.9588 | 0.9404 | **-0.0183** | -1 | 6 | 3 | 27 |
| **O3_STRONG** | 0.9396 | 0.9093 | **-0.0303** | -4 | 0 | 23 | 59 |
| **O4_MILD** | 0.7878 | 0.8183 | **+0.0304** | 224 | 177 | 0 | 6 |
| **O4_STRONG** | 0.6323 | 0.6648 | **+0.0325** | 521 | 450 | 0 | 7 |