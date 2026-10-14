"""
Tes unit untuk M2 - Stack, Queue, Postfix, Undo/Redo.
Jalankan: python -m unittest tests.test_m2
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.m2_antrean import (
    Stack, AntreanNaif, AntreanMelingkar, ManajerAntrean,
    ke_postfix, hitung_postfix, hitung_struk
)
from backend.m1_pesanan import Pesanan


def _p(oid, status='ANTRE'):
    """Buat pesanan dummy untuk tes."""
    return Pesanan(oid, "Test", "Resto", "Menu", 10000, 3, 0, '', status)


class TestStack(unittest.TestCase):
    """Tes Stack LIFO."""

    def test_push_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)

    def test_peek(self):
        s = Stack()
        s.push(42)
        self.assertEqual(s.peek(), 42)
        self.assertEqual(len(s), 1)  # peek tidak mengeluarkan

    def test_kosong(self):
        s = Stack()
        self.assertTrue(s.kosong())
        s.push(1)
        self.assertFalse(s.kosong())

    def test_pop_kosong(self):
        s = Stack()
        self.assertIsNone(s.pop())

    def test_peek_kosong(self):
        s = Stack()
        self.assertIsNone(s.peek())


class TestPostfix(unittest.TestCase):
    """Tes konversi infix -> postfix dan evaluasi."""

    def test_tanpa_kurung(self):
        """Ekspresi tanpa kurung: 3 + 5 * 2"""
        postfix, tabel, waktu, modul = ke_postfix("3 + 5 * 2")
        self.assertEqual(postfix, "3 5 2 * +")

    def test_berkurung(self):
        """Ekspresi berkurung: ( 3 * 12000 ) + ( 2 * 8500 ) - 5000"""
        postfix, tabel, waktu, modul = ke_postfix(
            "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
        self.assertEqual(postfix, "3 12000 * 2 8500 * + 5000 -")

    def test_minus_beruntun(self):
        """Minus beruntun: 10 - 3 - 2"""
        postfix, _, _, _ = ke_postfix("10 - 3 - 2")
        self.assertEqual(postfix, "10 3 - 2 -")

    def test_kurung_bersarang(self):
        """Kurung bersarang: ( ( 1 + 2 ) * 3 )"""
        postfix, _, _, _ = ke_postfix("( ( 1 + 2 ) * 3 )")
        self.assertEqual(postfix, "1 2 + 3 *")

    def test_hitung_contoh_utama(self):
        """Tes contoh: ( 3 * 12000 ) + ( 2 * 8500 ) - 5000 = 48000"""
        postfix, tabel_konversi, _, _ = ke_postfix(
            "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
        hasil, tabel, waktu, modul, galat = hitung_postfix(
            postfix, tabel_konversi)
        self.assertIsNone(galat)
        self.assertEqual(hasil, 48000)

    def test_hitung_minus(self):
        """Tes minus: 10 - 3 -> a=10, b=3, 10-3=7"""
        hasil, _, _, _, galat = hitung_postfix("10 3 -")
        self.assertIsNone(galat)
        self.assertEqual(hasil, 7)

    def test_hitung_bagi(self):
        """Tes pembagian: 20 / 4 = 5"""
        hasil, _, _, _, galat = hitung_postfix("20 4 /")
        self.assertIsNone(galat)
        self.assertEqual(hasil, 5)

    def test_bagi_nol(self):
        """Pembagian nol harus mengembalikan galat, bukan crash."""
        hasil, _, _, _, galat = hitung_postfix("10 0 /")
        self.assertIsNone(hasil)
        self.assertIn("nol", galat.lower())

    def test_hitung_struk(self):
        """Tes fungsi kasir terintegrasi."""
        postfix, hasil, tabel, waktu, modul, galat = hitung_struk(
            "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
        self.assertIsNone(galat)
        self.assertEqual(hasil, 48000)
        self.assertEqual(postfix, "3 12000 * 2 8500 * + 5000 -")

    def test_kolom_output_tanpa_kurung_buka(self):
        """Kolom output tabel langkah tidak boleh memuat '('."""
        _, tabel, _, _ = ke_postfix("( 1 + 2 ) * ( 3 + 4 )")
        for row in tabel:
            output_str = row[4]  # kolom output
            self.assertNotIn('(', output_str,
                             f"Output tabel memuat '(': {row}")


class TestAntreanNaif(unittest.TestCase):
    """Tes Antrean FIFO naif."""

    def test_enqueue_dequeue(self):
        q = AntreanNaif()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        val, ges = q.dequeue()
        self.assertEqual(val, 1)
        self.assertEqual(ges, 2)  # 2 geseran (3 elemen - 1)

    def test_dequeue_kosong(self):
        q = AntreanNaif()
        val, ges = q.dequeue()
        self.assertIsNone(val)
        self.assertEqual(ges, 0)

    def test_total_geseran(self):
        """Setiap dequeue menggeser n-1 elemen."""
        q = AntreanNaif()
        for i in range(5):
            q.enqueue(i)
        q.dequeue()  # 4 geseran
        q.dequeue()  # 3 geseran
        self.assertEqual(q.total_geseran, 7)


class TestAntreanMelingkar(unittest.TestCase):
    """Tes Antrean FIFO melingkar."""

    def test_enqueue_dequeue_dasar(self):
        q = AntreanMelingkar(4)
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)

    def test_dequeue_kosong(self):
        q = AntreanMelingkar(4)
        self.assertIsNone(q.dequeue())

    def test_penunjuk_berputar(self):
        """K=4: masuk 3, keluar 2, masuk 3 lagi → front/rear berputar."""
        q = AntreanMelingkar(4)
        q.enqueue('A')
        q.enqueue('B')
        q.enqueue('C')
        # front=0, rear=3, count=3
        self.assertEqual(q.count, 3)

        self.assertEqual(q.dequeue(), 'A')
        self.assertEqual(q.dequeue(), 'B')
        # front=2, rear=3, count=1

        q.enqueue('D')
        q.enqueue('E')
        q.enqueue('F')
        # front=2, rear=2 (berputar!), count=4
        self.assertEqual(q.count, 4)

        # Isi harus: C, D, E, F (mulai dari front=2)
        self.assertEqual(q.dequeue(), 'C')
        self.assertEqual(q.dequeue(), 'D')
        self.assertEqual(q.dequeue(), 'E')
        self.assertEqual(q.dequeue(), 'F')

    def test_enqueue_penuh_tumbuh(self):
        """Saat penuh, antrean harus tumbuh 2x."""
        q = AntreanMelingkar(4)
        for i in range(4):
            q.enqueue(i)
        self.assertEqual(q.kapasitas, 4)
        q.enqueue(4)  # Harus tumbuh
        self.assertEqual(q.kapasitas, 8)
        self.assertEqual(q.count, 5)
        # Isi tetap benar
        for i in range(5):
            self.assertEqual(q.dequeue(), i)


class TestManajerAntrean(unittest.TestCase):
    """Tes Manajer Antrean dengan undo/redo."""

    def setUp(self):
        self.ma = ManajerAntrean()
        self.p1 = _p("O-000001")
        self.p2 = _p("O-000002")
        self.p3 = _p("O-000003")

    def test_enqueue_kedua(self):
        """Enqueue harus menambah ke kedua antrean."""
        self.ma.enqueue(self.p1)
        self.assertEqual(len(self.ma.naif), 1)
        self.assertEqual(len(self.ma.circular), 1)

    def test_dequeue_sinkron(self):
        """Dequeue naif harus sinkron dengan circular."""
        self.ma.enqueue(self.p1)
        self.ma.enqueue(self.p2)
        keluar, ges, waktu, info, modul = self.ma.dequeue_naif(1)
        self.assertEqual(len(keluar), 1)
        self.assertEqual(keluar[0].oid, "O-000001")
        self.assertEqual(len(self.ma.naif), 1)
        self.assertEqual(len(self.ma.circular), 1)

    def test_undo_enqueue(self):
        """Undo ENQUEUE harus mengeluarkan dari belakang."""
        self.ma.enqueue(self.p1)
        self.ma.enqueue(self.p2)
        self.ma.undo_last()
        self.assertEqual(len(self.ma.naif), 1)
        self.assertEqual(len(self.ma.circular), 1)

    def test_undo_dequeue_ke_depan(self):
        """Undo DEQUEUE harus mengembalikan pesanan ke DEPAN antrean."""
        self.ma.enqueue(self.p1)
        self.ma.enqueue(self.p2)
        self.ma.enqueue(self.p3)
        # Dequeue 2 pesanan
        self.ma.dequeue_naif(2)
        self.assertEqual(len(self.ma.naif), 1)

        # Undo → kembalikan ke depan
        self.ma.undo_last()
        self.assertEqual(len(self.ma.naif), 3)
        # Pesanan pertama harus kembali ke depan
        val, _ = self.ma.naif.dequeue()
        self.assertEqual(val.oid, "O-000001")

    def test_redo(self):
        """Redo harus mengulangi aksi yang di-undo."""
        self.ma.enqueue(self.p1)
        self.ma.undo_last()
        self.assertEqual(len(self.ma.naif), 0)
        self.ma.redo_last()
        self.assertEqual(len(self.ma.naif), 1)

    def test_redo_kosong(self):
        """Redo pada tumpukan kosong harus memberi pesan."""
        pesan, waktu, modul = self.ma.redo_last()
        self.assertIn("kosong", pesan.lower())

    def test_aksi_baru_kosongkan_redo(self):
        """Aksi baru setelah undo harus mengosongkan redo."""
        self.ma.enqueue(self.p1)
        self.ma.undo_last()
        # Redo tersedia
        stats = self.ma.stats()
        self.assertEqual(stats[5], 1)  # redo_depth = 1
        # Aksi baru
        self.ma.enqueue(self.p2)
        stats = self.ma.stats()
        self.assertEqual(stats[5], 0)  # redo_depth = 0

    def test_stats(self):
        """Tes statistik antrean."""
        self.ma.enqueue(self.p1)
        self.ma.enqueue(self.p2)
        stats = self.ma.stats()
        # (naif_len, circ_len, kapasitas, total_geseran, undo_depth, redo_depth)
        self.assertEqual(stats[0], 2)
        self.assertEqual(stats[1], 2)
        self.assertEqual(stats[4], 2)  # 2 aksi di undo stack


if __name__ == '__main__':
    unittest.main()
