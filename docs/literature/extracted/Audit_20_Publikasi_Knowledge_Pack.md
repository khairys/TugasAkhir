# AUDIT MENDALAM 21 PUBLIKASI UNTUK SKRIPSI
## Evaluasi Ketahanan Model Deteksi Promosi Judi Online terhadap Penyamaran Teks pada Komentar YouTube

**Versi dokumen:** Audit Literatur v2.1 — korpus 21 publikasi  
**Tanggal audit:** 20 Oktober 2026  
**Bahan utama:** 20 PDF awal dari pengguna dan 1 publikasi tambahan (#21) yang teks lengkapnya telah diekstrak dan ditelaah melalui `docs/literature/extracted/21_online_gambling_youtube_semisupervised_indobert.md` pada branch `literature-extraction`. Semua PDF berhasil diekstrak menjadi teks yang dapat ditelusuri; audit membaca naskah lengkap, bukan abstrak saja, dengan perhatian pada pendahuluan, data dan definisi label, metode, pembagian data, hasil/tabel, diskusi, kesimpulan, keterbatasan yang dinyatakan, serta daftar pustaka. Halaman yang memuat tabel atau gambar utama juga diperiksa lewat render halaman. Metadata dan laman penerbit/arsip akademik diperiksa ulang secara daring ketika tersedia. Bila ada klaim yang teks lengkapnya ambigu, berbeda antarbagian, atau memiliki masalah bibliografi, dokumen menandainya sebagai temuan audit alih-alih merapikannya diam-diam.

> **Cara menggunakan dokumen ini.** Ini adalah *knowledge pack* penelitian, bukan naskah Bab I siap tempel tanpa penyuntingan. Gunakan ringkasan bukti untuk membangun argumentasi, kemudian kutip publikasi asli dengan gaya referensi UNDIP. Parafrasa dalam dokumen ini sengaja tidak berupa kutipan panjang verbatim. Angka dan temuan ditulis sejauh dapat ditelusuri dari naskah yang diaudit. “Interpretasi audit” dibedakan dari “temuan yang dilaporkan penulis”.

## Isi Dokumen

- **Bagian A:** ringkasan eksekutif dan prioritas audit.
- **Bagian B:** audit masing-masing dari 21 publikasi—identitas, tujuan, data, metode, hasil, kekuatan, keterbatasan, keputusan penggunaan, dan bukti yang dapat diekstrak.
- **Bagian C:** sintesis lintas publikasi, perbedaan istilah, research gap sementara, dan klaim yang harus dihindari.
- **Bagian D:** penilaian kecukupan literatur dan peta pencarian lanjutan.
- **Bagian E:** pemetaan sumber ke Bab I–V.
- **Bagian F:** *evidence bank* untuk argumentasi Bab I.
- **Bagian G:** konsistensi antara literatur dan dokumentasi eksperimen repositori.
- **Bagian H:** keputusan terhadap 21 publikasi dan daftar pemeriksaan sebelum penulisan.
- **Daftar pustaka:** metadata ringkas 21 publikasi yang diaudit.

---

# BAGIAN A. RINGKASAN EKSEKUTIF

## A1. Kesimpulan utama

Kumpulan 21 publikasi ini merupakan **fondasi yang memadai untuk menyusun peta literatur dan mulai merancang argumentasi Bab I**, tetapi **belum cukup untuk mengunci seluruh research gap tanpa perbandingan metode yang eksplisit dan pencarian tambahan yang terarah**. Korpus mencakup empat kebutuhan: (1) deteksi promosi/judi/spam pada komentar atau media sosial, (2) robustness dan perturbasi teks NLP, (3) mutu dataset, anotasi dan deduplikasi, serta (4) evaluasi berpasangan.

Kesenjangan yang masih perlu ditutup bukan sekadar “kurang jumlah jurnal”. Masalah utama adalah bahwa bukti untuk sejumlah klaim Bab I masih tidak langsung atau belum cukup spesifik. Contohnya, paper spam YouTube tidak otomatis membuktikan karakteristik promosi judi; paper judi yang membedakan “gambling-related” dari “non-gambling” tidak otomatis mendukung definisi “promotion/non-promotion”; normalisasi obfuscation tidak sama dengan mengukur ketahanan model terhadap teks mentah yang diobfuscate; dan paper evaluasi berpasangan pada level sistem tidak otomatis membenarkan semua rumus atau prosedur bootstrap yang digunakan dalam eksperimen Anda.

**Rekomendasi:** jangan menambah puluhan sumber secara acak. Pertahankan publikasi berdasarkan relevansi, bukan demi jumlah; gunakan hasil audit 21 publikasi untuk menilai klaim per klaim, lalu cari sumber tambahan hanya untuk kebutuhan bukti yang belum terisi—terutama konteks resmi Indonesia, studi obfuscation berbahasa alami yang benar-benar melakukan evaluasi sebelum/sesudah transformasi, definisi label promosi, dan justifikasi statistik untuk metrik perubahan F1.

## A2. Pemetaan tingkat relevansi

- **Studi domain langsung tentang judi, promosi, atau spam pada YouTube/media sosial Indonesia — publikasi #2–8, #18, dan #21.** Ini kelompok prioritas untuk membahas penelitian terdahulu. Setiap paper tetap harus dibandingkan berdasarkan definisi label, platform, langkah normalisasi, pembagian data, dan cara mengevaluasi penyamaran.
- **Teori dan metodologi robustness/perturbasi — publikasi 11–14 dan 17.** Kelompok utama untuk mendefinisikan robustness, menjelaskan input perturbation, dan mendukung rancangan pengujian.
- **Kualitas data dan anotasi — publikasi 15 dan 16.** Utamanya dipakai di Bab III untuk deduplikasi, pencegahan kebocoran, serta kualitas label.
- **Serangan teks dan evaluasi input berubah — publikasi 9, 12, 13, dan 17.** #9 memberi konteks adversarial attacks; #12 dan #13 lebih dekat pada perturbasi yang dapat diterapkan/diuji; #17 membahas evaluasi berpasangan, tetapi tidak identik dengan paired bootstrap CI untuk F1.
- **Representasi karakter/model karakter — publikasi 19 dan 20.** Hanya bukti pendukung tidak langsung: satu membahas SMS berbahasa Inggris dan satu membahas kode JavaScript, bukan komentar promosi judi Indonesia.
- **Spam YouTube generik — publikasi 1 dan 10.** Gunakan sebagai konteks pendukung saja, bukan landasan utama research gap promosi judi online.

## A3. Lima prinsip penting saat mengutip

1. **Akurasi atau F1 tinggi bukan bukti robustness.** Itu hanya menggambarkan kinerja pada data dan kondisi uji yang benar-benar digunakan.
2. **“Gambling-related” bukan sinonim “promosi judi online”.** Penyebutan, kritik, anti-judi, berita, atau percakapan tentang judi bisa termasuk gambling-related tanpa menjadi promosi.
3. **Model yang diuji setelah teks dinormalisasi berbeda dari model yang diuji pada teks tersamarkan mentah.** Normalisasi dapat menjadi pertahanan sistem, tetapi hasilnya bukan pengukuran murni sensitivitas model terhadap input obfuscated.
4. **Hindari klaim “belum pernah ada studi obfuscation pada judi online”.** Angelo et al. (2025) membahas normalisasi karakter pada komentar promosi YouTube, Ariyanto et al. (2026) menormalisasi istilah tersamarkan sebelum IndoBERT, dan Hidayat et al. (2026) secara eksplisit membahas komentar obfuscated dengan model hybrid.
5. **Jangan menjelaskan penyebab model gagal sebagai fakta yang sudah terbukti jika studi hanya mengamati pola prediksi.** Hubungan karakter Unicode dengan false positive, misalnya, dapat menunjukkan pola empiris; klaim bahwa attention atau tokenizer tertentu “menyebabkan” kesalahan membutuhkan pengujian mekanistik tambahan.

## A4. Prioritas sebelum Bab I ditulis

- **Prioritas 1 — perbandingan metode lintas studi:** bandingkan protokol Angelo et al. (2025), Hidayat et al. (2026), Ariyanto et al. (2026), Pariamalinya et al. (2026), Nugraha et al. (2026), dan Santika et al. (2025). Jurnal #21 sudah diaudit lengkap; tugas berikutnya adalah menyandingkan metode dan batas klaimnya, bukan mengaudit abstraknya lagi.
- **Prioritas 2 — harus disintesis:** Moradi & Samwald (2021), Wang et al. (2022), Khan et al. (2025), dan NL-Augmenter (Dhole et al., 2023).
- **Prioritas 3 — cukup untuk desain metode:** Mu et al. (2024), Klie et al. (2024), dan Peyrard et al. (2021), dengan catatan bahwa referensi paired evaluation belum tentu mendukung bootstrap F1 secara spesifik.
- **Tambahan terarah yang masih dibutuhkan:** statistik/laporan resmi Indonesia; sumber yang membedakan promosi dari sekadar konten terkait judi; studi robustness pada teks sosial Indonesia atau teks promosi yang menguji sampel sebelum/sesudah transformasi; dan sumber statistik evaluasi berpasangan/interval kepercayaan F1.

---

# BAGIAN B. AUDIT PER PUBLIKASI

## 1. Oh (2021) — *A YouTube Spam Comments Detection Scheme Using Cascaded Ensemble Machine Learning Model*

**Identitas:** Hayoung Oh. *IEEE Access*, 9 (2021), 144121–144128. DOI: https://doi.org/10.1109/ACCESS.2021.3121508. Artikel jurnal peer-reviewed.

**Tujuan dan cakupan.** Mengembangkan skema deteksi spam komentar YouTube memakai *cascaded ensemble machine learning* (ESM-S) serta membandingkan model individual dan ensemble. Fokusnya spam YouTube generik, bukan khusus judi online dan bukan evaluasi obfuscation.

**Data dan metode.** Penulis menguji komentar dari video musik populer yang berkaitan dengan Psy, Katy Perry, LMFAO, Eminem, dan Shakira. Sebagian data campuran bahasa disaring untuk eksperimen berbahasa Inggris. Artikel juga mendeskripsikan dataset komentar dalam skala besar yang mencakup 6.431.471 komentar dari video populer, dengan 481.334 komentar berlabel spam pada salah satu analisis. Model pembanding mencakup Decision Tree, Logistic Regression, Bernoulli Naive Bayes, Random Forest, SVM linear dan RBF, hard voting, soft voting, serta skema ESM-S. Metrik yang dibahas antara lain accuracy, F1, MCC, spam-caught, ham-blocked, dan ROC/AUC.

**Temuan yang dilaporkan.** ESM-S dilaporkan unggul pada accuracy, F1, dan MCC di beberapa eksperimen; ANN lebih baik pada metrik spam-caught dalam eksperimen tertentu, sedangkan Naive Bayes tertentu lebih baik untuk ham-blocked. Penulis juga melaporkan dataset dengan 1.000 spam dan 1.000 ham memberikan performa lebih baik daripada konfigurasi 5.000 dan 5.000 dalam skenario yang mereka uji.

**Kekuatan.** Sumber jurnal mapan; menyajikan beberapa model pembanding serta beragam metrik, bukan hanya akurasi.

**Keterbatasan untuk penelitian Anda.** Domain spam umum dan sebagian data berasal dari konteks lama serta video musik. Definisi spam mencakup bentuk yang tidak sama dengan “promosi judi online”. Tidak ada protokol pasangan teks normal-versus-obfuscated. Hasilnya tidak boleh digunakan untuk menyimpulkan ketahanan model Anda.

**Keputusan penggunaan:** **Pendukung sekunder.** Dapat disebut satu kalimat untuk menunjukkan bahwa klasifikasi komentar spam YouTube telah lama dikaji dengan ML. Tidak perlu menjadi pilar research gap Bab I.

**Bukti yang dapat diekstrak:** Oh membandingkan beberapa pengklasifikasi dan ensemble untuk spam/ham komentar YouTube serta melaporkan kinerja melalui lebih dari satu metrik. Lokator: bagian metode dan eksperimen, terutama bagian IV–V dan kesimpulan.

---

## 2. Situmorang et al. (2025) — *An Intelligent System for Detecting Online Gambling Promotion on Social Media Based on BERT and Adaptive Browser Extension*

**Identitas:** Gilbert Fernando Situmorang, Juliana Damayanti Manurung, Rivaldi Lubis, Nadya Sikana, dan Kenneth Lionggo. *Jurnal Nasional Pendidikan Teknik Informatika (JANAPATI)*, 14(3) (2025), 679–691. DOI: https://doi.org/10.23887/janapati.v14i3.103511.

**Tujuan dan cakupan.** Mengembangkan sistem deteksi promosi judi online yang memanfaatkan IndoBERT dengan *Domain-Adaptive Pre-Training* (DAPT), lalu mengintegrasikannya pada ekstensi browser. Studi menggabungkan evaluasi model dengan implementasi sistem.

**Data dan label.** Korpus utama bersumber dari X/Twitter, dengan pengumpulan awal sekitar 19.974 posting dan sampel stratifikasi 1.500 contoh: promosi judi, anti-judi, dan netral. Dua anotator independen dilaporkan memperoleh Cohen’s kappa 0,9001. Setelah pembersihan, jumlah akhir dilaporkan sekitar 1.401 contoh; terdapat ketidakkonsistenan angka 1.401/1.402 di bagian yang berbeda, sehingga angka final harus diambil dari tabel yang dijadikan otoritatif. Distribusi label final dilaporkan sebagai 431 promosi, 423 anti-promosi, dan 547 netral. Korpus tambahan tanpa label digunakan untuk DAPT.

**Metode.** IndoBERT + DAPT dibandingkan dengan IndoBERT fine-tuned tanpa DAPT, mBERT, BiLSTM, dan TF-IDF + SVM. Teks dinormalisasi dan dibersihkan; penelitian menekankan istilah domain serta promosi implisit. Model kemudian diintegrasikan pada ekstensi browser dan diuji fungsional pada konten sintetis di YouTube/X.

**Temuan yang dilaporkan.** IndoBERT + DAPT memperoleh F1 sekitar 0,9858 dan mengungguli baseline yang dilaporkan. IndoBERT tanpa DAPT dilaporkan sekitar 0,9786; mBERT sekitar 0,9750; SVM TF-IDF sekitar 0,9579; BiLSTM sekitar 0,9233.

**Kekuatan.** Sangat relevan untuk mendefinisikan promosi eksplisit dan implisit, menunjukkan penggunaan anotasi ganda/IAA, serta menjelaskan konteks pemakaian sistem deteksi promosi. Menyediakan perbandingan model dan konteks deployment.

**Keterbatasan untuk penelitian Anda.** Data berlabel utamanya dari X, bukan YouTube. Klasifikasi tiga kelas tidak identik dengan tugas biner Promotion/Non-Promotion Anda. Normalisasi dan DAPT adalah bagian dari pendekatan sistem; eksperimen bukan protokol utama model yang dilatih pada teks normal kemudian diuji pada pasangan teks obfuscated tanpa pertahanan khusus. Istilah “robust” pada naskah harus dibaca sesuai eksperimen yang benar-benar dilakukan, bukan otomatis dianggap pengukuran adversarial robustness.

**Keputusan penggunaan:** **Referensi inti domain, tetapi bukan bukti utama paired robustness.** Cocok untuk latar belakang promosi, definisi domain, tantangan ujaran implisit, dan praktik anotasi; beda platform dan kelas harus disebutkan.

**Bukti yang dapat diekstrak:** Penelitian memakai tiga kelas promosi/anti-promosi/netral, mengevaluasi IndoBERT dengan DAPT terhadap beberapa baseline, serta menguji ekstensi browser. Lokator: bagian II Method, Results, dan Conclusion.

---

## 3. Pariamalinya, Limbong, & Naibaho (2026) — *Classification of Online Gambling Spam Comments on YouTube Using Support Vector Machine*

**Identitas:** Umbu Anaagung Pariamalinya, Josua Josen A. Limbong, dan Julius Panda Putra Naibaho. *Indonesian Journal of Artificial Intelligence and Data Mining*, 9(1) (2026), 153–163. DOI: https://doi.org/10.24014/ijaidm.v9i1.39193.

**Tujuan dan data.** Menguji SVM untuk deteksi komentar spam judi online di YouTube. Artikel melaporkan 9.169 komentar yang diperoleh melalui YouTube Data API v3, setelah deduplikasi menjadi 7.793 komentar. Komentar berasal dari kanal bertopik gaming, pendidikan, dan hiburan. Kelas akhir dilaporkan 3.706 spam dan 4.087 non-spam.

**Metode.** Pembagian train/test 80:20, sekitar 6.234 data latih dan 1.559 data uji. Pipeline mencakup case folding, pembersihan URL/mention/emoji/simbol, normalisasi, stemming, tokenisasi, stopword removal, TF-IDF word unigram/bigram, dan SVM. Label dikonstruksi menggunakan daftar kata kunci/lexicon dan pemeriksaan manusia pada kasus tertentu; tingkat anotasi independen dua anotator dan statistik agreement tidak dilaporkan sekuat studi Situmorang/Perdana.

**Temuan yang dilaporkan.** Akurasi 99,62% dan F1 sekitar 0,996. Matriks konfusi yang dilaporkan menunjukkan sebagian besar komentar benar terklasifikasi pada test set kecil tersebut.

**Kekuatan.** Langsung relevan pada komentar YouTube Indonesia dan menggunakan SVM; berguna untuk menunjukkan bahwa deteksi spam judi dengan model klasik sudah diteliti.

**Keterbatasan dan perhatian kualitas.** Target “spam/non-spam” tidak otomatis sama dengan niat “promosi/non-promosi”. Normalisasi dan pembersihan agresif dapat mengubah atau menghapus fitur permukaan yang justru hendak diuji dalam penelitian robustness. Tidak ada evaluasi pasangan clean-obfuscated pada empat keluarga transformasi. Dalam PDF, tanggal “Revised Feb 31th, 2026” tidak valid secara kalender; ini red flag bibliografis/editorial yang harus dicatat, tetapi tidak cukup sendirian untuk membatalkan keseluruhan artikel. Penjelasan label dan validasi lintas sumber perlu diperiksa lebih teliti sebelum angka performa dipakai sebagai pembanding setara.

**Keputusan penggunaan:** **Sumber domain langsung dengan kehati-hatian metodologis.** Gunakan untuk mengonfirmasi keberadaan pendekatan SVM pada komentar spam judi YouTube; jangan gunakan sebagai bukti bahwa model SVM tahan terhadap obfuscation atau sebagai pembanding langsung F1 ke penelitian Anda.

**Bukti yang dapat diekstrak:** Data dikumpulkan dengan API YouTube, dideduplikasi, diproses dengan TF-IDF, dan diklasifikasikan memakai SVM. Lokator: bagian 2–3 (metode, pengumpulan data, preprocessing, evaluasi).

---

## 4. Nugraha et al. (2026) — *Comparative Analysis of IndoBERT and mBERT for Online Gambling Comment Detection in Indonesian Social Media*

**Identitas:** Satria Adi Nugraha, Citra Lestari, Karyna Budi Sanjaya, Rafi Abhista Naya, dan Jocelyn Jolie. *Jurnal Teknik Informatika (JUTIF)*, 7(2) (2026), 1931–1943. DOI: https://doi.org/10.52436/1.jutif.2026.7.2.5677.

**Tujuan dan data.** Membandingkan IndoBERT dan mBERT untuk klasifikasi komentar terkait judi pada YouTube dan Twitter/X. Naskah melaporkan sekitar 31.230 data berlabel dari dua platform. Label yang dipakai adalah gambling/non-gambling atau judi/non-judi; bukan secara eksplisit promosi/non-promosi.

**Metode.** Preprocessing, normalisasi dan tokenisasi subword; pembagian sekitar 80/10/10 untuk train/validation/test. Sepuluh persen data diperiksa oleh dua anotator, dengan Cohen’s kappa sekitar 0,85. Model dibandingkan dengan LSTM dan SVM TF-IDF. Uji McNemar dilaporkan untuk perbandingan tertentu antara model Transformer.

**Temuan yang dilaporkan.** IndoBERT memperoleh akurasi/F1 sekitar 0,98, mBERT sekitar 0,96, LSTM sekitar 0,91, dan SVM sekitar 0,88. Perbedaan IndoBERT dan mBERT dilaporkan signifikan dengan p sekitar 0,023. Artikel mengidentifikasi kesalahan terkait ujaran informal, konteks implisit, dan komentar yang memiliki bentuk penulisan tidak lazim.

**Kekuatan.** Sangat relevan untuk konteks Indonesia dan sebagai pembanding IndoBERT, mBERT, LSTM, serta SVM. Menyertakan statistik agreement dan uji perbedaan model.

**Keterbatasan serta red flags.** Tidak ada protokol utama yang memetakan performa model yang sama pada sampel bersih dan pasangan tersamarkan yang dihasilkan terkontrol; pembahasan noise/obfuscation tidak boleh diperlakukan sebagai hasil uji robustness jika metode tidak benar-benar melakukannya. Data berasal dari dua platform dan target kelas lebih luas daripada promosi. Lebih serius, daftar pustaka memiliki ketidaksesuaian yang jelas: beberapa sitasi di bagian pendahuluan digunakan untuk mendukung klaim deteksi judi/LLM, tetapi entri bibliografinya membahas topik tidak terkait (misalnya augmentasi jadwal kereta dan permintaan impor agregat). Klaim yang didukung entri seperti itu tidak boleh diambil sebagai landasan sebelum dilacak ke sumber yang benar.

**Keputusan penggunaan:** **Referensi inti pembanding model, dengan audit kualitas sitasi.** Gunakan hasil perbandingan model hanya dengan menyebut perbedaan label dan dataset; jangan mengandalkan klaim-klaim pendahuluan yang memiliki rujukan salah.

**Bukti yang dapat diekstrak:** Perbandingan model berbasis bahasa Indonesia dan multilingual pada komentar media sosial, termasuk statistik agreement dan uji beda. Lokator: Method, Result, Discussion, dan daftar pustaka.

---

## 5. Angelo, Robet, & Hendrik (2025) — *Comparative Performance of Machine Learning Algorithms for Detecting Online Gambling Promotional Comments on YouTube*

**Identitas:** Michael Angelo, Robet, dan Jackri Hendrik. *Jurnal Teknologi dan Manajemen Informatika*, 11(2) (2025), 132–142. DOI: https://doi.org/10.26905/jtmi.v11i2.16286.

**Tujuan.** Membandingkan beberapa algoritma machine learning dalam mendeteksi komentar promosi judi online YouTube sambil menangani variasi teks seperti Unicode, emoji, spasi tidak teratur, dan pengacakan karakter.

**Data dan pipeline.** Dataset yang dilabeli manual berjumlah 1.648 komentar; pseudo-labeling memperbesar korpus menjadi 9.111 komentar dengan hanya menerima prediksi berkeyakinan tinggi. Test set sekitar 1.823 komentar. Pipeline mencakup normalisasi karakter khusus, cleaning, tokenisasi, stopword removal, stemming Nazief–Adriani, TF-IDF, algoritma MNB/LR/RF/SVM, serta penggunaan SMOTE dan optimasi parameter. Normalisasi karakter dibuat untuk mengubah karakter/susunan yang disamarkan menjadi bentuk yang lebih kanonik.

**Temuan yang dilaporkan.** Model mencapai kinerja tinggi pada data setelah pipeline preprocessing; SVM dilaporkan mendapat F1 kelas promosi sekitar 0,9908. Penulis juga membandingkan versi baseline tanpa pseudo-labeling/SMOTE dan versi yang dioptimasi. Hasil menunjukkan bahwa gabungan langkah pipeline dan pseudo-labeling berkaitan dengan peningkatan F1 dibanding baseline manual saja. Naskah membahas bahwa obfuscation adalah strategi yang digunakan pelaku, dan menyebut robustness adversarial sebagai kebutuhan penelitian lanjutan.

**Kekuatan.** Ini merupakan salah satu paper yang paling dekat dengan penelitian Anda: platform, bahasa, dan maksud label berupa promosi judi YouTube. Normalisasi karakternya memberikan bukti langsung bahwa masalah variasi karakter sudah dipertimbangkan dalam domain ini.

**Keterbatasan dan beda desain.** Normalisasi diterapkan sebelum ekstraksi fitur/model. Karena itu, hasil yang dilaporkan lebih tepat dibaca sebagai performa sebuah pipeline deteksi yang menggunakan normalisasi, bukan sebagai pengukuran ketahanan intrinsik model pada teks mentah yang berubah. Naskah tidak menyajikan protokol inti paired clean-versus-obfuscated dengan model yang tetap beku pada delapan kondisi perturbasi, seperti rancangan penelitian Anda. Pseudo-labeling berpotensi memperkenalkan noise; skor tinggi saja tidak menunjukkan bahwa risiko tersebut telah hilang. Perlu periksa pemisahan data, duplikasi/template, dan penempatan SMOTE hanya pada data latih sebelum membuat evaluasi kualitas yang lebih jauh.

**Keputusan penggunaan:** **Referensi terpenting untuk membangun research gap, tetapi juga ancaman paling dekat terhadap klaim novelty.** Tidak boleh menyatakan belum ada studi yang menangani obfuscation pada komentar promosi YouTube. Gap harus diarahkan pada protokol pengukuran, pasangan input, model pembanding, dan kondisi penyamaran yang diverifikasi secara eksplisit.

**Bukti yang dapat diekstrak:** Pipeline normalisasi karakter dan TF-IDF untuk promosi judi YouTube; pengembangan label melalui pseudo-labeling; hasil kinerja beberapa classifier. Lokator: Dataset Collection, Dataset Preprocessing, Results, Analysis and Interpretation, serta Conclusion.

---

## 6. Perdana et al. (2024) — *Detecting Online Gambling Promotions on Indonesian Twitter Using Text Mining Algorithm*

**Identitas:** Reza Bayu Perdana, Ardin, Indra Budi, Aris Budi Santoso, Amanah Ramadiah, dan Prabu Kresna Putra. *International Journal of Advanced Computer Science and Applications*, 15(8) (2024), 942–949. DOI: https://doi.org/10.14569/IJACSA.2024.0150893.

**Tujuan dan data.** Mengidentifikasi ciri teks promosi judi online di Twitter/X Indonesia dan membandingkan metode klasifikasi. Dataset terdiri atas sekitar 6.038 tweet/post; pelabelan dilakukan dengan dua anotator dan Cohen’s kappa yang dilaporkan sekitar 0,9659.

**Metode.** Algoritma yang dibandingkan mencakup Random Forest, Logistic Regression, dan CNN dengan beberapa representasi: TF-IDF, Word2Vec, dan GloVe. Preprocessing meliputi pembersihan manual, stemming, serta metode back-translation melalui bahasa Inggris dan kembali ke bahasa Indonesia untuk menstandarkan variasi kata. Penulis mengamati istilah seperti “link”, “situs”, “prediksi”, “jackpot”, “maxwin”, dan “togel”.

**Temuan yang dilaporkan.** TF-IDF + Random Forest menjadi konfigurasi terbaik secara keseluruhan dengan precision sekitar 0,966, recall 0,958, F1 sekitar 0,962, dan accuracy sekitar 0,979. GloVe + CNN juga menunjukkan recall/precision tinggi, tetapi lebih lambat. Uji hipotesis tertentu menemukan perbedaan recall TF-IDF+RF dan Word2Vec+CNN tidak signifikan (p=0,130), sedangkan perbedaan F1 signifikan (p=0,047).

**Kekuatan.** Sangat baik untuk memberi konteks ciri-ciri bahasa promosi dan mendemonstrasikan bahwa target promosi dapat didefinisikan secara semantik, bukan sekadar spam umum. Agreement pelabelan dilaporkan tinggi.

**Keterbatasan.** Platformnya Twitter, bukan YouTube. Back-translation dapat menstandarkan kata tetapi juga berpotensi mengubah nuansa makna; hal ini bukan evaluasi robustness dengan mempertahankan teks asli yang diuji secara berpasangan. Tidak ada pengukuran penurunan F1 di bawah obfuscation terkontrol.

**Keputusan penggunaan:** **Referensi inti untuk karakteristik promosi dan label**, tetapi perlu dinyatakan bahwa domain/platform berbeda. Jangan bandingkan skor mentahnya langsung dengan skor penelitian Anda.

**Bukti yang dapat diekstrak:** Definisi target promosi, istilah leksikal yang umum, perbandingan fitur klasifikasi, serta agreement anotasi. Lokator: Introduction, Dataset/Preprocessing, Table VI–VII, dan Conclusion.

---

## 7. Ariyanto et al. (2026) — *Fine-Tuning IndoBERT for Detecting Online Gambling Promotion in Indonesian-Language Social Media Comments*

**Identitas:** Yuri Ariyanto, Deddy Kusbianto Purwoko Aji, Chandrasena Setiadi, Yan Watequlis Syaifudin, dan Anggrean Renozonarca. *International Journal of Engineering and Computer Science Applications (IJECSA)*, 5(2) (2026), 107–116. DOI: https://doi.org/10.30812/ijecsa.v5i2.6664.

**Tujuan dan data.** Melatih IndoBERT untuk mengklasifikasikan komentar YouTube Indonesia yang terkait judi dan komentar non-judi. Dataset 10.230 komentar dari repositori publik Kaggle, dengan split stratified 70% train, 15% validation, dan 15% test.

**Metode.** Preprocessing dirancang untuk mengubah kembali istilah yang disamarkan seperti bentuk angka-huruf (contoh dalam artikel: “sl0t”, “c4sino”, “m4xwin”) menjadi bentuk normal, kemudian teks ditokenisasi dan IndoBERT fine-tuned hingga tiga epoch dengan early stopping. Panjang maksimum token dilaporkan 128.

**Temuan yang dilaporkan.** Accuracy 0,9844; precision kelas gambling 0,9856; recall 0,9763; F1 kelas gambling 0,9809; Macro-F1 0,9838.

**Kekuatan.** Sangat dekat dengan domain YouTube Indonesia dan menyebut secara eksplisit normalisasi istilah yang disamarkan. Memberi informasi tentang pendekatan IndoBERT yang relevan.

**Keterbatasan penting.** Labelnya “gambling/non-gambling”, yang belum tentu identik dengan promosi/non-promosi. Penulis sendiri membatasi kontribusi pada pipeline normalisasi + fine-tuning dan tidak melakukan ablation yang memisahkan efek normalisasi dari efek model. Karena obfuscation dinormalisasi sebelum IndoBERT, evaluasi ini tidak menunjukkan seberapa besar degradasi model ketika menerima raw-obfuscated text tanpa pertahanan preprocessing. Klaim “model menangani obfuscation” perlu ditafsirkan dalam konteks pipeline yang digunakan.

**Keputusan penggunaan:** **Referensi domain inti dan salah satu pembanding terdekat.** Wajib dibandingkan dengan desain eksperimen Anda, khususnya karena sama-sama menggunakan IndoBERT dan istilah tersamarkan.

**Bukti yang dapat diekstrak:** Fine-tuning IndoBERT pada komentar YouTube; normalisasi istilah judi tersamarkan sebelum tokenisasi; skor pada held-out test set; pengakuan belum adanya ablation isolasi efek normalisasi. Lokator: Abstract, Method, Results, Limitations/Future Work.

---

## 8. Widiyanto, Prameswari, & Latief (2025) — *Gambling Comments Detection on YouTube: A Comparative Study of Tree-Based Boosting, LSTM and GRU Models*

**Identitas:** Agung Widiyanto, Mayesq Prameswari, dan Muhammad Abdul Latief. *JUTI: Jurnal Ilmiah Teknologi Informasi*, 23(2) (2025), 144–160. DOI: https://doi.org/10.12962/j24068535.v23i2.a1305.

**Tujuan dan data.** Membandingkan LightGBM, XGBoost, CatBoost, LSTM, dan GRU untuk mendeteksi komentar judi di YouTube. Penulis mengambil 11.673 komentar dari video dengan topik beragam dan memberi label secara manual. Kelas judi sekitar 10%, sehingga dataset sangat tidak seimbang.

**Metode.** Model boosting menggunakan TF-IDF; LSTM dan GRU menggunakan embedding Word2Vec. Data dibagi ke train, test, dan holdout; holdout dipakai untuk menilai performa di luar data yang dipakai untuk pelatihan/pengujian awal.

**Temuan yang dilaporkan.** LightGBM dilaporkan memiliki holdout F1 tertinggi 0,8737. GRU menunjukkan skor test yang tinggi (misalnya precision 0,9849 dan recall 0,9378), tetapi recall pada holdout turun menjadi sekitar 0,5022 dan F1 sekitar 0,6647. LSTM juga menunjukkan kinerja holdout lebih rendah dibanding test. Artikel menafsirkan pola ini sebagai masalah generalisasi/overfitting akibat data yang terbatas/berimbalance.

**Kekuatan.** Mendukung argumen bahwa skor pada satu test set tidak selalu menggambarkan generalisasi pada data berbeda. Berguna untuk membedakan isu generalisasi dari robustness.

**Keterbatasan.** Tidak menguji keluarga penyamaran teks dengan paired clean-obfuscated test. Target “gambling comments” lebih luas daripada “promosi”. Ada ketidakselarasan aritmetis pada beberapa ringkasan metrik di abstrak: precision 0,8912 dan recall 0,8886 tidak menghasilkan F1 0,8737 dengan rumus F1 standar pada kelas dan subset yang sama. Kemungkinan angka berasal dari ringkasan yang berbeda atau ada kesalahan pelaporan; verifikasi tabel hasil sebelum mengutip trio angka itu bersamaan.

**Keputusan penggunaan:** **Pendukung untuk isu generalisasi dan imbalance**, bukan bukti utama untuk obfuscation. Perbedaan generalisasi terhadap data holdout tidak boleh disebut robustness terhadap perubahan teks.

**Bukti yang dapat diekstrak:** Performa test dan holdout yang berbeda bagi LSTM/GRU; perbandingan model pada data imbalance; ruang lingkup label gambling-related. Lokator: Abstract, experimental setup, results, discussion, conclusion.

---

## 9. Yang et al. (2023) — *Generation-based Parallel Particle Swarm Optimization for Adversarial Text Attacks*

**Identitas:** Xinghao Yang, Yupeng Qi, Honglong Chen, Baodi Liu, dan Weifeng Liu. *Information Sciences*, 644 (2023), artikel 119237. DOI: https://doi.org/10.1016/j.ins.2023.119237.

**Tujuan dan metode.** Mengembangkan GP²SO untuk menghasilkan serangan adversarial teks dengan menggabungkan generasi kandidat pengganti dan Particle Swarm Optimization paralel. Artikel menargetkan kompromi antara attack success rate dan efisiensi serangan. Eksperimen memakai beberapa dataset tugas NLP umum (antara lain sentiment analysis, natural language inference, dan question answering) serta sejumlah model bahasa.

**Temuan yang dilaporkan.** Metode diukur menggunakan metrik serangan seperti attack success rate, proporsi kata yang diubah, dan waktu serangan. Hasil menunjukkan strategi yang diusulkan meningkatkan kombinasi efektivitas dan efisiensi dibanding baseline serangan yang diuji.

**Kekuatan.** Menjelaskan bahwa serangan adversarial teks merupakan satu jenis cara menguji kerentanan NLP dan bahwa evaluasi dapat melibatkan keberhasilan serangan serta besaran perturbasi, bukan hanya skor klasifikasi.

**Keterbatasan.** Ini terutama artikel pengembangan metode serangan pada tingkat kata, bukan evaluasi karakter/Unicode untuk komentar promosi judi Indonesia. Tidak mendukung secara langsung definisi keluarga O1–O4 Anda dan tidak membuktikan bahwa setiap transformasi di repo Anda setara dengan serangan optimasi semacam itu.

**Keputusan penggunaan:** **Pendukung konseptual, opsional untuk Bab I.** Lebih tepat masuk Bab II jika istilah adversarial attack dibahas. Jangan menjadikan artikel ini sebagai dasar tunggal bagi prosedur penyamaran terkontrol Anda.

**Bukti yang dapat diekstrak:** Perbedaan antara efektivitas serangan dan efisiensi, serta kebutuhan mengukur besaran modifikasi. Lokator: Methodology, dataset/victim models, Results, Conclusion.

---

## 10. Xiao & Liang (2024) — *Spam Detection for YouTube Video Comments Using Machine Learning Approaches*

**Identitas:** Andrew S. Xiao dan Qilian Liang. *Machine Learning with Applications*, 16 (2024), 100550. DOI: https://doi.org/10.1016/j.mlwa.2024.100550.

**Tujuan dan data.** Membandingkan delapan model untuk klasifikasi komentar YouTube menjadi spam/ham. Artikel menggunakan dataset komentar YouTube publik dari Kaggle dan membahas lima kumpulan terkait video (Psy, Katy Perry, LMFAO, Eminem, dan Shakira) atau pembagian per-video, dengan hasil ROC dan metrik per kumpulan. Appendix menyediakan tautan dataset dan notebook kode.

**Metode.** Gaussian Naive Bayes, Logistic Regression, KNN, MLP, SVM/SVC, Random Forest, Decision Tree, dan Voting Classifier. Fitur menggunakan TF-IDF, lalu model dibangun dan beberapa hyperparameter dituning. Evaluasi memakai accuracy, precision, recall, F1, dan AUC-ROC.

**Temuan yang dilaporkan.** Random Forest disebut mencapai precision rata-rata 100% dan AUC-ROC 0,9841 pada ringkasan abstrak; hasil per-video menunjukkan perbedaan performa antarmodel dan tidak semua model mencapai hasil serupa di setiap kumpulan. SVC, Random Forest, dan Voting Classifier termasuk model dengan F1 tinggi pada sejumlah hasil.

**Kekuatan.** Publikasi jurnal dengan kode/data yang ditautkan, sehingga dapat menjadi referensi untuk baseline dan metrik klasifikasi spam YouTube.

**Keterbatasan.** Spam/ham tidak sama dengan promosi judi. Dataset bukan komentar Indonesia yang dilabeli berdasarkan niat promosi. Artikel tidak menguji perturbasi mentah berpasangan dan tidak memberi bukti robustness terhadap bentuk penyamaran O1–O4.

**Keputusan penggunaan:** **Pendukung sekunder.** Boleh disebut dalam konteks pendekatan spam YouTube, tetapi tidak usah digunakan untuk klaim utama tentang deteksi judi atau research gap robustness.

**Bukti yang dapat diekstrak:** Perbandingan model spam/ham pada komentar YouTube dan penerapan beberapa metrik. Lokator: Experimental Results, Table 1–5, Appendix.

---

## 11. Wang, Wang, & Yang (2022) — *Measure and Improve Robustness in NLP Models: A Survey*

**Identitas:** Xuezhi Wang, Haohan Wang, dan Diyi Yang. Dalam *Proceedings of NAACL-HLT 2022*, hlm. 4569–4586. DOI: https://doi.org/10.18653/v1/2022.naacl-main.339. Teks resmi: https://aclanthology.org/2022.naacl-main.339/.

**Tujuan dan cakupan.** Survei yang berupaya menyatukan berbagai definisi robustness dalam NLP, metode pengukuran kegagalan, cara mengevaluasi robustness, dan strategi mitigasi.

**Isi utama.** Penulis membedakan berbagai definisi robustness yang terkait distribusi atau situasi pengujian yang berbeda, mengelompokkan metode untuk mengidentifikasi kegagalan, dan membahas mitigasi data-driven, model-driven, serta berbasis inductive prior. Paper menggarisbawahi bahwa skor benchmark standar tidak selalu mencerminkan perilaku model pada kondisi baru atau menantang.

**Kekuatan.** Sumber konseptual utama untuk mendefinisikan robustness dan membedakannya dari performa benchmark normal. Cakupannya luas dan bersifat sintesis.

**Keterbatasan untuk penelitian Anda.** Karena berbentuk survei, ia bukan bukti empiris langsung bahwa tiga model Anda akan gagal di bawah perturbasi tertentu. Kerangka di dalamnya perlu dipilih dan dioperasionalkan sesuai tugas komentar YouTube. Tidak perlu memindahkan seluruh taksonomi survei ke Bab I.

**Keputusan penggunaan:** **Referensi inti Bab II dan pendukung kuat paragraf keempat Bab I.** Gunakan untuk definisi dan posisi masalah robustness, bukan untuk klaim detektor judi online.

**Bukti yang dapat diekstrak:** Robustness mempunyai sejumlah definisi dan praktik evaluasi; benchmark normal saja tidak cukup untuk mewakili semua skenario deployment; evaluasi dan mitigasi adalah dua tujuan yang berbeda. Lokator: bagian awal survei, taksonomi evaluasi, mitigasi, dan open challenges.

---

## 12. Moradi & Samwald (2021) — *Evaluating the Robustness of Neural Language Models to Input Perturbations*

**Identitas:** Milad Moradi dan Matthias Samwald. Dalam *Proceedings of EMNLP 2021*, hlm. 1558–1570. DOI: https://doi.org/10.18653/v1/2021.emnlp-main.117. Teks resmi: https://aclanthology.org/2021.emnlp-main.117/.

**Tujuan.** Mengukur sensitivitas model bahasa terhadap modifikasi masukan yang meniru variasi/noise di dunia nyata, menggunakan perturbasi tingkat karakter dan kata serta sejumlah tugas NLP.

**Metode.** Paper mengembangkan berbagai manipulasi seperti penghapusan/penyisipan karakter, kesalahan pengetikan, penghapusan atau penggantian kata, dan variasi pada level kata lain. Model termasuk BERT, RoBERTa, XLNet, dan ELMo; tugas mencakup text classification, sentiment analysis, named entity recognition, semantic similarity, dan question answering. Untuk beberapa jenis transformasi yang dapat mengubah makna/label, paper melakukan penyesuaian atau penyaringan, tetapi tidak semua sampel transformasi otomatis melewati validasi manual yang identik.

**Temuan.** Kinerja turun pada banyak kondisi perturbasi walaupun perubahan pada teks relatif kecil; dampaknya bergantung pada tipe perturbasi, tingkatnya, model, dan tugas. Paper melaporkan bahwa sebagian besar sampel perturbasi tetap dinilai dapat dipahami dan maknanya terjaga dalam evaluasi manusia pada subset yang mereka audit. Penulis menyimpulkan bahwa evaluasi input perturbation sebaiknya melengkapi benchmark standar.

**Kekuatan.** Salah satu rujukan paling langsung untuk rancangan clean-versus-perturbed evaluation dan preservasi makna/label. Membantu menjelaskan kenapa kinerja model harus diuji pada masukan yang berubah secara terkontrol.

**Keterbatasan.** Tidak fokus pada komentar promosi judi Indonesia, IndoBERT, atau keseluruhan variasi Unicode yang digunakan dalam repositori Anda. Rincian perturbasi dan validasi label dari paper harus dibaca per tipe; jangan menyamaratakan semua transformasi sebagai semantik-preserving secara otomatis.

**Keputusan penggunaan:** **Referensi inti Bab I dan II.** Menjadi landasan umum untuk desain input perturbation, tetapi protokol spesifik O1–O4 tetap harus didukung dokumentasi eksperimen Anda dan literatur terkait teks sosial.

**Bukti yang dapat diekstrak:** Model NLP berperforma tinggi tetap dapat sensitif terhadap perturbasi; uji input yang dimodifikasi mengungkap aspek yang tidak terlihat pada benchmark asli; evaluasi perlu mempertimbangkan makna dan label. Lokator: Introduction, perturbation definitions, experiments/results, human validation, conclusion.

---

## 13. Dhole et al. (2023) — *NL-Augmenter: A Framework for Task-Sensitive Natural Language Augmentation*

**Identitas:** Kaustubh Dhole et al. *Northern European Journal of Language Technology*, 9 (2023). DOI: https://doi.org/10.3384/nejlt.2000-1533.2023.4725. Halaman resmi: https://aclanthology.org/2023.nejlt-1.5/.

**Tujuan.** Mengembangkan framework untuk augmentasi teks dengan banyak transformasi dan filter yang memeriksa apakah transformasi masih cocok untuk tugas tertentu. Katalog framework mencakup 117 transformasi dan 23 filter pada versi yang dilaporkan.

**Isi/metode.** Paper menjelaskan *transformation functions* dan *filters*, kebutuhan task sensitivity, serta penggunaan augmentasi untuk membangun dataset dan menguji model pada variasi input. Transformasi dapat mengubah karakter, kata, gaya, atau struktur; tidak semua transformasi menjamin semantik/label tetap terjaga untuk setiap task tanpa filter.

**Kekuatan.** Mendukung perlunya mendesain transformasi yang terkontrol dan mengecek validitasnya, alih-alih hanya membuat noise secara acak. Menunjukkan bahwa “perturbation” dan “augmentation” perlu ditentukan berdasarkan task dan semantik.

**Keterbatasan.** Framework bersifat luas dan bukan khusus obfuscation judi online. Jumlah operasi transformasi dalam paper tidak berarti semua operasi tersebut sesuai untuk komentar promosi atau harus dipakai dalam penelitian Anda. Transformasi dalam eksperimen Anda perlu punya aturan eksplisit serta audit perubahan.

**Keputusan penggunaan:** **Referensi metodologi inti untuk Bab II/III**, bukan inti urgensi Bab I. Gunakan untuk mendukung prinsip task-sensitive transformations, filter, dan validasi.

**Bukti yang dapat diekstrak:** Transformasi natural language perlu dilihat bersama filter dan tujuan tugas; variasi input dapat digunakan untuk menguji performa model; preservasi label adalah syarat yang harus diperiksa sesuai task. Lokator: framework overview, transformations/filters, evaluations, limitations.

---

## 14. Khan et al. (2025) — *Textual Variations in Social Media Text Processing Applications: Challenges, Solutions, and Trends*

**Identitas:** Jebran Khan, Kashif Ahmad, Senthil Kumar Jagatheesaperumal, dan Kyung-Ah Sohn. *Artificial Intelligence Review*, 58, artikel 89 (2025). DOI: https://doi.org/10.1007/s10462-024-11071-z.

**Tujuan.** Meninjau sumber variasi teks di media sosial, penyebab OOV, metode preprocessing/normalisasi, serta konsekuensi dan tantangan penanganan variasi.

**Cakupan.** Paper membedakan variasi disengaja dan tidak disengaja. Jenis yang dibahas antara lain typo, elongation, bentuk fonologis, penghilangan huruf, singkatan, kontraksi, pergeseran batas kata, substitution berdasarkan bunyi/visual, code-mixing, serta variasi morfologi. Paper juga membahas metode normalisasi tradisional dan aplikasi spesifik serta trade-off-nya.

**Temuan/sintesis utama.** Variasi teks dapat memunculkan OOV dan menurunkan efektivitas metode pemrosesan. Namun, normalisasi bukan solusi netral: dapat menghilangkan informasi yang relevan pada aplikasi tertentu, dan cara penanganan harus memperhatikan tujuan tugas, bahasa, jenis variasi, dan konteks data.

**Kekuatan.** Sangat membantu membangun kosa kata konseptual dan membedakan jenis variasi yang sering dicampur menjadi satu istilah “obfuscation”. Relevan untuk argumen bahwa preprocessing bisa membantu dalam sistem produksi tetapi juga mengubah kondisi pengukuran robustness.

**Keterbatasan.** Berbentuk survei dan lintas aplikasi; bukan eksperimen khusus promosi judi online atau model Anda. Temuan lintas domain harus diperkenalkan sebagai fondasi umum, bukan sebagai prevalensi obfuscation di YouTube Indonesia.

**Keputusan penggunaan:** **Referensi inti Bab II dan salah satu basis Bab I.** Sangat penting untuk definisi variasi dan trade-off normalisasi.

**Bukti yang dapat diekstrak:** Taksonomi variasi disengaja/tidak disengaja; hubungan variasi dengan OOV; normalisasi memiliki manfaat dan biaya kontekstual. Lokator: Sections 3–5, khususnya sumber variasi dan normalisasi sebagai pertahanan terhadap adversarial attacks.

---

## 15. Mu et al. (2024) — *Enhancing Data Quality through Simple De-duplication: Navigating Responsible Computational Social Science Research*

**Identitas:** Yida Mu, Mali Jin, Xingyi Song, dan Nikolaos Aletras. Dalam *Proceedings of EMNLP 2024*, hlm. 12477–12492. DOI: https://doi.org/10.18653/v1/2024.emnlp-main.694. Teks resmi: https://aclanthology.org/2024.emnlp-main.694/.

**Tujuan dan data.** Menganalisis kualitas 20 dataset media sosial yang umum dipakai dalam NLP/computational social science, dengan fokus pada duplikasi dan near-duplicate serta dampaknya terhadap evaluasi model.

**Metode.** Penulis menghitung tingkat duplikasi, melakukan deduplikasi/near-deduplication, lalu mengevaluasi dampak terhadap pembagian dataset dan skor model pada beberapa tugas. Analisis mencakup bagaimana pengulangan konten berpotensi tersebar lintas split, memunculkan label tidak konsisten dan data leakage.

**Temuan utama.** Duplikasi ditemukan dalam banyak dataset yang diteliti; deduplikasi dapat mengubah jumlah data dan peringkat/hasil model. Duplikat yang tidak ditangani dapat membuat performa tampak lebih tinggi daripada kemampuan model pada data benar-benar baru.

**Kekuatan.** Sumber empiris metodologis yang kuat untuk menjelaskan pentingnya pengendalian duplikasi dan near-duplicate, khususnya pada konten media sosial yang menggunakan template berulang.

**Keterbatasan.** Tidak berkaitan langsung dengan judi online atau obfuscation dan temuan tingkat duplikasi bervariasi antar dataset. Paper mendukung prinsip audit data, bukan angka spesifik yang dapat diterapkan begitu saja ke dataset Anda.

**Keputusan penggunaan:** **Referensi utama Bab III**; di Bab I hanya disebut bila perlu menguatkan alasan kualitas evaluasi, tetapi biasanya tidak perlu banyak detail.

**Bukti yang dapat diekstrak:** Duplicates dan near-duplicates pada dataset sosial dapat menimbulkan leakage serta label tidak konsisten dan memengaruhi klaim SOTA. Lokator: task/dataset overview, Data Leakage, Results, Discussion.

---

## 16. Klie, Eckart de Castilho, & Gurevych (2024) — *Analyzing Dataset Annotation Quality Management in the Wild*

**Identitas:** Jan-Christoph Klie, Richard Eckart de Castilho, dan Iryna Gurevych. *Computational Linguistics*, 50(3) (2024), 817–866. DOI: https://doi.org/10.1162/coli_a_00516.

**Tujuan.** Memeriksa bagaimana peneliti menerapkan praktik quality management saat membuat dataset teks, termasuk pengelolaan anotator, kesepakatan, adjudication, validasi, dan estimasi error.

**Data dan metode.** Penulis menyusun rekomendasi kualitas data dari literatur lalu memberi anotasi terhadap 591 publikasi yang memperkenalkan dataset teks. Mereka memetakan cara-cara quality management yang dilaporkan dan menilai seberapa banyak praktik yang diuraikan secara eksplisit.

**Temuan.** Artikel menunjukkan adanya variasi besar dalam pelaporan/praktik kualitas anotasi. Ia menekankan bahwa reliabilitas dataset memerlukan lebih dari satu angka agreement: pedoman anotasi, pelatihan anotator, adjudication, sampling untuk validasi, error estimation, dan dokumentasi juga relevan. Nilai kappa tidak boleh dianggap jaminan universal kualitas tanpa konteks task dan skema label.

**Kekuatan.** Review besar dan kuat untuk metodologi dataset; relevan dengan tantangan label promosi/non-promosi yang bisa ambigu.

**Keterbatasan.** Tidak memberi definisi langsung tentang apa yang harus dianggap promosi judi. Paper juga tidak menetapkan satu ambang agreement yang universal bagi semua task.

**Keputusan penggunaan:** **Referensi metodologi inti**, utamanya untuk Bab III dan untuk menjustifikasi perlunya aturan pelabelan yang eksplisit. Bukan bukti domain Bab I.

**Bukti yang dapat diekstrak:** Kualitas anotasi mencakup proses, panduan, agreement, adjudication, dan validasi; pelaporan kualitas tidak selalu lengkap dalam publikasi yang disurvei. Lokator: sections 3–6, terutama Quality Estimation, Quality Improvement, Adjudication, Analysis, Recommendations.

---

## 17. Peyrard et al. (2021) — *Better than Average: Paired Evaluation of NLP Systems*

**Identitas:** Maxime Peyrard, Wei Zhao, Steffen Eger, dan Robert West. Dalam *Proceedings of ACL-IJCNLP 2021*, hlm. 2301–2315. DOI: https://doi.org/10.18653/v1/2021.acl-long.179. Teks resmi: https://aclanthology.org/2021.acl-long.179/.

**Tujuan.** Menilai bagaimana kesimpulan perbandingan sistem NLP berubah saat agregasi skor memperhitungkan performa berpasangan pada item evaluasi yang sama, bukan hanya membandingkan rata-rata skor secara independen.

**Metode dan temuan.** Paper menggunakan kerangka Bradley–Terry dan metode agregasi berbasis pasangan serta membandingkannya dengan mean/median dalam simulasi dan data empiris. Penulis melaporkan bahwa metode agregasi dapat menghasilkan kesimpulan ranking yang berbeda dalam sekitar 30% dari setup evaluasi yang mereka telaah.

**Kekuatan.** Menegaskan bahwa fakta bahwa sistem/hasil diperoleh pada instance yang sama memberi informasi yang hilang jika hanya melihat nilai agregat. Konsep itu selaras dengan membandingkan prediksi komentar asli dan komentar pasangannya.

**Keterbatasan yang harus diperjelas.** Paper ini berfokus pada agregasi evaluasi sistem NLP (termasuk konteks skor sistem), bukan secara khusus prosedur pengukuran F1-drop pre/post perturbation dengan paired bootstrap. Karena itu, jangan menjadikan Peyrard et al. sebagai satu-satunya justifikasi untuk rumus F1 retention, bootstrap confidence interval, atau uji statistik F1 yang digunakan dalam repositori. Anda masih perlu sumber spesifik untuk metode inferensial tersebut.

**Keputusan penggunaan:** **Referensi pendukung untuk prinsip paired evaluation**, tetapi perlu satu sumber tambahan untuk statistik perubahan metrik F1.

**Bukti yang dapat diekstrak:** Mengabaikan pairing antarsampel dapat membuang informasi dan mengubah kesimpulan perbandingan. Lokator: introduction, aggregation methods, empirical analyses, discussion/conclusion.

---

## 18. Hidayat, Chamid, & Jazuli (2026) — *Implementasi Model Hybrid IndoBERT–LinearSVC untuk Deteksi Spam Judol Obfuscated pada Komentar YouTube*

**Identitas:** Danang Budiman Hidayat, Ahmad Abdul Chamid, dan Ahmad Jazuli. *Progresif: Jurnal Ilmiah Komputer*, 22(3) (Juli 2026), 820–833. DOI: https://doi.org/10.35889/progresif.v22i3.3914.

**Tujuan.** Membangun model hybrid untuk menangani komentar spam judi online YouTube yang berisi karakter Unicode non-standar dan bentuk obfuscation lain. Model menggabungkan representasi IndoBERT dari teks yang dinormalisasi dengan fitur character n-gram TF-IDF dari teks Unicode mentah yang diklasifikasi LinearSVC.

**Data.** Dari 45.592 baris awal, penulis melaporkan 34.036 baris setelah pembersihan (30.719 non-spam dan 3.317 spam). Analisis dalam dataset mereka mencatat sekitar 97,3% komentar spam mengandung karakter Unicode non-standar versus 39,5% non-spam. Penulis kemudian mengambil subset seimbang 6.000 data (3.000 per kelas), lalu membagi train 4.200, validation 900, dan test 900 (450 per kelas). Persentase dalam korpus terkumpul tersebut tidak boleh digeneralisasi ke seluruh YouTube karena cara pengumpulan dan samplingnya spesifik.

**Metode.** Jalur A IndoBERT fine-tuned menggunakan teks yang dinormalisasi. Jalur B TF-IDF character n-gram pada Unicode mentah + LinearSVC. Model hybrid menggabungkan [CLS] 768 dimensi dan vektor character TF-IDF 11.738 dimensi, total 12.506 dimensi. Artikel menguji konfigurasi n-gram dan nilai C. IndoBERT dan hybrid sama-sama dilaporkan F1 sekitar 0,9978 pada test set; LinearSVC karakter sekitar 0,9944.

**Temuan dan pembacaan kritis.** Paper secara eksplisit membahas obfuscated comments sehingga menjadi studi pembanding paling dekat. Namun, evaluasi khusus “Abl-6” menggunakan 450 komentar spam dari test set yang sama, yang seluruhnya dipilih dari pool komentar spam/obfuscated. Penulis sendiri mencatat evaluasi ini secara matematis identik dengan breakdown kelas spam pada evaluasi global, bukan test set independen. Karena itu, hasilnya menunjukkan performa detektor hybrid pada subset yang mereka bentuk; paper tidak menyajikan protokol utama clean model → paired clean-obfuscated set yang mencakup empat keluarga transformasi dengan dua tingkat severity, sebagaimana repositori Anda.

**Kekuatan.** Sangat relevan secara domain dan teknis; membedakan jalur teks ternormalisasi dari fitur karakter Unicode mentah dan melakukan ablation n-gram.

**Keterbatasan.** Label utamanya spam/non-spam; dataset uji diseimbangkan 50:50 sedangkan korpus setelah pembersihan sekitar 9,7% spam; sehingga metrik tidak langsung sebanding dengan dataset penelitian Anda yang kelas promosi sekitar 12,03%. “Mengatasi obfuscation” di sini terutama menggunakan strategi hybrid/mitigasi, bukan pengukuran paired degradation pada model-model beku yang dilatih hanya pada teks bersih. Klaim kausal tentang `[UNK]` atau mekanisme attention perlu dibedakan dari bukti langsung kinerja yang dilaporkan.

**Keputusan penggunaan:** **Wajib menjadi sumber inti untuk research gap dan perbandingan metode.** Kita harus mengakui ada studi obfuscation judi YouTube. Potensi pembeda ada pada desain evaluasi, pairing, keluarga/severity yang ditentukan sebelum uji, dan perbandingan tiga model tanpa retraining khusus kondisi.

**Bukti yang dapat diekstrak:** Normalisasi + jalur karakter mentah dalam model hybrid; statistik karakter Unicode di dataset penulis; penggunaan test set seimbang; evaluasi obfuscation-spam bukan subset independen dari test set global. Lokator: Method, dataset/results, Table 4–8, discussion/conclusion.

---

## 19. Soysaldı Şahin et al. (2026) — *Revisiting SMS Spam Detection: The Impact of Feature Representation on Classical Machine Learning Models*

**Identitas:** Meryem Soysaldı Şahin, Durmuş Özkan Şahin, dan Areej Fateh Salah. *Electronics*, 15(4) (2026), 894. DOI: https://doi.org/10.3390/electronics15040894.

**Tujuan dan data.** Meneliti pengaruh representasi fitur terhadap performa beberapa pengklasifikasi klasik pada dataset SMSSpamCollection berbahasa Inggris: 5.574 pesan, 747 spam dan 4.827 ham. Kombinasi fitur–classifier dibandingkan pada evaluasi 10-fold cross-validation.

**Metode.** Tujuh teknik representasi fitur dan enam classifier klasik diuji (42 kombinasi konfigurasi). Penulis mengkaji kompromi precision, recall, specificity, F1, AUC, serta biaya komputasi dalam data teks pendek dan tidak seimbang.

**Temuan yang dilaporkan.** Logistic Regression disebut sebagai konfigurasi terbaik secara keseluruhan dalam abstrak, dengan accuracy 98,55%, precision spam 98,55%, recall 90,50%, F1 94,32%, dan AUC 0,9893. Paper menekankan bahwa pilihan representasi berinteraksi dengan pilihan classifier; representasi karakter/subword dapat kompetitif dalam SMS noisy, tetapi efektivitasnya tergantung konfigurasi dan metrik.

**Kekuatan.** Publikasi yang relatif baru; menyediakan eksperimen terkendali tentang representasi fitur dan imbalance, relevan sebagai rasional mengapa model word-based dan character-based layak dibandingkan.

**Keterbatasan.** Dataset SMS berbahasa Inggris historis, tidak terkait judi, YouTube, ataupun transformasi paired obfuscation. Ia tidak membuktikan Char-CNN atau character n-gram akan paling robust pada komentar Indonesia. Hasilnya hanya analogi pada short-text spam.

**Keputusan penggunaan:** **Pendukung untuk argumen pilihan representasi**, terutama Bab II. Di Bab I cukup disebut jika perlu menjelaskan bahwa pilihan representasi adalah dimensi perbandingan yang bermakna; jangan gunakan untuk klaim langsung tentang model Anda.

**Bukti yang dapat diekstrak:** Dampak representasi fitur tidak dapat dipisahkan dari classifier; metrik precision/recall penting pada kelas spam minoritas; character-level representation relevan pada teks pendek yang bervariasi. Lokator: Introduction, Method, Results, Discussion/Limitations.

---

## 20. Ishida et al. (2023) — *MOJI: Character-level Convolutional Neural Networks for Malicious Obfuscated JavaScript Inspection*

**Identitas:** Ishida et al. *Applied Soft Computing*, 137 (2023), 110138. DOI: https://doi.org/10.1016/j.asoc.2023.110138.

**Tujuan.** Mengembangkan MOJI, CNN tingkat karakter untuk mendeteksi JavaScript malicious yang diobfuscate sambil mempertahankan fungsionalitas kode, dan membandingkannya dengan metode deteksi kode lain.

**Data dan metode.** Objeknya adalah kode JavaScript, bukan bahasa alami. Studi menggunakan korpus kode benign/malicious dengan sumber serta kondisi uji yang ditetapkan penulis, dan membandingkan CNN karakter dengan metode yang mengandalkan abstraksi/fitur syntax-tree dan antivirus pada sampel yang mengalami obfuscation.

**Temuan yang dilaporkan.** Penulis menunjukkan bahwa CNN karakter dapat memberikan kinerja tinggi pada tugas inspeksi JavaScript obfuscated dan mengungguli beberapa pendekatan berbasis AST dalam skenario yang diuji. Mereka juga menunjukkan performa antivirus dapat turun pada kondisi obfuscation tambahan.

**Kekuatan.** Menyediakan analogi teknis bahwa representasi karakter dapat mempertahankan sinyal lokal di tengah transformasi bentuk permukaan.

**Keterbatasan.** Domainnya kode program yang semantik/fungsinya dilestarikan, bukan komentar manusia. Operasi obfuscation kode dan bahasa alami tidak identik. Karena itu, artikel tidak membuktikan bahwa Char-CNN pada komentar YouTube pasti tangguh; ia hanya mendukung hipotesis representasi karakter untuk diuji, bukan kesimpulan yang telah diketahui.

**Keputusan penggunaan:** **Referensi analogis tingkat rendah–menengah.** Bisa dipakai di Bab II saat menjelaskan motivasi teknis char-level, dengan batas domain dijelaskan eksplisit. Tidak perlu menjadi sumber utama Bab I.

**Bukti yang dapat diekstrak:** CNN karakter dapat menangkap pola karakter pada program yang mengalami obfuscation; hasil tersebut berlaku pada inspeksi JavaScript dan harus dibatasi domainnya. Lokator: method, experiments, results, discussion/conclusion.

---

## 21. Santika et al. (2025) — *Online Gambling Promotion Detection in Indonesian YouTube Comments Using Semi-Supervised IndoBERT Classification*

**Status audit:** Kandidat relevan; dipertahankan sebagai studi domain inti, tetapi bukan sebagai bukti langsung evaluasi robustness.

**Identitas bibliografi.** Satriadi Putra Santika, Muhammad Alfhi Saputra, Amalia Zahra, dan Derwin Suhartono. *Procedia Computer Science*, 269 (2025), 1269–1278. Prosiding ICCSCI 2025 yang diterbitkan Elsevier. DOI: https://doi.org/10.1016/j.procs.2025.09.068. Naskah 10 halaman; artikel menyatakan lisensi open access CC BY-NC-ND. Dataset disebut tersedia melalui Zenodo: https://doi.org/10.5281/zenodo.15424844.

**Pertanyaan dan tujuan penelitian.** Penulis mengembangkan deteksi komentar promosi judi online berbahasa Indonesia pada YouTube melalui pembelajaran semi-supervised berbasis IndoBERT. Motivasi utamanya adalah keterbatasan anotasi manual. Studi berfokus pada peningkatan klasifikasi dengan pseudo-labeling; bukan pada eksperimen perturbasi teks atau pengukuran penurunan performa akibat obfuscation.

**Data dan proses pelabelan.** Penulis mengumpulkan 10.101 komentar YouTube berbahasa Indonesia dari 10 video kategori gaming yang dipilih pada 5 Mei 2025 menggunakan YouTube Data API v3. Sekitar 10% data dilabeli manual sebagai Promotion atau Non-Promotion. Pada tabel hasil, 1.010 komentar disebut sebagai bagian berlabel; setelah preprocessing dataset yang disebut tersisa adalah 9.880 data. Naskah menjelaskan beberapa indikator promosi: nama situs judi, ajakan seperti “main”, “coba”, dan istilah terkait seperti “jepe”, “nagih”, atau “slot”. Prosedur label pada metode menyebut pelabelan dilakukan oleh penulis pertama; ada keterangan pemeriksaan ulang oleh annotator, tetapi tidak ditemukan pelaporan nilai inter-annotator agreement yang terukur. Oleh karena itu, jangan menganggap reliabilitas labelnya setara dengan studi yang melaporkan Cohen’s kappa.

**Preprocessing.** Tahap prapemrosesan meliputi konversi/normalisasi karakter Unicode, penghapusan emoji, URL, karakter asing dan simbol, penggabungan keyword promosi yang terpisah spasi, lowercasing, tokenisasi, stemming, normalisasi slang, serta penghapusan stopword. Pembagian data dilaporkan menggunakan rasio 7:1,5:1,5. Langkah penggabungan keyword dan normalisasi secara langsung dapat memperbaiki pola obfuscation tertentu sebelum klasifikasi; karena itu studi ini tidak dapat digunakan untuk menyimpulkan bagaimana model yang menerima teks tersamarkan mentah akan bertahan.

**Metode dan pembanding.** Penelitian membandingkan TF-IDF+SVM, Logistic Regression, XGBoost, Random Forest, RNN, LSTM, CNN, dan IndoBERT. IndoBERT dilatih terlebih dahulu dengan subset berlabel, lalu model digunakan untuk menghasilkan pseudo-label bagi data yang belum berlabel. Data berlabel dan pseudo-label digabungkan untuk proses pelatihan ulang semi-supervised. Tidak ada pengujian yang dilaporkan dengan protokol pasangan sampel normal-versus-obfuscated yang ditransformasi secara terkontrol.

**Hasil yang dilaporkan.** Pada skenario awal dengan 10% data berlabel, tabel menunjukkan TF-IDF+SVM sebagai model dengan F1 tertinggi, 0,972; IndoBERT memperoleh F1 0,961. Setelah pseudo-labeling dan pelatihan ulang, IndoBERT memperoleh Accuracy 0,986, Precision 0,991, Recall 0,980, dan F1 0,985 pada tabel utama. Angka-angka ini menggambarkan hasil dalam split dan preprocessing penelitian tersebut, bukan ukuran robustness dan bukan angka yang bisa dibandingkan langsung dengan hasil repositori Anda tanpa memperhatikan perbedaan dataset, preprocessing, split, dan protokol evaluasi.

**Kekuatan.**
- Sangat dekat dengan domain dan target label penelitian ini: komentar YouTube Indonesia, promosi/non-promosi, dan evaluasi model IndoBERT serta SVM.
- Menjadi bukti bahwa deteksi promosi dengan label biner sudah pernah dilakukan pada konteks YouTube Indonesia.
- Menyediakan pembanding baseline SVM dan IndoBERT serta membahas keterbatasan adaptasi terhadap bahasa yang terus berkembang.
- Memiliki DOI penerbit dan kanal data publik, sehingga dapat ditelusuri lebih lanjut.

**Keterbatasan dan catatan audit.**
- Tujuan utama adalah semi-supervised learning/pseudo-labeling; bukan robustness evaluation.
- Preprocessing menghapus atau menormalkan beberapa variasi tekstual dan menggabungkan kata kunci terpisah spasi, sehingga variasi masukan yang menjadi objek penelitian Anda tidak dipertahankan sebagai kondisi uji mentah.
- Keterangan hasil menggunakan jumlah yang tidak seluruhnya konsisten: abstrak menyebut 10.101 data, 10% diberi label; bagian hasil menyebut 1.010 data manual, 9.880 data setelah preprocessing, dan matriks konfusi final 1.482 sampel. Tabel metrik semi-supervised tidak menjelaskan secara rinci pada tempat yang sama mengapa ukuran uji berbeda dari matriks konfusi. Angka perlu dirujuk bersama penjelasan section-specific dan tidak disatukan seolah berasal dari satu evaluasi yang identik.
- Klaim “generalize well on noisy, informal text” tidak sama dengan ketahanan terhadap transformasi obfuscation yang terkontrol; studi tidak melaporkan eksperimen paired clean-vs-obfuscated.
- Daftar pustaka memuat banyak referensi lintas topik; beberapa mendukung klaim latar belakang/metode, tetapi tidak semuanya menjadi bukti langsung untuk robustness.
- Kesimpulan penulis menyatakan belum ada mekanisme untuk menyesuaikan diri terhadap bahasa yang berkembang guna menghindari moderasi. Ini adalah keterbatasan yang dinyatakan penulis, tetapi tidak boleh diperluas menjadi klaim bahwa studi tersebut tidak pernah memproses variasi teks apa pun: metode mereka justru menormalisasi variasi tertentu.

**Keputusan penggunaan:** **Pertahankan sebagai kandidat inti untuk konteks domain dan pembanding deteksi promosi**, serta sebagai sumber yang menunjukkan bahwa evasion bahasa berkembang disebut sebagai keterbatasan di masa depan. **Jangan** gunakan sebagai bukti bahwa belum ada studi obfuscation yang diuji secara eksplisit, atau bahwa model IndoBERT/SVM penelitian tersebut rentan/tahan terhadap keluarga O1–O4.

**Bukti yang dapat diekstrak untuk Bab I.**
1. Studi deteksi *Promotion/Non-Promotion* pada komentar YouTube Indonesia sudah dilakukan dengan beberapa model, termasuk SVM, CNN, dan IndoBERT.
2. SVM menghasilkan F1 0,972 pada skenario awal yang dilaporkan, sedangkan IndoBERT mencapai F1 0,961; setelah pseudo-labeling, IndoBERT mencapai F1 0,985.
3. Penulis menyatakan sebagai keterbatasan bahwa model belum mengakomodasi pola bahasa yang berkembang untuk menghindari moderasi.
4. Studi tidak menjalankan protokol evaluasi pasangan normal-versus-obfuscated yang setara dengan eksperimen penelitian Anda.

**Bukti untuk Bab II–III.** Klasifikasi promosi/non-promosi pada komentar YouTube; pseudo-labeling; contoh fitur/indikator label; preprocessing yang mencakup penggabungan token ber-spasi; dan perbandingan model klasik dengan model neural. Tidak cocok dijadikan justifikasi langsung bagi empat keluarga obfuscation penelitian Anda, karena transformasi tersebut tidak dievaluasi sebagai set kondisi paired test.

**Lokator dalam artikel:** bagian Introduction (cakupan studi sebelumnya), Method (data collecting, data preprocessing, model/training, evaluation), Results and Discussion (dataset summary, tabel hasil supervised dan semi-supervised), dan Conclusion and Future Works.

---

---

# BAGIAN C. SINTESIS LINTAS-PUBLIKASI

## C1. Apa yang sudah mapan dalam literatur?

### 1. Deteksi komentar spam, judi, atau promosi sudah banyak diteliti

Oh (2021) dan Xiao & Liang (2024) menunjukkan bahwa klasifikasi spam/ham komentar YouTube menggunakan model ML klasik dan ensemble sudah ada. Perdana et al. (2024), Situmorang et al. (2025), Pariamalinya et al. (2026), Nugraha et al. (2026), Widiyanto et al. (2025), Ariyanto et al. (2026), Angelo et al. (2025), dan Hidayat et al. (2026) memperlihatkan bahwa deteksi konten judi/promosi pada media sosial Indonesia semakin khusus dan beragam. Jadi, **novelty penelitian Anda tidak dapat didasarkan pada “deteksi promosi judi online menggunakan ML/IndoBERT/SVM” secara umum.**

### 2. Variasi/penyamaran teks merupakan tantangan yang diakui

Moradi & Samwald (2021), Wang et al. (2022), NL-Augmenter (Dhole et al., 2023), dan Khan et al. (2025) memberi fondasi umum tentang input perturbation, robustness, transformasi teks, serta trade-off normalisasi. Domain promosi judi pun telah membahas variasi karakter: Angelo et al. mengaplikasikan normalisasi karakter, Ariyanto et al. menormalisasi istilah tersamarkan sebelum IndoBERT, dan Hidayat et al. secara eksplisit menguji pendekatan hybrid untuk spam judol obfuscated. Maka klaim “belum ada yang meneliti obfuscation pada judi online” tidak dapat dipertahankan.

### 3. Normalisasi teks dan pengukuran robustness adalah tujuan yang berbeda

Beberapa studi domain menangani bentuk teks tersamarkan melalui normalisasi sebelum klasifikasi atau memasukkan fitur karakter mentah dalam arsitektur hybrid. Pendekatan tersebut bisa menjadi mitigasi yang sah dan berguna. Akan tetapi, bila pertanyaan penelitian adalah “berapa besar model yang dilatih pada teks normal berubah performanya ketika menerima input tersamarkan?”, diperlukan pembandingan terpisah antara input normal dan input perturbasi dengan model tetap. Normalisasi sebelum model dapat mengubah objek yang diukur, sehingga skor pipeline tidak langsung menjadi metrik sensitivitas model mentah.

### 4. Model yang berbeda memiliki representasi dan trade-off berbeda

SVM word TF-IDF, character CNN, dan IndoBERT merepresentasikan teks dengan cara berbeda. Literatur domain sudah membandingkan SVM, Transformer, RNN, atau boosting pada dataset yang berbeda; literatur SMS/JavaScript memberi analogi tambahan mengenai representasi karakter. Namun, bukti bahwa char-level akan lebih tahan dari subword/word-level pada *dataset dan perturbasi khusus penelitian ini* baru dapat disimpulkan dari eksperimen repositori Anda, bukan digeneralisasikan dari paper lintas domain.

### 5. Integritas dataset dan anotasi harus dipertahankan

Mu et al. (2024) menunjukkan risiko duplikasi/near-duplicate bagi evaluasi; Klie et al. (2024) menunjukkan bahwa proses anotasi dan quality management perlu dijelaskan secara eksplisit. Ini penting karena komentar YouTube promosi dapat berupa template berulang, sementara klasifikasi promosi/non-promosi memerlukan pemahaman fungsi ujaran. Data splitting, deduplikasi, dan aturan label bukan sekadar detail implementasi: ini mempengaruhi kepercayaan terhadap klaim kinerja.

## C2. Perbedaan istilah yang wajib dijaga

| Istilah pada publikasi | Apa yang sering diklasifikasikan | Hubungan dengan tugas Anda |
|---|---|---|
| Spam / ham | Spam umum dibanding komentar sah | Bisa mencakup promosi, tetapi tidak sama dengan promosi judi. |
| Gambling / non-gambling | Teks yang terkait judi dibanding teks yang tidak terkait | Dapat memasukkan berita, kritik, pengalaman pribadi, atau anti-judi; tidak identik dengan promosi. |
| Gambling promotion / non-promotion | Komentar yang mempromosikan/mengajak/beriklan judi dibanding yang tidak | Paling dekat dengan label target penelitian Anda, asalkan definisi operasionalnya eksplisit. |
| Obfuscation-aware detection | Sistem memproses atau menormalisasi bentuk tersamarkan | Tidak otomatis menunjukkan model tetap dievaluasi pada teks raw-obfuscated. |
| Robustness evaluation | Mengukur stabilitas kinerja saat kondisi masukan/distribusi berubah | Fokus konsep penelitian Anda; harus ditopang protokol evaluasi eksplisit. |
| Generalization / holdout performance | Performa pada data baru yang mungkin berbeda sumber/distribusi | Berbeda dari robustness terhadap perturbasi terkontrol pada komentar yang sama. |

## C3. Research gap kerja yang dapat dipertahankan sementara

Rumusan gap berikut **masih bersifat sementara hingga perbandingan metode paper inti disahkan**:

> Meskipun penelitian sebelumnya telah mengembangkan sistem deteksi promosi/spam judi online pada media sosial dan sebagian sudah menerapkan normalisasi atau arsitektur untuk menangani teks tersamarkan, belum semua studi tersebut mengevaluasi ketahanan model dengan protokol yang secara eksplisit membandingkan prediksi pada komentar normal dan pasangan komentar yang disamarkan, menggunakan model tetap tanpa pelatihan ulang per kondisi, serta menganalisis perubahan kinerja lintas keluarga dan tingkat keparahan penyamaran. Penelitian ini difokuskan pada evaluasi komparatif tersebut untuk Linear SVM word-level TF-IDF, Char-CNN, dan IndoBERT pada komentar YouTube berbahasa Indonesia.

**Batas klaim:** frasa “belum semua studi tersebut” sengaja dipilih lebih aman daripada “belum ada penelitian”. Setelah metodologi Angelo dan Hidayat ditelaah berdampingan secara sistematis, gap harus dipersempit atau diubah bila mereka ternyata melakukan bagian yang sama.

## C4. Yang tidak boleh dijadikan klaim

- “Ini penelitian pertama tentang obfuscation judi online di YouTube.” Tidak didukung oleh koleksi ini.
- “Belum ada model yang menangani teks obfuscated judi online.” Tidak benar menurut publikasi #5, #7, dan #18.
- “IndoBERT selalu paling baik pada komentar judi.” Tidak dapat disimpulkan lintas dataset/label/normalisasi; repository Anda sendiri menguji konteks robustness berbeda.
- “Char-CNN selalu lebih robust daripada Transformer.” Tidak dapat disimpulkan dari MOJI atau SMS spam; harus dibatasi hasil eksperimen Anda.
- “Skor F1 0,99 dari studi lain berarti model tersebut lebih baik daripada model saya.” Skor tidak dapat dibandingkan langsung bila label, korpus, sampling, split, preprocessing, dan kondisi uji berbeda.
- “Normalisasi merupakan pengukuran robustness.” Normalisasi dapat menjadi pertahanan/pipeline preprocessing; bukan otomatis evaluasi perubahan performa pada raw perturbed inputs.
- “Paired Evaluation paper menjelaskan penuh bootstrap CI untuk F1.” Peyrard et al. fokus pada agregasi evaluasi berbasis pasangan, bukan secara spesifik semua statistik yang Anda gunakan.

---

# BAGIAN D. APAKAH 21 PUBLIKASI SUDAH CUKUP?

## D1. Jawaban singkat berbasis audit

**Korpus 21 publikasi cukup untuk menyusun argumentasi awal Bab I, tetapi belum otomatis cukup untuk mengunci research gap dan semua bukti empirisnya.** Publikasi #21 memperkuat bukti bahwa deteksi promosi biner pada komentar YouTube Indonesia sudah diteliti, sekaligus menyebut adaptasi terhadap bahasa yang digunakan untuk menghindari moderasi sebagai keterbatasan. Namun, paper itu tidak mengukur paired robustness sebagaimana protokol utama penelitian Anda. Kebutuhan tambahan masih bersifat terarah: sumber resmi untuk konteks, sumber statistik paired F1/CI, dan studi robustness teks yang protokolnya sangat dekat.

## D2. Peta kekurangan bukti dan pencarian lanjutan

### Prioritas wajib: konteks awal Bab I

**Argumen yang perlu diperkuat:** skala dan urgensi masalah judi online di Indonesia.

**Cari:** laporan primer Komdigi/PPATK dan dokumen hukum atau kebijakan resmi. Setiap angka harus memiliki tanggal, definisi, dan cakupan platform yang jelas. Jumlah konten yang ditindak tidak otomatis sama dengan jumlah komentar YouTube promosi.

Kata kunci: `site:komdigi.go.id penanganan konten perjudian 2025 Google YouTube`; `site:ppatk.go.id transaksi judi online 2024 laporan`; `site:peraturan.bpk.go.id perjudian UU 7 1974`.

### Prioritas wajib: definisi tugas

**Argumen yang perlu diperkuat:** perbedaan promosi, komentar terkait judi, anti-judi, berita, dan non-promosi.

**Cari:** studi yang mendefinisikan *promotional intent* atau tujuan komunikatif, beserta pedoman anotasi konten judi Indonesia. Banyak paper hanya memakai kelas gambling/non-gambling atau spam/ham, yang tidak identik dengan target penelitian Anda.

Kata kunci: `online gambling promotion intent classification YouTube comments dataset annotation`; `Indonesian online gambling promotional comments annotation guideline`; `gambling-related vs gambling promotion text classification`.

### Prioritas wajib: research gap

**Argumen yang perlu diperkuat:** apakah penelitian terdahulu menguji pasangan teks normal dan teks yang disamarkan secara eksplisit.

**Cari:** studi robustness/adversarial pada teks sosial yang menguji input asli dan perturbasi pasangannya. Angelo dan Hidayat telah membahas obfuscation; perbandingan metode lengkap harus dilakukan sebelum gap dikunci.

Kata kunci: `online gambling promotion YouTube paired obfuscated test robustness`; `clean test versus character perturbed text classification Indonesian social media`; `text obfuscation robustness evaluation paired samples social media`.

### Prioritas wajib: justifikasi keluarga penyamaran O1–O4

**Argumen yang perlu diperkuat:** validitas taksonomi substitusi karakter, insertion/deletion, whitespace, serta Unicode/variasi ortografis.

**Cari:** literatur text normalization dan character-level adversarial attack, terutama pada teks media sosial dan bahasa Indonesia. Khan dan Moradi memberi landasan umum, tetapi contoh domain langsung akan memperkuat justifikasi.

Kata kunci: `character-level adversarial perturbations social media text Unicode homoglyph`; `Indonesian noisy text character substitution obfuscation NLP`; `homoglyph attack text classification Unicode`.

### Prioritas wajib: statistik untuk hasil eksperimen

**Argumen yang perlu diperkuat:** pemakaian perubahan F1, retensi F1, dan interval kepercayaan berpasangan.

**Cari:** sumber metodologis khusus untuk *paired bootstrap confidence intervals* pada F1 atau perbandingan metrik klasifikasi yang bergantung pada prediksi berpasangan. Peyrard mendukung gagasan evaluasi berpasangan secara umum, tetapi tidak otomatis membenarkan semua prosedur bootstrap F1.

Kata kunci: `paired bootstrap confidence interval F1 score classification`; `bootstrap confidence intervals difference F1 paired predictions`; `statistical significance comparison classifiers paired test F1`.

### Prioritas baik: pembanding representasi dan kualitas anotasi

**Representasi kata–karakter–subword:** cari studi NLP yang membandingkan word-level, character-level, dan Transformer pada teks noisy/perturbed. Soysaldı berfokus pada SMS Inggris dan MOJI pada JavaScript, jadi keduanya hanya analogi lintas domain.

Kata kunci: `word-level character-level transformer robustness character perturbation text classification`; `character CNN noisy social media text classification adversarial`.

**Kualitas label dan preservasi semantik:** cari studi tentang pedoman anotasi, inter-annotator agreement, serta validasi manusia bahwa transformasi mempertahankan makna. Klie dan NL-Augmenter sudah membantu, namun tidak menggantikan prosedur validasi pada dataset Anda.

Kata kunci: `semantic preservation validation adversarial text perturbation human evaluation`; `annotation agreement imbalanced short social media classification labels`.

### Prioritas opsional: implikasi moderasi

Studi mengenai false positives/false negatives, cost-sensitive classification, atau evaluasi sistem moderasi dapat memperluas diskusi praktis, tetapi bukan syarat untuk argumen utama Bab I.

Kata kunci: `automated content moderation false positives fairness text classification online gambling`.

## D3. Prioritas pencarian yang paling efisien

1. **Cari 2–4 sumber resmi** untuk konteks nasional, bukan statistik dari artikel yang mengambil angka sekunder tanpa pelacakan.
2. **Cari 3–6 studi yang paling dekat pada robustness/obfuscation teks**, lalu bandingkan benar-benar protokol uji, bukan judulnya saja.
3. **Cari 1–3 sumber statistik evaluasi berpasangan**, khususnya jika skripsi akan membahas bootstrap confidence intervals, paired comparisons, atau signifikansi perubahan F1.
4. Bila masih ada celah, cari sumber langsung soal definisi “promosi” dan quality annotation. Hindari memperluas pencarian ke paper deteksi judi umum yang hanya menambah jumlah tetapi tidak menutup argumen.

Secara realistis, 6–12 sumber tambahan berkualitas mungkin sudah cukup untuk menutup gap utama; angka ini adalah target kerja, bukan kuota wajib. Satu sumber primer yang tepat dapat lebih bernilai daripada beberapa artikel umum yang tidak mendukung klaim Bab I.

## D4. Status korpus setelah revisi

Publikasi #21, *Online Gambling Promotion Detection in Indonesian YouTube Comments Using Semi-Supervised IndoBERT Classification* (Santika et al., 2025), telah dimasukkan ke Bagian B sebagai audit publikasi ke-21 dan ke daftar pustaka ringkas. Penelaahan mencakup bagian pendahuluan, pengumpulan data, pelabelan, preprocessing, metode, tabel hasil supervised dan semi-supervised, kesimpulan, serta daftar pustaka.

Kandidat tambahan #22–#24 yang pernah disebut di percakapan sebelumnya **tidak dimasukkan ke korpus audit ini** sesuai keputusan pengguna: satu kandidat dengan akses naskah yang tidak cukup jelas ditolak, sedangkan kandidat lainnya bukan artikel jurnal yang ingin dihitung sebagai anggota korpus. Dokumen ini tidak memperlakukan skripsi atau statistik pemerintah sebagai “jurnal”. Bila sumber resmi non-jurnal digunakan nantinya untuk memberikan konteks Bab I, sumber tersebut harus dicatat terpisah dari 21 publikasi yang diaudit.

# BAGIAN E. PEMETAAN SUMBER KE BAB SKRIPSI

Pemetaan berikut adalah panduan penggunaan, bukan kewajiban mengutip setiap publikasi pada semua bab.

## E1. Prioritas tinggi untuk Bab I

Fokus kelompok ini adalah konteks, penelitian terdahulu yang paling dekat, dan penyusunan *research gap*.

**#2 — Situmorang et al. (2025).** Promosi pada media sosial dan definisi kelas; platform utama X/Twitter.

**#4 — Nugraha et al. (2026).** Pembanding IndoBERT/mBERT; label *gambling-related* lebih luas daripada promosi.

**#5 — Angelo et al. (2025).** Studi YouTube yang paling dekat; penting untuk membandingkan normalisasi dengan evaluasi raw-obfuscated.

**#6 — Perdana et al. (2024).** Ciri dan definisi promosi, tetapi platformnya Twitter/X.

**#7 — Ariyanto et al. (2026).** IndoBERT dan normalisasi istilah tersamarkan; target kelas lebih luas daripada promosi saja.

**#11 — Wang et al. (2022), #12 — Moradi & Samwald (2021), dan #14 — Khan et al. (2025).** Landasan konsep robustness, perturbasi masukan, dan variasi teks.

**#18 — Hidayat et al. (2026).** Pembanding sangat dekat untuk obfuscation pada komentar YouTube dan pendekatan hybrid.

**#21 — Santika et al. (2025).** Studi langsung pada label Promotion/Non-Promotion di komentar YouTube Indonesia yang membandingkan SVM, CNN, dan IndoBERT dengan pseudo-labeling. Relevan untuk konteks domain, tetapi tidak melakukan paired clean-versus-obfuscated evaluation.

## E2. Prioritas tinggi untuk Bab II

Fokus kelompok ini adalah dasar teori, mekanisme representasi/model, serta sintesis kajian pustaka.

**Representasi dan arsitektur.** #3 membahas SVM; #4 dan #7 membahas BERT; #19 membahas representasi fitur untuk SMS; #20 membahas Char-CNN pada kode JavaScript yang diobfuscate. Untuk #19 dan #20, nyatakan batas domain dengan jelas.

**Robustness, transformasi, dan serangan teks.** Gunakan #9, #11, #12, #13, dan #14. Hindari menyamakan *adversarial attack*, variasi teks alami, normalisasi, dan evaluasi robustness sebagai istilah yang saling dapat dipertukarkan.

**Model deteksi spam/judi sebagai pembanding.** Gunakan #1, #3, #5, #6, #8, #10, dan #18 dengan mempertimbangkan perbedaan target label, data, dan preprocessing.

**Evaluasi berpasangan dan validitas perbandingan.** #15 dan #17 memberi landasan mengenai kualitas data dan evaluasi sistem berpasangan. Keduanya perlu dilengkapi sumber statistik yang secara khusus mendukung interval kepercayaan atau pengujian perubahan F1.

## E3. Prioritas tinggi untuk Bab III

Fokus kelompok ini adalah mutu dataset, pelabelan, transformasi, pembagian data, dan protokol evaluasi.

**Deduplikasi dan data leakage.** #15 Mu et al. (2024).

**Kualitas anotasi.** #16 Klie et al. (2024); #2, #4, dan #6 juga memberi contoh *agreement* yang dilaporkan.

**Konstruksi perturbasi dan task-sensitive transformations.** #12 Moradi & Samwald (2021), #13 Dhole et al. (2023), dan #14 Khan et al. (2025).

**Pembanding protokol pada domain.** #5 Angelo et al. (2025), #7 Ariyanto et al. (2026), dan #18 Hidayat et al. (2026).

## E4. Prioritas untuk Bab IV

Gunakan #5, #7, dan #18 untuk membandingkan konteks domain. Jangan membandingkan nilai F1 secara langsung jika label, dataset, preprocessing, split, dan kondisi uji berbeda.

Gunakan #11, #12, dan #14 untuk interpretasi robustness; #17 untuk konsep evaluasi berpasangan; serta #8 untuk mengingatkan bahwa performa holdout/generalization berbeda dari robustness pada perturbasi terkontrol.

Gunakan #19 dan #20 hanya sebagai analogi terbatas ketika membahas representasi karakter. Keduanya bukan bukti langsung untuk komentar YouTube berbahasa Indonesia.

# BAGIAN F. EVIDENCE BANK UNTUK BAB I

Di bawah ini adalah **parafrasa bukti yang aman dijadikan catatan penulisan**. Bukan kutipan langsung; penulis tetap harus membuka sumber asli untuk membuat sitasi dan memastikan konteks.

## F1. Urgensi masalah dan platform

- **Sumber yang cocok:** data resmi pemerintah untuk konteks nasional; Situmorang et al. (2025), Perdana et al. (2024), Widiyanto et al. (2025), dan Angelo et al. (2025) untuk bukti akademik penggunaan media sosial/komentar sebagai objek deteksi.
- **Bukti dari korpus:** studi yang diaudit berulang kali mengambil data dari X/Twitter dan YouTube untuk mengenali promosi atau komentar judi. Ini menunjukkan adanya perhatian penelitian pada masalah, tetapi jumlah sampel peneliti tidak sama dengan prevalensi populasi.
- **Batas inferensi:** angka komentar yang dikumpulkan peneliti tidak boleh digeneralisasi menjadi jumlah komentar judi di seluruh YouTube. Angka pemblokiran konten pada semua platform tidak boleh dilabeli sebagai angka khusus komentar YouTube.

## F2. Definisi promosi

- **Sumber yang cocok:** Situmorang et al. (2025), Perdana et al. (2024), Angelo et al. (2025), dan Santika et al. (2025). Santika et al. secara eksplisit menggunakan label Promotion/Non-Promotion pada komentar YouTube Indonesia.
- **Bukti dari korpus:** studi promosi menyebut indikator seperti ajakan untuk bermain, bonus, situs/link, kode promosi, kata domain, dan ekspresi persuasif; namun definisi antarstudi tidak seragam.
- **Batas inferensi:** kata seperti “judi”, “slot”, atau “togel” sendiri belum otomatis membuat komentar termasuk promosi. Penggunaan istilah yang berkaitan dengan judi harus ditafsirkan menurut fungsi komunikasi komentar dan aturan label penelitian.

## F3. Penyamaran teks dan variasi bentuk

- **Sumber yang cocok:** Khan et al. (2025), Moradi & Samwald (2021), Angelo et al. (2025), Ariyanto et al. (2026), Hidayat et al. (2026).
- **Bukti dari korpus:** variasi dapat berupa perubahan karakter, angka yang menyerupai huruf, ejaan tidak standar, pengulangan karakter, perubahan spasi/batas kata, serta homoglif Unicode. Literatur umum mengingatkan bahwa variasi dapat disengaja maupun tidak disengaja.
- **Batas inferensi:** tidak semua variasi ejaan bermotif pengelabuan; dan tidak semua transformasi otomatis mempertahankan makna. Definisi operasional O1–O4 harus dinyatakan terpisah dan divalidasi.

## F4. Performa normal versus robustness

- **Sumber yang cocok:** Wang et al. (2022), Moradi & Samwald (2021).
- **Bukti dari korpus:** model dengan kinerja tinggi pada benchmark/masukan bersih dapat sensitif terhadap perturbasi yang relatif kecil. Penambahan evaluasi pada masukan yang berubah dapat mengungkap kelemahan yang tidak terlihat dari skor standar.
- **Batas inferensi:** penurunan performa pada satu keluarga perturbasi tidak otomatis berarti model gagal pada seluruh variasi adversarial. Dampak bergantung pada jenis transformasi, severity, model, data, dan task.

## F5. Penelitian terdahulu dan gap

- **Sumber yang cocok:** Angelo et al. (2025), Hidayat et al. (2026), Ariyanto et al. (2026), Situmorang et al. (2025), Nugraha et al. (2026), Santika et al. (2025), dan Moradi & Samwald (2021).
- **Bukti dari korpus:** deteksi promosi/judi pada media sosial Indonesia dan penanganan teks tersamarkan sudah diteliti. Beberapa studi mengandalkan normalisasi sebelum klasifikasi; paper hybrid Hidayat menggabungkan input normalisasi untuk IndoBERT dan Unicode mentah untuk fitur karakter.
- **Batas inferensi:** jangan menyatakan tidak ada penelitian obfuscation. Gap harus didasarkan pada perbedaan yang spesifik setelah metode tiap paper disejajarkan: model beku atau dilatih ulang, paired samples atau bukan, keluarga/severity perturbasi, evaluasi raw text atau normalized pipeline, label, platform, dan metrik.

---

# BAGIAN G. AUDIT KONDISI REPOSITORI PENELITIAN TERHADAP LITERATUR

Bagian ini adalah pengecekan konsistensi yang relevan antara audit literatur dan dokumentasi eksperimen, bukan audit ulang kode menyeluruh.

Repositori `https://github.com/khairys/TugasAkhir` memuat laporan Stage 8 experimental lock dan Stage 10 robustness evaluation. Laporan Stage 10 menyatakan 4.116 sampel pada test set normal, label 0/1 tidak berubah dalam kondisi tersamarkan, delapan kondisi perturbasi (O1–O4 × MILD/STRONG), dan tiga model beku. Hasil utama yang tercantum di repositori: baseline F1 Promotion Char-CNN 0,9786; IndoBERT 0,9605; Linear SVM 0,9428. Rata-rata F1-drop berpasangan dilaporkan sekitar 0,0037 untuk Char-CNN, 0,0569 untuk SVM, dan 0,0839 untuk IndoBERT.

**Angka-angka tersebut adalah temuan penelitian Anda, bukan temuan 20 publikasi.** Angka ini dapat membantu memastikan pertanyaan penelitian cocok dengan hasil yang tersedia, tetapi Bab IV tetap menjadi lokasi laporan hasil dan interpretasi penuh. Bab I tidak perlu membuka dengan peringkat final model.

### G1. Poin konsistensi yang perlu diperiksa sebelum menulis Bab III/IV

1. **Terminologi O3:** beberapa deskripsi pada laporan eksperimen menyebut whitespace manipulation termasuk penyisipan spasi dan/atau penghapusan spasi/concatenation, sedangkan spesifikasi OBFUSCATION perlu dicek apakah implementasinya hanya menyisipkan spasi internal. Istilah dan implementasi harus konsisten.
2. **Terminologi O4:** spesifikasi menyebut Unicode homoglyph dan variasi ortografis/elongation. Maka jangan menyebut seluruh hasil O4 sebagai efek homoglyph semata tanpa memisahkan tipe transformasi aktual yang benar-benar terjadi.
3. **Makna label:** pastikan label repo “Promotion/Non-Promotion” didukung pedoman yang membedakan promosi dari komentar non-promosi tentang judi. Ini lebih penting daripada sekadar mempertahankan label secara mekanis pada transformasi.
4. **Paired F1 versus full-set F1:** saat melaporkan F1-drop, gunakan F1 Normal dan F1 Obfuscated dari subset pasangan yang sama jika definisinya memang paired robustness. Jangan mencampur skor full-set dengan skor paired dalam satu pengurangan tanpa penjelasan.
5. **Klaim mekanisme:** hasil false positive IndoBERT pada O4 menunjukkan kegagalan empiris pada kondisi O4; untuk menyatakan tokenizer/self-attention *menyebabkan* pola itu diperlukan evidence khusus (misalnya inspeksi token/subword atau eksperimen terkontrol). Uraikan sebagai hipotesis penjelas jika belum diuji.
6. **Independensi evaluasi:** paper #18 menyoroti mengapa subset spam obfuscated yang diambil dari test set global bukan test set independen. Dalam penelitian Anda, klaim nilai paired evaluation bertumpu pada pasangan source_record_id yang sama dan metrik dihitung pada subset `changed=True`, yang merupakan desain berbeda; jelaskan ini dengan rumus dan diagram.

---

# BAGIAN H. KEPUTUSAN AKHIR DAN CHECKLIST

## H1. Keputusan terhadap 21 publikasi

- **Pertahankan sebagai referensi utama:** #2, #5, #6, #7, #11, #12, #14, #18, dan #21.
- **Pertahankan sebagai pembanding langsung dengan caveat label/metode:** #3, #4, #8.
- **Pertahankan untuk metodologi kualitas/evaluasi:** #13, #15, #16, #17.
- **Pertahankan sebagai pendukung terbatas/analogi:** #1, #9, #10, #19, #20.
- **Audit bibliografi ekstra sebelum kutip:** terutama #3 (anomali tanggal), #4 (referensi mismatched), #8 (trio metrik abstrak perlu pengecekan), serta angka jumlah entri pada #2. Masalah editorial atau sitasi yang terdeteksi tidak otomatis berarti penelitian sepenuhnya salah; artinya setiap klaim harus ditelusuri lebih ketat.

Tidak ada alasan untuk menghapus sebuah paper hanya karena domainnya berbeda. Namun, paper lintas domain sebaiknya tidak disamakan statusnya dengan bukti langsung untuk komentar YouTube promosi judi.

## H2. Checklist sebelum menulis latar belakang

- [ ] Setiap angka urgensi punya sumber resmi primer dan definisi angka yang jelas.
- [ ] Setiap istilah “promosi”, “spam judi”, dan “komentar terkait judi” dibedakan.
- [ ] Angelo et al. dan Hidayat et al. sudah disejajarkan menggunakan matriks: label, data, preprocessing, model, split, raw/normalized, paired/not paired, families, severity, metrics.
- [ ] Tidak ada klaim “penelitian pertama” tanpa systematic search yang dapat dipertanggungjawabkan.
- [ ] Setiap klaim mengenai robustness mempunyai referensi yang benar-benar menguji perturbasi, bukan hanya menyebut obfuscation dalam pendahuluan.
- [ ] Justifikasi paired bootstrap/F1 CI sudah memiliki referensi statistik yang sesuai.
- [ ] Klaim teoritis tentang Char-CNN/IndoBERT ditulis sebagai hipotesis kecuali didukung bukti eksperimen langsung.
- [ ] Sumber ditandai untuk Bab I vs Bab II/III agar latar belakang tidak berubah menjadi penjelasan teknis panjang.

## H3. Rencana kerja berikutnya

**Langkah 1 — Lengkapi sumber:** tambahkan sumber resmi Indonesia dan audit kandidat langsung lain tentang robustness/obfuscation.

**Langkah 2 — Buat evidence map:** bandingkan #5, #7, #18, #12, dan kandidat tambahan yang paling dekat berdasarkan target label, data, preprocessing, model tetap/tidak, paired samples, keluarga/severity perturbasi, dan metrik.

**Langkah 3 — Tetapkan research gap:** gunakan bahasa yang terbatas oleh bukti, kemudian kunci pertanyaan penelitian Bab I.

**Langkah 4 — Mulai menulis:** susun 1.1 Latar Belakang bertahap; setiap paragraf dilengkapi tujuan argumen, klaim, bukti pendukung, dan transisi ke paragraf berikutnya.

---

# DAFTAR PUSTAKA RINGKAS (21 PUBLIKASI YANG DIAUDIT)

1. Oh, H. (2021). A YouTube Spam Comments Detection Scheme Using Cascaded Ensemble Machine Learning Model. *IEEE Access, 9*, 144121–144128. https://doi.org/10.1109/ACCESS.2021.3121508
2. Situmorang, G. F., Manurung, J. D., Lubis, R., Sikana, N., & Lionggo, K. (2025). An Intelligent System for Detecting Online Gambling Promotion on Social Media Based on BERT and Adaptive Browser Extension. *JANAPATI, 14*(3), 679–691. https://doi.org/10.23887/janapati.v14i3.103511
3. Pariamalinya, U. A., Limbong, J. J. A., & Naibaho, J. P. P. (2026). Classification of Online Gambling Spam Comments on YouTube Using Support Vector Machine. *Indonesian Journal of Artificial Intelligence and Data Mining, 9*(1), 153–163. https://doi.org/10.24014/ijaidm.v9i1.39193
4. Nugraha, S. A., Lestari, C., Sanjaya, K. B., Naya, R. A., & Jolie, J. (2026). Comparative Analysis of IndoBERT and mBERT for Online Gambling Comment Detection in Indonesian Social Media. *JUTIF, 7*(2), 1931–1943. https://doi.org/10.52436/1.jutif.2026.7.2.5677
5. Angelo, M., Robet, & Hendrik, J. (2025). Comparative Performance of Machine Learning Algorithms for Detecting Online Gambling Promotional Comments on YouTube. *Jurnal Teknologi dan Manajemen Informatika, 11*(2), 132–142. https://doi.org/10.26905/jtmi.v11i2.16286
6. Perdana, R. B., Ardin, B., Budi, I., Santoso, A. B., Ramadiah, A., & Putra, P. K. (2024). Detecting Online Gambling Promotions on Indonesian Twitter Using Text Mining Algorithm. *International Journal of Advanced Computer Science and Applications, 15*(8), 942–949. https://doi.org/10.14569/IJACSA.2024.0150893
7. Ariyanto, Y., Aji, D. K. P., Setiadi, C., Syaifudin, Y. W., & Renozonarca, A. (2026). Fine-Tuning IndoBERT for Detecting Online Gambling Promotion in Indonesian-Language Social Media Comments. *IJECSA, 5*(2), 107–116. https://doi.org/10.30812/ijecsa.v5i2.6664
8. Widiyanto, A., Prameswari, M., & Latief, M. A. (2025). Gambling Comments Detection on YouTube: A Comparative Study of Tree-Based Boosting, LSTM and GRU Models. *JUTI: Jurnal Ilmiah Teknologi Informasi, 23*(2), 144–160. https://doi.org/10.12962/j24068535.v23i2.a1305
9. Yang, X., Qi, Y., Chen, H., Liu, B., & Liu, W. (2023). Generation-based Parallel Particle Swarm Optimization for Adversarial Text Attacks. *Information Sciences, 644*, 119237. https://doi.org/10.1016/j.ins.2023.119237
10. Xiao, A. S., & Liang, Q. (2024). Spam Detection for YouTube Video Comments Using Machine Learning Approaches. *Machine Learning with Applications, 16*, 100550. https://doi.org/10.1016/j.mlwa.2024.100550
11. Wang, X., Wang, H., & Yang, D. (2022). Measure and Improve Robustness in NLP Models: A Survey. In *Proceedings of NAACL-HLT 2022* (pp. 4569–4586). https://doi.org/10.18653/v1/2022.naacl-main.339
12. Moradi, M., & Samwald, M. (2021). Evaluating the Robustness of Neural Language Models to Input Perturbations. In *Proceedings of EMNLP 2021* (pp. 1558–1570). https://doi.org/10.18653/v1/2021.emnlp-main.117
13. Dhole, K., et al. (2023). NL-Augmenter: A Framework for Task-Sensitive Natural Language Augmentation. *Northern European Journal of Language Technology, 9*. https://doi.org/10.3384/nejlt.2000-1533.2023.4725
14. Khan, J., Ahmad, K., Jagatheesaperumal, S. K., & Sohn, K.-A. (2025). Textual Variations in Social Media Text Processing Applications: Challenges, Solutions, and Trends. *Artificial Intelligence Review, 58*, 89. https://doi.org/10.1007/s10462-024-11071-z
15. Mu, Y., Jin, M., Song, X., & Aletras, N. (2024). Enhancing Data Quality through Simple De-duplication: Navigating Responsible Computational Social Science Research. In *Proceedings of EMNLP 2024* (pp. 12477–12492). https://doi.org/10.18653/v1/2024.emnlp-main.694
16. Klie, J.-C., Eckart de Castilho, R., & Gurevych, I. (2024). Analyzing Dataset Annotation Quality Management in the Wild. *Computational Linguistics, 50*(3), 817–866. https://doi.org/10.1162/coli_a_00516
17. Peyrard, M., Zhao, W., Eger, S., & West, R. (2021). Better than Average: Paired Evaluation of NLP Systems. In *Proceedings of ACL-IJCNLP 2021* (pp. 2301–2315). https://doi.org/10.18653/v1/2021.acl-long.179
18. Hidayat, D. B., Chamid, A. A., & Jazuli, A. (2026). Implementasi Model Hybrid IndoBERT–LinearSVC untuk Deteksi Spam Judol Obfuscated pada Komentar YouTube. *Progresif: Jurnal Ilmiah Komputer, 22*(3), 820–833. https://doi.org/10.35889/progresif.v22i3.3914
19. Soysaldı Şahin, M., Şahin, D. Ö., & Salah, A. F. (2026). Revisiting SMS Spam Detection: The Impact of Feature Representation on Classical Machine Learning Models. *Electronics, 15*(4), 894. https://doi.org/10.3390/electronics15040894
20. Ishida, M., Kaneko, N., & Sumi, K. (2023). MOJI: Character-level Convolutional Neural Networks for Malicious Obfuscated JavaScript Inspection. *Applied Soft Computing, 137*, 110138. https://doi.org/10.1016/j.asoc.2023.110138
21. Santika, S. P., Saputra, M. A., Zahra, A., & Suhartono, D. (2025). Online Gambling Promotion Detection in Indonesian YouTube Comments Using Semi-Supervised IndoBERT Classification. *Procedia Computer Science, 269*, 1269–1278. https://doi.org/10.1016/j.procs.2025.09.068

---
