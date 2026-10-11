# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- **Keduanya (RPC dan Message Queue/MQ).**
Kelompok kami memilih kedua jalur untuk memahami perbedaan komunikasi sinkron dan asinkron pada sistem FoodGo.

- **Jalur A — RPC (Sinkron):**  
Dipilih karena modul Pesanan membutuhkan respons langsung dari modul Pembayaran untuk mengecek saldo dan memastikan transaksi berhasil atau gagal.
- **Jalur B — Message Queue (Asinkron):**  
Dipilih karena pengiriman notifikasi pembayaran kepada modul Kurir tidak membutuhkan respons langsung. Pesan dapat disimpan dalam antrean RabbitMQ meskipun modul Kurir sedang tidak aktif.

RPC cocok untuk proses yang membutuhkan hasil langsung, sedangkan Message Queue cocok untuk proses yang tidak harus menunggu respons penerima.

---

## Kendala teknis
- Pada Jalur A (RPC), server dan client berhasil dijalankan tanpa error. Pengujian dilakukan dengan saldo awal user1 sebesar Rp50.000, pembayaran sebesar Rp20.000, dan menghasilkan saldo akhir Rp30.000 dengan status transaksi sukses.
- Pada Jalur B (Message Queue), terdapat kendala awal saat setup RabbitMQ menggunakan Docker karena image `rabbitmq:3-management` harus diunduh terlebih dahulu sehingga proses setup membutuhkan waktu lebih lama. Setelah proses download selesai, container RabbitMQ berhasil berjalan. Koneksi antara publisher, RabbitMQ sebagai message broker, dan consumer berhasil dilakukan menggunakan library `pika`.

    Hasil pengujian normal:
    - Publisher berhasil mengirim event pembayaran ke queue `pembayaran_berhasil`.
    - RabbitMQ berhasil menerima dan menyimpan pesan.
    - Consumer berhasil mengambil serta memproses notifikasi pembayaran.

---

## Uji "pesan tidak hilang" (khusus Jalur B)
### Langkah uji

1. Consumer dimatikan terlebih dahulu.
2. Publisher dijalankan untuk mengirim event pembayaran.
3. RabbitMQ Dashboard diperiksa untuk melihat pesan yang tersimpan.
4. Consumer dijalankan kembali untuk memproses pesan.

### Hasil yang diamati
Ketika consumer dimatikan, publisher tetap berhasil mengirim event pembayaran ke RabbitMQ. Pesan tidak hilang, tetapi tersimpan sementara pada queue:

```text
pembayaran_berhasil
```

Pada RabbitMQ Dashboard terlihat:

```text
Queue:
pembayaran_berhasil

Ready: 3
Total: 3
```

Hal tersebut menunjukkan bahwa RabbitMQ menyimpan pesan hingga consumer tersedia kembali. Setelah consumer dijalankan kembali, pesan berhasil diproses:

```text
Kurir menerima notifikasi pembayaran untuk user1 sejumlah 20000
Kurir menerima notifikasi pembayaran untuk user2 sejumlah 40000
Kurir menerima notifikasi pembayaran untuk user3 sejumlah 60000
```

Hasil pengujian membuktikan bahwa Message Queue menerapkan konsep **asynchronous decoupling**, yaitu publisher dan consumer tidak harus aktif pada waktu yang sama.

---

## Analisis Kondisi Kegagalan Komunikasi
### RPC Jika Server Mati

Pada RPC, client mengirim request langsung kepada server dan harus menunggu respons. Jika server mati saat proses request berlangsung, client tidak mendapatkan balasan sehingga komunikasi gagal. Request tidak tersimpan otomatis karena RPC tidak memiliki antrean pesan seperti Message Queue.

### Message Queue Jika Consumer Mati

Pada Message Queue, pesan dari publisher terlebih dahulu disimpan oleh RabbitMQ. Berdasarkan hasil pengujian, ketika consumer mati pesan tetap tersimpan pada queue `pembayaran_berhasil` dengan status `Ready: 3`. Setelah consumer aktif kembali, pesan berhasil diproses oleh modul Kurir.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah menjadi tulisan/kode sendiri |
|---|---|---|---|---|
| 11 Oktober 2026 | ChatGPT | Membantu memahami konsep RPC dan Message Queue pada Tugas 4 | Menjelaskan perbedaan komunikasi sinkron dan asinkron serta membantu memahami alur pengujian | Penjelasan digunakan sebagai referensi memahami konsep. Implementasi kode, pengujian program, dan hasil percobaan dilakukan secara mandiri |
| 11 Oktober 2026 | ChatGPT | Membantu mengecek hasil pengujian RPC, RabbitMQ, publisher, dan consumer | Membantu memahami hasil terminal dan konsep asynchronous decoupling | Hasil jurnal disusun berdasarkan percobaan langsung menggunakan RPC dan RabbitMQ |