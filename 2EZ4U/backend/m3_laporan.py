"""
M3 - Laporan: Sorting dan Searching
Modul untuk insertion sort, merge sort, linear search, binary search.
"""
import time as _time


# ============================================================
#  UTILITAS (diimpor ulang agar M3 mandiri dari M1)
# ============================================================

class Pencacah:
    """Pencacah perbandingan dan pemindahan."""
    __slots__ = ('n',)

    def __init__(self):
        self.n = 0

    def tambah(self, k=1):
        self.n += k

    def reset(self):
        self.n = 0


def _timer():
    return _time.perf_counter()


def _ms(awal, akhir):
    return (akhir - awal) * 1000.0


# ============================================================
#  FUNGSI KUNCI (key extractors)
# ============================================================

def _kunci_oid(p):
    """Ambil angka dari oid untuk perbandingan numerik. O-000001 -> 1."""
    return int(p.oid[2:])


def _kunci_harga(p):
    """Kunci harga (angka)."""
    return p.harga


def _kunci_selesai(p):
    """
    Kunci waktu selesai.
    Pesanan tanpa waktu selesai (None) diletakkan di akhir.
    Kami pakai tuple (flag, nilai): (0, detik) untuk yang ada, (1, 0) untuk None.
    Ini agar saat perbandingan, None selalu 'lebih besar'.
    """
    if p.t_selesai_detik is None:
        return (1, 0)
    return (0, p.t_selesai_detik)


def _ambil_kunci(nama_kunci):
    """Kembalikan fungsi kunci berdasarkan nama."""
    if nama_kunci == 'oid':
        return _kunci_oid
    elif nama_kunci == 'harga':
        return _kunci_harga
    elif nama_kunci == 'selesai':
        return _kunci_selesai
    else:
        raise ValueError(f"Kunci tidak dikenal: {nama_kunci}. Pilih: oid, harga, selesai")


def _bandingkan_kunci(a, b):
    """
    Bandingkan dua nilai kunci.
    Mendukung int, tuple (untuk selesai), dsb.
    Kembalikan: -1 (a < b), 0 (a == b), 1 (a > b).
    """
    if a < b:
        return -1
    if a > b:
        return 1
    return 0


# ============================================================
#  INSERTION SORT — O(n²), stabil, di tempat
# ============================================================

BATAS_INSERTION = 20000  # Batas maksimum untuk insertion sort


def insertion_sort(data, nama_kunci, pencacah_bandingan=None, pencacah_pindah=None):
    """
    Insertion sort stabil di tempat.
    data: list Python biasa (bukan Array buatan, sudah di-copy).
    nama_kunci: 'oid', 'harga', atau 'selesai'.
    
    Syarat stabil: geser memakai '>' (bukan '>=') sehingga elemen
    dengan kunci sama tetap pada urutan semula.
    
    DITOLAK jika n > 20.000.
    
    Kembalikan: (data_terurut, jumlah_bandingan, jumlah_pindah, waktu_ms, modul, galat)
    """
    n = len(data)
    if n > BATAS_INSERTION:
        return (None, 0, 0, 0,
                "M3 - Insertion Sort",
                f"DITOLAK: {n} baris melebihi batas {BATAS_INSERTION}. "
                f"Gunakan merge sort untuk data penuh.")

    kunci_fn = _ambil_kunci(nama_kunci)
    pb = pencacah_bandingan if pencacah_bandingan else Pencacah()
    pp = pencacah_pindah if pencacah_pindah else Pencacah()

    t0 = _timer()

    for i in range(1, n):
        tmp = data[i]
        kunci_tmp = kunci_fn(tmp)
        j = i - 1
        while j >= 0:
            pb.tambah()  # Hitung perbandingan
            kunci_j = kunci_fn(data[j])
            if _bandingkan_kunci(kunci_j, kunci_tmp) > 0:
                # data[j] > tmp → geser ke kanan
                data[j + 1] = data[j]
                pp.tambah()  # Hitung pemindahan
                j -= 1
            else:
                break
        data[j + 1] = tmp
        if j + 1 != i:
            pp.tambah()  # Pemindahan final (tmp ke posisi baru)

    t1 = _timer()
    return data, pb.n, pp.n, _ms(t0, t1), "M3 - Insertion Sort", None


# ============================================================
#  MERGE SORT — O(n log n), stabil
# ============================================================

def merge_sort(data, nama_kunci, pencacah_bandingan=None, pencacah_pindah=None):
    """
    Merge sort stabil.
    data: list Python biasa.
    
    Penggabungan memakai '<=' agar elemen kiri didahulukan saat
    kunci sama (menjamin stabilitas).
    
    Kembalikan: (data_terurut, jumlah_bandingan, jumlah_pindah, waktu_ms, modul, galat)
    """
    kunci_fn = _ambil_kunci(nama_kunci)
    pb = pencacah_bandingan if pencacah_bandingan else Pencacah()
    pp = pencacah_pindah if pencacah_pindah else Pencacah()

    t0 = _timer()
    hasil = _merge_sort_rekursif(data, kunci_fn, pb, pp)
    t1 = _timer()
    return hasil, pb.n, pp.n, _ms(t0, t1), "M3 - Merge Sort", None


def _merge_sort_rekursif(data, kunci_fn, pb, pp):
    """Implementasi rekursif merge sort."""
    n = len(data)
    if n <= 1:
        return data

    tengah = n // 2
    kiri = _merge_sort_rekursif(data[:tengah], kunci_fn, pb, pp)
    kanan = _merge_sort_rekursif(data[tengah:], kunci_fn, pb, pp)
    return _gabung(kiri, kanan, kunci_fn, pb, pp)


def _gabung(kiri, kanan, kunci_fn, pb, pp):
    """
    Gabungkan dua sub-array yang sudah terurut.
    Pakai '<=' untuk elemen kiri agar stabil.
    Sisa salah satu bagian wajib disalin setelah loop utama.
    """
    hasil = [None] * (len(kiri) + len(kanan))
    i = j = k = 0

    while i < len(kiri) and j < len(kanan):
        pb.tambah()
        kunci_kiri = kunci_fn(kiri[i])
        kunci_kanan = kunci_fn(kanan[j])
        if _bandingkan_kunci(kunci_kiri, kunci_kanan) <= 0:
            # Kiri <= Kanan → ambil kiri (stabilitas)
            hasil[k] = kiri[i]
            i += 1
        else:
            hasil[k] = kanan[j]
            j += 1
        pp.tambah()
        k += 1

    # Salin sisa bagian kiri
    while i < len(kiri):
        hasil[k] = kiri[i]
        pp.tambah()
        i += 1
        k += 1

    # Salin sisa bagian kanan
    while j < len(kanan):
        hasil[k] = kanan[j]
        pp.tambah()
        j += 1
        k += 1

    return hasil


# ============================================================
#  LINEAR SEARCH — O(n)
# ============================================================

def _ekstrak_target_num(target):
    """Konversi input target (str, int, atau Pesanan) ke integer nomor OID."""
    if hasattr(target, 'oid'):
        s = target.oid
    else:
        s = str(target).strip()
    if s.startswith('O-') or s.startswith('o-'):
        return int(s[2:])
    return int(s)


def linear_search(data, target_oid, pencacah=None):
    """
    Cari pesanan dengan oid tertentu secara linear.
    data: list/iterable objek Pesanan.
    
    Kembalikan: (indeks, pesanan, jumlah_bandingan, waktu_ms, modul)
    Jika tidak ditemukan: (-1, None, jumlah_bandingan, waktu_ms, modul)
    """
    pb = pencacah if pencacah else Pencacah()
    t0 = _timer()

    try:
        target_num = _ekstrak_target_num(target_oid)
    except Exception:
        t1 = _timer()
        return -1, None, pb.n, _ms(t0, t1), "M3 - Linear Search"

    for i in range(len(data)):
        pb.tambah()
        p = data[i]
        p_num = int(p.oid[2:])
        if p_num == target_num:
            t1 = _timer()
            return i, p, pb.n, _ms(t0, t1), "M3 - Linear Search"

    t1 = _timer()
    return -1, None, pb.n, _ms(t0, t1), "M3 - Linear Search"


# ============================================================
#  BINARY SEARCH — O(log n) pada data terurut oid
# ============================================================

def binary_search(data_terurut, target_oid, pencacah=None):
    """
    Cari pesanan dengan oid tertentu secara binary search.
    data_terurut: list yang sudah terurut menurut oid (numerik).
    
    Perbandingan oid: ambil angka dari oid (O-000001 -> 1).
    Ini dipilih karena oid zero-padded 6 digit, sehingga perbandingan
    string pun benar, tapi perbandingan numerik lebih intuitif.
    
    Kembalikan: (indeks, pesanan, jumlah_bandingan, waktu_ms, modul)
    """
    pb = pencacah if pencacah else Pencacah()
    t0 = _timer()

    try:
        target_num = _ekstrak_target_num(target_oid)
    except Exception:
        t1 = _timer()
        return -1, None, pb.n, _ms(t0, t1), "M3 - Binary Search"

    lo = 0
    hi = len(data_terurut) - 1

    while lo <= hi:
        pb.tambah()
        mid = (lo + hi) // 2
        mid_num = int(data_terurut[mid].oid[2:])

        if mid_num == target_num:
            t1 = _timer()
            return mid, data_terurut[mid], pb.n, _ms(t0, t1), "M3 - Binary Search"
        elif mid_num < target_num:
            lo = mid + 1
        else:
            hi = mid - 1

    t1 = _timer()
    return -1, None, pb.n, _ms(t0, t1), "M3 - Binary Search"


# ============================================================
#  MANAJER LAPORAN
# ============================================================

class ManajerLaporan:
    """
    Manajer laporan: sorting dan searching pesanan.
    Menyimpan cache indeks terurut oid untuk binary search.
    """

    def __init__(self):
        self._cache_terurut_oid = None
        self._waktu_bangun_cache = 0

    def _bangun_cache_oid(self, manajer_pesanan):
        """
        Bangun daftar terurut oid (sekali) menggunakan merge sort.
        Kembalikan waktu pembangunan (ms).
        """
        data = manajer_pesanan.array.to_list()
        pb = Pencacah()
        pp = Pencacah()
        t0 = _timer()
        self._cache_terurut_oid = _merge_sort_rekursif(data, _kunci_oid, pb, pp)
        t1 = _timer()
        self._waktu_bangun_cache = _ms(t0, t1)
        return self._waktu_bangun_cache

    def sort_insertion(self, manajer_pesanan, nama_kunci, n=None):
        """
        Urutkan n pesanan pertama dengan insertion sort.
        Kembalikan: (data_terurut, bandingan, pindah, waktu_ms, modul, galat)
        """
        if n is None:
            n = len(manajer_pesanan.array)
        # Ambil n data pertama sebagai list biasa
        data = []
        for i in range(min(n, len(manajer_pesanan.array))):
            data.append(manajer_pesanan.array.get(i))
        return insertion_sort(data, nama_kunci)

    def sort_merge(self, manajer_pesanan, nama_kunci, n=None):
        """
        Urutkan n pesanan pertama dengan merge sort.
        Kembalikan: (data_terurut, bandingan, pindah, waktu_ms, modul, galat)
        """
        if n is None:
            n = len(manajer_pesanan.array)
        data = []
        for i in range(min(n, len(manajer_pesanan.array))):
            data.append(manajer_pesanan.array.get(i))
        return merge_sort(data, nama_kunci)

    def cari_linear(self, manajer_pesanan, target_oid):
        """
        Cari pesanan dengan linear search di array asli.
        Kembalikan: (indeks, pesanan, bandingan, waktu_ms, modul)
        """
        data = manajer_pesanan.array.to_list()
        return linear_search(data, target_oid)

    def cari_binary(self, manajer_pesanan, target_oid):
        """
        Cari pesanan dengan binary search.
        Jika cache belum ada, bangun dulu (sekali).
        Kembalikan: (indeks, pesanan, bandingan, waktu_ms, modul, info_cache)
        """
        info_cache = ""
        if self._cache_terurut_oid is None:
            wkt = self._bangun_cache_oid(manajer_pesanan)
            info_cache = f"Indeks OID dibangun sekali (merge sort): {wkt:.2f} ms"

        idx, p, banding, wkt, modul = binary_search(
            self._cache_terurut_oid, target_oid)
        return idx, p, banding, wkt, modul, info_cache

    def reset_cache(self):
        """Reset cache indeks (misalnya setelah data berubah)."""
        self._cache_terurut_oid = None
