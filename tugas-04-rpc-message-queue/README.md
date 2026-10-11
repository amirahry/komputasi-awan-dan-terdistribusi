# Tugas 4 — Komunikasi Antar Komponen

## Implementasi

Pada sistem FoodGo terdapat modul Pembayaran dan modul Pesanan/Kurir yang harus berkomunikasi secara reliabel. Kelompok kami mengimplementasikan dua metode komunikasi:

1. **Remote Procedure Call (RPC)** sebagai komunikasi sinkron.
2. **Message Queue (MQ) menggunakan RabbitMQ** sebagai komunikasi asinkron.

RPC digunakan untuk proses yang membutuhkan respons langsung seperti pengecekan saldo dan pembayaran. Message Queue digunakan untuk proses yang tidak membutuhkan respons langsung seperti pengiriman notifikasi pembayaran berhasil kepada modul Kurir.

---

# Analisis Pemilihan Komunikasi

## Jalur A — RPC (Sinkron)
RPC dipilih untuk proses pengecekan saldo dan pembayaran karena modul Pesanan membutuhkan hasil secara langsung dari modul Pembayaran. Pada RPC, client mengirim request kepada server dan harus menunggu respons sebelum proses dapat dilanjutkan. Berdasarkan hasil pengujian, client berhasil melakukan request ke server dan menerima hasil pembayaran.

Hasil pengujian:
```text
Saldo user1: 50000

Hasil pembayaran:
{'status': 'sukses', 'saldo_akhir': 30000}
```
Hal tersebut menunjukkan bahwa komunikasi sinkron RPC berjalan dengan baik. Apabila server RPC mati saat proses request berlangsung, client tidak akan mendapatkan respons karena RPC tidak memiliki tempat penyimpanan pesan sementara. Request akan gagal dan harus dilakukan kembali ketika server tersedia.

---

## Jalur B — Message Queue (Asinkron)
Message Queue dipilih untuk pengiriman notifikasi pembayaran kepada Kurir karena modul Pembayaran tidak perlu menunggu modul Kurir selesai memproses pesan.

Pada implementasi ini:
- Publisher berperan sebagai modul Pembayaran.
- RabbitMQ berperan sebagai message broker.
- Consumer berperan sebagai modul Kurir.

Publisher mengirim event `pembayaran_berhasil` ke RabbitMQ tanpa menunggu balasan dari consumer. Hasil pengujian normal:

Publisher berhasil mengirim pesan:
```text
Event terkirim:
user1
user2
user3
```
Consumer berhasil menerima pesan:
```text
Kurir menerima notifikasi pembayaran untuk user1 sejumlah 20000
Kurir menerima notifikasi pembayaran untuk user2 sejumlah 40000
Kurir menerima notifikasi pembayaran untuk user3 sejumlah 60000
```
Hal tersebut menunjukkan bahwa komunikasi asinkron menggunakan Message Queue berhasil berjalan.

---

# Pengujian Asynchronous Decoupling (Pesan Tidak Hilang)
Pengujian dilakukan dengan skenario:
1. Consumer dimatikan.
2. Publisher dijalankan untuk mengirim event pembayaran.
3. RabbitMQ Dashboard diperiksa untuk melihat pesan yang tersimpan.
4. Consumer dijalankan kembali untuk memproses pesan.

Hasil pengujian:
Ketika consumer mati, pesan tidak hilang tetapi tersimpan pada queue RabbitMQ `pembayaran_berhasil`. Pada RabbitMQ Dashboard terlihat:

```text
Queue:
pembayaran_berhasil

Ready: 3
Total: 3
```
Hal ini menunjukkan bahwa RabbitMQ menyimpan pesan sementara sampai consumer tersedia kembali. Setelah consumer dijalankan kembali, pesan berhasil diproses:

```text
Kurir menerima notifikasi pembayaran untuk user1 sejumlah 20000
Kurir menerima notifikasi pembayaran untuk user2 sejumlah 40000
Kurir menerima notifikasi pembayaran untuk user3 sejumlah 60000
```
Berdasarkan hasil tersebut, Message Queue berhasil menerapkan konsep **asynchronous decoupling**, yaitu pengirim dan penerima pesan tidak harus aktif pada waktu yang sama.

---

# Kesimpulan
RPC dan Message Queue memiliki fungsi yang berbeda. RPC lebih cocok digunakan untuk proses yang membutuhkan respons langsung seperti pengecekan saldo dan transaksi pembayaran. Message Queue lebih cocok digunakan untuk proses asinkron seperti notifikasi pembayaran karena pesan tetap tersimpan ketika consumer tidak tersedia. Jika RPC digunakan untuk notifikasi Kurir, modul Pembayaran dapat ikut terhambat karena harus menunggu respons dari Kurir. Sebaliknya, jika Message Queue digunakan untuk pengecekan saldo, sistem membutuhkan mekanisme tambahan untuk mendapatkan respons langsung sehingga kurang efisien.