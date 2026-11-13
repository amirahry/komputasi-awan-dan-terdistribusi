"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana.
"""

from platform import system
import time
import threading

REPLICATION_DELAY = 2.0  # detik, simulasi lambatnya sinkronisasi antar server

class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}

    def write(self, user_id: str, saldo_baru: float, version: int):
        self.saldo[user_id] = saldo_baru
        self.last_write_version[user_id] = version
        print(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru} (versi {version})")

    def read(self, user_id: str) -> float:
        return self.saldo.get(user_id, 0.0)
    
class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0

    def top_up(self, user_id: str, jumlah: float):
        """Top-up selalu ditulis dulu ke server Jakarta (mis. server terdekat pelanggan)."""
        self.version_counter += 1
        version = self.version_counter
        saldo_baru = self.jakarta.read(user_id) + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

        # TODO 1: Replikasi ke Bandung dengan delay buatan
        timer = threading.Timer(
            REPLICATION_DELAY,
            self.bandung.write,
            args=(user_id, saldo_baru, version)
        )
        timer.start()

        print(
            f"[Replikasi] Pembaruan ke Bandung "
            f"tertunda {REPLICATION_DELAY} detik"
        )
       
    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        return replica.read(user_id)

    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int) -> float:
        
        # TODO 2: Periksa versi dan alihkan pembacaan jika diperlukan
        replica = self.jakarta if server == "Jakarta" else self.bandung
        versi_replica = replica.last_write_version.get(user_id, 0)

        if versi_replica >= versi_minimal:
            print(
                f"[RYW] {replica.name} memiliki versi "
                f"{versi_replica}, data dapat dibaca"
            )
            return replica.read(user_id)

        print(
            f"[RYW] {replica.name} masih versi {versi_replica}, "
            f"membutuhkan versi {versi_minimal}"
        )

        # Mengalihkan pembacaan ke Jakarta jika Bandung belum sinkron
        versi_jakarta = self.jakarta.last_write_version.get(user_id, 0)

        if versi_jakarta >= versi_minimal:
            print(f"[RYW] Redirect ke Jakarta (versi {versi_jakarta})")
            return self.jakarta.read(user_id)

        raise RuntimeError(
            "Tidak ada replika yang memenuhi versi minimal pelanggan"
        )

def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("=== Skenario NAIF (tanpa Read-Your-Writes) ===")
    system.top_up(user_id, 50000)
    time.sleep(0.5)  # pelanggan langsung pesan makanan < REPLICATION_DELAY detik kemudian
    print("Baca saldo dari Bandung (naif):", system.baca_saldo_naif(user_id, "Bandung"))
    print("-> Harusnya 50000, tapi karena delay replikasi, hasilnya bisa 0 (BUG)")

    time.sleep(REPLICATION_DELAY + 0.5)

    print("\n=== Skenario dengan Read-Your-Writes ===")
    system.top_up(user_id, 20000)
    versi_terakhir = system.version_counter

    # TODO 3: Tunjukkan hasil pembacaan dengan Read-Your-Writes
    saldo_ryw = system.baca_saldo_read_your_writes(
        user_id, "Bandung", versi_terakhir
    )

    print(f"Baca saldo dengan Read-Your-Writes: Rp{saldo_ryw:,.0f}")
    print("-> Seharusnya Rp70,000; hasil benar meskipun Bandung belum tersinkronisasi")

    time.sleep(REPLICATION_DELAY + 0.5)
    print(f"Saldo akhir Bandung setelah replikasi: Rp{system.bandung.read(user_id):,.0f}")

if __name__ == "__main__":
    main()
