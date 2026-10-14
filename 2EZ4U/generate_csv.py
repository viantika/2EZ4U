"""
Modul Generator Data Pesanan CSV untuk Sistem Pengiriman Makanan 2EZ4U.

Modul ini bertanggung jawab untuk menghasilkan berkas CSV berisi data pesanan
dalam skala besar (200.000 baris) dengan konfigurasi yang realistis dan konsisten.
Seluruh logika dibuat berbasis OOP serta mematuhi batasan struktur data.
"""

import csv
import os
import random


class GeneratorDataPesanan:
    """
    Kelas generator data pesanan pengiriman makanan berbasis OOP.
    
    Menghasilkan data pesanan dengan distribusi prioritas, status transaksi,
    durasi waktu penyelesaian, dan nama pelanggan yang realistis.
    """

    def __init__(self, seed: int = 42):
        """
        Inisialisasi generator dengan seed acak untuk memastikan hasil reproduktif.
        
        Args:
            seed (int): Nilai seed acak (standar: 42).
        """
        self._seed = seed
        random.seed(self._seed)

        # Daftar restoran mitra sesuai simpul pada peta kampus (peta.csv)
        self._daftar_resto = (
            "kantin-pusat",
            "kafe-teknik",
            "warung-bu-ida",
            "kedai-kopi",
            "kantin-asrama",
            "bakso-pak-yon",
        )

        # Daftar katalog menu beserta harga (dalam Rupiah)
        self._daftar_menu = (
            ("nasi-goreng", 15000),
            ("mie-goreng", 13000),
            ("mie-ayam", 13000),
            ("bakso", 16000),
            ("soto-ayam", 14000),
            ("ayam-geprek", 19000),
            ("ayam-bakar", 22000),
            ("nasi-padang", 25000),
            ("nasi-campur", 20000),
            ("pecel-lele", 18000),
            ("gado-gado", 15000),
            ("sate-ayam", 24000),
            ("iga-penyet", 27000),
            ("bubur-ayam", 11000),
            ("roti-bakar", 12000),
            ("kentang-goreng", 14000),
            ("burger-kampus", 21000),
            ("gorengan", 6000),
            ("es-teh", 5000),
            ("air-mineral", 4000),
            ("teh-tarik", 9000),
            ("kopi-susu", 18000),
            ("juice-alpukat", 17000),
            ("es-campur", 12000),
        )

        # Kumpulan nama untuk variasi nama pelanggan Indonesia
        self._awalan_gelar = (
            "", "", "", "", "", "",
            "Dr. ", "Drs. ", "Ir. ", "H. ", "Hj. ", "R. ", "Tgk. ", "Dt. ",
        )

        self._nama_depan = (
            "Budi", "Siti", "Agus", "Dewi", "Eko", "Rina", "Joko", "Sri",
            "Hendra", "Nur", "Bambang", "Indah", "Rizky", "Fitri", "Dian",
            "Ahmad", "Putri", "Adi", "Tri", "Bayu", "Wahyu", "Ratna",
            "Wawan", "Mega", "Yusuf", "Ayu", "Fajar", "Lestari", "Doni",
            "Tia", "Aris", "Wulan", "Surya", "Intan", "Galih", "Maya",
            "Dimas", "Nia", "Ilham", "Ratih", "Oskar", "Rahmi", "Cici",
            "Malika", "Usyi", "Radika", "Ani", "Rafid", "Ami", "Gandewa",
            "Wasis", "Teguh", "Irma", "Karimah", "Lasmanto", "Liman",
            "Kamaria", "Laras", "Safina", "Malik", "Ina", "Hani", "Yuni",
            "Cengkir", "Praba", "Panji", "Jessica", "Bakiman", "Hilda",
            "Nova", "Cinta", "Zulfa",
        )

        self._nama_belakang = (
            "Santoso", "Wijaya", "Kusuma", "Pratama", "Saputra", "Lestari",
            "Hidayat", "Nugroho", "Setiawan", "Utomo", "Purnomo", "Wibowo",
            "Susanto", "Handayani", "Simanjuntak", "Siregar", "Nasution",
            "Tampubolon", "Firmansyah", "Gunawan", "Mahendra", "Pradipta",
            "Widiastuti", "Haryanto", "Dabukke", "Puspita", "Dongoran",
            "Hartati", "Usamah", "Pangestu", "Rajasa", "Tarihoran",
            "Megantara", "Melani", "Hidayanto", "Wacana", "Marbun",
            "Rahayu", "Adriansyah", "Maryadi", "Kurniawan", "Laksita",
            "Wastuti", "Uwais",
        )

        self._akhiran_gelar = (
            "", "", "", "", "", "",
            ", S.T.", ", S.Kom", ", S.E.", ", S.Pd", ", S.Sos", ", S.Si",
            ", M.Kom", ", M.M.", ", M.T.", ", S.Ked", ", S.H.", ", S.Farm",
            ", S.Pt", ", M.Ak",
        )

    def buat_nama_pelanggan(self) -> str:
        """
        Menghasilkan nama pelanggan acak lengkap dengan gelar/kehormatan.
        Nama yang mengandung koma (gelar belakang) akan otomatis dikutip oleh csv.writer.
        
        Returns:
            str: Nama pelanggan lengkap.
        """
        prefix = random.choice(self._awalan_gelar)
        depan = random.choice(self._nama_depan)
        belakang = random.choice(self._nama_belakang)
        suffix = random.choice(self._akhiran_gelar)
        return f"{prefix}{depan} {belakang}{suffix}"

    def buat_pesanan(self, nomor_urutan: int) -> tuple:
        """
        Menghasilkan satu data baris pesanan sesuai aturan distribusi.
        
        Aturan:
        - oid: O-000001 s.d. O-200000
        - prioritas: 1=VIP (~5%), 2=Prioritas (~15%), 3=Reguler (~80%)
        - t_masuk_detik: 0 s.d. 86399 (detik dalam satu hari)
        - status: DONE (~70%), CANCEL (~20%), ANTRE (~10%)
        - t_selesai_detik: kosong untuk ANTRE, masuk+120-3600 untuk DONE, masuk+30-600 untuk CANCEL
        
        Args:
            nomor_urutan (int): Nomor urutan pesanan (1-indexed).
            
        Returns:
            tuple: Tuple berisi kolom data pesanan.
        """
        oid = f"O-{nomor_urutan:06d}"
        pelanggan = self.buat_nama_pelanggan()
        resto = random.choice(self._daftar_resto)

        menu_item = random.choice(self._daftar_menu)
        menu_nama = menu_item[0]
        harga = menu_item[1]

        # Distribusi prioritas: ~5% VIP (1), ~15% Prioritas (2), ~80% Reguler (3)
        rand_prioritas = random.randint(1, 100)
        if rand_prioritas <= 5:
            prioritas = 1
        elif rand_prioritas <= 20:
            prioritas = 2
        else:
            prioritas = 3

        # Waktu masuk pesanan (0 s.d. 86399 detik dalam sehari)
        t_masuk_detik = random.randint(0, 86399)

        # Distribusi status: ~70% DONE, ~20% CANCEL, ~10% ANTRE
        rand_status = random.randint(1, 100)
        if rand_status <= 70:
            status = "DONE"
            t_selesai_detik = str(t_masuk_detik + random.randint(120, 3600))
        elif rand_status <= 90:
            status = "CANCEL"
            t_selesai_detik = str(t_masuk_detik + random.randint(30, 600))
        else:
            status = "ANTRE"
            t_selesai_detik = ""

        return (
            oid,
            pelanggan,
            resto,
            menu_nama,
            harga,
            prioritas,
            t_masuk_detik,
            t_selesai_detik,
            status,
        )

    def generate_csv(self, jalur_berkas: str, total_baris: int = 200000) -> None:
        """
        Menuliskan seluruh data pesanan ke dalam berkas CSV.
        
        Args:
            jalur_berkas (str): Jalur berkas CSV tujuan.
            total_baris (int): Jumlah baris data yang ingin dihasilkan.
        """
        folder_tujuan = os.path.dirname(jalur_berkas)
        if folder_tujuan and not os.path.exists(folder_tujuan):
            os.makedirs(folder_tujuan, exist_ok=True)

        header = (
            "oid",
            "pelanggan",
            "resto",
            "menu",
            "harga",
            "prioritas",
            "t_masuk_detik",
            "t_selesai_detik",
            "status",
        )

        with open(jalur_berkas, mode="w", newline="", encoding="utf-8") as berkas_csv:
            penulis_csv = csv.writer(berkas_csv)
            penulis_csv.writerow(header)

            ukuran_kelompok = 5000
            kelompok_baris = []

            for i in range(1, total_baris + 1):
                kelompok_baris.append(self.buat_pesanan(i))

                if len(kelompok_baris) == ukuran_kelompok:
                    penulis_csv.writerows(kelompok_baris)
                    kelompok_baris = []

            if len(kelompok_baris) > 0:
                penulis_csv.writerows(kelompok_baris)
                kelompok_baris = []


def main() -> None:
    """Fungsi utama untuk menjalankan pembuatan berkas CSV pesanan."""
    jalur_proyek = os.path.dirname(os.path.abspath(__file__))
    jalur_csv = os.path.join(jalur_proyek, "data", "pesanan.csv")

    print(f"Memulai pembuatan data pesanan sebanyak 200.000 baris...")
    print(f"Berkas tujuan: {jalur_csv}")

    generator = GeneratorDataPesanan(seed=42)
    generator.generate_csv(jalur_csv, total_baris=200000)

    print("Pembuatan berkas CSV data pesanan selesai berhasil!")


if __name__ == "__main__":
    main()
