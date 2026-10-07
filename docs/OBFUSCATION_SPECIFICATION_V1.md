# SPESIFIKASI FORMAL PENYAMARAN TEKS (TEXT OBFUSCATION) v1

**Judul Penelitian:**  
*Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Penyamaran Teks pada Komentar YouTube Bahasa Indonesia*

**Repositori:** `https://github.com/khairys/TugasAkhir`  
**Pipeline State:** `Stage 7 — Obfuscation Design & Pilot Validation (Completed & Frozen)`  
**Status Spesifikasi:** **`FROZEN_V1`**  
**Global Seed:** `42`

---

## 1. Tujuan Penelitian (Research Purpose)
Penelitian ini bertujuan untuk mengevaluasi ketahanan (*robustness*) model klasifikasi teks (Linear SVM, Character-level CNN, dan IndoBERT) dalam mendeteksi komentar promosi judi online pada platform YouTube berbahasa Indonesia ketika teks komentar mengalami penyamaran (*text obfuscation*).

Penyamaran teks dalam eksperimen ini berfungsi sebagai **kondisi pengujian evaluasi (*evaluation condition*)**, bukan langkah prapemrosesan (*preprocessing*). Model dilatih menggunakan data normal/alami (*clean training data*), kemudian diuji menggunakan pasangan uji:
1. **Normal Test Set**: Komentar asli tanpa manipulasi buatan.
2. **Obfuscated Test Set**: Komentar yang persis sama namun dikenai transformasi penyamaran terkontrol (*controlled perturbations*).

Degradasi performa ($F_1\text{-score}$, presisi, *recall*) antara kondisi Normal vs Obfuscated menjadi ukuran kuantitatif ketahanan model.

---

## 2. Definisi Penyamaran Teks (Definition of Obfuscation)
Dalam konteks deteksi promosi judi online berbahasa Indonesia, penyamaran teks (*text obfuscation*) didefinisikan sebagai:
> *Modifikasi representasi ortografis dan leksikal pada tingkat karakter atau batas kata (token boundary) yang dirancang untuk mengelabui filter pencarian berbasis kata kunci atau model deteksi otomatis, tanpa menghilangkan maksud komunikatif dasar bagi pembaca manusia.*

Batasan tegas:
* **Bukan parafrase:** Tidak diperbolehkan mengganti kata dengan sinonim, merangkum, menerjemahkan, atau menggunakan LLM untuk menulis ulang kalimat.
* **Bukan de-obfuscation:** Teks masukan tidak boleh dinormalisasi sebelum ditransformasi.
* **Operasi murni berbasis string/karakter:** Transformasi hanya diterapkan langsung pada representasi string asli (`text_raw`).

---

## 3. Taksonomi Penyamaran: O1 — Character Substitution
* **Tujuan:** Mengganti karakter huruf tertentu dengan karakter angka atau simbol visual yang mirip (*leetspeak/visual similarity*), menyerupai trik spambot di YouTube (misal `situs` $\rightarrow$ `s1tu5`).
* **Kamus Substitusi Baku:**
  ```python
  CHAR_SUBSTITUTION_MAP = {
      "a": "4", "A": "4",
      "e": "3", "E": "3",
      "i": "1", "I": "1",
      "o": "0", "O": "0",
      "s": "5", "S": "5",
      "t": "7", "T": "7",
      "g": "9", "G": "9",
      "b": "8", "B": "8",
  }
  ```
* **Aturan:**
  * Hanya karakter yang terdaftar secara eksplisit yang boleh diganti.
  * Tidak ada substitusi rekursif (karakter hasil substitusi tidak diganti ulang).
  * Pemilihan token dan posisi karakter dilakukan secara deterministik menggunakan generator acak terikat seed.

---

## 4. Taksonomi Penyamaran: O2 — Character Insertion / Deletion
* **Tujuan:** Menguji ketahanan model terhadap salah eja (*typos*) yang disengaja atau pengelabuan berbasis jarak edit leksikal.
* **Operasi Terkendali:**
  1. **Insertion (Duplikasi):** Menyisipkan satu karakter duplikat pada posisi internal kata (misal `gacor` $\rightarrow$ `gaccor`).
  2. **Deletion (Penghapusan):** Menghapus satu karakter internal kata (misal `sekarang` $\rightarrow$ `sekrang`).
* **Aturan Keamanan Preservasi:**
  * Karakter pertama dan karakter terakhir dari kata **dilarang dihapus**.
  * Penghapusan hanya diizinkan jika panjang alfanumerik kata $\ge 5$, sehingga panjang kata setelah penghapusan tetap $\ge 4$.
  * Maksimal satu operasi (insersi atau delesi) per token terpilih.
  * Token tidak boleh dirusak berulang-ulang.

---

## 5. Taksonomi Penyamaran: O3 — Whitespace Manipulation
* **Tujuan:** Menguji ketahanan segmentasi kata dan pembagian token (*token boundary perturbation*), di mana pembuat spam menyisipkan spasi di tengah kata agar luput dari kamus kata terlarang (misal `situs` $\rightarrow$ `s itus` atau `gacor` $\rightarrow$ `ga cor`).
* **Aturan:**
  * Spasi normal tunggal disisipkan di antara dua karakter alfanumerik internal dalam satu token yang memenuhi syarat.
  * Dilarang memecah URL, alamat email, *mention* `@`, atau *hashtag* `#`.
  * Tidak diperbolehkan melakukan *whitespace normalization* setelah transformasi; spasi yang disisipkan harus tetap ada sebagai representasi penyamaran.

---

## 6. Taksonomi Penyamaran: O4 — Unicode / Orthographic Manipulation
* **Tujuan:** Menguji ketahanan representasi sub-word tokenizer (pada IndoBERT) dan ekstraksi n-gram karakter (pada Char-CNN & SVM) terhadap karakter homoglif visual dan perpanjangan fonetis (*elongation*).
* **Dua Sub-mekanisme Terkendali:**
  1. **Unicode Confusable Homoglyph Substitution:** Mengganti karakter huruf Latin dengan karakter Cyrillic yang identik secara visual:
     ```python
     UNICODE_CONFUSABLE_MAP = {
         "a": "\u0430", "A": "\u0410",
         "c": "\u0441", "C": "\u0421",
         "e": "\u0435", "E": "\u0415",
         "o": "\u043E", "O": "\u041E",
         "p": "\u0440", "P": "\u0420",
         "x": "\u0445", "X": "\u0425",
     }
     ```
  2. **Orthographic Elongation (Pemanjangan Huruf Vokal):** Jika token tidak memiliki karakter yang terdaftar pada peta homoglif Cyrillic, dilakukan duplikasi huruf vokal (`a, i, u, e, o`) untuk meniru gaya bahasa santai/slang (misal `bagus` $\rightarrow$ `baguus`).

---

## 7. Tingkat Keparahan (Severity Levels)
Implementasi membagi penyamaran ke dalam 3 level terkontrol:

1. **Level 0 — NORMAL (Kontrol Negatif):**
   * `text_obfuscated == text_original`
   * `changed = False`, `modified_char_count = 0`.
2. **Level 1 — MILD (Penyamaran Ringan):**
   * Tepat 1 token yang terpengaruh per teks komentar.
   * Modifikasi karakter minimal (rasio modifikasi tipikal $\le 5\%$, batas diagnostik maksimal $20\%$).
   * Teks dijamin sangat mudah dibaca dan dipahami pembaca manusia.
3. **Level 2 — STRONG (Penyamaran Kuat):**
   * Maksimal 2 token yang terpengaruh per teks komentar.
   * Modifikasi terkontrol (rasio modifikasi tipikal $\le 10\%$, batas diagnostik maksimal $35\%$).
   * Tetap mempertahankan makna dasar tanpa merusak keterbacaan kalimat.

---

## 8. Perlindungan Token Khusus (Token Protection Rules)
Transformasi penyamaran **DILARANG KERAS** menyentuh span teks berikut:
* **URL / Tautan Web:** Cocok dengan regex `(https?://\S+|www\.\S+)`.
* **Alamat Email:** Cocok dengan regex `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b`.
* **User Mentions & Hashtags:** Token berawalan `@` atau `#`.
* **Angka Murni (*Standalone Numbers*):** Misal `100000`, `2024`.
* **Emoji Murni / Tanda Baca Murni:** Token tanpa karakter alfanumerik.
* **Token Pendek:** Token dengan jumlah karakter alfanumerik $< 4$ (misal `di`, `ke`, `yg`, `ya`).

---

## 9. Mekanisme Keacakan Deterministik (Deterministic Seeding)
Untuk menjamin keterulangan eksperimen (*strict reproducibility*), generator tidak menggunakan seed global acak, melainkan menghitung *seed integer unik* per rekaman menggunakan fungsi hash SHA-256:
```python
payload = f"{seed}|{source_record_id}|{family}|{severity}"
digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
integer_seed = int(digest[:16], 16)
rng = random.Random(integer_seed)
```
Dengan mekanisme ini:
* Menjalankan ulang script pada sistem operasi mana pun dengan seed 42 menghasilkan teks penyamaran yang 100% identik *byte-for-byte*.
* Pemilihan posisi transformasi bersifat independen antar-keluarga dan antar-rekaman.

---

## 10. Prinsip Preservasi Label (Label Preservation Principle)
Untuk setiap pasangan data:
$$\text{canonical\_label}(\text{text\_obfuscated}) \equiv \text{canonical\_label}(\text{text\_original})$$
* Generator penyamaran bersifat **label-agnostic** (tidak melihat apakah teks berlabel 0 atau 1 saat mentransformasi).
* Label kanonikal tidak pernah diubah secara otomatis oleh script.

---

## 11. Persyaratan Preservasi Semantik (Semantic Preservation Requirement)
Penyamaran yang berhasil adalah penyamaran yang mengelabui mesin pendeteksi tetapi **tetap dipahami oleh manusia**.
Jika suatu modifikasi merusak pesan atau mengubah fungsi komunikatif (misal mengubah kalimat promosi menjadi tidak bermakna sama sekali), maka transformasi tersebut dinyatakan tidak valid.

---

## 12. Penanganan Kasus Tanpa Target (Failure & No-Change Handling)
Jika suatu komentar sangat pendek, hanya berisi emoji, angka, atau hanya memuat token yang terlindungi:
* Generator **TIDAK MEMAKSAKAN** transformasi yang merusak.
* Generator mengembalikan:
  ```text
  changed = False
  status = "NO_CHANGE"
  failure_reason = "No eligible target or token found for transformation."
  text_obfuscated = text_original
  ```
* Kasus `NO_CHANGE` tidak boleh dihitung sebagai perturbasi yang sukses dalam evaluasi ketahanan.

---

## 13. Protokol Pilot Dataset (Stage 7)
* **Sumber Data:** Diambil secara deterministik dari `data/processed/main_pool_candidate_v2.csv` (seed=42).
* **Ukuran Sampel Pilot:** 200 rekaman unik (100 Promosi, 100 Non-Promosi).
* **Kondisi per Rekaman:** 9 kondisi:
  1. `NORMAL`
  2. `O1_CHAR_SUBSTITUTION MILD`
  3. `O1_CHAR_SUBSTITUTION STRONG`
  4. `O2_CHAR_INSERT_DELETE MILD`
  5. `O2_CHAR_INSERT_DELETE STRONG`
  6. `O3_WHITESPACE MILD`
  7. `O3_WHITESPACE STRONG`
  8. `O4_UNICODE_ORTHOGRAPHIC MILD`
  9. `O4_UNICODE_ORTHOGRAPHIC STRONG`
* **Total Baris Pilot:** $200 \times 9 = 1.800$ baris pada `data/interim/obfuscation_pilot_v1.csv`.

---

## 14. Skema Output Data
File output pilot [obfuscation_pilot_v1.csv](file:///d:/Gathan/Kuliah/TUGAS%20AKHIR/Code/data/interim/obfuscation_pilot_v1.csv) memiliki kolom:
1. `pair_id`: Identifier unik pasangan (misal `DS1_000001_O1_CHAR_SUBSTITUTION_MILD`).
2. `source_record_id`: ID rekaman asal.
3. `source_dataset`: Dataset asal (DS1, DS2, DS4).
4. `canonical_label`: Label kanonikal biner (0 atau 1).
5. `family`: Keluarga penyamaran (`NORMAL`, `O1`, `O2`, `O3`, `O4`).
6. `severity`: Tingkat keparahan (`NORMAL`, `MILD`, `STRONG`).
7. `seed`: Nilai seed global (`42`).
8. `text_original`: Teks mentah asli dari Main Pool.
9. `text_obfuscated`: Teks hasil penyamaran.
10. `changed`: Boolean (`True` jika berubah, `False` jika tidak).
11. `status`: Status eksekusi (`SUCCESS` atau `NO_CHANGE`).
12. `failure_reason`: Keterangan kegagalan jika `NO_CHANGE`.
13. `modified_char_count`: Jumlah edit karakter (jarak Levenshtein).
14. `modified_char_ratio`: Rasio edit terhadap panjang teks asli.
15. `modified_token_count`: Jumlah token yang terpengaruh.

---

## 15. Protokol dan Hasil Audit Manusia (Human Audit Completion)
Validasi preservasi makna dan label telah dilakukan secara menyeluruh terhadap seluruh **320 sampel** pada `data/review/obfuscation_pilot_review_v1.csv`:
* **Komposisi seimbang:** 4 keluarga $\times$ 2 severity (MILD, STRONG) $\times$ 2 label (0, 1) $\times$ 20 sampel = 320 sampel.
* **Hasil Verifikasi Kontekstual:**
  * `human_label_preserved`: **320/320 (100% YES)**.
  * `human_meaning_preserved`: **320/320 (100% YES)**.
  * `human_transformation_valid`: **320/320 (100% YES)**.
  * `review_status`: **APPROVED (320/320)**.
* **Temuan Audit:**
  * 160 sampel Non-Promosi (Label 0) terverifikasi murni sebagai percakapan YouTube organik (teknologi, gaming non-judi, interaksi publik, konsultasi religi anti-riba) tanpa muatan promosi judi online.
  * 160 sampel Promosi (Label 1) terverifikasi sebagai spam/ajakan/iklan judi online yang mempromosikan entitas/platform judi online (seperti Alexis17, Gunungwin, Victory007, Mona4D, Probet855, Dora77, Banteng Hoki, PSToto99, Mahakam4D, Pulau777, Weton88, dll).
  * Seluruh manipulasi karakter (O1-O4) pada tingkat MILD dan STRONG terbukti mempertahankan keterbacaan (*human readability*) bagi pembaca manusia, sementara integritas fungsi komunikasi dan label klasifikasi tidak mengalami pergeseran.
* **Status Audit:** **`AUDIT_COMPLETED_AND_APPROVED`** $\rightarrow$ Spesifikasi resmi dibekukan (**`FROZEN_V1`**).

---

## 16. Instruksi Reproducibility (Keterulangan Eksperimen)
Untuk menguji dan menjalankan ulang seluruh pipeline penyamaran:
1. **Jalankan unit tests:**
   ```bash
   pytest tests/obfuscation
```
2. **Jalankan pembuatan pilot dataset:**
   ```bash
   python scripts/13_build_obfuscation_pilot.py
```
3. **Jalankan validasi otomatis:**
   ```bash
   python scripts/14_validate_obfuscation_pilot.py
```

---

## 17. Langkah yang Ditunda untuk Stage 8 (Pending for Stage 8)
* **Official Train/Val/Test Split:** Partisi resmi data menggunakan `StratifiedGroupKFold` berbasis `leakage_group_id`.
* **Generasi Test Set Terobfuscasi Final:** Pembuatan file `test_obfuscated_final.csv`.
* **Pelatihan Model & Evaluasi:** Pelatihan Linear SVM, Character-level CNN, dan IndoBERT pada data latih normal, serta inferensi performa pada kondisi Normal Test vs Obfuscated Test.
