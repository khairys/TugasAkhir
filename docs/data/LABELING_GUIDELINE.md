# PEDOMAN ANOTASI DAN HARMONISASI LABEL (LABELING GUIDELINES)

### Penelitian: Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Text Obfuscation pada Komentar YouTube Bahasa Indonesia

---

## 1. Definisi Target Klasifikasi Biner
- **Kelas 1 (`Promotion`)**: Komentar yang secara langsung maupun tidak langsung mendorong, memengaruhi, membujuk, meyakinkan, mengarahkan, atau mengajak audiens untuk bermain, mendaftar, mengakses, atau menggunakan layanan judi online.
- **Kelas 0 (`Non-Promotion`)**: Komentar yang tidak berfungsi mempromosikan perjudian, mencakup kritik sosial, opini hukum/berita, keluhan terhadap spammer, komentar anti-judi, konteks non-judi (misal slot kartu memori), dan komentar umum YouTube.

## 2. Kriteria dan Subkategori Promosi (Kelas 1)
1. **Explicit Advertisement**: Ajakan langsung atau informasi tawaran promosi (contoh: *"daftar di X"*, *"bonus freechip 100rb"*, *"depo disini"*).
2. **Call to Action (CTA)**: Dorongan bertindak (contoh: *"buruan join"*, *"ketik di google X"*, *"gas sekarang"*).
3. **Promotional Claim**: Klaim performa kemenangan atau kemudahan platform (contoh: *"gacor parah"*, *"wd lancar kilat"*, *"depo kecil pasti jepe"*).
4. **Testimonial / Social Proof**: Cerita testimoni pengalaman cuan/menang yang berfungsi sebagai *social proof* (contoh: *"berkat X kebeli mobil"*, *"thanks X uang jajan cair"*).
5. **Site / Brand Endorsement**: Rekomendasi merek/situs judi (contoh: *"X paling terpercaya"*, *"main di X aja"*).
6. **Obfuscated Promotion**: Seluruh promosi di atas yang kata-katanya disamarkan menggunakan font unicode matematika (`𝗔𝗟𝗘𝗫𝗜𝗦𝟭𝟳`), pemisahan spasi (`T O K E 6 9`), karakter sensor (`█ambil4d█`), atau timestamp palsu YouTube (`0:56 WiFi4D bukti nyata`). *Bentuk obfuscation tidak mengubah label semantik menjadi 0!*.

## 3. Kriteria dan Subkategori Non-Promosi (Kelas 0)
1. **Anti-Gambling**: Ajakan menjauhi judi atau edukasi dampak buruk judol (contoh: *"jangan main judi, bikin miskin"*).
2. **Kritik / Berita / Diskusi Sosial**: Pembahasan fenomena judi dari sudut pandang sosial, penegakan hukum, atau berita (contoh: *"pemerintah harus berantas judol sampai ke akarnya"*).
3. **Keluhan terhadap Spammer**: Protes penonton terhadap bot spammer (contoh: *"isi komentar judol semua anjir"*, *"ora promosi slot woiii"*).
4. **Konteks Non-Judi (False Keyword Trap)**: Komentar memuat kata mirip judi tetapi konteksnya murni non-judi (contoh: *"masih ada slot microSD"* -> slot memori gadget; *"hero Miya dapat bonus damage"* -> skill game).
5. **Komentar Reaksi Umum**: Komentar biasa YouTube (contoh: *"lucu banget"*, *"pertama"*, diskusi taktik esport MPL).

## 4. Prinsip Penanganan Kasus Ambigu & Larangan Keyword-Only
- **Larangan Keyword-Only Labeling**: Dilarang keras menetapkan label hanya karena teks memuat kata `slot`, `judi`, `zeus`, atau `bonus`. Konteks komunikatif wajib dianalisis.
- **Uncertain Label Handling**: Jika konteks komentar tidak dapat dipastikan secara aman, komentar WAJIB dialihkan ke `label_review_queue.csv` dengan `canonical_label = NULL` dan `label_status = 'review'`, bukan dipaksakan masuk ke dataset supervised.
