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

Oleh karena itu, pada tugas ini digunakan pendekatan multitreading untuk mensimulasikan cara pemrosesan banyak pesanan secara konkuren dengan overhead yang lebih ringan dibandingkan dengan membuat satu proses OS penuh untuk setiap request.

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

### 3. Analisis Perbandingan Threading dan Proses OS

Pada pendekatan awal FoodGo, setiap request dapat digambarkan sebagai:

```text
Request 1 -> Process 1
Request 2 -> Process 2
Request 3 -> Process 3
...
Request 100 -> Process 100
```

Jika pendekatan tersebut digunakan, setiap request membutuhkan proses OS yang berbeda. Proses memiliki ruang alamat memori sendiri serta resource yang dikelola secara terpisah oleh sistem operasi. Pembuatan proses yang banyak secara sekaligus dapat menghasilkan overhead yang lebih besar karena sistem operasi harus mengelola setiap proses secara independen.

Pada solusi multithreading, strukturnya menjadi:

```text
1 Process Python
       │
       ├── Thread 1
       ├── Thread 2
       ├── Thread 3
       ├── ...
       └── Thread 10
```

Struktur diatas menunjukkan beberapa thread yang berada di dalam satu proses dan berbagi ruang alamat memori serta resource proses yang sama. Karena hal tersebut, thread tidak memerlukan pembuatan satu proses OS baru untuk setiap pesanan.

Pada simulasi FoodGo, pendekatan ini lebih sesuai karena masalah awal yang ingin dikurangi adalah overhead akibat terlalu banyak proses OS. Selain itu, simulasi pemrosesan pesanan menyerupai pekerjaan yang memiliki waktu tunggu, seperti validasi data, komunikasi jaringan, penyimpanan data, atau aktivitas I/O lainnya. Untuk jenis pekerjaan seperti ini, multithreading dapat digunakan agar ketika satu thread sedang menunggu, thread lain tetap dapat melanjutkan pekerjaan. Penggunaan multiprocessing sebenarnya dapat memberikan paralelisme dengan proses terpisah, tetapi pendekatan tersebut tidak sesuai dengan tujuan studi kasus yaitu mengurangi ketergantungan terhadap banyak proses OS yang berat.

### 4. Analisis Race Condition

Pada simulasi FoodGo, penggunaan multithreading menimbulkan konsekuensi karena beberapa thread berada dalam proses yang sama dan dapat mengakses data bersama.

Pada program terdapat variabel:

```python
processed_count = 0
```

Variabel tersebut digunakan untuk menghitung jumlah pesanan yang telah selesai diproses. Karena semua thread menggunakan variabel yang sama, `processed_count()` merupakan shared data. Skeleton program juga menjelaskan bahwa counter tersebut sengaja dibuat rawan race condition jika diakses tanpa proteksi.

Pada percobaan tanpa `Lock`, digunakan mekanisme seperti:

```pyhton
temp = processed_count
time.sleep(0.01)
processed_count = temp + 1
```

Hasil pengujian menunjukkan:

```text
Total Pesanan diproses: 36 (seharusnya 100)
```

Nilai tersebut lebih kecil dari 100 karena beberapa thread dapat membaca nilai `processed_count` yang sama sebelum thread lain selesai memperbarui nilainya.

Contohnya:

```text
Nilai awal processed_count = 10

Thread A membaca nilai 10
Thread B membaca nilai 10

Thread A menghitung 10 + 1 = 11
Thread B menghitung 10 + 1 = 11

Thread A menyimpan 11
Thread B juga menyimpan 11
```

Secara logika, dua operasi increment seharusnya menghasilkan nilai 12. Namun karena kedua thread menggunakan nilai awal yang sama, salah satu hasil increment menjadi hilang dan nilai akhirnya hanya 11. Kondisi itu disebut sebagai **race coondition**, yaitu kondisi ketika hasil program dipengaruhi oleh urutan atau waktu eksekusi beberapa thread yang mengakses shared data secara bersamaan.

Pengguanan:

```python
time.sleep(0.01)
```

pada percobaan tanpa lock, variabel diatas digunakan untuk memperbesar jendela waktu terjadinya konflik sehingga race condition lebih mudah diamati. Hasil race condition juga tidak harus selalu menghasilkan angka 36. Ketika program dijalankan kembali, hasilnya dapat berubah karena urutan penjadwalan thread tidak selalu sama pada setiap eksekusi.

### 5. Analisis Perbaikan Race Condition Menggunakan Lock

Race condition diperbaiki menggunakan objek:

```pyhton
lock = threading.lock()
```

Kemudian bagian yang melakukan perubahan terhadap `processed_count` dilindungi menggunakan:

```pyhton
with lock:
   processed_count += 1
```

Bagian tersebut merupakan **critical section**, yaitu bagian kode yang mengakses atau mengubah shared data dan tidak boleh dieksekusi oleh beberapa thread secara bersamaan. 

Ketika satu thread memperoleh lock, thread tersebut dapat melakukan perubahan terhadap `processed_count`. Thread lain yang ingin memasuki critical section harus menunggu sampai lock dilepaskan.

Alurnya dapat digambarkan sebagai:

```text
Thread A
   │
   ├── memperoleh Lock
   │
   ├── processed_count += 1
   │
   └── melepas Lock
            │
            ↓
       Thread B dapat masuk
```

Setelah menggunakan `Lock`, hasil pengujian menjadi:

```text
Total pesanan diproses: 100 (seharusnya 100)
```

Hasil tersebut menunjukkan bahwa seluruh operasi increment berhasil tercatat tanpa saling menimpa. Skeleton juga secara langsung meminta dua tahap pengujian, yaitu menjalankan increment tanpa lock terlebih dahulu dan kemudian membungkus increment menggunakan `with_lock` untuk membandingkan hasil kedua kondisi tersebut.

Dengan begitu, `Lock` berfungsi sebagai mekanisme sinkronisasi yang memastikan hanya satu thread yang dapat melakukan perubahan terhadap counter pada satu waktu.

### 6. Analisis Perbandingan Hasil Tanpa Lock dan Dengan Lock

Hasil kedua percobaan menunjukkan perbedaan yang jelas antara program tanpa sinkronisasi dan program yang menggunakann sinkronisasi.

| Kondisi | Hasil Pengujian | Analisis |
|---|---|---|
| Tanpa Lock | `36 dari 100` | Beberapa thread membaca dan memperbarui shared data secara bersamaan sehingga sebagian increment hilang |
|Dengan Lock | `100 dari 100` | Critical section dilindungi sehingga hanya satu thread yang dapat mengubah counter pada satu waktu |
| Urutan penyelesaian orer | Tidak selalu sama | Thread tetap berjalan secara konkuren dan urutan eksekusinya ditentukan oleh scheduler |

Percobaan tanpa lock menunjukkan bahwa multithreading tanpa sinkronisasi dapat menghasilkan data yang tidak konsisten.

Sebaliknya, penggunaan lock membuat nilai akhir counter konsisten dengan jumlah pesanan yang sebenarnya diproses. Walaupun nilai akhir setelah menggunakan lock menjadi 100, urutan pesanan yang selesai tetap tidak harus sama.

Dengan demikian, penggunaan Lock tidak menghilangkan sifat konkuren dari program. Thread tetap dapat bekerja secara bersamaan, sedangkan Lock hanya membatasi akses pada critical section yang mengubah shared data agar tidak terjadi race condition.

### 7. Analisis Penggunaan Docker Container

Setelah program multithreading berhasil dijalankan secara langsung pada laptop, program kemudian dikemas menggunakan Docker.

Dockerfile digunakan untuk menentukan environment tempat program dijalankan, seperti base image Python, working directory, file program yang disalin, dan command yang dijalankan ketika container dimulai.

Program ini hanya menggunakan Python standard library, yaitu `threading`, `random`, dan `time`, sehingga tidak membutuhkan depedency eksternal tambahan. FIle `requirements.txt` tetap disertakan dalam struktur prokect, tetapi tidak berisi package yang perlu di-install.

Dockerfile kemudian menyalin source code program ke dalam container dan menjalankan `src/order_simulator.py` menggunakan Python ketika container dimulai.

Proses build dilakukan menggunakan:

```bash
docker build -t foodgo-order-sim .
```

Perintah tersebut membuat Docker image berdasarkan konfigurasi pada Dockerfile. Setelah image berhasil dibuat, container dijalankan menggunakan:

```bash
docker run --rm foodgo-order-sim
```

Pada versi final program yang telah menggunakan Lock, hasil di dalam container adalah:

```text
Total pesanan diproses: 100 (seharusnya 100)
```

Hasil tersebut menunjukkan bahwa program tetap dapat berjalan dengan benar ketika dipindahkan dari environment laptop langsung ke environment container.

Docker membantu menyediakan environment yang lebih konsisten karena versi Python dan struktur aplikasi dapat ditentukan melalui Dockerfile. Dengan demikian, komputer lain yang memiliki Docker tidak harus menggunakan konfigurasi Python lokal yang sama persis dengan komputer pengembang. Program akan menggunakan environment yang telah ditentukan dalam image.

### 8. Analisis Hubungan Docker dengan Multithreading dan Race Condition

Docker dan multithreading menyelesaikan permasalahan yang berbeda. Multithreading digunakan untuk mengatur cara program menjalankan beberapa pekerjaan secara konkuren, dimana mekanisme Lock diterapkan guna menjaga konsistensi shared data ketika beberapa thread melakukan akses terhadap resource yang sama. Sementara itu, Docker digunakan untuk menyediakan environment eksekusi program yang lebih konsisten dan terisolasi.

Penggunaan Docker tidak menghilangkan race condition. Jika versi program tanpa Lock dijalankan di dalam container, beberapa thread tetap dapat mengakses `processed_count` secara bersamaan dan race condition tetap dapat terjadi. Selain itu, Docker tidak menjamin hasil container tanpa lock akan sama setiap kali program dijalankan.

```text
Run 1 -> 36 dari 100
Run 2 -> 29 dari 100
Run 3 -> 42 dari 100
```

Nilai tersebut hanya contoh karena hasil aktual bergantung pada bagaimana thread dijadwalkan ketika program berjalan. Hal yang sama dapat terjadi ketika program dijalankan pada laptop yang berbeda. Docker membuat environment aplikasi lebih konsisten, tetapi kondisi resource dan penjadwalan thread pada host dapat tetap berbeda. Setelah menggunakan Lock, nilai akhir counter menjadi konsisten:

```text
Total pesanan diproses: 100 (seharusnya 100)
```

Namun urutan pesanan yang selesai masih dapat berbeda. Oleh karena itu, Docker tidak digunakan untuk memperbaiki race condition. Race condition diperbaiki pada level aplikasi menggunakan mekanisme sinkronisasi seperti `threading_Lock()`.

### 9. Kesimpulan Analsis

Berdasarkan implementasi dan hasil pengujian, permasalahan utama pada studi kasus FoodGo berasal dari penggunaan proses OS baru untuk setiap request. Pendekatan tersebut dapat menghasilkan overhead besar ketika banyak pesanan masuk secara bersamaan karena server harus membuat dan mengelola banyak proses.

Pada tugas ini, solusi yang digunakan adalah membagi 100 pesanan kepada 10 worker thread dalam satu proses Python. Dengan pendekatan tersebut, beberapa pesanan dapat diproses secara konkuren tanpa harus membuat satu proses OS baru untuk setiap request. Penggunaan multithreading memberikan efisiensi resource yang lebih baik untuk skenario simulasi ini karena thread berada dalam proses yang sama dan dapat berbagi resource. Namun, penggunaan shared memory menimbulkan risiko race condition. Hal tersebut dibuktikan melalui percobaan tanpa Lock, ketika hasil `processed_count` hanya mencapai:

```text
36 dari 100
```

Hasil tersebut terjadi karena beberapa thread dapat membaca dan memperbarui nilai counter secara bersamaan sehingga sebagian increment hilang.

Setelah critical section dilindungi menggunakan:

```pyhton
with lock:
   processed_count += 1
```

Nilai akhirnya menjadi:

```text
100 dari 100
```

Hal tersebut membuktikan bahwa `threading.Lock()` dapat digunakan untuk menyinkronkan akses terhadap shared data dan mencegah race condition pada counter. Setelah implementasi multithreading dan sinkronasi berhasil, program dikemas menggunakan Docker container. Program final tetap menghasilkan nilai `processed_count` sebesar 100 ketika dijalankan di dalam container. Dari hasil tersebut dapat disimpulkan bahwa ketiga konsep pada tugas memiliki fungsi yang saling melengkapi.

Secara teknis, multithreading berperan penting dalam meminimalkan kebutuhan pembuatan banyak proses pada OS sekaligus memungkinkan pekerjaan berjalan secara konkuren. Efisiensi ini kemudian didukung oleh mekanisme Lock yang menjaga konsistensi data saat digunakan bersama oleh thread. Terakhir, Docker menyempurnakan ekosistem tersebut dengan menyediakan environment eksekusi yang konsisten serta mempermudah aplikasi untuk dideploy atau dijalankan di berbagai sistem lain tanpa kendala dependensi.

Dengan demikian, implementasi yang dilakukan tidak hanya berhasil memproses seluruh pesanan, tetapi juga menunjukkan hubungan antar efisiensi penggunaan resource, masalah sinkronisasi pada multithreading, dan penggunaan container sebagai environment untuk menjalankan aplikasi.

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
