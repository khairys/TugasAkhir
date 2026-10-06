# MASTER INSTRUCTION

## Dataset Harmonization, Cleaning, and Quality Control

### Penelitian: Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Text Obfuscation pada Komentar YouTube Bahasa Indonesia

## 0. Tujuan Utama

Tugas agent pada tahap ini adalah membersihkan, mengharmonisasi, mengaudit, dan menyiapkan lima dataset sumber untuk penelitian NLP.

Agent TIDAK bertugas:

* melatih model;
* melakukan hyperparameter tuning;
* membuat data obfuscation sintetis;
* menentukan model terbaik;
* melakukan oversampling/SMOTE;
* melakukan stemming/stopword removal sebagai preprocessing utama;
* menghapus dataset sumber secara permanen.

Tujuan akhirnya adalah menghasilkan satu data pool yang:

1. memiliki skema kolom yang konsisten;
2. mempertahankan raw/original text;
3. memiliki label yang telah diharmonisasi terhadap definisi penelitian;
4. bebas dari duplicate persis yang dapat menyebabkan leakage;
5. memiliki informasi provenance setiap record;
6. memiliki informasi duplicate/near-duplicate family;
7. memiliki review queue untuk kasus label yang tidak dapat diputuskan secara aman;
8. siap digunakan untuk tahap train/validation/test split pada tahap berikutnya;
9. memungkinkan peneliti menjelaskan dengan jelas bagaimana setiap record masuk atau keluar dari dataset final.

Prinsip utama:

> Raw data is immutable. Processed data is derived data.

Jangan pernah mengubah file raw asli.

---

# 1. SUMBER DATASET

Gunakan lima dataset berikut sebagai RAW SOURCE POOL.

### DS1 — fahruu

Dataset:
`fahruu/komentar-judi-online`

Raw text:
`comment`

Jumlah awal:
8.440 baris.

Duplikasi persis:
1.809.

Source label:
`label`

Catatan:
Dataset relatif jelas membedakan komentar diskusi sosial dengan komentar promosi/spam judi.

---

### DS2 — kyyyy8_all

Dataset:
`kyyyy8/dataset-komentar-judi-online-di-youtube`

Raw text:
`text`

Jumlah awal:
45.592 baris.

Source label:
`label`

Dataset memiliki `text_preprocessed`, tetapi kolom tersebut BUKAN sumber text utama.

---

### DS3 — yaemico

Dataset:
`yaemico/deteksi-judi-online`

Raw text:
`message`

Jumlah awal:
6.350 baris.

Metadata:

* `datetime`
* `author_name`

Source label:
`label`

Dataset ini sangat spesifik terhadap live chat CCTV Jogja dan memiliki tingkat text duplication yang tinggi.

Jangan membuang DS3 pada tahap ini.

DS3 tetap diproses dan diaudit seperti dataset lain. Peran akhirnya sebagai training data atau OOD test ditentukan setelah harmonisasi selesai.

---

### DS4 — kyyyy8_platform

Dataset:
`kyyyy8/dataset-komentar-judi-online-platform-youtube`

Raw text:
`text`

Jumlah awal:
18.902 baris.

Metadata:

* `comment_id`
* `author`
* `time_parsed`

Source label:
`label`

Dataset ini memiliki metadata yang sangat berharga untuk leakage analysis.

---

### DS5 — ferdiansakti

Dataset:
`ferdiansakti/gambling-comments-from-youtube-platform`

Raw text:
`Comments`

Jumlah awal:
4.720 baris.

Source label:
`Label`

Dataset memiliki distribusi label yang berat ke label 1 dan banyak komentar yang berkaitan dengan kampanye `ambil4d`.

Jangan membuang dataset ini pada tahap awal.

---

# 2. STRUKTUR DATA YANG WAJIB DIBUAT

Buat canonical schema berikut.

```text
record_id
source_dataset
source_row_id

text_raw

source_label
canonical_label
label_status
label_reason
adjudication_note

author
timestamp

exact_duplicate_group
whitespace_duplicate_group
normalized_variant_group
near_duplicate_group

is_exact_duplicate
is_cross_dataset_duplicate
is_label_conflict

data_quality_status
exclusion_reason

provenance_notes
```

Tidak semua dataset memiliki seluruh informasi.

Jika field tidak tersedia, isi:

```text
NULL
```

JANGAN mengarang metadata.

Contoh:

DS1 tidak mempunyai author:
`author = NULL`

DS4 memiliki author:
`author = nilai asli`

---

# 3. RAW TEXT ADALAH SUMBER UTAMA

Gunakan:

DS1:
`comment`

DS2:
`text`

DS3:
`message`

DS4:
`text`

DS5:
`Comments`

Jangan menggunakan:

DS1:
`final_comment`

DS2:
`text_preprocessed`

DS3:
`cleaned_message`

DS4:
`text_preprocessed`

sebagai pengganti raw text.

Kolom preprocessing bawaan hanya boleh dipertahankan sebagai metadata sumber dan bahan audit.

JANGAN:

* lowercase seluruh data;
* menghapus punctuation;
* menghapus emoji;
* menghapus whitespace;
* menghapus Unicode;
* menghapus angka;
* mengganti slang;
* stemming;
* stopword removal;
* menghapus simbol;
* mengubah nama situs;
* melakukan Unicode normalization terhadap text utama.

Alasannya: penelitian ini secara khusus meneliti ketahanan terhadap text obfuscation.

Unicode, emoji, separator, angka, whitespace, punctuation, dan karakter aneh dapat merupakan bagian dari sinyal obfuscation.

---

# 4. RAW DATA IMMUTABILITY

Sebelum melakukan proses apa pun:

1. Pastikan kelima file raw dapat dibaca.
2. Simpan checksum/hash setiap file.
3. Catat:

   * filename;
   * path;
   * jumlah baris;
   * jumlah kolom;
   * nama kolom;
   * encoding;
   * checksum.
4. Jangan overwrite raw file.

Buat struktur:

```text
data/
├── raw/
│   ├── ds1_fahruu/
│   ├── ds2_kyyyy8_all/
│   ├── ds3_yaemico/
│   ├── ds4_kyyyy8_platform/
│   └── ds5_ferdiansakti/
│
├── interim/
├── processed/
├── review/
├── audit/
└── manifests/
```

---

# 5. SOURCE LABEL DAN CANONICAL LABEL HARUS DIPISAH

Jangan langsung overwrite label asli.

Gunakan:

```text
source_label
```

untuk label yang berasal dari dataset.

Gunakan:

```text
canonical_label
```

untuk label setelah harmonisasi terhadap definisi penelitian.

Gunakan:

```text
label_status
```

dengan nilai seperti:

```text
accepted
review
excluded
```

Source label tidak boleh dihapus.

---

# 6. DEFINISI LABEL PENELITIAN

Target penelitian:

```text
1 = Promotion
0 = Non-Promotion
```

Definisi kelas 1:

Komentar dikategorikan sebagai Promotion apabila fungsi komunikatif komentarnya secara langsung atau tidak langsung mendorong, memengaruhi, membujuk, meyakinkan, mengarahkan, atau mengajak orang untuk bermain, mendaftar, mencoba, mengakses, atau menggunakan layanan judi online.

Promotion mencakup, tetapi tidak terbatas pada:

### A. Explicit advertisement

Contoh:

```text
main di X
daftar X
join X
bonus 100rb
depo disini
klik link
```

### B. Call to action

Contoh:

```text
buruan daftar
yuk join
gas sekarang
ketik di google X
coba X
```

### C. Promotional claim

Contoh:

```text
gacor banget
maxwin terus
wd lancar
bonus besar
depo kecil bisa menang besar
```

### D. Testimonial / social proof

Testimonial TIDAK otomatis menjadi Non-Promotion hanya karena tidak menggunakan kata “daftar”.

Apabila testimonial memberikan endorsement atau social proof yang berfungsi untuk meyakinkan orang agar menggunakan atau bermain di platform judi tertentu, kategorikan:

```text
Promotion = 1
```

Contoh pola:

```text
baru main di X langsung menang besar
thanks X udah bikin cuan
di X wd-nya lancar banget
deposit sedikit bisa jadi banyak
```

Namun, sekadar menyebut pengalaman tanpa fungsi promosi tidak boleh otomatis dijadikan 1.

Keputusan harus berdasarkan fungsi komunikatif komentar.

### E. Brand/site endorsement

Contoh:

```text
X paling gacor
X terpercaya
X terbaik
main X aja
```

Jika konteks menunjukkan X merupakan platform judi dan komentar tersebut merupakan endorsement, label:

```text
1
```

### F. Obfuscated promotion

Promosi tetap merupakan kelas 1 meskipun kata-katanya disamarkan menggunakan:

* Unicode;
* angka;
* simbol;
* separator;
* emoji;
* whitespace;
* karakter mirip;
* intentional misspelling;
* kombinasi karakter;
* timestamp;
* variasi penulisan nama situs.

Obfuscation tidak mengubah label semantik.

---

# 7. DEFINISI NON-PROMOTION

Label 0 mencakup komentar yang tidak berfungsi mempromosikan perjudian.

Termasuk:

### A. Anti-gambling

Contoh:

```text
jangan main judi
judi merusak kehidupan
mending nabung daripada judi
```

### B. Kritik / berita / diskusi sosial

Contoh:

```text
judi online sudah meresahkan masyarakat
pemerintah harus memberantas judol
```

### C. Keluhan terhadap spammer

Contoh:

```text
jangan spam judol
komentarnya judol semua
blokir akun judi ini
```

### D. Informasi netral

Penyebutan judi tanpa ajakan/promosi.

Contoh:

```text
banyak kasus judi online sekarang
```

### E. Konteks non-judi

Jangan menggunakan keyword sebagai satu-satunya dasar.

Contoh:

```text
slot microSD
```

`slot` pada konteks tersebut bukan perjudian.

### F. Komentar biasa

Komentar YouTube yang tidak berhubungan dengan promosi judi:

```text
mantap
pertama
wkwkwk
videonya bagus
```

---

# 8. JANGAN MENGGUNAKAN KEYWORD-ONLY LABELING

JANGAN melakukan aturan:

```text
contains("slot") => Promotion
```

JANGAN melakukan:

```text
contains("judi") => Promotion
```

JANGAN melakukan:

```text
contains nama situs => Promotion
```

tanpa melihat konteks.

Audit menemukan contoh false positive seperti penggunaan `slot` untuk microSD dan komentar yang justru mengkritik spam judi.

Keyword hanya boleh digunakan sebagai sinyal untuk REVIEW.

---

# 9. LABEL CONFLICT

Situasi penting:

Jika satu raw text muncul pada dua dataset dengan label berbeda:

```text
DS2 = 1
DS4 = 0
```

jangan memilih label secara otomatis.

Lakukan:

1. Identifikasi semua source record.
2. Tampilkan raw text.
3. Tampilkan seluruh source label.
4. Tentukan canonical label berdasarkan definisi penelitian.
5. Simpan alasan keputusan.
6. Simpan seluruh provenance.

Untuk konflik DS2 vs DS4, audit telah menemukan:

```text
10.561 shared unique texts
48 conflicting labels
```

Konflik tersebut harus diperlakukan sebagai kasus adjudication.

Jangan menggunakan:

```text
DS4 always wins
```

atau:

```text
DS2 always wins
```

sebagai aturan label.

Metadata DS4 boleh diprioritaskan apabila memilih record canonical karena metadata lebih lengkap, tetapi label tetap harus ditentukan berdasarkan definisi penelitian.

---

# 10. UNCERTAIN LABEL

Jika komentar tidak dapat diputuskan secara masuk akal antara Promotion dan Non-Promotion:

```text
canonical_label = NULL
label_status = review
```

Jangan memaksakan label.

Buat:

```text
review/label_review_queue.csv
```

minimal berisi:

```text
record_id
text_raw
source_dataset
source_label
proposed_label
reason
confidence
```

Kasus uncertain lebih baik dikeluarkan sementara dari supervised training daripada dipaksa menjadi label yang tidak dapat dipertanggungjawabkan.

---

# 11. EXACT DUPLICATION

Lakukan exact duplicate detection menggunakan raw text.

Buat:

```text
exact_text_hash
```

menggunakan hash cryptographic, misalnya SHA-256.

Exact duplicate berarti raw text identik.

Untuk exact duplicates:

* jangan menyimpan ratusan copy identik sebagai independent samples;
* simpan satu canonical record;
* simpan jumlah kemunculan;
* simpan provenance seluruh source;
* simpan duplicate count.

Contoh:

```text
duplicate_count = 931
```

bukan berarti record harus muncul 931 kali di final supervised dataset.

---

# 12. WHITESPACE DUPLICATION

Buat duplicate key tambahan yang hanya melakukan transformasi konservatif:

* strip leading/trailing whitespace;
* collapse repeated whitespace.

Jangan melakukan lowercase.
Jangan melakukan Unicode normalization.
Jangan menghapus punctuation.
Jangan menghapus emoji.

Tujuannya hanya mendeteksi apakah dua teks sebenarnya sama karena perbedaan whitespace.

---

# 13. UNICODE-NORMALIZED DUPLICATION

Boleh membuat key audit tambahan menggunakan Unicode normalization.

Tetapi:

> JANGAN menggunakan key ini untuk otomatis menghapus record.

Alasan:

Dua teks dapat terlihat serupa setelah Unicode normalization tetapi secara mentah berbeda karena memang merupakan bentuk obfuscation.

Contoh:

```text
ALEXIS17
𝗔𝗟𝗘𝗫𝗜𝗦𝟭𝟳
ＡＬＥＸＩＳ１７
```

Ketiganya berpotensi merupakan bentuk obfuscation yang justru penting untuk penelitian.

Gunakan hasil ini hanya untuk:

```text
normalized_variant_group
```

dan analisis.

---

# 14. NEAR-DUPLICATE

Near-duplicate tidak boleh langsung dihapus.

Buat analisis menggunakan metode seperti:

* character n-gram similarity;
* edit distance;
* MinHash/LSH;
* cosine similarity.

Tujuan pertama adalah menemukan:

```text
duplicate/template families
```

bukan langsung menghapusnya.

Contoh:

```text
Main di X gacor banget
Main di X gacor abiss
Main di X paling gacor
```

harus dapat teridentifikasi sebagai keluarga template yang mirip.

Namun ketiga record tidak boleh otomatis dianggap sama.

---

# 15. DUPLICATE FAMILY DAN LEAKAGE

Setiap near-duplicate family harus memiliki:

```text
near_duplicate_group
```

Group ini nantinya dapat digunakan untuk memastikan kelompok teks serupa tidak tersebar secara sembarangan antara train dan test.

Ini sangat penting karena bot dapat menghasilkan banyak variasi minor dari template yang sama.

Tujuan penelitian bukan menguji apakah model bisa menghafal satu template spam.

---

# 16. CROSS-DATASET DEDUPLICATION

Deduplication harus dilakukan:

```text
within-dataset
```

dan:

```text
across-dataset
```

Jangan hanya melakukan deduplication di masing-masing CSV secara terpisah.

Jika:

```text
DS1 -> text A
DS2 -> text A
DS4 -> text A
```

maka ketiganya harus dikenali sebagai satu logical text entity.

Simpan:

```text
source_datasets = DS1;DS2;DS4
```

atau struktur provenance ekuivalen.

---

# 17. PRIORITAS UNTUK DUPLICATE RECORD

Jika beberapa dataset memiliki raw text identik dan label canonical sama:

Pilih satu canonical record.

Prioritas record boleh berdasarkan:

1. kelengkapan metadata;
2. kualitas source;
3. original/raw field;
4. kestabilan provenance.

Untuk overlap DS2 dan DS4, DS4 memiliki metadata lebih lengkap.

Namun:

> Metadata priority ≠ label priority.

Label tetap ditentukan melalui harmonisasi semantik.

---

# 18. DATA QUALITY CHECK

Untuk setiap record, periksa:

### Valid

* text bukan NULL;
* text bukan whitespace-only;
* label valid atau masuk review;
* encoding valid.

### Suspicious

Flag apabila:

* text sangat panjang;
* text sangat pendek;
* hanya emoji;
* hanya angka;
* hanya simbol;
* hanya URL;
* Unicode ekstrem;
* repeated characters ekstrem;
* whitespace ekstrem;
* karakter kontrol;
* malformed encoding.

Jangan langsung membuang suspicious record.

Buat:

```text
data_quality_flags
```

dan review distribusinya.

---

# 19. EMPTY TEXT

Jika raw text:

```text
NULL
```

atau:

```text
""
```

atau whitespace-only,

maka:

```text
data_quality_status = invalid
```

dan record tidak boleh masuk modeling dataset.

Tetapi raw record tetap harus disimpan dalam audit/quarantine.

Jangan mencoba mengambil text dari:

```text
final_comment
text_preprocessed
cleaned_message
```

untuk menggantikan raw text.

---

# 20. METADATA

Pertahankan metadata asli jika tersedia.

Contoh:

DS4:

```text
comment_id
author
time_parsed
```

DS3:

```text
author_name
datetime
```

Metadata tidak boleh digunakan sebagai input model pada penelitian utama.

Metadata digunakan untuk:

* provenance;
* leakage detection;
* grouping;
* temporal analysis;
* audit.

Jangan memasukkan:

```text
author
comment_id
timestamp
```

ke dalam text model.

---

# 21. AUTHOR LEAKAGE

Jika author metadata tersedia:

buat:

```text
author_group_id
```

Jangan menganggap seluruh author dari dataset berbeda sebagai entity yang sama hanya berdasarkan username string.

Gunakan author grouping hanya pada dataset yang benar-benar memiliki metadata author.

Pada tahap split nanti:

> komentar dari author yang sama sebaiknya tidak tersebar secara bebas antara train dan test apabila metadata cukup valid.

Tujuannya mencegah model belajar signature bot tertentu.

---

# 22. TEMPORAL INFORMATION

Untuk DS3 dan DS4, timestamp harus dipertahankan.

Buat:

```text
timestamp_standardized
```

tanpa mengubah timestamp asli.

Pertahankan:

```text
timestamp_original
```

dan:

```text
timestamp_standardized
```

Jangan membuang timestamp.

Timestamp dapat digunakan pada tahap berikutnya untuk mengevaluasi kemungkinan temporal leakage.

---

# 23. JANGAN MELAKUKAN CLASS BALANCING SEKARANG

Jangan:

* oversampling;
* undersampling;
* SMOTE;
* duplication buatan;
* random balancing.

Pertahankan distribusi hasil cleaning apa adanya.

Class balancing adalah keputusan experimental design, bukan cleaning.

---

# 24. JANGAN MEMBUAT DATA SINTETIS

Tidak boleh menghasilkan:

* synthetic comments;
* paraphrase;
* back translation;
* generated spam;
* generated non-spam;
* obfuscation variants.

Tahap ini hanya membersihkan dan mengharmonisasi data existing.

Obfuscation akan dirancang pada tahap penelitian selanjutnya.

---

# 25. KHUSUS DS1

DS1 memiliki duplicate yang cukup tinggi.

Proses:

1. preserve raw;
2. deduplicate exact;
3. lakukan label audit;
4. pertahankan variasi bahasa/slang;
5. jangan menggunakan `final_comment` sebagai text utama.

Jangan mengubah:

```text
gue
lu
bgt
udh
```

menjadi bentuk baku pada raw text.

---

# 26. KHUSUS DS2 DAN DS4

DS2 dan DS4 berasal dari uploader yang sama dan memiliki overlap sangat besar.

Perlakukan keduanya sebagai satu lineage:

```text
kyyyy8 lineage
```

Jangan memperlakukan DS2 dan DS4 sebagai dua sumber data yang benar-benar independent.

Proses:

1. cross-dataset matching;
2. identify 10.561 shared texts;
3. identify 48 conflicts;
4. adjudicate conflicts;
5. merge shared identical records;
6. preserve DS4 metadata ketika tersedia;
7. retain unique DS2 records;
8. retain unique DS4 records;
9. jangan double-count shared text.

---

# 27. KHUSUS DS3

DS3 adalah live-chat CCTV Jogja dan memiliki duplicate spam sangat tinggi.

Jangan membuangnya.

Lakukan:

1. exact dedup;
2. duplicate family analysis;
3. label audit;
4. metadata preservation;
5. domain/source tagging.

Buat field:

```text
source_domain = youtube_live_chat
```

dan pertahankan kandidat:

```text
candidate_role = OOD_candidate
```

sebagai status sementara saja.

Jangan menjadikannya OOD final secara permanen pada tahap cleaning tanpa keputusan penelitian berikutnya.

---

# 28. KHUSUS DS5

DS5 memiliki imbalance tinggi dan konsentrasi pada campaign/site tertentu.

Lakukan:

1. exact dedup;
2. template-family detection;
3. identify campaign concentration;
4. calculate site/entity frequency;
5. preserve unique examples;
6. jangan langsung menghapus seluruh record yang menyebut `ambil4d`.

Jangan melakukan:

```text
if text contains "ambil4d": drop
```

Karena nama situs sendiri tidak berarti record tersebut tidak valid.

Buat analisis:

```text
campaign/entity frequency report
```

yang menunjukkan seberapa besar dataset dipengaruhi campaign tertentu.

---

# 29. IDENTIFICATION OF GAMBLING SITE / ENTITY

Agent boleh melakukan entity extraction untuk audit.

Contoh:

```text
site/entity
```

Tetapi entity extraction bukan label.

Satu record dapat:

```text
entity = X
canonical_label = 0
```

jika komentar tersebut mengkritik X.

Contoh:

```text
X itu penipu jangan pernah main
```

Tidak otomatis menjadi Promotion.

---

# 30. LABEL AUDIT BERBASIS KATEGORI

Buat kolom tambahan:

```text
promotion_type
```

Nilai yang disarankan:

```text
explicit_ad
call_to_action
testimonial
social_proof
promotional_claim
site_endorsement
obfuscated_promotion
anti_gambling
neutral_gambling_discussion
criticism
spam_complaint
non_gambling
ambiguous
```

Kolom ini terutama untuk audit.

Jangan gunakan sebagai target utama model.

Target tetap:

```text
canonical_label
```

---

# 31. OUTLIER DAN SHORT TEXT

Jangan membuang komentar pendek hanya karena panjangnya kecil.

Contoh:

```text
gacor
wd lancar
join X
maxwin
```

dapat menjadi Promotion.

Sebaliknya:

```text
mantap
haha
gas
```

tidak otomatis Promotion.

Short text harus dinilai berdasarkan konteks dan fungsi.

---

# 32. OBFUSCATION MUST BE PRESERVED

Flag kemungkinan obfuscation apabila ditemukan:

* Mathematical Alphanumeric Unicode;
* full-width characters;
* zero-width characters;
* separator characters;
* random punctuation;
* inserted spaces;
* symbol substitution;
* digit substitution;
* deliberate spelling variation;
* emoji insertion;
* mixed scripts;
* timestamp insertion.

Tetapi:

> Flagging obfuscation ≠ changing the text.

Simpan text apa adanya.

Buat:

```text
obfuscation_candidate = true/false
```

hanya sebagai audit flag jika diperlukan.

Jangan menjadikan flag tersebut sebagai label kelas.

---

# 33. DATASET SPLIT BELUM DILAKUKAN

Pada tahap ini jangan membuat:

```text
train.csv
validation.csv
test.csv
```

final.

Yang harus disiapkan sekarang adalah:

```text
clean_pool.csv
```

dan metadata grouping yang diperlukan untuk split.

Split dilakukan setelah:

* canonical dataset selesai;
* label harmonisasi selesai;
* duplicate resolution selesai;
* methodology final diputuskan.

---

# 34. SPLIT-READY INFORMATION

Pastikan dataset final memiliki informasi yang memungkinkan strategi split berikut:

### Text duplicate grouping

```text
exact_duplicate_group
```

### Template similarity

```text
near_duplicate_group
```

### Author grouping

```text
author_group_id
```

jika tersedia.

### Source grouping

```text
source_dataset
```

### Temporal grouping

```text
timestamp_standardized
```

jika tersedia.

Dengan demikian nanti kita bisa menguji strategi leakage control tanpa mengulang preprocessing dataset.

---

# 35. CONSISTENCY CHECK

Setelah semua proses:

Pastikan:

```text
jumlah source records
=
jumlah canonical records
+
jumlah duplicate records
+
jumlah invalid records
+
jumlah review records
```

atau berikan reconciliation table yang menjelaskan seluruh perubahan.

Tidak boleh ada record “hilang” tanpa alasan.

---

# 36. RECONCILIATION TABLE

Buat laporan:

```text
dataset_reconciliation.csv
```

Dengan minimal:

```text
source_dataset
raw_rows
invalid_rows
exact_duplicate_rows
cross_dataset_duplicate_rows
conflict_rows
review_rows
accepted_rows
excluded_rows
final_unique_rows
```

Jumlah harus dapat diverifikasi.

---

# 37. CROSS-DATASET OVERLAP REPORT

Buat:

```text
cross_dataset_overlap.csv
```

Dengan:

```text
dataset_a
dataset_b
shared_exact_texts
shared_whitespace_texts
shared_normalized_variants
label_conflicts
```

Khusus laporkan dengan detail:

```text
DS2 vs DS4
```

termasuk seluruh conflict records.

---

# 38. LABEL CONFLICT REPORT

Buat:

```text
label_conflicts.csv
```

Minimal:

```text
text_raw
source_dataset
source_label
canonical_label
decision
reason
```

Semua 48 konflik DS2–DS4 harus dapat ditelusuri.

Juga cek conflict lintas DS1/DS4 dan pasangan dataset lain.

---

# 39. DUPLICATE REPORT

Buat:

```text
duplicate_summary.csv
duplicate_groups.csv
```

Minimal:

```text
group_id
duplicate_type
text_raw
frequency
source_datasets
labels
```

Untuk setiap duplicate family, simpan frequency.

Contoh:

```text
exact
KETIK DI GOOGLE:WISDOMTOTO
frequency = 931
```

---

# 40. QUALITY REPORT

Buat:

```text
data_quality_report.md
```

Isi:

1. dataset awal;
2. jumlah record;
3. missing;
4. duplicate;
5. invalid;
6. conflicting label;
7. ambiguous;
8. Unicode;
9. emoji;
10. URL;
11. abnormal whitespace;
12. short text;
13. long text;
14. class distribution;
15. source concentration;
16. author concentration;
17. campaign/entity concentration.

---

# 41. LABEL GUIDELINE REPORT

Buat:

```text
labeling_guideline.md
```

Dokumen harus menjelaskan:

* definisi Promotion;
* definisi Non-Promotion;
* testimonial;
* social proof;
* explicit ad;
* implicit promotion;
* anti-gambling;
* neutral discussion;
* criticism;
* ambiguous cases;
* slot/microSD type ambiguity;
* obfuscated promotion;
* unknown/uncertain cases.

Dokumen ini akan menjadi dasar untuk methodology dan annotation justification dalam skripsi.

---

# 42. FINAL CANONICAL DATASET

Setelah proses selesai, hasil utama:

```text
processed/canonical_dataset.csv
```

Minimal:

```text
record_id
source_dataset
source_row_id
text_raw
source_label
canonical_label
label_status
author
timestamp
exact_duplicate_group
near_duplicate_group
data_quality_status
provenance_notes
```

Hanya record dengan:

```text
label_status = accepted
```

yang boleh masuk ke supervised dataset candidate.

---

# 43. REVIEW QUEUE

Jika ada record:

```text
label_status = review
```

jangan masukkan ke final supervised dataset.

Sediakan:

```text
review/label_review_queue.csv
```

dan:

```text
review/data_quality_review_queue.csv
```

Review queue harus kecil sejauh mungkin, tetapi jangan memaksakan label hanya demi mengurangi ukuran queue.

---

# 44. DATASET ROLE SETELAH CLEANING

Setelah canonical dataset selesai, buat laporan komposisi kandidat.

Secara sementara:

```text
DS1 = Core candidate
DS2 + DS4 = Unified Kyyyy8 candidate
DS3 = OOD candidate
DS5 = Auxiliary candidate
```

Tetapi status tersebut BELUM FINAL.

Agent harus memberikan bukti berupa:

* ukuran;
* distribusi label;
* duplicate rate;
* source concentration;
* conflict rate;
* diversity;
* metadata availability;
* near-duplicate structure.

Keputusan final mengenai:

* training pool;
* validation pool;
* test pool;
* OOD test;

dibuat setelah laporan ini diperiksa.

---

# 45. JANGAN MELAKUKAN RANDOM SAMPLING SEMBARANGAN

Jangan melakukan:

```python
df.sample(...)
```

untuk menghapus data hanya demi mengecilkan dataset.

Jika perlu sampling, jelaskan:

```text
why
how
sampling frame
random seed
selection criteria
```

dan simpan manifest record yang dipilih.

---

# 46. REPRODUCIBILITY

Semua proses harus reproducible.

Gunakan:

```text
random_seed
```

yang tetap untuk proses yang memerlukan randomness.

Simpan:

```text
scripts/
configs/
logs/
manifests/
```

Jangan melakukan perubahan manual langsung pada CSV final tanpa script atau log.

---

# 47. EXPECTED OUTPUT FILES

Agent harus menghasilkan setidaknya:

```text
audit/
├── dataset_inventory.csv
├── dataset_reconciliation.csv
├── cross_dataset_overlap.csv
├── label_conflicts.csv
├── duplicate_summary.csv
├── data_quality_report.md
└── dataset_audit_summary.md

review/
├── label_review_queue.csv
└── data_quality_review_queue.csv

processed/
└── canonical_dataset.csv

manifests/
├── raw_file_manifest.csv
└── canonical_record_manifest.csv
```

Jika diperlukan:

```text
interim/
├── ds1_harmonized.csv
├── ds2_harmonized.csv
├── ds3_harmonized.csv
├── ds4_harmonized.csv
└── ds5_harmonized.csv
```

---

# 48. FINAL AUDIT SUMMARY

Setelah selesai, agent harus memberikan satu ringkasan:

## Dataset Overview

```text
Raw records:
84,004
```

Lalu hitung hasil aktual:

```text
Canonical unique records:
...

Accepted:
...

Review:
...

Invalid:
...

Excluded:
...
```

## Label Distribution

```text
Promotion:
...

Non-Promotion:
...
```

## Source Contribution

```text
DS1:
...

DS2:
...

DS3:
...

DS4:
...

DS5:
...
```

## Leakage Risk

Laporkan:

```text
Exact duplicate families:
...

Near duplicate families:
...

Author groups:
...

Cross-source duplicates:
...

Label conflicts:
...
```

## Major Findings

Tuliskan masalah terbesar yang masih tersisa.

## Recommendation

Berikan rekomendasi untuk tahap berikutnya:

```text
Training candidate:
Validation candidate:
Normal test candidate:
OOD candidate:
Remaining review:
```

Jangan menentukan model atau obfuscation pada laporan ini.

---

# 49. STOP CONDITIONS

Agent harus berhenti sebelum tahap modeling apabila salah satu kondisi berikut terjadi:

1. Raw file berubah.
2. Jumlah record tidak dapat direkonsiliasi.
3. Banyak record hilang tanpa alasan.
4. Konflik label tidak terdokumentasi.
5. Duplicate cross-dataset belum ditangani.
6. Raw text telah berubah karena preprocessing.
7. Obfuscation telah “diperbaiki” otomatis.
8. Label ditentukan hanya berdasarkan keyword.
9. DS2 dan DS4 digabung tanpa menangani overlap.
10. Record review dipaksa menjadi label tanpa dasar.

Jika salah satu terjadi, perbaiki pipeline terlebih dahulu.

---

# 50. DEFINISI “SELESAI”

Tahap dataset dianggap selesai hanya jika:

* kelima raw dataset tetap tersedia;
* seluruh source memiliki provenance;
* canonical schema tersedia;
* raw text dipertahankan;
* source label tetap tersedia;
* canonical label tersedia;
* duplicate telah diaudit;
* cross-dataset duplicate telah ditangani;
* konflik label telah didokumentasikan;
* ambiguous records dipisahkan;
* leakage groups tersedia;
* distribusi label diketahui;
* kontribusi tiap dataset diketahui;
* seluruh perubahan dapat direproduksi;
* final dataset dapat dijelaskan secara metodologis.

Jangan lanjut ke training model sebelum seluruh requirement di atas terpenuhi.
