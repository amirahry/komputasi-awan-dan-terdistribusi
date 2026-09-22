# Jurnal Proses — Tugas 2

## Rabu, 23 September 2026
- Opsi arsitektur yang dipertimbangkan:
  - **Service-Oriented Architecture (SOA)**

      Dipertimbangkan karena pada Tugas 1 ditemukan bahwa FoodGo mengalami masalah akibat arsitektur monolitik. Seluruh model seperti pesanan, pembayaran, katalog resto, dan notifikasi kurir masih saling bergantung sehingga perubahan pada satu modul dapat memengaruhi modul lainnya.
  - **Publish-Subscribe** 
  
      Dipertimbangkan karena proses seperti notifikasi kurir dan pemberitahuan pesanan ke resto tidak selalu membutuhkan respons langsung. Pola ini memungkinkan komunikasi antar service menggunakan event sehingga coupling dapat dikurangi.
  - **Kombinasi SOA + Publish-Subscribe**

    Dipertimbangkan karena SOA dapat menangani pemisahan service utama, sedangkan Publish-Subscribe dapat digunakan untuk komunikasi asynchronous.
    
- Kenapa akhirnya pilih SOA + Pub-Sub:
  - Kelompok memilih **SOA sebagai arsitektur utama dan Publish-Subscribe sebagai pola komunikasi tambahan**.
  - SOA sesuai dengan kebutuhan FoodGo untuk memisahkan modul utama menjadi service yang lebih independen.
  - Publish-Subscribe digunakan untuk proses notifikasi agar service pengirim tidak harus menunggu service penerima selesai memproses.
  - Kombinasi ini dipilih karena dapat mengurangi coupling dan mendukung deployment service secara terpisah.
  
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa):
  
  **Versi 1**
    - Diagram awal hanya menunjukkan pemisahan modul utama FoodGo menjadi beberapa service.
    - Hubungan antar service masih terlihat langsung sehingga konsep asynchronous communication belum terlihat.

  **Versi 2**
  - Menambahkan API Gateway sebagai jalur masuk request dari pelanggan.
  - Menambahkan Message Broker sebagai penghubung event antar service.
  - Mengubah komunikasi notifikasi kurir menjadi pola Publish-Subscribe.
  - Memberikan label komunikasi sinkron dan asynchronous agar alur interaksi antar komponen lebih jelas.
  - Perubahan dilakukan agar desain lebih sesuai dengan tujuan utama yaitu mengurangi coupling antar modul.
    
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 23 September 2026 | ChatGPT | Kami sedang merancang arsitektur FoodGo berdasarkan masalah coupling pada sistem monolitik. Bantu kami mencari pertimbangan penggunaan SOA dan Publish-Subscribe serta komponen umum yang biasanya digunakan. | Memberikan ide mengenai pemisahan service, penggunaan message broker, dan komunikasi asynchronous. | Kelompok menggunakan ide tersebut sebagai bahan diskusi awal, kemudian menentukan rancangan berdasarkan kebutuhan FoodGo. |
| 23 September 2026 | Claude | Kami sudah memilih SOA dan Publish-Subscribe untuk FoodGo. Bantu kami memahami komponen apa saja yang perlu dipertimbangkan dalam rancangan arsitektur serta hubungan antar service yang umum digunakan. | Memberikan masukan mengenai komponen seperti API Gateway dan message Broker serya alasan penggunaannya dalam komunikasi antar service. | Kelompok menyesuaikan masukan tersebut dengan kebutuhan FoodGo dan menentukan sendiri komponen yang digunakan pada rancangan akhir. |
