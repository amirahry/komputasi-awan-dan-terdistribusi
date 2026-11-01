# Jurnal Proses — Tugas 6

## Implementasi `find_successor`

### Permasalahan yang Ditemui (mis. lupa wrap-around di ring)

Salah satu kendala dalam implementasi `find_successor` adalah penanganan *wrap-around*. Jika pencarian hanya memeriksa node dengan ID hash `>= key_hash`, key yang nilai hash-nya melebihi seluruh ID node aktif tidak akan memiliki node penanggung jawab. Contohnya, setelah `node-jakarta-1` (hash 177) keluar, `kurir-005` (hash 175) tidak dapat ditempatkan dengan pencarian linear biasa karena node aktif terbesar hanya memiliki hash 136.

### Cara Memperbaikinya

Node diurutkan berdasarkan nilai hash menggunakan `sorted(self.nodes.keys())`. Fungsi kemudian mencari node pertama dengan `node_id >= key_hash`. Apabila tidak ditemukan, fungsi mengembalikan `sorted_nodes[0]`, yaitu node dengan hash terkecil, sesuai mekanisme *wrap-around* pada ring Chord.

Ditambahkan pula validasi `if not self.nodes` yang menghasilkan `ValueError("Ring masih kosong.")` agar pencarian pada ring kosong ditangani secara jelas.

Perbaikan ini terlihat pada skenario *leave*: setelah node 177 keluar, tanggung jawab `kurir-005` (hash 175) berpindah ke node 40 (`node-bandung-1`).

## Skenario `join()` / `leave()`

### 1. Node Baru Bergabung (`join`)

Sebelum `node-medan-1` bergabung, `kurir-012` (hash 116) disimpan oleh `node-surabaya-1` (hash 136). Pencarian `lookup("kurir-012")` menghasilkan alamat IP `192.168.1.13`.

Ketika `node-medan-1` (hash 123) bergabung, program terlebih dahulu menentukan *successor* lama sebelum memperbarui keanggotaan ring. Berdasarkan alur simulasi, node baru dikeluarkan sementara dari `self.nodes` saat mencari *successor* sebelumnya, lalu dimasukkan kembali. Setelah penyesuaian kepemilikan key, `kurir-012` berpindah dari node 136 ke node 123.

**Bukti output program:**

```text
--- Node baru bergabung ---
[JOIN] kurir-012 (hash=116) berpindah dari node 136 ke node 123
[JOIN] Node 'node-medan-1' (id=123) bergabung, alamat 10.0.0.5
[LOOKUP] kurir-012 ditemukan di node 123
kurir-012 -> 192.168.1.13
```

Setelah *join*, IP `kurir-012` tetap sama. Perubahan hanya terjadi pada node penanggung jawab, sedangkan key kurir lain tetap berada pada node sebelumnya.

### 2. Node Keluar (`leave`)

Sebelum `node-jakarta-1` (hash 177) keluar, node tersebut bertanggung jawab atas `kurir-005` (hash 175). Program mengidentifikasi key yang terdampak melalui `affected_keys` sebelum menghapus node dari ring.

Setelah node 177 dihapus, fungsi `find_successor` menentukan node pengganti. Karena tidak ada node aktif dengan hash `>= 175`, pencarian melakukan *wrap-around* ke node dengan hash terkecil, yaitu `node-bandung-1` (hash 40).

**Bukti output program:**

```text
--- Sebuah node keluar ---
[LEAVE] kurir-005 (hash=175) berpindah dari node 177 ke node 40
[LEAVE] Node 'node-jakarta-1' (id=177) keluar dari ring
[LOOKUP] kurir-005 ditemukan di node 40
kurir-005 -> 192.168.1.14
[LOOKUP] kurir-002 ditemukan di node 40
kurir-002 -> 192.168.1.11
```

Setelah *leave*, `kurir-005` dapat ditemukan pada node 40 dengan IP yang tetap, yaitu `192.168.1.14`. `kurir-002` juga tetap berada pada node 40 dengan IP `192.168.1.11`. Dengan demikian, hanya key yang sebelumnya menjadi tanggung jawab node keluar yang perlu dialihkan.

### 3. Ringkasan Hasil Pengujian

| Skenario | Key terdampak | Node sebelumnya | Node setelah perubahan | Hasil |
|---|---|---|---|---|
| `join` node 123 | `kurir-012` (116) | 136 (`node-surabaya-1`) | 123 (`node-medan-1`) | *Lookup* berhasil; IP tetap `192.168.1.13` |
| `leave` node 177 | `kurir-005` (175) | 177 (`node-jakarta-1`) | 40 (`node-bandung-1`) | *Lookup* berhasil; IP tetap `192.168.1.14` |

Program juga memiliki penanganan untuk permintaan penghapusan node yang tidak terdaftar, serta mencegah node terakhir keluar apabila masih terdapat data yang harus disimpan.

### Kesimpulan

Pengujian menunjukkan bahwa mekanisme `find_successor`, `join`, dan `leave` dalam simulasi FoodGo dapat menyesuaikan kepemilikan key ketika susunan node berubah. Mekanisme *wrap-around* memastikan key tetap memiliki penanggung jawab meskipun nilai hash-nya lebih besar daripada seluruh ID node aktif. Sementara itu, *consistent hashing* membatasi perpindahan key pada bagian ring yang terdampak, tanpa mengubah ID maupun alamat IP kurir.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 30/10/26 | ChatGPT | Apa saja aspek yang perlu dipertimbangkan dalam membandingkan Chord DHT dengan flat naming dan DNS untuk kasus FoodGo? | Memberikan ide perbandingan mengenai distribusi data, pembaruan IP, efisiensi pencarian, dan skalabilitas. | Ide digunakan sebagai acuan dalam menyusun pembahasan README berdasarkan pemahaman materi. |
| 30/10/26 | ChatGPT | Bagaimana konsep dasar consistent hashing pada Chord DHT? | Menjelaskan gambaran umum pembagian key berdasarkan nilai hash dan node penanggung jawab. | Penjelasan digunakan sebagai bahan pemahaman konsep distribusi key pada ring Chord. |
| 30/10/26 | ChatGPT | Apa yang perlu diperhatikan ketika node bergabung atau keluar dari ring Chord? | Memberikan gambaran mengenai perubahan kepemilikan key saat terjadi perubahan jumlah node. | Informasi dijadikan referensi untuk memahami skenario join dan leave sebelum melakukan pengujian. |
| 30/10/26 | ChatGPT | Bagaimana urutan yang tepat untuk menjelaskan ring topology? | Menyarankan urutan pembahasan mulai dari nilai hash, posisi node, hingga distribusi key. | Saran digunakan untuk membantu menyusun struktur penjelasan diagram ring pada README. |
| 30/10/26 | ChatGPT | Apa saja hal penting yang perlu dicatat dalam jurnal proses simulasi Chord DHT? | Menyarankan pencatatan kendala, proses penyelesaian, skenario pengujian, dan hasil pengamatan. | Saran digunakan sebagai panduan penyusunan jurnal sesuai proses pengerjaan yang dilakukan. |
