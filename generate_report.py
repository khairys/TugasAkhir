import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Load json data
with open('datasets_analysis_summary.json', encoding='utf-8') as f:
    stats_data = json.load(f)

with open('datasets_samples_and_edge_cases.json', encoding='utf-8') as f:
    samples_data = json.load(f)

ds_stats = stats_data['datasets']
overlap = stats_data['overlap']

md = []

md.append("# LAPORAN AUDIT & ANALISIS KOMPREHENSIF 5 DATASET DETEKSI JUDI ONLINE")
md.append("\n**Dokumen Audit Data Eksploratif untuk Tugas Akhir / Penelitian NLP Deteksi Teks Judi Online**")
md.append(f"\n*Tanggal Audit: 6 Oktober 2026* | *Prinsip: Audit Sebelum Manipulasi (Preserve Raw Text)*\n")
md.append("---\n")

md.append("## DAFTAR ISI")
md.append("1. [Ringkasan Eksekutif & Matriks Perbandingan](#1-ringkasan-eksekutif--matriks-perbandingan)")
md.append("2. [Analisis Mendalam Per Dataset (Profil, Fitur, Karakteristik & Sampel Data)](#2-analisis-mendalam-per-dataset)")
md.append("   - [2.1 fahruu/komentar-judi-online (DS1)](#21-dataset-1-fahruukomentar-judi-online)")
md.append("   - [2.2 kyyyy8/dataset-komentar-judi-online-di-youtube (DS2)](#22-dataset-2-kyyyy8dataset-komentar-judi-online-di-youtube)")
md.append("   - [2.3 yaemico/deteksi-judi-online (DS3)](#23-dataset-3-yaemicodeteksi-judi-online)")
md.append("   - [2.4 kyyyy8/dataset-komentar-judi-online-platform-youtube (DS4)](#24-dataset-4-kyyyy8dataset-komentar-judi-online-platform-youtube)")
md.append("   - [2.5 ferdiansakti/gambling-comments-from-youtube-platform (DS5)](#25-dataset-5-ferdiansaktigambling-comments-from-youtube-platform)")
md.append("3. [Analisis Lintas Dataset: Overlap Data, Kontaminasi & Konflik Label](#3-analisis-lintas-dataset-overlap-data-kontaminasi--konflik-label)")
md.append("4. [Analisis Semantik & Inkonsistensi Pelabelan Antar Dataset](#4-analisis-semantik--inkonsistensi-pelabelan-antar-dataset)")
md.append("5. [Analisis Metadata & Pencegahan Data Leakage](#5-analisis-metadata--pencegahan-data-leakage)")
md.append("6. [Analisis Kasus Borderline & Teks Ambigu](#6-analisis-kasus-borderline--teks-ambigu)")
md.append("7. [Evaluasi Kolom Preprocessing vs Raw Text](#7-evaluasi-kolom-preprocessing-vs-raw-text)")
md.append("8. [Rekomendasi Awal: KEEP / REVIEW / EXCLUDE](#8-rekomendasi-awal-keep--review--exclude)")
md.append("\n---\n")

# Section 1: Executive Summary
md.append("## 1. RINGKASAN EKSEKUTIF & MATRIKS PERBANDINGAN\n")
md.append("Audit ini dilakukan terhadap 5 dataset publik asal platform YouTube/Kaggle yang berfokus pada deteksi komentar/teks promosi judi online berbahasa Indonesia. Tujuan audit adalah memetakan kualitas data, duplikasi, anomali teks, artefak preprocessing yang merusak, tumpang tindih (overlap), serta risiko kebocoran data (*data leakage*) sebelum dilakukan pemodelan machine learning atau deep learning.\n")

md.append("### Tabel 1.1: Matriks Perbandingan Teknis 5 Dataset\n")
md.append("| Kode | Nama Dataset | File Target | Baris | Kolom | Missing / Null | Exact Duplicates | Text Duplicates | Distribusi Label (0 : 1) |")
md.append("|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|")

for item_key, ds in ds_stats.items():
    missing_str = ", ".join([f"{k}: {v}" for k, v in ds["missing"].items() if v > 0]) or "0"
    dist_str = f"{ds['label_dist'].get('0', 0):,} ({ds['label_dist_pct'].get('0', 0)}%) : {ds['label_dist'].get('1', 0):,} ({ds['label_dist_pct'].get('1', 0)}%)"
    md.append(f"| **{item_key}** | `{ds['name']}` | [`{Path(ds['file']).name}`](file:///{ds['file'].replace(chr(92), '/')}) | {ds['rows']:,} | {ds['cols']} | {missing_str} | {ds['exact_duplicates']:,} | {ds['text_duplicates']:,} | {dist_str} |")

md.append("\n### Tabel 1.2: Karakteristik Teks Mentah (Raw Text Profiling)\n")
md.append("| Kode | Kolom Raw | Karakter (Min/Rata2/Maks) | Kata (Min/Rata2/Maks) | Ada Emoji (%) | Ada Angka (%) | Unicode Math / Simbol Khusus (%) | Ada URL (%) | Anomali Whitespace (%) | Simbol >15% (%) |")
md.append("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")

for item_key, ds in ds_stats.items():
    st = ds["stats"]
    c_stat = f"{st['char_len']['min']} / {st['char_len']['mean']} / {st['char_len']['max']}"
    w_stat = f"{st['word_len']['min']} / {st['word_len']['mean']} / {st['word_len']['max']}"
    md.append(f"| **{item_key}** | `{ds['raw_col']}` | {c_stat} | {w_stat} | {st['has_emojis']['pct']}% | {st['has_digits']['pct']}% | {st['has_special_unicode']['pct']}% | {st['has_url']['pct']}% | {st['whitespace_anomaly']['pct']}% | {st['symbol_heavy']['pct']}% |")

md.append("\n---\n")

# Section 2: Detailed dataset breakdown
md.append("## 2. ANALISIS MENDALAM PER DATASET\n")

ds_meta = {
    "DS1_fahruu": {
        "title": "2.1 Dataset 1: fahruu/komentar-judi-online",
        "provenance": "Komentar diambil dari video YouTube yang membahas isu investigasi judi online dan sindikatnya (teridentifikasi dari penyebutan figur seperti Ferry Irwandi, Gunawan Sadbor, Budi Arie/Kominfo, serta kasus backdoor situs pemerintah).",
        "semantics": {
            "comment": "Teks asli (raw text) komentar YouTube, masih mempertahankan huruf kapital, emotikon, tanda baca, dan slang pengguna.",
            "final_comment": "Teks hasil normalisasi bahasa gaul/slang ke bahasa baku (misal: 'gue' -> 'saya', 'bgt' -> 'banget', 'udh' -> 'sudah'). Mengandung 83 data null.",
            "label": "Kelas biner: 0 = Bukan Komentar Judi (diskusi umum, opini sosial, kritik pemerintah), 1 = Komentar Promosi / Spam Judi Online (sindikasi bot seperti GunungWin, Alexis17)."
        }
    },
    "DS2_kyyyy8_all": {
        "title": "2.2 Dataset 2: kyyyy8/dataset-komentar-judi-online-di-youtube",
        "provenance": "Koleksi berskala besar (45.592 baris) komentar dari berbagai kanal YouTube Indonesia, mencakup siaran esports (Mobile Legends MPL: RRQ, ONIC, EVOS), ulasan gadget/smartphone, hingga video viral.",
        "semantics": {
            "text": "Teks mentah komentar YouTube tanpa modifikasi.",
            "label": "Kelas biner: 0 = Komentar umum non-judi (74,35%), 1 = Spam promosi judi online (25,65%).",
            "text_preprocessed": "Teks yang telah melalui pembersihan huruf kecil (*case folding*) dan penghapusan karakter non-alfanumerik. Terdapat **1.213 baris bernilai NaN** karena komentar asli hanya memuat emotikon/simbol sehingga terhapus total."
        }
    },
    "DS3_yaemico": {
        "title": "2.3 Dataset 3: yaemico/deteksi-judi-online",
        "provenance": "Data tangkapan live chat YouTube dari siaran langsung CCTV publik Daerah Istimewa Yogyakarta (file: `youtube_chat_jogja_clean.csv`). Live streaming CCTV publik sering menjadi target bot spammer judi online.",
        "semantics": {
            "datetime": "Waktu pengiriman pesan obrolan (format: YYYY-MM-DD HH:MM:SS). Sangat berguna untuk deteksi burst spam.",
            "author_name": "Nama akun pengirim pesan di live chat YouTube.",
            "message": "Pesan asli live chat. Catatan: terdapat 2 baris bernilai null.",
            "cleaned_message": "Pesan setelah tanda baca dibersihkan. Terdapat 2 baris bernilai null.",
            "label": "Kelas biner: 0 = Chat warga/penonton umum (49,81%), 1 = Spam promosi bot judi online (50,19%)."
        }
    },
    "DS4_kyyyy8_plat": {
        "title": "2.4 Dataset 4: kyyyy8/dataset-komentar-judi-online-platform-youtube",
        "provenance": "Dataset YouTube terkurasi dengan metadata API resmi (`comment_id`, `author`, `time_parsed`). Berisi 18.902 komentar dengan proporsi label yang seimbang (52,11% judi vs 47,89% non-judi).",
        "semantics": {
            "comment_id": "ID unik komentar dari YouTube Data API v3 (misal: `UgxYuOnKVrvEasBZ3mR4AaABAg`). Berguna untuk mencegah data leakage.",
            "author": "Username pengunggah komentar (diawali tanda `@`).",
            "time_parsed": "Unix timestamp waktu komentar diunggah.",
            "text": "Teks asli komentar mentah.",
            "label": "Kelas biner: 0 = Non-judi, 1 = Promosi judi online.",
            "text_preprocessed": "Teks hasil pra-pemrosesan (stemming & stopword removal). Terdapat 476 baris NaN."
        }
    },
    "DS5_ferdiansakti": {
        "title": "2.5 Dataset 5: ferdiansakti/gambling-comments-from-youtube-platform",
        "provenance": "Dataset komentar YouTube berfokus pada invasi bot promosi kasino/slot `ambil4d` di berbagai kolom komentar kanal Indonesia.",
        "semantics": {
            "Comments": "Teks komentar mentah dari pengguna dan bot spam YouTube.",
            "Label": "Kelas biner: 0 = Bukan Judi (25,15%), 1 = Promosi Judi (74,85% - mayoritas promosi sindikat ambil4d)."
        }
    }
}

for ds_id, meta in ds_meta.items():
    info = ds_stats[ds_id]
    s_data = samples_data[ds_id]
    
    md.append(f"### {meta['title']}\n")
    md.append(f"- **File Lokasi**: [`{info['file']}`](file:///{info['file'].replace(chr(92), '/')})")
    md.append(f"- **Dimensi**: {info['rows']:,} baris × {info['cols']} kolom")
    md.append(f"- **Provenance / Sumber**: {meta['provenance']}")
    md.append(f"- **Duplikasi**: {info['exact_duplicates']:,} baris duplikat persis ({round(info['exact_duplicates']/info['rows']*100, 2)}%), {info['text_duplicates']:,} teks duplikat ({round(info['text_duplicates']/info['rows']*100, 2)}%)")
    md.append(f"- **Distribusi Label**: Label 0 = {info['label_dist'].get('0', 0):,} ({info['label_dist_pct'].get('0', 0)}%) | Label 1 = {info['label_dist'].get('1', 0):,} ({info['label_dist_pct'].get('1', 0)}%)\n")
    
    md.append("#### Arti & Semantik Setiap Kolom:")
    for col in info["col_names"]:
        dtype = info["col_dtypes"][col]
        miss = info["missing"].get(col, 0)
        desc = meta["semantics"].get(col, "Kolom data")
        md.append(f"- `{col}` (*{dtype}*, null: {miss}): {desc}")
    
    md.append("\n#### Top Spam Bot Duplicates:")
    for txt, cnt in list(s_data["top_duplicates"].items())[:3]:
        md.append(f"- `{cnt}x kemunculan`: \"{txt}\"")
        
    md.append("\n#### 25 Contoh Data Label 0 (Bukan Judi):")
    for i, smp in enumerate(s_data["samples_0"][:25], 1):
        clean_smp = smp.replace("|", "\\|")
        md.append(f"{i}. \"{clean_smp}\"")
        
    md.append("\n#### 25 Contoh Data Label 1 (Judi Online):")
    for i, smp in enumerate(s_data["samples_1"][:25], 1):
        clean_smp = smp.replace("|", "\\|")
        md.append(f"{i}. \"{clean_smp}\"")
        
    md.append("\n" + "-"*40 + "\n")

# Section 3: Cross-dataset Overlap & Conflict
md.append("## 3. ANALISIS LINTAS DATASET: OVERLAP DATA, KONTAMINASI & KONFLIK LABEL\n")
md.append("Analisis komparatif dilakukan dengan mencocokkan teks (*exact match* pada teks yang telah dinormalkan huruf kecil dan spasi luarnya) antar-pasang dataset. Temuan ini sangat krusial jika Anda berencana menggabungkan (*concatenate*) dataset ini menjadi satu korpus besar.\n")

md.append("### Tabel 3.1: Matriks Irisan Teks Antar Dataset\n")
md.append("| Pasangan Dataset | Jumlah Teks Sama (Shared Unique) | Jumlah Konflik Label | Catatan / Indikasi |")
md.append("|---|:---:|:---:|---|")

for pair_name, v in overlap.items():
    shared = v["shared_unique_texts"]
    conflicts = v["label_conflicts"]
    if conflicts > 0:
        catatan = f"⚠️ **KRUSIAL**: Terdapat {conflicts} teks dengan label berlawanan!"
    elif shared > 100:
        catatan = f"Overlap tinggi ({shared:,} teks), terindikasi bersumber dari uploader/skraping yang sama."
    elif shared > 0:
        catatan = "Overlap wajar (komentar pendek umum seperti 'pertama', 'mantap', dll)."
    else:
        catatan = "Tidak ada overlap terdeteksi."
    md.append(f"| `{pair_name}` | {shared:,} | {conflicts} | {catatan} |")

md.append("\n### Temuan Kritis: Konflik Label Antara DS2 dan DS4 (Uploader: kyyyy8)")
md.append("Dataset `DS2_kyyyy8_all` (45.592 baris) dan `DS4_kyyyy8_plat` (18.902 baris) memiliki **10.561 teks yang identik**. Namun, terdapat **48 teks dengan label berlawanan (*conflicting labels*)**! Contoh bukti inkonsistensi pelabelan:\n")

md.append("1. **Komentar Diskusi Esports (Non-Judi Salah Dilabeli Judi di DS4):**")
md.append("   - Teks: *\"padahal udah pada tau kunci onic itu di duo mid sama roam dan kebiasaan rrq gonta ganti pemain di mpl...\"*")
md.append("   - Label di DS2: `0` (Bukan Judi - Benar)")
md.append("   - Label di DS4: `1` (Judi - **False Positive Annotation Error**)")
md.append("   - Teks: *\"bang bikent vibes nya udah beda banget udah ga berapi api kaya dulu\"*")
md.append("   - Label di DS2: `0` (Bukan Judi - Benar)")
md.append("   - Label di DS4: `1` (Judi - **False Positive Annotation Error**)\n")

md.append("2. **Komentar Promosi Situs Judi (Judi Lolos Dilabeli Non-Judi di DS4):**")
md.append("   - Teks: *\"0:56 wifi4d bukti nyata, bukan sekadar janji.🎉\"*")
md.append("   - Label di DS2: `1` (Judi - Benar, 'wifi4d' adalah nama situs slot)")
md.append("   - Label di DS4: `0` (Bukan Judi - **False Negative Annotation Error**)\n")

md.append("3. **Konflik Antara DS1 (fahruu) dan DS4 (kyyyy8):**")
md.append("   - Teks: *\"gasskuyy dari bang toing katanya,ga ruda-ho ki-badai petir🔥🔥\"*")
md.append("   - Label di DS1: `1` (Judi - merujuk 'garuda hoki' & 'petir zeus')")
md.append("   - Label di DS4: `0` (Non-judi)\n")

# Section 4: Semantic differences
md.append("## 4. ANALISIS SEMANTIK & INKONSISTENSI PELABELAN ANTAR DATASET\n")
md.append("Berdasarkan audit anotasi manual, definisi 'Judi Online' antar pembuat dataset memiliki nuansa yang berbeda:\n")
md.append("1. **DS1 (fahruu)**: Mendefinisikan kelas 1 secara spesifik pada **promosi atau ajakan aktif bermain situs judi** (misal memuat nama bandar seperti `GunungWin`, `Alexis17`). Komentar warga yang membahas judi dari sudut pandang sosial/hukum tetap dilabeli 0.")
md.append("2. **DS2 & DS4 (kyyyy8)**: Menunjukkan adanya *human annotator noise* atau kesalahan pelabelan otomatis berbasis aturan sederhana. Beberapa komentar murni esports dan review gawai masuk ke label 1.")
md.append("3. **DS3 (yaemico)**: Fokus pada lingkungan **Live Chat spamming**. Semua pesan bot yang memuat promo kredit gratis ('Freechip', 'VIP 500rb', 'Ketik di google') dilabeli 1, sedangkan sapaan penonton biasa ('hujan deras min', 'salam dari bantul') dilabeli 0.")
md.append("4. **DS5 (ferdiansakti)**: Sangat terdistorsi (*imbalance* 74,8% label 1) karena didominasi oleh ribuan bot satu sindikat (`ambil4d`). Anotasi di sini lebih sempit karena hampir seluruh korpus diambil dari video yang dibanjiri bot kampanye tersebut.\n")

# Section 5: Metadata & Leakage
md.append("## 5. ANALISIS METADATA & PENCEGAHAN DATA LEAKAGE\n")
md.append("Salah satu jebakan terbesar dalam deteksi komentar spam/judi online adalah **Data Leakage** akibat duplikasi masif oleh bot akun ternak.\n")
md.append("- **Kasus Nyata**: Di DS3, pesan `KETIK DI GOOGLE:WISDOMTOTO` muncul **931 kali**! Di DS1, pesan `*GUNUNGWIN* yang paling bagus!` muncul **71 kali**.")
md.append("- **Dampak Jika Train-Test Split Dilakukan Acak (Random Split)**: Teks spam yang sama persis akan tersebar ke set *training* dan set *testing*. Model NLP (terutama TF-IDF, BERT, atau LLM) hanya akan 'menghafal' teks bot tersebut. Akibatnya, nilai akurasi uji tampak fantastis (99%), namun model akan gagal total ketika diuji pada teks baru di dunia nyata (*overfitting to bot signatures*).")
md.append("- **Pencegahan Menggunakan Metadata**:")
md.append("  * **Author Grouping (`GroupKFold` by `author`/`author_name`)**: Memastikan komentar dari satu akun/bot hanya ada di train ATAU test, tidak boleh bocor ke keduanya.")
md.append("  * **Temporal Split (`time_parsed` / `datetime`)**: Membagi data berdasarkan lini masa (misal 70% waktu awal untuk train, 30% waktu akhir untuk test). Pola ini menguji apakah model mampu mendeteksi istilah slang/situs baru yang muncul belakangan.")
md.append("  * **Teks Deduplikasi Pre-Split**: Sebelum data dibagi, seluruh teks duplikat harus dikurangi (*deduplicated*) agar evaluasi menguji kemampuan pemahaman bahasa, bukan frekuensi kemunculan spam.\n")

# Section 6: Borderline cases
md.append("## 6. ANALISIS KASUS BORDERLINE & TEKS AMBIGU\n")
md.append("Audit menemukan beberapa kategori teks yang berisiko tinggi membingungkan model kecerdasan buatan:\n")

md.append("### Kategori A: Kata Kunci 'Judi'/'Slot' dalam Konteks Positif / Non-Judi (False Positive Trap)")
md.append("Model sederhana berbasis kamus kata kunci (*lexicon-based*) akan gagal pada komentar berikut karena mengandung kata judi/slot padahal bermakna kontra-judi (Label 0):\n")
md.append("- *\"all-rounder, sensor lengkap, masih ada slot mircoSD\"* (DS2) -> Kata 'slot' adalah slot kartu memori smartphone.")
md.append("- *\"ora promosi slot woiii\"* (DS3) -> Warga lokal menegur spammer di live chat.")
md.append("- *\"pak budi kan sudah pernah klarifikasi, bahwa dia akan/lagi fokus ke koperasi... liat aja tuh udah panen berapa milyar hasil dari koperasi judol mereka\"* (DS1) -> Kritik satir terhadap pemerintah.")
md.append("- *\"Isi komentar nya judol semua anjir\"* (DS5) -> Keluhan penonton terhadap spam bot.")
md.append("- *\"Gunawan Sadbor jadi duta anti judol lucu bet anying\"* (DS1) -> Opini berita sosial.\n")

md.append("### Kategori B: Stealth Promotion & Font Obfuscation (False Negative Trap)")
md.append("Bot judi masa kini tidak lagi menulis kata 'judi online' atau 'slot gacor' secara gamblang. Mereka menggunakan teknik evasif berikut:\n")
md.append("- **Mathematical Alphanumeric Unicode (Bypass Filter)**: Menggunakan font tebal/miring unicode matematika seperti `𝗔𝗟𝗘𝗫𝗜𝗦𝟭𝟳`, `𝗕𝗔𝗥𝗗𝗜𝟰𝗗`, `𝐊𝐄𝐌𝐁𝐀𝐑𝟕𝟖`, `ＰＵＬＡＵＷＩＮ`. Di DS4, terdapat **35,21%** teks yang menggunakan karakter ini!")
md.append("- **Simbol Pemisah & Sensor Diri**: `ALEXIS-☯17☯`, `█ambil4d█`, `w!f!4d`, `ga ruda-ho ki-badai petir`.")
md.append("- **Penyamaran Timestamp YouTube**: Menulis timestamp palsu agar terlihat seperti komentar relevan: `0:56 wifi4d bukti nyata, bukan sekadar janji.🎉`.")
md.append("- **Teks Sangat Pendek Tanpa Kata Kunci**: `VIP 500 RIBU`, `info link gacor`, `WD lancar`.\n")

# Section 7: Preprocessing vs Raw
md.append("## 7. EVALUASI KOLOM PREPROCESSING VS RAW TEXT\n")
md.append("Sesuai instruksi audit: **Pertahankan raw/original text, jangan lakukan stemming, stopword removal, atau cleaning prematur!**")
md.append("Berikut evaluasi kolom pra-pemrosesan bawaan yang terdapat pada dataset:\n")
md.append("1. **Kolom `final_comment` pada DS1 (fahruu)**: Mengubah kata 'gue' -> 'saya', 'lu' -> 'kamu', serta menghapus angka jam. Hal ini berisiko menghilangkan variasi dialek dan ritme penulisan asli.")
md.append("2. **Kolom `text_preprocessed` pada DS2 & DS4 (kyyyy8)**:")
md.append("   - Menghapus seluruh emotikon, tanda baca, dan karakter non-ASCII.")
md.append("   - **Kerusakan Data**: Terdapat **1.213 baris di DS2 dan 476 baris di DS4 yang menjadi kosong (NaN)** karena komentar aslinya hanya memuat emoji/simbol.")
md.append("   - Mengonversi font Unicode matematika (seperti `𝗔𝗟𝗘𝗫𝗜𝗦`) secara serampangan atau menghapusnya, padahal jenis font ini adalah *fitur diskriminatif terkuat* untuk mendeteksi bot judi!")
md.append("3. **Kolom `cleaned_message` pada DS3 (yaemico)**: Menghapus tanda baca, namun format bot seperti `:fire:` atau simbol chat YouTube menjadi teks biasa.\n")
md.append("> **Kesimpulan Teknis**: Untuk pemodelan modern berbasis Transformer/BERT (seperti IndoBERT) atau LLM, **wajib menggunakan kolom Raw Text (`comment`, `text`, `message`, `Comments`)**. Arsitektur Transformer membutuhkan konteks utuh, tanda baca, huruf kapital, dan simbol untuk memahami makna kalimat.\n")

# Section 8: Recommendations
md.append("## 8. REKOMENDASI AWAL: KEEP / REVIEW / EXCLUDE\n")
md.append("*(Catatan: Rekomendasi ini adalah panduan strategis; tidak ada data yang diubah atau dihapus pada tahap ini)*\n")

md.append("### 1. `fahruu/komentar-judi-online` (DS1) -> **STATUS: KEEP (DIREKOMENDASIKAN)**")
md.append("- **Alasan**: Kualitas anotasi sangat baik, pemisahan konteks diskusi sosial vs promosi judi sangat jelas, rasio label seimbang (62% : 38%), serta memuat variasi bahasa slang Indonesia yang kaya.")
md.append("- **Saran Penggunaan**: Gunakan kolom `comment` (raw), lakukan deduplikasi teks terlebih dahulu.\n")

md.append("### 2. `kyyyy8/dataset-komentar-judi-online-platform-youtube` (DS4) -> **STATUS: REVIEW (PERLU KURASI)**")
md.append("- **Alasan**: Memiliki metadata terlengkap (`comment_id`, `author`, `time_parsed`) yang sangat berharga untuk pengujian bebas *leakage*. Namun, terdeteksi memiliki sedikitnya 48 konflik anotasi dengan DS2 dan beberapa false positive pada diskusi esport.")
md.append("- **Saran Penggunaan**: Lakukan verifikasi otomatis/manual pada 48 data berkonflik sebelum digabungkan.\n")

md.append("### 3. `kyyyy8/dataset-komentar-judi-online-di-youtube` (DS2) -> **STATUS: REVIEW / SELECTIVE MERGE**")
md.append("- **Alasan**: Berukuran terbesar (45.592 baris), namun memiliki tumpang tindih (overlap) sebanyak 10.561 baris dengan DS4 tanpa metadata pendukung. Jika digabung langsung tanpa deduplikasi lintas dataset, akan terjadi redundancy masif.")
md.append("- **Saran Penggunaan**: Ambil subset unik yang tidak beririsan dengan DS4 setelah deduplikasi teks.\n")

md.append("### 4. `yaemico/deteksi-judi-online` (DS3) -> **STATUS: REVIEW (KHUSUS DOMAIN LIVE CHAT)**")
md.append("- **Alasan**: Karakteristik data sangat spesifik (Live Chat CCTV Jogja, kalimat sangat pendek, duplikasi spam ekstrem >57%).")
md.append("- **Saran Penggunaan**: Sangat baik jika digunakan sebagai **Out-of-Distribution (OOD) Test Set** untuk menguji apakah model yang dilatih pada komentar YouTube standar mampu mendeteksi spam di lingkungan *Live Streaming*.\n")

md.append("### 5. `ferdiansakti/gambling-comments-from-youtube-platform` (DS5) -> **STATUS: REVIEW / OVERSAMPLED BOT SPECIFIC**")
md.append("- **Alasan**: Sangat tidak seimbang (74,8% label 1) dan terkonsentrasi pada satu nama situs (`ambil4d`). Jika dimasukkan tanpa pembobotan, model berisiko bias hanya mengenali pola sindikat `ambil4d`.")
md.append("- **Saran Penggunaan**: Deduplikasi agresif pada teks promosi `ambil4d` dan gunakan sebagai data pengaya (*data augmentation*).\n")

# Write file
output_path = Path("LAPORAN_AUDIT_DAN_ANALISIS_5_DATASET.md")
output_path.write_text("\n".join(md), encoding="utf-8")
print(f"Report written successfully to {output_path.resolve()}")
