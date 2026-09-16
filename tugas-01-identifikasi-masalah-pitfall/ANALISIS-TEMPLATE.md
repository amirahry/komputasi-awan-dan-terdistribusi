# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** 6

| Nama | NIM | Kontribusi |
|---|---|---|
| Assyifa Dwi Safitri | 103072400064 | Pitfall 2 (Latency is Zero) dan Pitfall 3 (solusi & trade-off) |
| Amirah Essary Yunsarah Sujuthi | 103072400077 | Pitfall 1 (The network is reliable) dan Pitfall 3 (analisis masalah & dampak) |

## Pitfall 1: The network is reliable — ditulis oleh Amirah Essary Yunsarah Sujuthi

**Bukti di skenario:** Tim menemukan bahwa kode mereka menulis asumsi seperti "# network is always reliable, no need for retry" dan tidak ada timeout sama sekali pada pemanggilan antar service. Modul pesanan memanggil modul pembayaran dan menunggu respons tanpa batas waktu.

**Kenapa ini keliru:** Menganggap jaringan selalu reliable merupakan asumsi yang keliru dan tidak sesuai dengan kondisi sistem terdistribusi nyata. Komunikasi antar service dapat mengalami berbagai gangguan, seperti keterlambatan respons, koneksi gagal, atau service tujuan yang sedang mengalami masalah. Pada kasus FoodGo, tidak adanya timeout dan retry membuat sistem tidak memiliki mekanisme untuk menangani gangguan komunikasi antar service.

**Dampak ke FoodGo:** Tidak adanya timeout dan retry membuat modul pesanan terus menunggu respons dari modul pembayaran ketika terjadi keterlambatan. Saat trafik meningkat, banyak permintaan yang tertahan sehingga proses pemesanan menjadi semakin lambat. Akibatnya, performa aplikasi menurun dan dapat menyebabkan sistem mengalami crash.

**Solusi desain awal:** FoodGo dapat menerapkan timeout pada komunikasi antar service agar proses tidak menunggu tanpa batas waktu. Selain itu, retry dengan batas percobaan tertentu dapat digunakan untuk menangani gangguan sementara. Jika modul pembayaran terus mengalami masalah, circuit breaker dapat digunakan untuk membatasi dampak agar tidak menyebar ke service lain.

**Trade-off:** Retry dapat membantu mengatasi gangguan sementara, tetapi jika service sedang mengalami overload, percobaan ulang dapat menambah beban dan memperparah kondisi sistem.

---

## Pitfall 2: Latency is Zero — ditulis oleh Assyifa Dwi Safitri

**Bukti di skenario:** Modul pesanan memanggil modul pembayaran dan menunggu respons tanpa batas waktu. Selain itu, aplikasi FoodGo menjadi sangat lambat dan beberapa permintaan mengalami timeout ketika terjadi lonjakan pesanan.

**Kenapa ini keliru:** Menganggap latency atau waktu yang dibutuhkan untuk komunikasi antar service tidak menjadi masalah merupakan asumsi yang keliru dalam sistem distribusi. Komunikasi antar service membutuhkan waktu karena harus melalui jaringan, sehingga respons tidak selalu langsung diterima. Waktu respons juga dapat meningkat ketika service sedang mengalami beban yang tinggi. Pada kasus FoodGo, modul pesananan harus menunggu respons dari modul pembayaran, sehingga keterlambatan pada modul pembayaran dapat memengaruhi proses pemesanan.

**Dampak ke FoodGo:** Ketika trafik meningkat, waktu respons modul pembayaran dapat menjadi lebih lama. Sehingga, modul pesanan yang menunggu respons tersebut akan membuat semakin banyak permintaan tertahan. Akibatnya, waktu pemrosesan pesanan menjadi semakin lama, aplikasi terasa lambat, dan beberapa permintaan akhirnya mengalami timeout. Jika permintaan yang tertahan terus bertambah, penggunaan resource server juga dapat meningkat dan berkontribusi terhadap crash.

**Solusi desain awal:** FoodGo dapat menetapkan timeout yang sesuai pada komunikasi antar service agar modul pesanan tidak menunggu respons yang terlalu lama. Selain itu, proses yang tidak harus mendapatkan respons secara langsung dapat menggunakan komunikasi asynchronous atau message queue, sehingga modul pesanan tidak perlu terus menunggu modul lain menyelesaikan prosesnya.

**Trade-off:** Penggunaan komunikasi asynchronous dapat membuat sistem lebih responsif dan mampu menghadapi lonjakan trafik, tetapi hasil dari suatu proses tidak selalu dapat diterima secara langsung oleh pengguna. Sistem juga perlu menangani status sementara, seperti pesanan atau pembayaran yang masih dalam proses.

---

## Pitfall 3: Single Point of Failure akibat Arsitektur Monolitik — ditulis oleh Assyifa & Amirah

**Bukti di skenario:** Saat trafik meningkat, satu server menangani seluruh modul FoodGo seperti pesanan, pembayaran, dan notifikasi kurir. Semua modul tersebut berjalan dalam satu proses monolitik yang sama sehingga server menjadi kewalahan.

**Kenapa ini keliru:** Menggabungkan seluruh fungsi dalam satu server dan satu proses membuat sistem memiliki satu titik kegagalan. Jika server mengalami gangguan atau salah satu modul membutuhkan beban besar, modul lain yang berjalan pada server yang sama dapat ikut terdampak.

**Dampak ke FoodGo:** Ketika jumlah pesanan meningkat, server harus menangani proses pesanan, pembayaran, dan notifikasi secara bersamaan. Kondisi ini menyebabkan sistem sulit menangani lonjakan trafik. Jika server mengalami kegagalan, seluruh layanan FoodGo dapat ikut berhenti dan membutuhkan restart manual.

**Solusi desain awal:** FoodGo dapat memisahkan modul utama menjadi beberapa service agar setiap bagian dapat berjalan secara lebih independen. Selain itu, scalling dapat dilakukan pada service yang membutuhkan kapasitas lebih besar dan load balancing dapat digunakan untuk membagi beban permintaan agar tidak bergantung pada satu server saja.

**Trade-off:** Pemisahan service dapat meningkatkan fleksibilitas sistem dan mengurangi dampak kegagalan pada satu bagian, tetapi membuat arsitektur menjadi lebih kompleks. FoodGo perlu melakukan pengelolaan tambahan seperti monitoring, komunikasi antar service, dan proses deployment.

---

## Kesimpulan Kelompok
Berdasarkan hasil analisis, masalah utama FoodGo disebabkan oleh arsitektur monolitik dan kurangnya mekanisme dalam menangani gangguan komunikasi antar service. Untuk memperbaiki masalah tersebut, FoodGo dapat menerapkan Service-Oriented Architecture (SOA) dengan memisahkan modul pesanan, pembayaran, katalog resto, dan notifikasi menjadi service yang berbeda.

Selain itu, pola Publish-Subscribe dapat digunakan pada proses seperti notifikasi agar antar modul tidak saling bergantung secara langsung. Arsitektur ini dapat membantu FoodGo meningkatkan skalabilitas dan mengurangi dampak kegagalan pada satu bagian sistem, meskipun membutuhkan pengelolaan komunikasi antar service dan monitoring yang lebih kompleks. 
