# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| Assyifa Dwi Safitri | 103072400064 | [pitfall/bagian yang dikerjakan] |
| Amirah Essary Yunsarah Sujuthi | 103072400077 | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: The network is reliable — ditulis oleh Amirah Essary Yunsarah Sujuthi

**Bukti di skenario:** Tim menemukan bahwa kode mereka menulis asumsi seperti "# network is always reliable, no need for retry" dan tidak ada timeout sama sekali pada pemanggilan antar service. Modul pesanan memanggil modul pembayaran dan menunggu respons tanpa batas waktu.

**Kenapa ini keliru:** Menganggap jaringan selalu reliable merupakan asumsi yang keliru dan tidak sesuai dengan kondisi sistem terdistribusi nyata. Komunikasi antar service dapat mengalami berbagai gangguan, seperti keterlambatan respons, koneksi gagal, atau service tujuan yang sedang mengalami masalah. Pada kasus FoodGo, tidak adanya timeout dan retry membuat sistem tidak memiliki mekanisme untuk menangani gangguan komunikasi antar service.

**Dampak ke FoodGo:** Tidak adanya timeout dan retry membuat modul pesanan terus menunggu respons dari modul pembayaran ketika terjadi keterlambatan. Saat trafik meningkat, banyak permintaan yang tertahan sehingga proses pemesanan menjadi semakin lambat. Akibatnya, performa aplikasi menurun dan dapat menyebabkan sistem mengalami crash.

**Solusi desain awal:** FoodGo dapat menerapkan timeout pada komunikasi antar service agar proses tidak menunggu tanpa batas waktu. Selain itu, retry dengan batas percobaan tertentu dapat digunakan untuk menangani gangguan sementara. Jika modul pembayaran terus mengalami masalah, circuit breaker dapat digunakan untuk membatasi dampak agar tidak menyebar ke service lain.

**Trade-off:** Retry dapat membantu mengatasi gangguan sementara, tetapi jika service sedang mengalami overload, percobaan ulang dapat menambah beban dan memperparah kondisi sistem.

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:**
**Kenapa ini keliru:**
**Dampak ke FoodGo:**
**Solusi desain awal:**
**Trade-off:** 

## Pitfall 3: Single Point of Failure akibat Arsitektur Monolitik — ditulis oleh Assyifa & Amirah

**Bukti di skenario:**
**Kenapa ini keliru:**
**Dampak ke FoodGo:**
**Solusi desain awal:**
**Trade-off:** 

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
