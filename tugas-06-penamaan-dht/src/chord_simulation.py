
"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}

        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        if node_id in self.nodes:
            print(f"Node '{node_name}' sudah ada.")
            return

        self.nodes[node_id] = node_ip

        # TODO 2: cari successor LAMA dari node_id ini (successor sebelum node
        # baru bergabung, gunakan find_successor() dengan node_id INI dikecualikan
        # dulu dari self.nodes saat mencari).
        del self.nodes[node_id]

        old_successor = (
            self.find_successor(node_id)
            if self.nodes else None
        )

        self.nodes[node_id] = node_ip

        # TODO 3: pindahkan semua key di self.data yang seharusnya menjadi
        # tanggung jawab node baru (key dengan hash <= node_id, tapi masih
        # dipegang oleh successor lama) ke bawah tanggung jawab node baru.
        # (Untuk simulasi sederhana, cukup print log siapa mengambil alih apa -
        # tidak perlu benar-benar memindahkan struktur data kompleks.)
        if old_successor is not None:
            for key_hash, (kurir_id, ip_kurir) in self.data.items():
                new_successor = self.find_successor(key_hash)

                if new_successor == node_id:
                    print(
                        f"[JOIN] {kurir_id} (hash={key_hash}) "
                        f"berpindah dari node {old_successor} "
                        f"ke node {node_id}"
                    )
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        # TODO 4: hapus node_id dari self.nodes.
        if node_id not in self.nodes:
            print(f"Node '{node_name}' tidak ditemukan.")
            return

        if len(self.nodes) == 1 and self.data:
            print("Node terakhir tidak bisa keluar selama data masih ada.")
            return

        affected_keys = [
            (key_hash, kurir_id)
            for key_hash, (kurir_id, ip_kurir) in self.data.items()
            if self.find_successor(key_hash) == node_id
        ]

        del self.nodes[node_id]

        # TODO 5: cari successor BARU untuk tiap key yang tadinya dipegang
        # node ini, pindahkan ke successor tersebut.
        for key_hash, kurir_id in affected_keys:
            new_successor = self.find_successor(key_hash)

            print(
                f"[LEAVE] {kurir_id} (hash={key_hash}) "
                f"berpindah dari node {node_id} "
                f"ke node {new_successor}"
            )
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: implementasikan logika successor di atas menggunakan
        # self.nodes.keys(). Kembalikan node_id (bukan IP).
        if not self.nodes:
            raise ValueError("Ring masih kosong.")

        sorted_nodes = sorted(self.nodes.keys())

        for node_id in sorted_nodes:
            if node_id >= key_hash:
                return node_id

        return sorted_nodes[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7: panggil find_successor(key_hash) untuk menentukan node
        # penanggung jawab, lalu simpan (kurir_id, ip_kurir) ke self.data[key_hash].
        node_id = self.find_successor(key_hash)

        self.data[key_hash] = (kurir_id, ip_kurir)

        print(
            f"[REGISTER] {kurir_id} (hash={key_hash}) "
            f"disimpan di node {node_id}, IP={ip_kurir}"
        )

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8: gunakan find_successor(key_hash) untuk menemukan node
        # penanggung jawab, lalu kembalikan ip_kurir dari self.data jika ada.
        if not self.nodes:
            return None

        node_id = self.find_successor(key_hash)

        data_kurir = self.data.get(key_hash)

        if data_kurir is not None and data_kurir[0] == kurir_id:
            print(
                f"[LOOKUP] {kurir_id} ditemukan "
                f"di node {node_id}"
            )
            return data_kurir[1]

        return None


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan beberapa kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")
    ring.register_kurir("kurir-012", "192.168.1.13")
    ring.register_kurir("kurir-005", "192.168.1.14")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))
    print("kurir-005 ->", ring.lookup("kurir-005"))
    print("kurir-012 ->", ring.lookup("kurir-012"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-012 ->", ring.lookup("kurir-012"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-005 ->", ring.lookup("kurir-005"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()
