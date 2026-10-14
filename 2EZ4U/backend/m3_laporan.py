import time as _time

class Pencacah:
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

def _kunci_oid(p):
    return int(p.oid[2:])


def _kunci_harga(p):
    return p.harga


def _kunci_selesai(p):
    if p.t_selesai_detik is None:
        return (1, 0)
    return (0, p.t_selesai_detik)


def _ambil_kunci(nama_kunci):
    if nama_kunci == 'oid':
        return _kunci_oid
    elif nama_kunci == 'harga':
        return _kunci_harga
    elif nama_kunci == 'selesai':
        return _kunci_selesai
    else:
        raise ValueError(f"Kunci tidak dikenal: {nama_kunci}. Pilih: oid, harga, selesai")


def _bandingkan_kunci(a, b):
    if a < b:
        return -1
    if a > b:
        return 1
    return 0
    
BATAS_INSERTION = 20000  

def insertion_sort(data, nama_kunci, pencacah_bandingan=None, pencacah_pindah=None):
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
            pb.tambah()
            kunci_j = kunci_fn(data[j])
            if _bandingkan_kunci(kunci_j, kunci_tmp) > 0:
                data[j + 1] = data[j]
                pp.tambah()
                j -= 1
            else:
                break
        data[j + 1] = tmp
        if j + 1 != i:
            pp.tambah()

    t1 = _timer()
    return data, pb.n, pp.n, _ms(t0, t1), "M3 - Insertion Sort", None

def merge_sort(data, nama_kunci, pencacah_bandingan=None, pencacah_pindah=None):
    kunci_fn = _ambil_kunci(nama_kunci)
    pb = pencacah_bandingan if pencacah_bandingan else Pencacah()
    pp = pencacah_pindah if pencacah_pindah else Pencacah()

    t0 = _timer()
    hasil = _merge_sort_rekursif(data, kunci_fn, pb, pp)
    t1 = _timer()
    return hasil, pb.n, pp.n, _ms(t0, t1), "M3 - Merge Sort", None


def _merge_sort_rekursif(data, kunci_fn, pb, pp):
    n = len(data)
    if n <= 1:
        return data

    tengah = n // 2
    kiri = _merge_sort_rekursif(data[:tengah], kunci_fn, pb, pp)
    kanan = _merge_sort_rekursif(data[tengah:], kunci_fn, pb, pp)
    return _gabung(kiri, kanan, kunci_fn, pb, pp)


def _gabung(kiri, kanan, kunci_fn, pb, pp):
    hasil = [None] * (len(kiri) + len(kanan))
    i = j = k = 0

    while i < len(kiri) and j < len(kanan):
        pb.tambah()
        kunci_kiri = kunci_fn(kiri[i])
        kunci_kanan = kunci_fn(kanan[j])
        if _bandingkan_kunci(kunci_kiri, kunci_kanan) <= 0:
            hasil[k] = kiri[i]
            i += 1
        else:
            hasil[k] = kanan[j]
            j += 1
        pp.tambah()
        k += 1

    while i < len(kiri):
        hasil[k] = kiri[i]
        pp.tambah()
        i += 1
        k += 1

    while j < len(kanan):
        hasil[k] = kanan[j]
        pp.tambah()
        j += 1
        k += 1

    return hasil

def _ekstrak_target_num(target):
    if hasattr(target, 'oid'):
        s = target.oid
    else:
        s = str(target).strip()
    if s.startswith('O-') or s.startswith('o-'):
        return int(s[2:])
    return int(s)


def linear_search(data, target_oid, pencacah=None):
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

def binary_search(data_terurut, target_oid, pencacah=None):
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

class ManajerLaporan:
    def __init__(self):
        self._cache_terurut_oid = None
        self._waktu_bangun_cache = 0

    def _bangun_cache_oid(self, manajer_pesanan):
        data = manajer_pesanan.array.to_list()
        pb = Pencacah()
        pp = Pencacah()
        t0 = _timer()
        self._cache_terurut_oid = _merge_sort_rekursif(data, _kunci_oid, pb, pp)
        t1 = _timer()
        self._waktu_bangun_cache = _ms(t0, t1)
        return self._waktu_bangun_cache

    def sort_insertion(self, manajer_pesanan, nama_kunci, n=None):
        if n is None:
            n = len(manajer_pesanan.array)
        data = []
        for i in range(min(n, len(manajer_pesanan.array))):
            data.append(manajer_pesanan.array.get(i))
        return insertion_sort(data, nama_kunci)

    def sort_merge(self, manajer_pesanan, nama_kunci, n=None):
        if n is None:
            n = len(manajer_pesanan.array)
        data = []
        for i in range(min(n, len(manajer_pesanan.array))):
            data.append(manajer_pesanan.array.get(i))
        return merge_sort(data, nama_kunci)

    def cari_linear(self, manajer_pesanan, target_oid):
        data = manajer_pesanan.array.to_list()
        return linear_search(data, target_oid)

    def cari_binary(self, manajer_pesanan, target_oid):
        info_cache = ""
        if self._cache_terurut_oid is None:
            wkt = self._bangun_cache_oid(manajer_pesanan)
            info_cache = f"Indeks OID dibangun sekali (merge sort): {wkt:.2f} ms"

        idx, p, banding, wkt, modul = binary_search(
            self._cache_terurut_oid, target_oid)
        return idx, p, banding, wkt, modul, info_cache

    def reset_cache(self):
        self._cache_terurut_oid = None
