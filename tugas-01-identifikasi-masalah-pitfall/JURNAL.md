# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## Rabu, 16 September 2026
- Peserta: Assyifa Dwi Safitri, Amirah Essary Yunsarah Sujuthi
- Poin diskusi:
  - Membahas masalah utama pada studi kasus FoodGo dan mencari masalah yang berhubungan dengan konsep Fallacies of Distributed Computing.
  - Menentukan tiga masalah utama, yaitu *The network is realibe*, *Latency is zero*, dan *Single Point of Failure* akibat arsitektur monolitik.
  - Membedakan fokus pembahasan *The network is reliable* dan *Latency is zero*.
  - Menentukan solusi awal seperti *timeout, retry, circuit breaker*, dan pemisahan service.
- Perbedaan pendapat:
  - Sempat mempertimbangkan *Bandwidth is infinite*, tetapi kami memilih *Latency is zero* karena lebih sesuai dengan skenario modul pesanan yang menunggu respons pembayaran.
    

## [Tanggal diskusi 2]
- ...

## Review Silang
- Assyifa mengomentari analisis Amirah:
  - Memberikan masukan agar pembahasan *The network is reliable* lebih fokus pada masalah kegagalan komunikasi antar *service* dan tidak terlalu berfokus pada dampak sistem lambat.
  - Menyarankan agar solusi *retry* diberikan batas percobaan agar tidak memperparah kondisi ketika service mengalami gangguan.
- Amirah mengomentari analisis Assyifa:
  - Memberikan masukan agar pembahasan *Latency is zero* dibedakan dari *The network is reliable* dengan menekankan keterlambatan waktu komunikasi antar *service*.
  - Menyarankan agar dampak latency dikaitkan dengan kondisi ketika trafik meningkat dan banyak permintaan yang menunggu.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah menjadi tulisan sendiri |
|---|---|---|---|---|
| 16 September 2026 | ChatGPT | Kami sedang menganalisis studi kasus FoodGo tentang sistem terdistribusi yang mengalami masalah seperti aplikasi lambat, server *crash*, dan komunikasi antar *service* tanpa *timeout*. Bantu jelaskan beberapa pitfall yang mungkin berkaitan dengan kasus tersebut, seperti *The network is reliable*, *Latency is zero*, dan *Bandwidth is infinite*, serta bantu memahami perbedaan konsepnya untuk menentukan pitfall yang paling sesuai. | Menjelaskan hubungan antara gejala pada studi kasus dengan beberapa pitfall sistem terdistribusi dan membantu membandingkan konsep *The network is reliable*, *Latency is zero*, dan *Bandwidth is infinite*. | Kelompok menggunakan penjelasan tersebut sebagai bahan diskusi awal, kemudian menentukan pitfall yang paling sesuai berdasarkan pemahaman kelompok terhadap studi kasus FoodGo dan menyusun analisis secara mandiri. |
