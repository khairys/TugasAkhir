# LAPORAN AUDIT & ANALISIS KOMPREHENSIF 5 DATASET DETEKSI JUDI ONLINE

**Dokumen Audit Data Eksploratif untuk Tugas Akhir / Penelitian NLP Deteksi Teks Judi Online**

*Tanggal Audit: 6 Oktober 2026* | *Prinsip: Audit Sebelum Manipulasi (Preserve Raw Text)*

---

## DAFTAR ISI
1. [Ringkasan Eksekutif & Matriks Perbandingan](#1-ringkasan-eksekutif--matriks-perbandingan)
2. [Analisis Mendalam Per Dataset (Profil, Fitur, Karakteristik & Sampel Data)](#2-analisis-mendalam-per-dataset)
   - [2.1 fahruu/komentar-judi-online (DS1)](#21-dataset-1-fahruukomentar-judi-online)
   - [2.2 kyyyy8/dataset-komentar-judi-online-di-youtube (DS2)](#22-dataset-2-kyyyy8dataset-komentar-judi-online-di-youtube)
   - [2.3 yaemico/deteksi-judi-online (DS3)](#23-dataset-3-yaemicodeteksi-judi-online)
   - [2.4 kyyyy8/dataset-komentar-judi-online-platform-youtube (DS4)](#24-dataset-4-kyyyy8dataset-komentar-judi-online-platform-youtube)
   - [2.5 ferdiansakti/gambling-comments-from-youtube-platform (DS5)](#25-dataset-5-ferdiansaktigambling-comments-from-youtube-platform)
3. [Analisis Lintas Dataset: Overlap Data, Kontaminasi & Konflik Label](#3-analisis-lintas-dataset-overlap-data-kontaminasi--konflik-label)
4. [Analisis Semantik & Inkonsistensi Pelabelan Antar Dataset](#4-analisis-semantik--inkonsistensi-pelabelan-antar-dataset)
5. [Analisis Metadata & Pencegahan Data Leakage](#5-analisis-metadata--pencegahan-data-leakage)
6. [Analisis Kasus Borderline & Teks Ambigu](#6-analisis-kasus-borderline--teks-ambigu)
7. [Evaluasi Kolom Preprocessing vs Raw Text](#7-evaluasi-kolom-preprocessing-vs-raw-text)
8. [Rekomendasi Awal: KEEP / REVIEW / EXCLUDE](#8-rekomendasi-awal-keep--review--exclude)

---

## 1. RINGKASAN EKSEKUTIF & MATRIKS PERBANDINGAN

Audit ini dilakukan terhadap 5 dataset publik asal platform YouTube/Kaggle yang berfokus pada deteksi komentar/teks promosi judi online berbahasa Indonesia. Tujuan audit adalah memetakan kualitas data, duplikasi, anomali teks, artefak preprocessing yang merusak, tumpang tindih (overlap), serta risiko kebocoran data (*data leakage*) sebelum dilakukan pemodelan machine learning atau deep learning.

### Tabel 1.1: Matriks Perbandingan Teknis 5 Dataset

| Kode | Nama Dataset | File Target | Baris | Kolom | Missing / Null | Exact Duplicates | Text Duplicates | Distribusi Label (0 : 1) |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **DS1_fahruu** | `fahruu/komentar-judi-online` | [`judi_online.csv`](file:///datasets/fahruu_komentar-judi-online/judi_online.csv) | 8,440 | 3 | final_comment: 83 | 1,809 | 1,809 | 5,267 (62.41%) : 3,173 (37.59%) |
| **DS2_kyyyy8_all** | `kyyyy8/dataset-komentar-judi-online-di-youtube (dataset.csv)` | [`dataset.csv`](file:///datasets/kyyyy8_dataset-komentar-judi-online-di-youtube/dataset.csv) | 45,592 | 3 | text_preprocessed: 1213 | 10,999 | 11,000 | 33,899 (74.35%) : 11,693 (25.65%) |
| **DS3_yaemico** | `yaemico/deteksi-judi-online` | [`youtube_chat_jogja_clean.csv`](file:///datasets/yaemico_deteksi-judi-online/youtube_chat_jogja_clean.csv) | 6,350 | 5 | message: 2, cleaned_message: 2 | 0 | 3,621 | 3,163 (49.81%) : 3,187 (50.19%) |
| **DS4_kyyyy8_plat** | `kyyyy8/dataset-komentar-judi-online-platform-youtube` | [`dataset_komentarJudol_preprocessed_nonAnom.csv`](file:///datasets/kyyyy8_dataset-komentar-judi-online-platform-youtube/dataset_komentarJudol_preprocessed_nonAnom.csv) | 18,902 | 6 | text_preprocessed: 476 | 0 | 8,243 | 9,052 (47.89%) : 9,850 (52.11%) |
| **DS5_ferdiansakti** | `ferdiansakti/gambling-comments-from-youtube-platform` | [`rawdata.csv`](file:///datasets/ferdiansakti_gambling-comments-from-youtube-platform/rawdata.csv) | 4,720 | 2 | 0 | 516 | 518 | 1,187 (25.15%) : 3,533 (74.85%) |

### Tabel 1.2: Karakteristik Teks Mentah (Raw Text Profiling)

| Kode | Kolom Raw | Karakter (Min/Rata2/Maks) | Kata (Min/Rata2/Maks) | Ada Emoji (%) | Ada Angka (%) | Unicode Math / Simbol Khusus (%) | Ada URL (%) | Anomali Whitespace (%) | Simbol >15% (%) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **DS1_fahruu** | `comment` | 1 / 79.78 / 2014 | 1 / 12.72 / 315 | 37.52% | 40.46% | 14.3% | 0.05% | 10.0% | 4.87% |
| **DS2_kyyyy8_all** | `text` | 1 / 62.38 / 6804 | 1 / 10.07 / 908 | 44.3% | 34.14% | 16.54% | 0.15% | 5.39% | 11.0% |
| **DS3_yaemico** | `message` | 0 / 32.98 / 414 | 0 / 4.06 / 33 | 0.02% | 30.58% | 1.59% | 0.0% | 0.02% | 3.31% |
| **DS4_kyyyy8_plat** | `text` | 1 / 55.94 / 888 | 1 / 8.62 / 160 | 50.35% | 42.04% | 35.21% | 0.2% | 9.31% | 14.59% |
| **DS5_ferdiansakti** | `Comments` | 4 / 62.0 / 1003 | 1 / 10.1 / 172 | 41.95% | 60.42% | 32.12% | 1.84% | 2.25% | 1.8% |

---

## 2. ANALISIS MENDALAM PER DATASET

### 2.1 Dataset 1: fahruu/komentar-judi-online

- **File Lokasi**: [`datasets/fahruu_komentar-judi-online/judi_online.csv`](file:///datasets/fahruu_komentar-judi-online/judi_online.csv)
- **Dimensi**: 8,440 baris × 3 kolom
- **Provenance / Sumber**: Komentar diambil dari video YouTube yang membahas isu investigasi judi online dan sindikatnya (teridentifikasi dari penyebutan figur seperti Ferry Irwandi, Gunawan Sadbor, Budi Arie/Kominfo, serta kasus backdoor situs pemerintah).
- **Duplikasi**: 1,809 baris duplikat persis (21.43%), 1,809 teks duplikat (21.43%)
- **Distribusi Label**: Label 0 = 5,267 (62.41%) | Label 1 = 3,173 (37.59%)

#### Arti & Semantik Setiap Kolom:
- `comment` (*str*, null: 0): Teks asli (raw text) komentar YouTube, masih mempertahankan huruf kapital, emotikon, tanda baca, dan slang pengguna.
- `final_comment` (*str*, null: 83): Teks hasil normalisasi bahasa gaul/slang ke bahasa baku (misal: 'gue' -> 'saya', 'bgt' -> 'banget', 'udh' -> 'sudah'). Mengandung 83 data null.
- `label` (*int64*, null: 0): Kelas biner: 0 = Bukan Komentar Judi (diskusi umum, opini sosial, kritik pemerintah), 1 = Komentar Promosi / Spam Judi Online (sindikasi bot seperti GunungWin, Alexis17).

#### Top Spam Bot Duplicates:
- `71x kemunculan`: "*GUNUNGWIN* yang paling bagus!  Terima kasih uang jajannya"
- `52x kemunculan`: "baru narik 2jt dari *GUNUNGWIN* nasib nasib gk jadi proses pinjol"
- `49x kemunculan`: "Gokil parah, di *GUNUNGWIN* ada bonus DEPOSIT yang bisa di-claim sampai kiamat."

#### 25 Contoh Data Label 0 (Bukan Judi):
1. "Hallo warga sipil sekalian jam 11 malam. ini gue menunggu pembuktian santet dari seseorang yang mengatakan pukul 00.00 WIB gue bakal kena, jadi mari kita saksikan bersama di live youtube"
2. "kalo tanya menteri sebelumnya ngapain. Jawabannya ya gak ngapa-ngapain, data breacing aja gak tau. Atau malah dia juga ikut melindungi."
3. "Gak sia sia ngikutin mas fery ,smg makin tercerahkan"
4. "Sehat sehat bang, karena lu berani"
5. "DANA E WALLET NYA PADA JOEDOL"
6. "Versi reelsnya bg mau share"
7. "Appraised Bang, Lanjutkan .... Semoga Pak Prabowo dan jajarannya bene2 yang di harapkan kebanyakan rakyat indonesia. Brantas Judi online sampai ke akar2nya."
8. "Saluran whatsapp juga jadi sarang judol sekarang bang, udah menyebar kemana mana dah"
9. "Siapa tahu Budi Ari menjadi Induk semang Judol, bawahan hanya Pelaksanaan lapangan,"
10. "keren kamu bung🔥🔥"
11. "lu keren ngasih bandingnya bukan sama orang miskin yang mencari peruntungan, dan lebih kerennya lagi, lu nyari referensi dari orang terdekat lau, keren lu bang"
12. "Para penjudi itu udah disadari di edukasi kl itu scam/tipu2  tetep aja main biarin lah biar acur hidupnya"
13. "Kawal ketat!!🔥"
14. "Tetap Hati2 bang Fery, ,"
15. "Siapakah sosok manusia laknat inisial "AL" tersebut? 🤔"
16. "Lama lama kayak ryuzaki deathnote"
17. "penyakit akut"
18. "istri saya meninggal karena diagnosa tumor otak nopember 2023, yg awalnya hanya dikira sakit kepala biasa saja"
19. "Undang Dokter / Ahli Ahli : * Nyari Informasi Medis * Nyari Materi Stand-up"
20. "Very useful and informative! Thankyou❤"
21. "Pesan dari dokternya mengingatkanku dgn drakor hometown cha cha cha😢 soal ibu yg gk boleh hanya memprioritaskan keluarganya masalah kesehatan"
22. "gua nangis nonton ini😣"
23. "Mending nabung buat masa depan daripada buang uang di judi. 💰"
24. "Ikut komunitas buku, diskusi seru dan wawasan bertambah. 📚"
25. "Kontennya kece, selalu nunggu upload! 🔔"

#### 25 Contoh Data Label 1 (Judi Online):
1. "ALEXIS-☯17☯ emang ga main-main soal keamanan data member"
2. "alexis17 dapet damage gak ada obat dong tadi malem, hoki tingkat dewa."
3. "Koleksi genre slice of life ALEXIS17 udah satu lemari penuh."
4. "Selera humor ALEXIS17 agak komedi situasi, tapi seru."
5. "Kuliah online bikin bersyukur, mending liat postingan ALEXIS17."
6. "Collab Alexis17 sama konten viral pasti bakal viral. Cuy!"
7. "Anjay mantep, di ALEXIS 🎀17🎀 bisa main slot sambil nge-PowerMill."
8. "Bermain di BERKAH99 membantu saya mengatasi masalah hutang yang menghantui."
9. "⭐𝘼𝙇𝙀𝙓𝙄𝙎17 tuh emang bener-bener ngubah hidup gue, dari pengangguran jadi pengusaha"
10. "Hanya di Pulau7/7/7, uang bisa datang cepat banget."
11. "Mau jadi kaya raya? Pulau 7/7/7 tempatnya, bro!"
12. "gak kerasa bentar lagi hari raya , jadi jangan lupa juga untuk coba 【H】【o】【k】【i】【7】【7】【7】"
13. "Dengan 🍭 *KYT4D* 🍭, aku percaya bahwa tidak ada yang tidak mungkin"
14. "Depo receh aja udah bisa traktir temen, thanks 𝗩𝗜𝗖𝗧𝗢𝗥𝗬𝟬𝟬𝟳 🎉"
15. "Banyak pilihan game seru di satu platform, ya cuma di PawPaw4D."
16. "9:11  bang tadi jam segitu menang besar w di 🚩𝙎𝙂𝙄88🚩"
17. "Alhamdulillah, 𝐌𝐎𝐍𝐀𝟒𝐃 keren! Visual, cerita balance. 🙏"
18. "02:55 P U L A U W I N tempat ngetawain nasib bareng"
19. "terima kasi rezekinya  ⭐𝙎𝙂𝙄88"
20. "Ynag penting bisa nekan tomboil 🔍𝐊𝗨𝗦𝗨𝗠𝗔𝗧𝟎𝗧𝟎🏆,🌟"
21. "terimakasih selalu upload kak, walaupun masih sibuk banget 🎉𝐏𝐑0𝐁𝐄𐊗𝟖𝟓𝟓8̲5̲5̲"
22. "Spin dikit, cuan banyak 💸 Yuk join 𝐏𝐑0𝐁𝐄𐊗𝟖𝟓𝟓!"
23. "Tergacor hanya di  💃 ⚡ 𝘽𝙀𝙍𝙇𝙄𝘼𝙉 33 ⚡"
24. "Gak bosenin sama sekali kalau udah buka ＰＵＬＡＵＷＩＮ."
25. "Gak percaya? Cobain DORA77, jaminan gacor! Loss? Itu cuma mitos! 😂"

----------------------------------------

### 2.2 Dataset 2: kyyyy8/dataset-komentar-judi-online-di-youtube

- **File Lokasi**: [`datasets/kyyyy8_dataset-komentar-judi-online-di-youtube/dataset.csv`](file:///datasets/kyyyy8_dataset-komentar-judi-online-di-youtube/dataset.csv)
- **Dimensi**: 45,592 baris × 3 kolom
- **Provenance / Sumber**: Koleksi berskala besar (45.592 baris) komentar dari berbagai kanal YouTube Indonesia, mencakup siaran esports (Mobile Legends MPL: RRQ, ONIC, EVOS), ulasan gadget/smartphone, hingga video viral.
- **Duplikasi**: 10,999 baris duplikat persis (24.12%), 11,000 teks duplikat (24.13%)
- **Distribusi Label**: Label 0 = 33,899 (74.35%) | Label 1 = 11,693 (25.65%)

#### Arti & Semantik Setiap Kolom:
- `text` (*str*, null: 0): Teks mentah komentar YouTube tanpa modifikasi.
- `label` (*int64*, null: 0): Kelas biner: 0 = Komentar umum non-judi (74,35%), 1 = Spam promosi judi online (25,65%).
- `text_preprocessed` (*str*, null: 1213): Teks yang telah melalui pembersihan huruf kecil (*case folding*) dan penghapusan karakter non-alfanumerik. Terdapat **1.213 baris bernilai NaN** karena komentar asli hanya memuat emotikon/simbol sehingga terhapus total.

#### Top Spam Bot Duplicates:
- `98x kemunculan`: "Pertama"
- `65x kemunculan`: "Aku bisa bang"
- `64x kemunculan`: "9"

#### 25 Contoh Data Label 0 (Bukan Judi):
1. "Tadinya kupikir kalo kalah demeg itu disebabkan oleh faktor HP yg kentang yg tidak mampu memberikan…"
2. "aduu aduan"
3. "Kalo bang david kurang suka buat saya aja bang, iziinnnn🙏🙏😅😅"
4. "Z FOLD AJA BLM KEBELI UDH ADA TRIFOLD"
5. "bacanya sambil nangis, aku juga gitu ka .. cmn bedanya bukan karna di jodohin, tp beda agama dan sudah pasti harus mencari pasangan masing2 yang se agama..akuu juga ke jogja, explore tmpat2 baru, dan mungkin jogja adalah opsi terakhir ku kalau mau berpergian lg, karna pasti rasanya beda kalau kita kesana tp gak sama dia )):"
6. "1:08 tololnya pemain inter di blkng"
7. "​@YoutubeQ-l7dbcot kntol mkny nonton match lainnya"
8. "Dari beberapa info yang aku dapet karena jalur narkoba dari arah Amerika Selatan itu udah merenggut 300.000 nyawa warga sipil Amrik sendiri yang dimana salah satu jalurnya lewat Venezuela, trump udah nyiapin rencana buat ke Meksiko dan Kolombia"
9. "Kok steven jdi mirip azka ya"
10. "UNDANG PATER YANCE DIREKTUR UTAMA STELA MARIS BATAM"
11. "Wanda ga tau sopan santun.."
12. "​@FitriAni-me7ri Menurutku cieh wajar ... galak. Bnyk kok pemain belakang maen kasar..."
13. "I neeedddd moreee episodee jennn ❤❤"
14. "Iya biar kita ada hiburan"
15. "Barakalahufiik..."
16. "Lanjut lgi bg tamatin"
17. "Nunggu skin Bane Tuan crab auto beli sih😁"
18. "Bang gua udah like dan subscribe Gua it_isturu"
19. "​ @mjhgbbj terus lu mau rrq lawan siapa onic id onic ph atau srg?"
20. "Bang bkent, suka kamu 😂😂"
21. "biarin aja selagi ga makan ternak warga mah"
22. "Keren ketua sampe turun tangan ikut demo👍"
23. "Ujung2 nya buat ketua nya itu kan cuman gimick doang wkkwwkkw"
24. "Van desel bujang"
25. "Selamat anda mendapatkan hadiah uang seberapa 10juta rupiah🎉"

#### 25 Contoh Data Label 1 (Judi Online):
1. "Baru aja daftar di ✅ 𝗕𝗔𝗥𝗗𝗜𝟰𝗗 ✅. spin 10k dapet 5 scatter! Langsung ajak temen daftar.."
2. "Mampir sebentar, betah selamanya ♠🐉 ℕ𝕒𝕤𝕒𝔾𝕒𝕞𝕚𝕟𝕘 💙🎅"
3. "Gila hoki! Main modal receh malah tembus 20jt 🅱️🅰️🅽 🆃🅴🅽🅶 🅷🅾️ 🅺🅸🎉"
4. "Tenang melangkah hasil besar Seacrh Google ❄️𝗝 𝗨 𝗡 𝗜 𝗢 𝗥 𝟴 𝟴❄️"
5. "Cocok dimainkan siapa saja, Ketik Di Google❣️ 𝗝 𝗨 𝗡 𝗜 𝗢 𝗥 𝟴 𝟴❣️"
6. "Sekali nyampe,pengen lama 🍓💀 ṄäṡäĠäṁïṅġ 🌷🐯"
7. "Seru banget vlognya! 💕𝐌0𝐍𝐀𝟒𝐃🟣 bikin petualanganmu kelihatan epik, kapan ke tempat lain lagi?"
8. "Bikin senyum sendiri! 𝐓𝐈𝐌𝐎𝟒𝐃"
9. "Sumpah,🏴‍☠️𝓟𝓡𝓞𝓑𝓔𝓣855🏴‍☠️luar biasa! Visualnya kece, ceritanya menyentuh, dan hadiahnya bikin jantungan. Pengalaman gaming yang top!💯"
10. "Gila, ❤𝐌𝐎𝐍𝐀 𝟒𝐃🔴 bikin nagih! Ceritanya dalam, visualnya ciamik, kemenangannya bikin kaget! 🔥"
11. "Desain kaos distro lokal mulai banyak cetak ＰＵＬＡＵＷＩＮ."
12. "Mending cuan beneran di ɪꜱᴛᴀɴᴀʙᴇᴛ17🌠 dari pada cuma scroll doang"
13. "Cuman mo bilang makasih udh ngasih tauGa ru da Ho ki gua jp😽🔥"
14. "05:00 ＰⓤＬＡＵ777, peluang besar untuk setiap pemain"
15. "Insyaallah dah kebeli !!💙P R O B E T  8 5 5💙"
16. "Musik dan efek sinkron banget, vibes keren ❤𝐒𝐔𝐑𝐘𝐀𝟖𝟖❤ 🎵🔥"
17. "Gokiill jepe trus gua diG ar u da H o k i😎"
18. "𝐃⁠​𝐎​𝐑‍𝐀⁠‌𝟕‌⁠𝟕 Inspiratif banget, terima kasih."
19. "baru 25 menit udah Jp 40jeti diGar uda hoki🙈"
20. "😎 Pulau777 selalu top buat hiburan"
21. "Mantap sekali! Main di 𝐃⁠​𝐎‍𝐑⁠⁠𝐀⁠‍𝟕‍⁠𝟕lancar, cuan pun lancar jaya!"
22. "Jakpot langsung mengalir begitu main di 𝐃​‌𝐎‌⁠𝐑‍𝐀‍𝟕‍‍𝟕, nggak bisa percaya!"
23. "Mencari platform yang mudah digunakan dan lugas? 𝐃⁠​𝐎‍𝐑⁠⁠𝐀⁠‍𝟕‍⁠𝟕mungkin jawabannya."
24. "Auto sultan berkat 𝐃‍‌𝐎‌‍𝐑⁠​𝐀⁠𝟕​​𝟕! Keren abis!"
25. "mudah maxwinnya hanya di 𝐆𝐄𝐋𝐎𝐑𝐀𝟒𝐃"

----------------------------------------

### 2.3 Dataset 3: yaemico/deteksi-judi-online

- **File Lokasi**: [`datasets/yaemico_deteksi-judi-online/youtube_chat_jogja_clean.csv`](file:///datasets/yaemico_deteksi-judi-online/youtube_chat_jogja_clean.csv)
- **Dimensi**: 6,350 baris × 5 kolom
- **Provenance / Sumber**: Data tangkapan live chat YouTube dari siaran langsung CCTV publik Daerah Istimewa Yogyakarta (file: `youtube_chat_jogja_clean.csv`). Live streaming CCTV publik sering menjadi target bot spammer judi online.
- **Duplikasi**: 0 baris duplikat persis (0.0%), 3,621 teks duplikat (57.02%)
- **Distribusi Label**: Label 0 = 3,163 (49.81%) | Label 1 = 3,187 (50.19%)

#### Arti & Semantik Setiap Kolom:
- `datetime` (*str*, null: 0): Waktu pengiriman pesan obrolan (format: YYYY-MM-DD HH:MM:SS). Sangat berguna untuk deteksi burst spam.
- `author_name` (*str*, null: 0): Nama akun pengirim pesan di live chat YouTube.
- `message` (*str*, null: 2): Pesan asli live chat. Catatan: terdapat 2 baris bernilai null.
- `cleaned_message` (*str*, null: 2): Pesan setelah tanda baca dibersihkan. Terdapat 2 baris bernilai null.
- `label` (*int64*, null: 0): Kelas biner: 0 = Chat warga/penonton umum (49,81%), 1 = Spam promosi bot judi online (50,19%).

#### Top Spam Bot Duplicates:
- `931x kemunculan`: "KETIK DI GOOGLE:WISDOMTOTO"
- `554x kemunculan`: "100RB GRATIS WISDOMTOTO:fire:"
- `513x kemunculan`: "FREEBET 100RB :fire:WISDOMTOTO:fire:"

#### 25 Contoh Data Label 0 (Bukan Judi):
1. "assalamu'alaikum.."
2. "sampe jam brp"
3. "selamat ulang tahun jogja"
4. ":face-pink-tears:"
5. "ya itu bener itu mbak/mas za Saputra"
6. "bujang anom"
7. "sampe jam berapa sih?"
8. "Sabar ok"
9. "nek ragelem"
10. "Selamat ulang taun jugja Semoga Tambah jaya sukses Semua nya Amin ,,,aku orang jugja lagi di Rantau,,,"
11. "keren bang"
12. "maburo mas"
13. "Astaga watik"
14. "tak itik"
15. "STOP JUDOL:no_entry::no_entry:"
16. "@edelweiss enda : iya"
17. "1 motor 5000"
18. "wih ada mbak aku"
19. "selamat ulang tahun kota Jogja semoga semakin istimewa :fire::fire:"
20. "tukang drone gajine kurang yak e wkwk"
21. "es es es"
22. "pibesdey jogjaku istimewa:red_heart::red_heart:"
23. "spam langsung blok saja"
24. "senang lihatnya, istimewa"
25. "menyala jogjaku:fire::fire:"

#### 25 Contoh Data Label 1 (Judi Online):
1. "VIP 500 RIBU"
2. "info link gacor"
3. "NewMember :star:PAS4D Pasti Jp SUDAH PASTI"
4. "cuman di :smiling_face_with_heart_eyes:PAS4D:smiling_face_with_heart_eyes:DAFTAR dapat Freechip"
5. ":star:PAS4D Tempat Cari Cuan No 1 Indonesia"
6. "PAS4D :star: Gacor"
7. ":star:PAS4D Anti Rungkad Boskuh"
8. "100RB GRATIS WISDOMTOTO:fire:"
9. "KETIK DI GOOGLE:WISDOMTOTO"
10. "100rb gratis wisdomtoto:sparkler:"
11. "DAFTAR DAPAT100RB"
12. "KETIK DI GOOGLE : WISDOMTOTO"
13. "tolong komen acaranya saja dong..jangan wisdomtoto tu apa sih..ga ngerti aku..smg itu bukan orang Jogja :smirking_face:"
14. "100 rb gratis wisdomtoto"
15. "BWTOGEL lagi gacorr"
16. "𝗱𝗽 𝟭𝟬𝟬 𝗷𝗱 𝟮𝗷𝘁 buruan gas di :fire: 𝗠𝗘𝗧𝗘𝗢𝗥𝗪𝗜𝗡 :fire:"
17. "FREEBET 100RB :fire:WISDOMTOTO:fire:"
18. "SLOT GACOR:fire: WISDOMTOTO:fire:"
19. "slot gacor"
20. "FREEBET 100RB WISDOMTOTO:fire:"
21. "MAU PAS4D SAIKI WISDOMTOTO"
22. "yang ketik wisdomtoto itu blokir aja minnn menganggu aja"
23. "𝗱𝟯𝗣𝟬 𝟭𝟬𝟬 j𝗱 𝟮𝗷𝘁 buruan gas 𝗚𝗔𝗥𝗔𝗡𝗦𝗜 𝟭𝟬𝟬% di :fire: 𝗠𝗘𝗧𝗘𝗢𝗥𝗪𝗜𝗡 :fire:"
24. "FREEBET 100RB :fire: WISDOMTOTO :fire:"
25. "PASTI MAXWIN:fire: WISDOMTOTO:fire:"

----------------------------------------

### 2.4 Dataset 4: kyyyy8/dataset-komentar-judi-online-platform-youtube

- **File Lokasi**: [`datasets/kyyyy8_dataset-komentar-judi-online-platform-youtube/dataset_komentarJudol_preprocessed_nonAnom.csv`](file:///datasets/kyyyy8_dataset-komentar-judi-online-platform-youtube/dataset_komentarJudol_preprocessed_nonAnom.csv)
- **Dimensi**: 18,902 baris × 6 kolom
- **Provenance / Sumber**: Dataset YouTube terkurasi dengan metadata API resmi (`comment_id`, `author`, `time_parsed`). Berisi 18.902 komentar dengan proporsi label yang seimbang (52,11% judi vs 47,89% non-judi).
- **Duplikasi**: 0 baris duplikat persis (0.0%), 8,243 teks duplikat (43.61%)
- **Distribusi Label**: Label 0 = 9,052 (47.89%) | Label 1 = 9,850 (52.11%)

#### Arti & Semantik Setiap Kolom:
- `comment_id` (*str*, null: 0): ID unik komentar dari YouTube Data API v3 (misal: `UgxYuOnKVrvEasBZ3mR4AaABAg`). Berguna untuk mencegah data leakage.
- `author` (*str*, null: 0): Username pengunggah komentar (diawali tanda `@`).
- `time_parsed` (*float64*, null: 0): Unix timestamp waktu komentar diunggah.
- `text` (*str*, null: 0): Teks asli komentar mentah.
- `label` (*int64*, null: 0): Kelas biner: 0 = Non-judi, 1 = Promosi judi online.
- `text_preprocessed` (*str*, null: 476): Teks hasil pra-pemrosesan (stemming & stopword removal). Terdapat 476 baris NaN.

#### Top Spam Bot Duplicates:
- `86x kemunculan`: "Pertama"
- `53x kemunculan`: "😂😂"
- `48x kemunculan`: "😂😂😂"

#### 25 Contoh Data Label 0 (Bukan Judi):
1. "Gw ingat ayat keramat ini "Di pulangkan oleh tim yg mereka pilih" 😂"
2. "Andai aja yang lolosnya TLID tapi sayang di Play off langsung lawan final boss onic"
3. "Wkwkwkwkwk"
4. "Keliatan sudah kagak niat"
5. "Aduh... Aduh... Bisa ga sih guy...?... Wkwkkwkwkwk"
6. "Badut mah tetep aja badut ygy"
7. "ini diaa bacotan yany gua tunggu🤣"
8. "Lihat yng lengkap .. kalah 2 1 kongdom bocor 😂😂😂😂"
9. "Bang pascol main Mario go-kart pasti mantap"
10. "woi bujang"
11. "Semoga bugnya nggak bikin kita semua ikut panik juga, hehe 😄"
12. "P mabar 267025513"
13. "smlm yg doate ngakakak wkwkwkwk"
14. "Bang pascol rumah aku deket rumah mu"
15. "Gimana wak pas ikut demo"
16. "Msh inget aja, jaman Ama Luan luan"
17. "Respek bang pascolll semangat bang"
18. "Biasa awal seson gini"
19. "Uy"
20. "NIAT LH KAU SIKIT BIKIN JUDUL SETAN..APA PULAK  YU ????"
21. "Kern 😂😂😂😂😂"
22. "😅😅😅😅"
23. "2:22"
24. "Ini saatnya ga sih kent lu pindah jadi Sonicker😂😂"
25. "Selamat anda mendapatkan hadiah uang seberapa 10juta rupiah🎉"

#### 25 Contoh Data Label 1 (Judi Online):
1. "𝗔𝗟𝗘𝗫𝗜𝗦𝟭𝟳❤️ tuh emang selalu relate sama vibe video kayak gini"
2. "Scatter nyata bukan wacana ❤𝙍𝘼𝙅𝘼𝟲𝟮❤ 😁"
3. "04:34 Subhanallah,🌍ℙℝ𝕆𝔹𝔼𝕋855🌍bikin pengalaman main jadi beda! Ceritanya penuh makna, visualnya keren, dan hadiahnya bikin dompet senyum!💯"
4. "❤𝐌𝐎𝐍𝐀 𝟒𝐃🔴 emang luar biasa! Baru main sebentar, langsung dapet kejutan gede. Ceritanya top banget! 🌟"
5. "Rezeki dari,🎱𝓟𝓡𝓞𝓑𝓔𝓣855🎱bikin senyum lebar hari ini. Terima kasih banyak!💯"
6. "Ngobrol sama stranger di kereta pun bisa nyambung gara-gara ❝PULAUWIN❞."
7. "Ngopi sambil muter diGaruda Hoki Manteeb bat🐼"
8. "Sound yang dipake ⭐SGI ퟴퟴ⭐️ selalu pas banget"
9. "Memang pantas sih mendapatkan gelar terbaik 𝕊𝔸𝕐𝔸𝟜𝔻 sebagus ini tampilan dan konsepnya"
10. "̶P̶U̶L̶A̶U̶7̶7̶7̶. platform untuk pemain yang siap menang"
11. "JARANG BANGET saya nemu channel nya seperti ini 🤎𝐏𝐑𝐎𝐁𝐄𝐓 𝟖𝟓𝟓🤎 dan jangan pernah lewatkan channel terbaru disini !!"
12. "Gameplay super smooth, mantap banget ❤𝐌𝐀𝐁𝐀𝐑𝟖𝟖❤ ⚡🎮"
13. "00:30 Wow💙P R O B E T  8 5 5💙beda banget! Ceritanya mengalir, visualnya kece !!"
14. "Pecah terus di 𝐃𝐎𝐑𝐀𝟕𝟕, maxwin"
15. "Puas banget 𝐀⁠⁠𝐄‌‌𝐑‌𝐎⁠𝟖⁠𝟖 liat videonya."
16. "00:57🀄ℙℝ𝕆𝔹𝔼𝕋855🀄emang juara! Baru main sekali, langsung jatuh cinta sama konsep dan ceritanya. Harus coba!💯"
17. "Push rank emang butuh kerja tim! Kalo mau push rekening, cobain Kyt4d aja! Dijamin lebih mudah dari push Mythic~ 📊💎"
18. "🎶 Main asik tiap hari di Pulau777"
19. "hari ini dapat hadiah besar dari ＪＵＲＡＧＡＮＱＱ"
20. "Awalnya iseng doang main di 𝐃⁠​𝐎‍𝐑⁠⁠𝐀⁠‍𝟕‍⁠𝟕, eh malah ketagihan! Cuan terus nih!"
21. "Main cuma sebentar, hasilnya luar biasa! Kalo belum coba di 𝐃​‌𝐎‌⁠𝐑‍𝐀‍𝟕‍‍𝟕, pasti bakal nyesel!"
22. "𝐃⁠​𝐎‍𝐑⁠⁠𝐀⁠‍𝟕‍⁠𝟕memberikan kesempatan untuk mencapai potensi penuh Anda."
23. "Tarik semua hasil jerih payah di 𝐃⁠​𝐎‍𝐑⁠⁠𝐀⁠‍𝟕‍⁠𝟕, saatnya investasi masa depan!"
24. "09:11 Gak nyangka, 𝙋𝙧𝙤𝙗𝙚𝙩8️⃣5️⃣5️⃣ sekeren ini! Ceritanya relate, visualnya top! 🔥"
25. "Gua dulu pernah fans RRQ jaman TUTURU.... setelah itu gua fans ONIC sampai sekarang ......... Tau sendiri kan RRQ skrg cuma bacot sama teori saja yg gede, fakta dan praktek nya nihil alias HAMPA.... 😂😂😂😂😂,  Gini kok di bilang raja dari segala raja ... Hahaha MEMEEEKKKK MEMEEEKKKK"

----------------------------------------

### 2.5 Dataset 5: ferdiansakti/gambling-comments-from-youtube-platform

- **File Lokasi**: [`datasets/ferdiansakti_gambling-comments-from-youtube-platform/rawdata.csv`](file:///datasets/ferdiansakti_gambling-comments-from-youtube-platform/rawdata.csv)
- **Dimensi**: 4,720 baris × 2 kolom
- **Provenance / Sumber**: Dataset komentar YouTube berfokus pada invasi bot promosi kasino/slot `ambil4d` di berbagai kolom komentar kanal Indonesia.
- **Duplikasi**: 516 baris duplikat persis (10.93%), 518 teks duplikat (10.97%)
- **Distribusi Label**: Label 0 = 1,187 (25.15%) | Label 1 = 3,533 (74.85%)

#### Arti & Semantik Setiap Kolom:
- `Label` (*int64*, null: 0): Kelas biner: 0 = Bukan Judi (25,15%), 1 = Promosi Judi (74,85% - mayoritas promosi sindikat ambil4d).
- `Comments` (*str*, null: 0): Teks komentar mentah dari pengguna dan bot spam YouTube.

#### Top Spam Bot Duplicates:
- `13x kemunculan`: "itu si rojali doyan banget main di ambil4d sampe kebeli mobil"
- `10x kemunculan`: "Sangat keren! Meraih kemenangan besar di ambil4d langsung berlibur ke luar negeri!"
- `10x kemunculan`: "alasan aku menikah karena aku dapat modal dari ambil4d"

#### 25 Contoh Data Label 0 (Bukan Judi):
1. "Lah ke sol*r*a yg nunggu 1 jam aja masih gw tunggu in 😂"
2. "Kremes nya halal kan?"
3. "Gw ngeri sekarang mau makan di resto yg punya Chindo...semenjak kasus ayam bakar Haram solo ...jd ngeriii 😮"
4. "Seru kayanya yah...labirin...kebersamaannya pasti lbh kuat...😊"
5. "Jepit di ketek juga masak"
6. "Kabupaten Babelan kali... 😂"
7. "pernah bg -14"
8. "sini bang mampir kerumah ane, di perum cadar 2 jejalen... hehehe"
9. "Aci Ojek Online  Cocok Tuh Aci Tunggal Transportasi Anak Indonesia Cocok Buat Costumer Aci Terbaru Coba Deh"
10. "Belum punya, tapi itu hanya masalah waktu..."
11. "Mari kita berbuat untuk kepentingan bersama"
12. "Keren y❤"
13. "Ga lengkap klo ga ad keluarga besar suzuki rc jet cooled"
14. "Ajak aku kerja sama km bang biar bsa dpet thr 1 ferari"
15. "Aku kelas 3 bang 🎉🎉🎉😊❤😊❤"
16. "Temenku udah 150 streak bang"
17. "Bang semalem gw mimpi, lu ada di barisan Roy CS ikut sidang ijasah palsu.... 😂😂😂"
18. "😂 banyak yang Tidak bisa di bicarakan, ada musuh dalam selimut, coba lihat mobil listrik Indonesia 2x gagal, juga. 🎉 Mafi ini lebih kuat dari pada presiden, sangat kejam. Mafia ini belum bisa di sentuh, sampai sekarang,🎉"
19. "Mobil listrik tanah air selain yg duku ngga di lulusin pemerintah gara2 kerjaannga Dahlan Iskan ada ngga ya?"
20. "Baru?modelnya ngk berubah🤣🤣🤣"
21. "Aura botinya terasa kuat"
22. "jgn lupa e-toll nya diisi!"
23. "suami pelita utk istri nya  kebaikan ramah utk teman terdekatnya"
24. "MasyaAllah umi"
25. "Olahraga pagi membuat badan segar."

#### 25 Contoh Data Label 1 (Judi Online):
1. "Ketik google ambil4d abis itu klik deh baru ketauan apa itu ambil4d"
2. "👨‍🦲dewadora👨‍🦲 menyediakan platform untuk relaksasi dan hiburan. 😌"
3. "Keuntungan melimpah di 𝐃𝐎𝐑 𝐀 𝟕 𝟕☝, bener-bener puas banget! 🐋"
4. "Terima kasih 😴AERO-DELAPANDELAPAN! Hari ini menang besar dan bisa buat kebutuhan keluarga."
5. "Terima kasih banyak 👐dewadora👐,hari ini benar-benar gacir! 🏂"
6. "Nggak salah pilih main di 👇dewadora👇, rezekinya ngalir terus. Top banget! 🦇"
7. "dе p𝐨 diki𝐭, 𝘫adi 𝐤aya di dora77✊"
8. "𝘿𝙊𝙍𝘼 𝟳 𝟳🙅 gaсhor bang𝙚t, mek𝙨win terus"
9. "🎰 Game terbaik, peluang menang terbesar! suhu328! 💥"
10. "Dengan 𝗗-𝗢-𝗥-𝗔-𝟳-𝟳🤗 saya berhasil, dari tukang bakso jadi bos restoran. ☕"
11. "DO𝑅𝘈𝟽𝟩 menawarkan sekilas tentang masa depan interaksi daring."
12. "gimana sih caranya daftar di poipet308, denger2 lagi bagi thr"
13. "Siapa yang nemu video ini dari rekomendasi? 🔺pluto88🔺"
14. "⚡ Semua jadi mungkin, karena macau328 terbaik! 🎰💥"
15. "🎯 Kesempatan emas menanti di suhu328! 💥"
16. "Berkat 𝐷O𝘙𝘼77 saya mendapatkan modal yang membantu mengembangkan usaha saya."
17. "Hasil dari 𝐷ОRА𝟩𝟽 membuktikan saya bisa beralih dari pembantu rumah jadi pengusaha kebersihan."
18. "Kalo lo suka hasil cepet, lo harus kenalan sama 📈𝑲 𝑨 𝑲 𝑰 777😎."
19. "PawPaw4D itu hiburan digital yang paling aku suka akhir-akhir ini!"
20. "H0k1e banget nih di dibed4d, 🎯 menang gede terus, Jeipe gede 💥"
21. "Tarik semua kemenangan dari 𝘋𝘌𝙒𝐀𝐃OЯА, saatnya belanja!"
22. "Main di 𝐴𝐆𝙐𝑆𝘛𝘖𝐓𝑂-bikin aku lebih optimis sama rezeki, thank you!"
23. "Gachor maxwin modal malam jadi 9!"
24. "Daftar di olympus128 bonus 155%!"
25. "WD 5x tanpa kendala di manjurbet.com!"

----------------------------------------

## 3. ANALISIS LINTAS DATASET: OVERLAP DATA, KONTAMINASI & KONFLIK LABEL

Analisis komparatif dilakukan dengan mencocokkan teks (*exact match* pada teks yang telah dinormalkan huruf kecil dan spasi luarnya) antar-pasang dataset. Temuan ini sangat krusial jika Anda berencana menggabungkan (*concatenate*) dataset ini menjadi satu korpus besar.

### Tabel 3.1: Matriks Irisan Teks Antar Dataset

| Pasangan Dataset | Jumlah Teks Sama (Shared Unique) | Jumlah Konflik Label | Catatan / Indikasi |
|---|:---:|:---:|---|
| `DS1_fahruu vs DS2_kyyyy8_all` | 57 | 0 | Overlap wajar (komentar pendek umum seperti 'pertama', 'mantap', dll). |
| `DS1_fahruu vs DS3_yaemico` | 9 | 0 | Overlap wajar (komentar pendek umum seperti 'pertama', 'mantap', dll). |
| `DS1_fahruu vs DS4_kyyyy8_plat` | 31 | 1 | ⚠️ **KRUSIAL**: Terdapat 1 teks dengan label berlawanan! |
| `DS1_fahruu vs DS5_ferdiansakti` | 14 | 0 | Overlap wajar (komentar pendek umum seperti 'pertama', 'mantap', dll). |
| `DS2_kyyyy8_all vs DS3_yaemico` | 41 | 0 | Overlap wajar (komentar pendek umum seperti 'pertama', 'mantap', dll). |
| `DS2_kyyyy8_all vs DS4_kyyyy8_plat` | 10,561 | 48 | ⚠️ **KRUSIAL**: Terdapat 48 teks dengan label berlawanan! |
| `DS2_kyyyy8_all vs DS5_ferdiansakti` | 8 | 0 | Overlap wajar (komentar pendek umum seperti 'pertama', 'mantap', dll). |
| `DS3_yaemico vs DS4_kyyyy8_plat` | 16 | 0 | Overlap wajar (komentar pendek umum seperti 'pertama', 'mantap', dll). |
| `DS3_yaemico vs DS5_ferdiansakti` | 2 | 0 | Overlap wajar (komentar pendek umum seperti 'pertama', 'mantap', dll). |
| `DS4_kyyyy8_plat vs DS5_ferdiansakti` | 5 | 0 | Overlap wajar (komentar pendek umum seperti 'pertama', 'mantap', dll). |

### Temuan Kritis: Konflik Label Antara DS2 dan DS4 (Uploader: kyyyy8)
Dataset `DS2_kyyyy8_all` (45.592 baris) dan `DS4_kyyyy8_plat` (18.902 baris) memiliki **10.561 teks yang identik**. Namun, terdapat **48 teks dengan label berlawanan (*conflicting labels*)**! Contoh bukti inkonsistensi pelabelan:

1. **Komentar Diskusi Esports (Non-Judi Salah Dilabeli Judi di DS4):**
   - Teks: *"padahal udah pada tau kunci onic itu di duo mid sama roam dan kebiasaan rrq gonta ganti pemain di mpl..."*
   - Label di DS2: `0` (Bukan Judi - Benar)
   - Label di DS4: `1` (Judi - **False Positive Annotation Error**)
   - Teks: *"bang bikent vibes nya udah beda banget udah ga berapi api kaya dulu"*
   - Label di DS2: `0` (Bukan Judi - Benar)
   - Label di DS4: `1` (Judi - **False Positive Annotation Error**)

2. **Komentar Promosi Situs Judi (Judi Lolos Dilabeli Non-Judi di DS4):**
   - Teks: *"0:56 wifi4d bukti nyata, bukan sekadar janji.🎉"*
   - Label di DS2: `1` (Judi - Benar, 'wifi4d' adalah nama situs slot)
   - Label di DS4: `0` (Bukan Judi - **False Negative Annotation Error**)

3. **Konflik Antara DS1 (fahruu) dan DS4 (kyyyy8):**
   - Teks: *"gasskuyy dari bang toing katanya,ga ruda-ho ki-badai petir🔥🔥"*
   - Label di DS1: `1` (Judi - merujuk 'garuda hoki' & 'petir zeus')
   - Label di DS4: `0` (Non-judi)

## 4. ANALISIS SEMANTIK & INKONSISTENSI PELABELAN ANTAR DATASET

Berdasarkan audit anotasi manual, definisi 'Judi Online' antar pembuat dataset memiliki nuansa yang berbeda:

1. **DS1 (fahruu)**: Mendefinisikan kelas 1 secara spesifik pada **promosi atau ajakan aktif bermain situs judi** (misal memuat nama bandar seperti `GunungWin`, `Alexis17`). Komentar warga yang membahas judi dari sudut pandang sosial/hukum tetap dilabeli 0.
2. **DS2 & DS4 (kyyyy8)**: Menunjukkan adanya *human annotator noise* atau kesalahan pelabelan otomatis berbasis aturan sederhana. Beberapa komentar murni esports dan review gawai masuk ke label 1.
3. **DS3 (yaemico)**: Fokus pada lingkungan **Live Chat spamming**. Semua pesan bot yang memuat promo kredit gratis ('Freechip', 'VIP 500rb', 'Ketik di google') dilabeli 1, sedangkan sapaan penonton biasa ('hujan deras min', 'salam dari bantul') dilabeli 0.
4. **DS5 (ferdiansakti)**: Sangat terdistorsi (*imbalance* 74,8% label 1) karena didominasi oleh ribuan bot satu sindikat (`ambil4d`). Anotasi di sini lebih sempit karena hampir seluruh korpus diambil dari video yang dibanjiri bot kampanye tersebut.

## 5. ANALISIS METADATA & PENCEGAHAN DATA LEAKAGE

Salah satu jebakan terbesar dalam deteksi komentar spam/judi online adalah **Data Leakage** akibat duplikasi masif oleh bot akun ternak.

- **Kasus Nyata**: Di DS3, pesan `KETIK DI GOOGLE:WISDOMTOTO` muncul **931 kali**! Di DS1, pesan `*GUNUNGWIN* yang paling bagus!` muncul **71 kali**.
- **Dampak Jika Train-Test Split Dilakukan Acak (Random Split)**: Teks spam yang sama persis akan tersebar ke set *training* dan set *testing*. Model NLP (terutama TF-IDF, BERT, atau LLM) hanya akan 'menghafal' teks bot tersebut. Akibatnya, nilai akurasi uji tampak fantastis (99%), namun model akan gagal total ketika diuji pada teks baru di dunia nyata (*overfitting to bot signatures*).
- **Pencegahan Menggunakan Metadata**:
  * **Author Grouping (`GroupKFold` by `author`/`author_name`)**: Memastikan komentar dari satu akun/bot hanya ada di train ATAU test, tidak boleh bocor ke keduanya.
  * **Temporal Split (`time_parsed` / `datetime`)**: Membagi data berdasarkan lini masa (misal 70% waktu awal untuk train, 30% waktu akhir untuk test). Pola ini menguji apakah model mampu mendeteksi istilah slang/situs baru yang muncul belakangan.
  * **Teks Deduplikasi Pre-Split**: Sebelum data dibagi, seluruh teks duplikat harus dikurangi (*deduplicated*) agar evaluasi menguji kemampuan pemahaman bahasa, bukan frekuensi kemunculan spam.

## 6. ANALISIS KASUS BORDERLINE & TEKS AMBIGU

Audit menemukan beberapa kategori teks yang berisiko tinggi membingungkan model kecerdasan buatan:

### Kategori A: Kata Kunci 'Judi'/'Slot' dalam Konteks Positif / Non-Judi (False Positive Trap)
Model sederhana berbasis kamus kata kunci (*lexicon-based*) akan gagal pada komentar berikut karena mengandung kata judi/slot padahal bermakna kontra-judi (Label 0):

- *"all-rounder, sensor lengkap, masih ada slot mircoSD"* (DS2) -> Kata 'slot' adalah slot kartu memori smartphone.
- *"ora promosi slot woiii"* (DS3) -> Warga lokal menegur spammer di live chat.
- *"pak budi kan sudah pernah klarifikasi, bahwa dia akan/lagi fokus ke koperasi... liat aja tuh udah panen berapa milyar hasil dari koperasi judol mereka"* (DS1) -> Kritik satir terhadap pemerintah.
- *"Isi komentar nya judol semua anjir"* (DS5) -> Keluhan penonton terhadap spam bot.
- *"Gunawan Sadbor jadi duta anti judol lucu bet anying"* (DS1) -> Opini berita sosial.

### Kategori B: Stealth Promotion & Font Obfuscation (False Negative Trap)
Bot judi masa kini tidak lagi menulis kata 'judi online' atau 'slot gacor' secara gamblang. Mereka menggunakan teknik evasif berikut:

- **Mathematical Alphanumeric Unicode (Bypass Filter)**: Menggunakan font tebal/miring unicode matematika seperti `𝗔𝗟𝗘𝗫𝗜𝗦𝟭𝟳`, `𝗕𝗔𝗥𝗗𝗜𝟰𝗗`, `𝐊𝐄𝐌𝐁𝐀𝐑𝟕𝟖`, `ＰＵＬＡＵＷＩＮ`. Di DS4, terdapat **35,21%** teks yang menggunakan karakter ini!
- **Simbol Pemisah & Sensor Diri**: `ALEXIS-☯17☯`, `█ambil4d█`, `w!f!4d`, `ga ruda-ho ki-badai petir`.
- **Penyamaran Timestamp YouTube**: Menulis timestamp palsu agar terlihat seperti komentar relevan: `0:56 wifi4d bukti nyata, bukan sekadar janji.🎉`.
- **Teks Sangat Pendek Tanpa Kata Kunci**: `VIP 500 RIBU`, `info link gacor`, `WD lancar`.

## 7. EVALUASI KOLOM PREPROCESSING VS RAW TEXT

Sesuai instruksi audit: **Pertahankan raw/original text, jangan lakukan stemming, stopword removal, atau cleaning prematur!**
Berikut evaluasi kolom pra-pemrosesan bawaan yang terdapat pada dataset:

1. **Kolom `final_comment` pada DS1 (fahruu)**: Mengubah kata 'gue' -> 'saya', 'lu' -> 'kamu', serta menghapus angka jam. Hal ini berisiko menghilangkan variasi dialek dan ritme penulisan asli.
2. **Kolom `text_preprocessed` pada DS2 & DS4 (kyyyy8)**:
   - Menghapus seluruh emotikon, tanda baca, dan karakter non-ASCII.
   - **Kerusakan Data**: Terdapat **1.213 baris di DS2 dan 476 baris di DS4 yang menjadi kosong (NaN)** karena komentar aslinya hanya memuat emoji/simbol.
   - Mengonversi font Unicode matematika (seperti `𝗔𝗟𝗘𝗫𝗜𝗦`) secara serampangan atau menghapusnya, padahal jenis font ini adalah *fitur diskriminatif terkuat* untuk mendeteksi bot judi!
3. **Kolom `cleaned_message` pada DS3 (yaemico)**: Menghapus tanda baca, namun format bot seperti `:fire:` atau simbol chat YouTube menjadi teks biasa.

> **Kesimpulan Teknis**: Untuk pemodelan modern berbasis Transformer/BERT (seperti IndoBERT) atau LLM, **wajib menggunakan kolom Raw Text (`comment`, `text`, `message`, `Comments`)**. Arsitektur Transformer membutuhkan konteks utuh, tanda baca, huruf kapital, dan simbol untuk memahami makna kalimat.

## 8. REKOMENDASI AWAL: KEEP / REVIEW / EXCLUDE

*(Catatan: Rekomendasi ini adalah panduan strategis; tidak ada data yang diubah atau dihapus pada tahap ini)*

### 1. `fahruu/komentar-judi-online` (DS1) -> **STATUS: KEEP (DIREKOMENDASIKAN)**
- **Alasan**: Kualitas anotasi sangat baik, pemisahan konteks diskusi sosial vs promosi judi sangat jelas, rasio label seimbang (62% : 38%), serta memuat variasi bahasa slang Indonesia yang kaya.
- **Saran Penggunaan**: Gunakan kolom `comment` (raw), lakukan deduplikasi teks terlebih dahulu.

### 2. `kyyyy8/dataset-komentar-judi-online-platform-youtube` (DS4) -> **STATUS: REVIEW (PERLU KURASI)**
- **Alasan**: Memiliki metadata terlengkap (`comment_id`, `author`, `time_parsed`) yang sangat berharga untuk pengujian bebas *leakage*. Namun, terdeteksi memiliki sedikitnya 48 konflik anotasi dengan DS2 dan beberapa false positive pada diskusi esport.
- **Saran Penggunaan**: Lakukan verifikasi otomatis/manual pada 48 data berkonflik sebelum digabungkan.

### 3. `kyyyy8/dataset-komentar-judi-online-di-youtube` (DS2) -> **STATUS: REVIEW / SELECTIVE MERGE**
- **Alasan**: Berukuran terbesar (45.592 baris), namun memiliki tumpang tindih (overlap) sebanyak 10.561 baris dengan DS4 tanpa metadata pendukung. Jika digabung langsung tanpa deduplikasi lintas dataset, akan terjadi redundancy masif.
- **Saran Penggunaan**: Ambil subset unik yang tidak beririsan dengan DS4 setelah deduplikasi teks.

### 4. `yaemico/deteksi-judi-online` (DS3) -> **STATUS: REVIEW (KHUSUS DOMAIN LIVE CHAT)**
- **Alasan**: Karakteristik data sangat spesifik (Live Chat CCTV Jogja, kalimat sangat pendek, duplikasi spam ekstrem >57%).
- **Saran Penggunaan**: Sangat baik jika digunakan sebagai **Out-of-Distribution (OOD) Test Set** untuk menguji apakah model yang dilatih pada komentar YouTube standar mampu mendeteksi spam di lingkungan *Live Streaming*.

### 5. `ferdiansakti/gambling-comments-from-youtube-platform` (DS5) -> **STATUS: REVIEW / OVERSAMPLED BOT SPECIFIC**
- **Alasan**: Sangat tidak seimbang (74,8% label 1) dan terkonsentrasi pada satu nama situs (`ambil4d`). Jika dimasukkan tanpa pembobotan, model berisiko bias hanya mengenali pola sindikat `ambil4d`.
- **Saran Penggunaan**: Deduplikasi agresif pada teks promosi `ambil4d` dan gunakan sebagai data pengaya (*data augmentation*).
