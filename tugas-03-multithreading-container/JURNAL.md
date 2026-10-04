# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 

Percobaan awal dilakukan dengan menjalankan program multithreading tanpa menggunakan mekanisme lock pada variabel bersama processed_count. Hasil yang diperoleh :

```text
Total pesanan diproses: 36 (seharusnya 100)
RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!
```

- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): 

Pada percobaan tanpa lock, proses penambahan nilai processed_count dilakukan tanpa perlindungan terhadap akses bersamaan antar thread. Implementasi percobaan tanpa lock dilakukan dengan 

```python
temp = processed_count
time.sleep(0.01)
processed_count = temp + 1
```
Pada proses tersebut, thread membaca nilai processed_count menyimpannya sementara pada temp, lalu melakukan penambahan nilai. time.sleep(0.01) digunakan untuk memperbesar kemungkinan terjadinya konflik antar thread agar race condition lebih mudah diamati. 

Ketika beberapa thread mengakses processed_count secara bersamaan, beberapa thread dapat membaca nilai lama yang sama sehingga perubahan nilai dapat tertimpa. Akibatnya, sebagian proses increment tidak tercatat dan hasil akhir processed_count menjadi kurang dari jumlah pesanan sebenarnya serta dapat berbeda setiap kali program dijalankan.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 

Setelah dilakukan perbaikan menggunakan threading.Lock(), hasil yang diperoleh:

```text
Total pesanan diproses: 100 (seharusnya 100)
```
Penggunaan 'Lock' dilakukan untuk melindungi akses terhadap variabel bersama (`processed_count`) agar perubahan data tidak dilakukan secara bersamaan oleh beberapa thread. Implementasi dilakukan dengan 

```python
with lock:
    processed_count += 1
```
Kode tersebut digunakan untuk mengunci proses perubahan nilai processed_count atau membuat bagian increment menjadi area kritis (critical section). Ketika satu thread sedang menjalankan proses increment, thread lain harus menunggu sampai proses tersebut selesai. Dengan cara ini, perubahan nilai tidak dilakukan secara bersamaan sehingga data tidak saling tertimpa.

Dengan lock membuat setiap proses penambahan tercatat dengan benar, sehingga race condition dapat dicegah dan hasil akhir tetap sesuai dengan jumlah pesanan yang diproses.

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: 

Pada tahap awal, Docker Desktop belum dapat menjalankan container karena Doctor Engine belum aktif. Error awal yang muncul adalah:

```bash
Virtualization support not detected
```

Permasalahan tersebut terjadi karena fitur virtualisasi pada laptop belum terdeteksi oleh Docker Desktop. Setelah dilakukan pengecekan, virtualisasi CPU masih perlu diaktifkan melalui BIOS.

Perbaikan dilakukan dengan:
1. Mengaktifkan fitur virtualisasi pada BIOS
2. Menginstall dan mengaktifkan Windows Subsystem for Linux (WSL 2).
3. Mengatur Docker Desktop agar menggunakan WSL 2 sebagai backend untuk menjalankan Linux container.

Setelah konfigurasi berhasil, Docker Desktop dapat menjalankan Docker Engine.

Pada proses berikutnya, dilakukan pengujian build image menggunakan:

```bash
docker build -t foodgo-order-sim .
```

dan menjalankan container dengan:
```bash
docker run --rm foodgo-order-sim
```

Hasil pengujian:

```text
Total pesanan diproses: 100 (seharusnya 100)
```
Program berhasil berjalan di dalam Docker container dengan lingkungan Linux dan menghasilkan output yang sesuai.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 30 September 2026 | ChatGPT | Membantu memahami tugas, multithreading, race condition, dan Lock. | Menjelaskan konsep dan alur pengerjaan tugas. | Digunakan sebagai referensi pemahaman konsep sebelum implementasi kode dan pengujian mandiri. |
| 30 September 2026 | ChatGPT | Membantu proses instalasi Docker Desktop, konfigurasi WSL 2 Linux, dan mengatasi kendala saat menjalankan Docker. | Memberikan panduan instalasi Docker, mengaktifkan WSL 2, menjalankan Ubuntu Linux, mengecek konfigurasi Docker Engine, serta troubleshooting saat Docker belum dapat digunakan. | Langkah-langkah tersebut diterapkan langsung pada perangkat hingga lingkungan Linux melalui WSL 2 dan Docker berhasil berjalan untuk menjalankan container project. |