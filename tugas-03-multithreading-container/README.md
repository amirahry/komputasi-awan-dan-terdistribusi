# Tugas 3 (Pekan 3) — Efisiensi Proses & Kontainer

**Materi terkait:** Threading, Virtualization, Containers.

## Studi Kasus

Server FoodGo boros sumber daya karena setiap permintaan pesanan masuk diproses sebagai **proses baru yang berat** (mis. `fork()` proses OS penuh per request). Saat 100 pesanan masuk bersamaan, server kehabisan memori karena tiap proses membawa overhead-nya sendiri.

## Tugas Kelompok

1. Implementasikan **simulasi pesanan masuk** di Python (`src/order_simulator.py`) yang memproses banyak pesanan **secara konkuren memakai multithreading** (bukan multiprocessing, bukan sekuensial biasa).
2. Program harus mensimulasikan **race condition yang sengaja dibuat lalu diperbaiki** — buktikan pemahaman kalian tentang `Lock`/sinkronisasi dengan cara:
   - Jalankan dulu versi TANPA lock, tunjukkan hasil counter yang salah (screenshot/log).
   - Perbaiki dengan `threading.Lock()`, tunjukkan hasil counter yang benar.
   - Tulis perbandingan ini di `JURNAL.md`.
3. Paketkan program ke dalam **Docker container** (`Dockerfile` disediakan skeleton-nya, lengkapi bagian yang kosong).
4. Jalankan container di laptop, buktikan program tetap berjalan benar di dalam container (screenshot/video di `bukti/`).

## Skeleton yang Disediakan

- `src/order_simulator.py` — kerangka program dengan `# TODO` di bagian logika inti (worker function, penggunaan lock, agregasi hasil). **Kalian wajib mengisi bagian TODO sendiri** — ini bagian penilaian utama.
- `requirements.txt` — kosong/minimal (program ini sengaja hanya pakai standard library Python, tidak perlu dependency eksternal).
- `Dockerfile` — kerangka dengan beberapa baris `# TODO`, lengkapi agar image bisa di-build dan dijalankan.

## Cara Menjalankan (Setelah Skeleton Dilengkapi)

Tanpa Docker (langsung di laptop, untuk debugging cepat):
```bash
cd tugas-03-multithreading-container
python3 src/order_simulator.py
```

Dengan Docker (wajib untuk submission akhir):
```bash
cd tugas-03-multithreading-container
docker build -t foodgo-order-sim .
docker run --rm foodgo-order-sim
```

## Analisis Implementasi

### 1. Analisis Permasalahan pada Studi Kasus

Permasalahan utama pada server FoodGo adalah penggunaan proses OS baru untuk setiap request pesanan. Jika setiap pesanan diproses dengan membuat proses baru, misalnya menggunakan 'fork()', maka ketika banyak pesanan masuk secara bersamaan server harus membuat banyak proses terpisah.

Pada kondisi 100 pesanan yang masuk secara bersamaan, pendekatan tersebut dapat menyebabkan penggunaan resource meningkat karena setiap proses memiliki ruang alamat memori, struktur proses, dan resource prosesnya sendiri. Semakin banyak proses yang dibuat, semakin besar pula overhead yang harus ditangani oleh sistem operasi.

Permasalahan ini tidak hanya berkaitan dengan jumlah pekerjaan yang harus diproses, tetapi juga bagaimana cara pekerjaan tersebut dieksekusi. Jika setiap request selalu menghasilkan proses OS baru, maka server harus melakukan pembuatan, penjadwalan, pengelolaan, dan penghentian banyak proses.

Oleh karena itu, pada tugas digunakan pendekatan multitreading untuk mensimulasikan cara pemrosesan banyak pesanan secara konkuren dengan overhead yang lebih ringan dibandingkan dengan membuat satu proses OS penuh untuk setiap request.

### 2. Analisis Implementasi Multithreading

Pada simulasi FoodGo terdapat 100 pesanan yang harus diproses dengan 10 worker thread.

Konfigurasi program menggunakan:

```python
NUM_ORDERS = 100
NUM_WORKERS = 10
```

Artinya, setiap 100 pesanan dibagi kepada 10 worker sehingga setiap worker memperoleh bagian pekerjaan untuk diproses. Konfigurasi 100 pesanan dan 10 worker tersebut memang telah ditentukan pada skeleton program. Setiap thread menjalankan fungsi `worker()` yang kemudian memanggil `process_order()` untuk setiap pesanan.

Secara sederhana, struktur eksekusinya dapat digambarkan sebagai:

```text
1 Process Python
│
├── Thread Worker 1
├── Thread Worker 2
├── Thread Worker 3
├── ...
└── Thread Worker 10
```

Thread dibuat menggunakan `threading.Thread`, kemudian seluruh thread dijalankan menggunakan `start()`. Setelah seluruh worker dijalankan, program menggunakan `join()` untuk menunggu sampai semua thread selesai sebelum menampilkan nilai akhir `processed_count`. Skeleton meminta pembagian `order_ids`, pembuatan thread, menjalankan seluruh thread, dan kemudian melakukan `join()` sebelum hasil akhir ditampilkan.

Dengan mekanisme tersebut, program tidak memproses seluruh pesanan satu per satu secara sekuensial. Beberapa worker dapat aktif dalam waktu yang sama dan melakukan pekerjaan secara konkuren.

Penggunaan `time.sleep()` pada fungsi pemrosesan bukan penyebab utama program menjadi konkuren. Konkurensi terjadi karena worker benar-benar dijalankan sebagai beberapa thread dengan `threading.Thread()`. Pada skeleton, `time.sleep()` digunakan untuk mensimulasikan pekerjaan seperti validasi atau perhitungan pesanan.

## Struktur Submission

```
tugas-03-multithreading-container/
├── README.md          # Analisis: race condition, perbaikan, kenapa threading (bukan multiprocessing/proses OS)
├── JURNAL.md           # Log sebelum/sesudah lock, error yang ditemui saat build Docker
├── Dockerfile
├── requirements.txt
├── src/
│   └── order_simulator.py
└── bukti/              # Screenshot/video: hasil counter salah (tanpa lock), hasil benar (dengan lock), container jalan
```

## Rubrik Penilaian (Tugas 3)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi multithreading benar | 30% | Worker benar-benar konkuren (bukan `time.sleep` yang menyamarkan sekuensial), pakai `threading` |
| Bukti race condition & perbaikan lock | 25% | Ada bukti nyata (log/screenshot) sebelum & sesudah, bukan cuma klaim di teks |
| Dockerfile & eksekusi container | 20% | Image ter-build, container jalan dan hasilkan output yang sama seperti tanpa Docker |
| Analisis (kenapa threading, bukan proses berat) | 15% | Mengaitkan balik ke masalah "server boros resource" di studi kasus |
| Proses & kontribusi kelompok | 10% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI soal opsi umum menangani race condition (mis. "apa saja cara sinkronisasi thread di Python"); **tidak boleh** meminta AI menuliskan isi bagian `# TODO` di `order_simulator.py`/`Dockerfile`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Bagian `# TODO` di `order_simulator.py` dan `Dockerfile` sengaja dikosongkan — solusi yang identik persis antar kelompok (termasuk nama variabel, komentar) akan diperiksa lebih lanjut.
- `JURNAL.md` wajib menunjukkan bukti nyata percobaan **sebelum** (race condition muncul) dan **sesudah** (`Lock()` dipasang) — bukan cuma klaim tanpa data pembanding.
