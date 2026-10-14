import unittest
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.m3_laporan import (
    insertion_sort, merge_sort, linear_search, binary_search,
    ManajerLaporan, Pencacah, BATAS_INSERTION
)
from backend.m1_pesanan import Pesanan


def _p(oid_num, harga=10000, selesai=100):
    return Pesanan(f"O-{oid_num:06d}", "Test", "Resto", "Menu",
                   harga, 3, 0, selesai if selesai else '', 'DONE')


class TestInsertionSort(unittest.TestCase):

    def test_acak(self):
        data = [_p(i, harga=random.randint(1000, 50000))
                for i in range(100)]
        hasil, banding, pindah, waktu, modul, galat = insertion_sort(
            list(data), 'harga')
        self.assertIsNone(galat)
        for i in range(len(hasil) - 1):
            self.assertLessEqual(hasil[i].harga, hasil[i + 1].harga)

    def test_terurut(self):
        data = [_p(i, harga=i * 100) for i in range(50)]
        hasil, banding, pindah, _, _, galat = insertion_sort(
            list(data), 'harga')
        self.assertIsNone(galat)
        for i in range(len(hasil) - 1):
            self.assertLessEqual(hasil[i].harga, hasil[i + 1].harga)

    def test_terbalik(self):
        data = [_p(i, harga=(100 - i) * 100) for i in range(50)]
        hasil, banding, pindah, _, _, galat = insertion_sort(
            list(data), 'harga')
        self.assertIsNone(galat)
        for i in range(len(hasil) - 1):
            self.assertLessEqual(hasil[i].harga, hasil[i + 1].harga)

    def test_duplikat(self):
        data = [_p(i, harga=5000) for i in range(20)]
        hasil, _, _, _, _, galat = insertion_sort(list(data), 'harga')
        self.assertIsNone(galat)
        self.assertEqual(len(hasil), 20)

    def test_stabil(self):
        data = [_p(3, harga=5000), _p(1, harga=5000), _p(2, harga=5000)]
        hasil, _, _, _, _, _ = insertion_sort(list(data), 'harga')
        oids = [int(p.oid[2:]) for p in hasil]
        self.assertEqual(oids, [3, 1, 2])

    def test_tolak_lebih_dari_batas(self):
        data = [_p(i) for i in range(BATAS_INSERTION + 1)]
        hasil, _, _, _, _, galat = insertion_sort(list(data), 'oid')
        self.assertIsNone(hasil)
        self.assertIn("DITOLAK", galat)

    def test_perbandingan_dilaporkan(self):
        data = [_p(i, harga=random.randint(1, 100)) for i in range(50)]
        _, banding, _, _, _, _ = insertion_sort(list(data), 'harga')
        self.assertGreater(banding, 0)


class TestMergeSort(unittest.TestCase):

    def test_acak(self):
        data = [_p(i, harga=random.randint(1000, 50000))
                for i in range(200)]
        hasil, banding, pindah, waktu, modul, galat = merge_sort(
            list(data), 'harga')
        self.assertIsNone(galat)
        for i in range(len(hasil) - 1):
            self.assertLessEqual(hasil[i].harga, hasil[i + 1].harga)

    def test_terurut(self):
        data = [_p(i, harga=i * 100) for i in range(100)]
        hasil, _, _, _, _, galat = merge_sort(list(data), 'harga')
        self.assertIsNone(galat)
        for i in range(len(hasil) - 1):
            self.assertLessEqual(hasil[i].harga, hasil[i + 1].harga)

    def test_terbalik(self):
        data = [_p(i, harga=(100 - i) * 100) for i in range(100)]
        hasil, _, _, _, _, galat = merge_sort(list(data), 'harga')
        self.assertIsNone(galat)
        for i in range(len(hasil) - 1):
            self.assertLessEqual(hasil[i].harga, hasil[i + 1].harga)

    def test_duplikat(self):
        data = [_p(i, harga=5000) for i in range(50)]
        hasil, _, _, _, _, _ = merge_sort(list(data), 'harga')
        self.assertEqual(len(hasil), 50)

    def test_stabil(self):
        data = [_p(3, harga=5000), _p(1, harga=5000), _p(2, harga=5000)]
        hasil, _, _, _, _, _ = merge_sort(list(data), 'harga')
        oids = [int(p.oid[2:]) for p in hasil]
        self.assertEqual(oids, [3, 1, 2])

    def test_perbandingan_dilaporkan(self):
        data = [_p(i, harga=random.randint(1, 100)) for i in range(100)]
        _, banding, _, _, _, _ = merge_sort(list(data), 'harga')
        self.assertGreater(banding, 0)


class TestHasilIdentik(unittest.TestCase):

    def test_identik(self):
        random.seed(99)
        data = [_p(i, harga=random.randint(1000, 50000))
                for i in range(200)]
        hasil_i, _, _, _, _, _ = insertion_sort(list(data), 'harga')
        hasil_m, _, _, _, _, _ = merge_sort(list(data), 'harga')
        self.assertEqual(len(hasil_i), len(hasil_m))
        for a, b in zip(hasil_i, hasil_m):
            self.assertEqual(a.oid, b.oid)
            self.assertEqual(a.harga, b.harga)


class TestLinearSearch(unittest.TestCase):

    def test_ditemukan_tengah(self):
        data = [_p(i) for i in range(1, 101)]
        idx, p, banding, waktu, modul = linear_search(data, "O-000050")
        self.assertEqual(idx, 49)
        self.assertEqual(p.oid, "O-000050")

    def test_ditemukan_kiri(self):
        data = [_p(i) for i in range(1, 101)]
        idx, p, banding, _, _ = linear_search(data, "O-000001")
        self.assertEqual(idx, 0)

    def test_ditemukan_kanan(self):
        data = [_p(i) for i in range(1, 101)]
        idx, p, banding, _, _ = linear_search(data, "O-000100")
        self.assertEqual(idx, 99)

    def test_tidak_ditemukan(self):
        data = [_p(i) for i in range(1, 101)]
        idx, p, banding, _, _ = linear_search(data, "O-000999")
        self.assertEqual(idx, -1)
        self.assertIsNone(p)

    def test_array_kosong(self):
        idx, p, banding, _, _ = linear_search([], "O-000001")
        self.assertEqual(idx, -1)


class TestBinarySearch(unittest.TestCase):

    def _data_terurut(self, n=100):
        return [_p(i) for i in range(1, n + 1)]

    def test_ditemukan_tengah(self):
        data = self._data_terurut()
        idx, p, banding, _, _ = binary_search(data, "O-000050")
        self.assertEqual(idx, 49)
        self.assertEqual(p.oid, "O-000050")

    def test_ditemukan_kiri(self):
        data = self._data_terurut()
        idx, p, banding, _, _ = binary_search(data, "O-000001")
        self.assertEqual(idx, 0)

    def test_ditemukan_kanan(self):
        data = self._data_terurut()
        idx, p, banding, _, _ = binary_search(data, "O-000100")
        self.assertEqual(idx, 99)

    def test_tidak_ditemukan(self):
        data = self._data_terurut()
        idx, p, banding, _, _ = binary_search(data, "O-000999")
        self.assertEqual(idx, -1)
        self.assertIsNone(p)

    def test_array_kosong(self):
        idx, p, banding, _, _ = binary_search([], "O-000001")
        self.assertEqual(idx, -1)

    def test_perbandingan_sedikit(self):
        data = self._data_terurut()
        _, _, banding, _, _ = binary_search(data, "O-000050")
        self.assertLessEqual(banding, 7)


class TestSortKunciSelesai(unittest.TestCase):

    def test_none_di_akhir(self):
        data = [
            _p(1, selesai=500),
            _p(2, selesai=None),
            _p(3, selesai=100),
            _p(4, selesai=None),
            _p(5, selesai=200),
        ]
        hasil, _, _, _, _, _ = merge_sort(list(data), 'selesai')
        self.assertEqual(hasil[0].t_selesai_detik, 100)
        self.assertEqual(hasil[1].t_selesai_detik, 200)
        self.assertEqual(hasil[2].t_selesai_detik, 500)
        self.assertIsNone(hasil[3].t_selesai_detik)
        self.assertIsNone(hasil[4].t_selesai_detik)


class TestKataTermarang(unittest.TestCase):

    def test_tidak_ada_kata_terlarang(self):
        import re
        pola_terlarang = [
            r'\bsorted\s*\(',
            r'\.sort\s*\(',
            r'\bheapq\b',
            r'\bbisect\b',
            r'\bcollections\b',
            r'\bdict\s*\(',
            r'\bset\s*\(',
        ]
        backend_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'backend')
        for fname in os.listdir(backend_dir):
            if not fname.endswith('.py') or fname == '__init__.py':
                continue
            fpath = os.path.join(backend_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                isi = f.read()
            baris_list = isi.split('\n')
            for no, baris in enumerate(baris_list, 1):
                stripped = baris.strip()
                if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                    continue
                if stripped.startswith('- Tidak menggunakan'):
                    continue
                for pola in pola_terlarang:
                    if re.search(pola, baris):
                        self.fail(
                            f"Pola terlarang '{pola}' ditemukan di "
                            f"{fname} baris {no}: {baris.strip()}")


if __name__ == '__main__':
    unittest.main()
