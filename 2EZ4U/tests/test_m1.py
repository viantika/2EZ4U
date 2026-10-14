"""
Tes unit untuk M1 - Array Dinamis dan Linked List.
Jalankan: python -m unittest tests.test_m1
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.m1_pesanan import (
    Array, LinkList, Node, Pesanan, Pencacah,
    ManajerPesanan, format_waktu, format_harga
)


class TestPencacah(unittest.TestCase):
    def test_inisialisasi(self):
        p = Pencacah()
        self.assertEqual(p.n, 0)

    def test_tambah(self):
        p = Pencacah()
        p.tambah()
        self.assertEqual(p.n, 1)
        p.tambah(5)
        self.assertEqual(p.n, 6)

    def test_reset(self):
        p = Pencacah()
        p.tambah(10)
        p.reset()
        self.assertEqual(p.n, 0)


class TestFormatWaktu(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(format_waktu(0), "00:00:00")
        self.assertEqual(format_waktu(3661), "01:01:01")
        self.assertEqual(format_waktu(86399), "23:59:59")

    def test_none(self):
        self.assertEqual(format_waktu(None), "-")
        self.assertEqual(format_waktu(''), "-")


class TestFormatHarga(unittest.TestCase):
    def test_ribuan(self):
        self.assertEqual(format_harga(12000), "12.000")
        self.assertEqual(format_harga(1000000), "1.000.000")
        self.assertEqual(format_harga(500), "500")
        self.assertEqual(format_harga(0), "0")


class TestArray(unittest.TestCase):
    """Tes Array dinamis buatan sendiri."""

    def test_append_dan_len(self):
        a = Array(4)
        for i in range(10):
            a.append(i)
        self.assertEqual(len(a), 10)

    def test_tumbuh_benar(self):
        """Kapasitas awal 4, harus tumbuh: 4 → 8 → 16 saat penuh."""
        a = Array(4)
        self.assertEqual(a.kapasitas, 4)

        # Isi 4 elemen → masih muat
        for i in range(4):
            a.append(i)
        self.assertEqual(a.kapasitas, 4)

        # Tambah 1 lagi → tumbuh jadi 8
        a.append(4)
        self.assertEqual(a.kapasitas, 8)
        self.assertEqual(len(a), 5)

        # Isi sampai 8 elemen
        for i in range(5, 8):
            a.append(i)
        self.assertEqual(a.kapasitas, 8)

        # Tambah 1 lagi → tumbuh jadi 16
        a.append(8)
        self.assertEqual(a.kapasitas, 16)
        self.assertEqual(len(a), 9)

    def test_get(self):
        a = Array(4)
        for i in range(5):
            a.append(i * 10)
        self.assertEqual(a.get(0), 0)
        self.assertEqual(a.get(2), 20)
        self.assertEqual(a.get(4), 40)

    def test_get_invalid(self):
        a = Array(4)
        a.append(1)
        with self.assertRaises(ValueError):
            a.get(5)
        with self.assertRaises(ValueError):
            a.get(-1)

    def test_insert_awal(self):
        """Insert di indeks 0 (VIP) — harus geser semua."""
        a = Array(4)
        for i in range(3):
            a.append(i)  # [0, 1, 2]
        p = Pencacah()
        a.insert(0, 99, p)  # [99, 0, 1, 2]
        self.assertEqual(a.get(0), 99)
        self.assertEqual(a.get(1), 0)
        self.assertEqual(len(a), 4)
        self.assertEqual(p.n, 3)  # 3 geseran

    def test_insert_tengah(self):
        """Insert di tengah (PRIORITAS)."""
        a = Array(8)
        for i in range(4):
            a.append(i)  # [0, 1, 2, 3]
        a.insert(2, 99)   # [0, 1, 99, 2, 3]
        self.assertEqual(a.get(2), 99)
        self.assertEqual(a.get(3), 2)
        self.assertEqual(len(a), 5)

    def test_insert_akhir(self):
        """Insert di akhir (REGULER) = append."""
        a = Array(4)
        for i in range(3):
            a.append(i)
        a.insert(3, 99)  # [0, 1, 2, 99]
        self.assertEqual(a.get(3), 99)
        self.assertEqual(len(a), 4)

    def test_hapus_awal(self):
        a = Array(4)
        for i in range(4):
            a.append(i)  # [0, 1, 2, 3]
        val = a.hapus(0)
        self.assertEqual(val, 0)
        self.assertEqual(a.get(0), 1)
        self.assertEqual(len(a), 3)

    def test_hapus_tengah(self):
        a = Array(8)
        for i in range(5):
            a.append(i)  # [0, 1, 2, 3, 4]
        val = a.hapus(2)
        self.assertEqual(val, 2)
        self.assertEqual(a.get(2), 3)
        self.assertEqual(len(a), 4)

    def test_hapus_akhir(self):
        a = Array(4)
        for i in range(4):
            a.append(i)
        val = a.hapus(3)
        self.assertEqual(val, 3)
        self.assertEqual(len(a), 3)

    def test_hapus_invalid(self):
        a = Array(4)
        a.append(1)
        with self.assertRaises(ValueError):
            a.hapus(5)

    def test_iter(self):
        a = Array(4)
        for i in range(5):
            a.append(i)
        self.assertEqual(list(a), [0, 1, 2, 3, 4])


class TestLinkList(unittest.TestCase):
    """Tes Linked List."""

    def test_append_dan_len(self):
        ll = LinkList()
        for i in range(10):
            ll.append(i)
        self.assertEqual(len(ll), 10)

    def test_prepend(self):
        """Prepend (VIP) harus O(1)."""
        ll = LinkList()
        ll.append(1)
        ll.append(2)
        ll.prepend(0)  # [0, 1, 2]
        self.assertEqual(ll.get(0), 0)
        self.assertEqual(ll.get(1), 1)
        self.assertEqual(len(ll), 3)

    def test_insert_awal(self):
        ll = LinkList()
        for i in range(3):
            ll.append(i)
        ll.insert(0, 99)
        self.assertEqual(ll.get(0), 99)
        self.assertEqual(len(ll), 4)

    def test_insert_tengah(self):
        ll = LinkList()
        for i in range(4):
            ll.append(i)
        ll.insert(2, 99)
        self.assertEqual(ll.get(2), 99)
        self.assertEqual(ll.get(3), 2)
        self.assertEqual(len(ll), 5)

    def test_insert_akhir(self):
        ll = LinkList()
        for i in range(3):
            ll.append(i)
        ll.insert(3, 99)
        self.assertEqual(ll.get(3), 99)
        self.assertEqual(len(ll), 4)

    def test_get_invalid(self):
        ll = LinkList()
        ll.append(1)
        with self.assertRaises(ValueError):
            ll.get(5)

    def test_hapus_awal(self):
        ll = LinkList()
        for i in range(4):
            ll.append(i)
        val = ll.hapus(0)
        self.assertEqual(val, 0)
        self.assertEqual(ll.get(0), 1)
        self.assertEqual(len(ll), 3)

    def test_hapus_tengah(self):
        ll = LinkList()
        for i in range(5):
            ll.append(i)
        val = ll.hapus(2)
        self.assertEqual(val, 2)
        self.assertEqual(ll.get(2), 3)
        self.assertEqual(len(ll), 4)

    def test_hapus_akhir(self):
        ll = LinkList()
        for i in range(4):
            ll.append(i)
        val = ll.hapus(3)
        self.assertEqual(val, 3)
        self.assertEqual(len(ll), 3)
        # Pastikan tail diperbarui
        self.assertEqual(ll.tail.nilai, 2)

    def test_hapus_invalid(self):
        ll = LinkList()
        ll.append(1)
        with self.assertRaises(ValueError):
            ll.hapus(5)

    def test_iter(self):
        ll = LinkList()
        for i in range(5):
            ll.append(i)
        self.assertEqual(list(ll), [0, 1, 2, 3, 4])


class TestSisipanSama(unittest.TestCase):
    """Pastikan tiga jenis sisipan menghasilkan urutan yang sama
    di Array dan LinkList."""

    def _buat_pesanan(self, oid, prioritas):
        return Pesanan(oid, "Test", "Resto", "Menu", 10000,
                       prioritas, 0, '', 'ANTRE')

    def test_urutan_sisip_sama(self):
        """VIP di depan, PRIORITAS di tengah, REGULER di belakang."""
        a = Array(8)
        ll = LinkList()

        # Tambah 3 reguler
        for i in range(3):
            p = self._buat_pesanan(f"O-{i+1:06d}", 3)
            a.append(p)
            ll.append(p)

        # Tambah VIP di depan
        p_vip = self._buat_pesanan("O-000004", 1)
        a.insert(0, p_vip)
        ll.prepend(p_vip)

        # Tambah PRIORITAS di tengah
        p_pri = self._buat_pesanan("O-000005", 2)
        mid = len(a) // 2
        a.insert(mid, p_pri)
        ll.insert(mid, p_pri)

        # Tambah REGULER di belakang
        p_reg = self._buat_pesanan("O-000006", 3)
        a.append(p_reg)
        ll.append(p_reg)

        # Bandingkan urutan
        arr_oids = [a.get(i).oid for i in range(len(a))]
        ll_oids = [ll.get(i).oid for i in range(len(ll))]
        self.assertEqual(arr_oids, ll_oids)


class TestManajerPesanan(unittest.TestCase):
    """Tes pemuatan CSV dan operasi manajer."""

    def test_muat_csv(self):
        """Tes muat CSV (hanya jika file ada)."""
        path = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'data', 'pesanan.csv')
        if not os.path.exists(path):
            self.skipTest("File pesanan.csv tidak ditemukan")

        mp = ManajerPesanan()
        jumlah, waktu, modul = mp.muat_csv(path)
        self.assertEqual(jumlah, 200000)
        self.assertEqual(len(mp.array), 200000)
        self.assertEqual(len(mp.linklist), 200000)
        self.assertTrue(waktu > 0)


if __name__ == '__main__':
    unittest.main()
