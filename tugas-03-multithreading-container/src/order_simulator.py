"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading 
 
Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO. 
Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten). 
"""

import threading 
import random 
import time 
 
NUM_ORDERS = 100        # jumlah pesanan simulasi yang masuk 
NUM_WORKERS = 10        # jumlah thread pekerja 
 
# Counter bersama untuk menghitung total pesanan yang berhasil diproses. 
# Sengaja rawan race condition jika diakses tanpa proteksi. 
processed_count = 0 
 
# TODO 1: Buat objek Lock di sini untuk melindungi `processed_count`. 
lock = threading.Lock()         #Lock untuk mencegah race condition
 
 
def process_order(order_id: int) -> None: 
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja.""" 
    global processed_count 
 
    # Simulasikan kerja nyata (mis. validasi, hitung total harga) 
    time.sleep(random.uniform(0.001, 0.01)) 
 
    # TODO 2: Tambahkan increment `processed_count` DI SINI. 
    # Langkah 1: jalankan dulu tanpa lock (increment biasa: processed_count += 1) 
    #            dan buktikan hasil akhirnya sering salah (< NUM_ORDERS). 
    # Langkah 2: bungkus increment dengan `with lock:` dan buktikan hasilnya 
    #            selalu tepat NUM_ORDERS. Simpan bukti kedua kondisi ini 
    #            di JURNAL.md / folder bukti/. 

    # PERCOBAAN TANPA LOCK (digunakan untuk membuktikan race condition).
    # temp = processed_count
    # time.sleep(0.01)
    # processed_count = temp + 1

    # PERCOBAAN DENGAN LOCK (versi akhir untuk mencegah race condition).
    with lock:
        processed_count += 1   
 
def worker(order_ids: list) -> None:  
    """Satu thread pekerja memproses sekumpulan order_id.""" 
    for order_id in order_ids: 
        process_order(order_id) 
 
 
def main() -> None: 
    order_ids = list(range(1, NUM_ORDERS + 1)) 
 
    # TODO 3: Bagi `order_ids` menjadi NUM_WORKERS bagian, buat satu 
    # threading.Thread per bagian yang menjalankan `worker(...)`, 
    # start semua thread, lalu join semua thread sebelum lanjut. 
    
    threads = []

    # Membagi jumlah pesanan menjadi beberapa bagian untuk setiap thread.
    chunk_size = len(order_ids) // NUM_WORKERS

    for i in range(NUM_WORKERS):

        start = i * chunk_size

        # Thread terakhir mengambil sisa order jika pembagian tidak rata.
        if i == NUM_WORKERS - 1:
            end = len(order_ids)
        else:
            end = start + chunk_size

        order_chunk = order_ids[start:end]

        # Membuat thread baru yang menjalankan fungsi worker.
        thread = threading.Thread(
            target=worker,
            args=(order_chunk,)
        )

        threads.append(thread)

         # Menjalankan thread.
        thread.start()
 
    for t in threads: 
        t.join() 
 
    print(f"Total pesanan diproses: {processed_count} (seharusnya {NUM_ORDERS})") 
    if processed_count != NUM_ORDERS: 
        print("RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!") 
    else:
        print("Semua pesanan berhasil diproses dengan aman")
 
 
if __name__ == "__main__": 
    main()