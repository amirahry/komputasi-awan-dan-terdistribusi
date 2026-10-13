# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4:
  - Pada TODO 1, kendala yang ditemukan adalah mengatur penerimaan pesan antar node seperti **ELECTION**, **OK**, dan **COORDINATOR** agar setiap node dapat merespons sesuai aturan Bully Algorithm.
  - Pada TODO 2, kendala yang ditemukan adalah mengatur proses election agar hanya mengirim pesan ke node dengan ID lebih tinggi dan menunggu respons **OK** sebelum menentukan leader.
  - Pada TODO 3, kendala yang ditemukan adalah memastikan pesan **COORDINATOR** dikirim ke seluruh node setelah leader baru terpilih agar semua node memiliki informasi leader yang sama.
  - Pada TODO 4, kendala yang ditemukan adalah membuat mekanisme pengecekan ketika leader berhenti merespons sehingga node lain dapat menjalankan election ulang.
  - Setelah dilakukan perbaikan, proses pemilihan leader berhasil berjalan sesuai aturan Bully Algorithm.

## Skenario 1: Start normal
- Leader yang terpilih: **Node 5**
- Log/observasi:
  - Seluruh node (Node 1 sampai Node 5) dijalankan hampir bersamaan.
  - Node dengan ID lebih rendah mengirim pesan **ELECTION** kepada node dengan ID lebih tinggi.
  - Node yang memiliki ID lebih tinggi memberikan respons **OK**.
  - Node 5 menjadi leader karena memiliki ID tertinggi dan tidak terdapat node lain dengan prioritas lebih tinggi.
  - Node 5 mengirim pesan **COORDINATOR** kepada seluruh node untuk mengumumkan dirinya sebagai leader.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: **Node 4**
- Berapa lama waktu sampai leader baru terdeteksi:
  - Sekitar **5 detik** setelah Node 5 dimatikan.
- Log/observasi:
  - Node 5 sebagai leader dihentikan menggunakan **CTRL + C**.
  - Node lain mendeteksi bahwa leader tidak merespons.
  - Proses election dijalankan kembali oleh node yang masih aktif.
  - Node 4 terpilih sebagai leader baru karena memiliki ID tertinggi dari node yang masih hidup.
  - Node 4 mengirim pesan **COORDINATOR** kepada node lain sebagai pemberitahuan leader baru.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 13 Oktober 2026 | ChatGPT | "Saya sedang mengerjakan tugas implementasi Bully Algorithm. Jelaskan konsep kerja Bully Algorithm, alur pesan ELECTION, OK, dan COORDINATOR, serta hal-hal yang perlu diperhatikan dalam proses implementasi." | Memberikan penjelasan mengenai konsep leader election, mekanisme pemilihan berdasarkan ID node, dan alur komunikasi antar node. | Digunakan sebagai pemahaman awal mengenai konsep algoritma. Implementasi program tetap disesuaikan dengan skeleton kode yang diberikan pada tugas. |
| 13 Oktober 2026 | ChatGPT | "Saya mengalami kendala pada simulasi 5 node Bully Algorithm. Bantu identifikasi kemungkinan penyebab proses election tidak berjalan sesuai aturan dan apa yang perlu dicek." | Memberikan saran pengecekan alur komunikasi socket, proses election, penerimaan pesan, dan mekanisme pendeteksian leader. | Saran digunakan sebagai bahan evaluasi dan debugging. Perbaikan dilakukan sendiri dengan menyesuaikan kode yang sudah tersedia. |
| 13 Oktober 2026 | ChatGPT | "Bantu berikan outline dokumentasi README dan jurnal proses untuk tugas Bully Algorithm agar mencakup implementasi, alasan pemilihan leader, kelemahan algoritma, dan hasil pengujian." | Memberikan struktur penulisan dokumentasi seperti deskripsi sistem, implementasi algoritma, skenario pengujian, dan kesimpulan. | Outline digunakan sebagai panduan penyusunan laporan. Isi akhir dibuat berdasarkan hasil implementasi dan pengujian yang dilakukan. |
| 13 Oktober 2026 | ChatGPT | "Bantu cek apakah hasil log simulasi Bully Algorithm sudah sesuai dengan aturan bahwa node dengan ID tertinggi yang masih hidup menjadi leader." | Memberikan arahan untuk membandingkan hasil log dengan aturan Bully Algorithm. | Digunakan untuk validasi hasil pengujian dan memastikan dokumentasi sesuai dengan hasil simulasi. |