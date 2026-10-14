import csv
import time as _time

class Pencacah:
    __slots__ = ('n',)

    def __init__(self):
        self.n = 0

    def tambah(self, k=1):
        self.n += k

    def reset(self):
        self.n = 0


def format_waktu(detik):
    if detik is None or detik == '':
        return '-'
    detik = int(detik)
    jam = detik // 3600
    menit = (detik % 3600) // 60
    det = detik % 60
    return f"{jam:02d}:{menit:02d}:{det:02d}"


def format_harga(harga):
    s = str(int(harga))
    hasil = []
    for idx, c in enumerate(reversed(s)):
        if idx > 0 and idx % 3 == 0:
            hasil.append('.')
        hasil.append(c)
    return ''.join(reversed(hasil))


def _timer():
    return _time.perf_counter()


def _ms(awal, akhir):
    return (akhir - awal) * 1000.0


def timer(fungsi, *args, **kwargs):
    t0 = _time.perf_counter()
    hasil = fungsi(*args, **kwargs)
    t1 = _time.perf_counter()
    return hasil, (t1 - t0) * 1000.0
    
class Pesanan:
    __slots__ = ('oid', 'pelanggan', 'resto', 'menu', 'harga',
                 'prioritas', 't_masuk_detik', 't_selesai_detik', 'status')

    def __init__(self, oid, pelanggan, resto, menu, harga,
                 prioritas, t_masuk_detik, t_selesai_detik, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = int(harga) if harga != '' else 0
        self.prioritas = int(prioritas) if prioritas != '' else 3
        self.t_masuk_detik = int(t_masuk_detik) if str(t_masuk_detik) != '' else 0
        self.t_selesai_detik = (int(t_selesai_detik)
                                if str(t_selesai_detik) != '' else None)
        self.status = status

    def __repr__(self):
        return f"Pesanan({self.oid}, {self.pelanggan})"
        
class Array:
    def __init__(self, kapasitas=4):
        self._data = [None] * kapasitas
        self._size = 0
        self._kapasitas = kapasitas

    def _tumbuh(self):
        kap_baru = self._kapasitas * 2
        baru = [None] * kap_baru
        for i in range(self._size):
            baru[i] = self._data[i]
        self._data = baru
        self._kapasitas = kap_baru

    def append(self, nilai):
        if self._size == self._kapasitas:
            self._tumbuh()
        self._data[self._size] = nilai
        self._size += 1

    def insert(self, i, nilai, pencacah=None):
        if i < 0 or i > self._size:
            raise ValueError(f"Indeks {i} di luar jangkauan (0..{self._size})")
        if self._size == self._kapasitas:
            self._tumbuh()
        #geser elemen ke kanan satu per satu
        j = self._size
        while j > i:
            self._data[j] = self._data[j - 1]
            if pencacah is not None:
                pencacah.tambah()
            j -= 1
        self._data[i] = nilai
        self._size += 1

    def get(self, i):
        if i < 0 or i >= self._size:
            raise ValueError(f"Indeks {i} di luar jangkauan (0..{self._size - 1})")
        return self._data[i]

    def set_item(self, i, nilai):
        if i < 0 or i >= self._size:
            raise ValueError(f"Indeks {i} di luar jangkauan (0..{self._size - 1})")
        self._data[i] = nilai

    def hapus(self, i, pencacah=None):
        if i < 0 or i >= self._size:
            raise ValueError(f"Indeks {i} di luar jangkauan (0..{self._size - 1})")
        val = self._data[i]
        #geser elemen ke kiri
        j = i
        while j < self._size - 1:
            self._data[j] = self._data[j + 1]
            if pencacah is not None:
                pencacah.tambah()
            j += 1
        self._data[self._size - 1] = None
        self._size -= 1
        return val

    def __len__(self):
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]

    @property
    def kapasitas(self):
        return self._kapasitas

    def slice(self, mulai, jumlah):
        hasil = []
        akhir = min(mulai + jumlah, self._size)
        for i in range(mulai, akhir):
            hasil.append(self._data[i])
        return hasil

    def to_list(self):
        hasil = [None] * self._size
        for i in range(self._size):
            hasil[i] = self._data[i]
        return hasil

class Node:
    __slots__ = ('nilai', 'next')

    def __init__(self, nilai):
        self.nilai = nilai
        self.next = None


class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, nilai):
        baru = Node(nilai)
        if self.tail is None:
            self.head = baru
            self.tail = baru
        else:
            self.tail.next = baru
            self.tail = baru
        self._size += 1

    def prepend(self, nilai):
        baru = Node(nilai)
        baru.next = self.head
        self.head = baru
        if self.tail is None:
            self.tail = baru
        self._size += 1

    def insert(self, i, nilai, pencacah=None):
        if i < 0 or i > self._size:
            raise ValueError(f"Indeks {i} di luar jangkauan (0..{self._size})")
        if i == 0:
            self.prepend(nilai)
            return
        if i == self._size:
            self.append(nilai)
            return
        baru = Node(nilai)
        cur = self.head
        for step in range(i - 1):
            cur = cur.next
            if pencacah is not None:
                pencacah.tambah()
        baru.next = cur.next
        cur.next = baru
        self._size += 1

    def get(self, i):
        if i < 0 or i >= self._size:
            raise ValueError(f"Indeks {i} di luar jangkauan (0..{self._size - 1})")
        cur = self.head
        for _ in range(i):
            cur = cur.next
        return cur.nilai

    def hapus(self, i, pencacah=None):
        if i < 0 or i >= self._size:
            raise ValueError(f"Indeks {i} di luar jangkauan (0..{self._size - 1})")
        if i == 0:
            val = self.head.nilai
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self._size -= 1
            return val
        cur = self.head
        for step in range(i - 1):
            cur = cur.next
            if pencacah is not None:
                pencacah.tambah()
        val = cur.next.nilai
        if cur.next == self.tail:
            self.tail = cur
        cur.next = cur.next.next
        self._size -= 1
        return val

    def __len__(self):
        return self._size

    def __iter__(self):
        cur = self.head
        while cur is not None:
            yield cur.nilai
            cur = cur.next

    def slice(self, mulai, jumlah):
        hasil = []
        cur = self.head
        idx = 0
        while cur is not None and idx < mulai:
            cur = cur.next
            idx += 1
        count = 0
        while cur is not None and count < jumlah:
            hasil.append(cur.nilai)
            cur = cur.next
            count += 1
        return hasil

    def to_list(self):
        hasil = []
        cur = self.head
        while cur is not None:
            hasil.append(cur.nilai)
            cur = cur.next
        return hasil

class ManajerPesanan:
    def __init__(self):
        self.array = Array(256)
        self.linklist = LinkList()
        self._next_oid_num = 1
        self._dimuat = False

    def muat_csv(self, path):
        t0 = _timer()
        self.array = Array(262144)    # 2^18
        self.linklist = LinkList()
        max_oid = 0

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                p = Pesanan(
                    oid=row[0], pelanggan=row[1], resto=row[2],
                    menu=row[3], harga=row[4], prioritas=row[5],
                    t_masuk_detik=row[6], t_selesai_detik=row[7],
                    status=row[8]
                )
                self.array.append(p)
                self.linklist.append(p)
                num = int(row[0].split('-')[1])
                if num > max_oid:
                    max_oid = num

        self._next_oid_num = max_oid + 1
        self._dimuat = True
        t1 = _timer()
        return len(self.array), _ms(t0, t1), "M1 - Load"

    @property
    def sudah_dimuat(self):
        return self._dimuat

    def _oid_berikutnya(self):
        oid = f"O-{self._next_oid_num:06d}"
        self._next_oid_num += 1
        return oid
        
    def lihat_array(self, indeks, jumlah=10):
        t0 = _timer()
        if indeks < 0 or indeks >= len(self.array):
            t1 = _timer()
            return [], _ms(t0, t1), "Indeks di luar jangkauan", "M1 - Array Lihat"
        data = self.array.slice(indeks, jumlah)
        t1 = _timer()
        return (data, _ms(t0, t1),
                f"{len(data)} baris dari indeks {indeks}", "M1 - Array Lihat")

    def lihat_linklist(self, indeks, jumlah=10):
        t0 = _timer()
        if indeks < 0 or indeks >= len(self.linklist):
            t1 = _timer()
            return [], _ms(t0, t1), "Indeks di luar jangkauan", "M1 - LinkList Lihat"
        data = self.linklist.slice(indeks, jumlah)
        t1 = _timer()
        return (data, _ms(t0, t1),
                f"{len(data)} baris dari indeks {indeks}", "M1 - LinkList Lihat")

    def tambah_array(self, pelanggan, resto, menu_item, harga, prioritas):
        t0 = _timer()
        oid = self._oid_berikutnya()
        p = Pesanan(oid, pelanggan, resto, menu_item, harga,
                    prioritas, 0, '', 'ANTRE')
        pencacah = Pencacah()

        if prioritas == 3:
            posisi = len(self.array)
            self.array.append(p)
        elif prioritas == 2:
            posisi = len(self.array) // 2
            self.array.insert(posisi, p, pencacah)
        else:
            posisi = 0
            self.array.insert(0, p, pencacah)

        t1 = _timer()
        return p, posisi, _ms(t0, t1), pencacah.n, "M1 - Array Tambah"

    def tambah_linklist(self, pelanggan, resto, menu_item, harga, prioritas):
        t0 = _timer()
        oid = self._oid_berikutnya()
        p = Pesanan(oid, pelanggan, resto, menu_item, harga,
                    prioritas, 0, '', 'ANTRE')
        pencacah = Pencacah()

        if prioritas == 3:
            posisi = len(self.linklist)
            self.linklist.append(p)
        elif prioritas == 2:
            posisi = len(self.linklist) // 2
            self.linklist.insert(posisi, p, pencacah)
        else:
            posisi = 0
            self.linklist.prepend(p)

        t1 = _timer()
        return p, posisi, _ms(t0, t1), pencacah.n, "M1 - LinkList Tambah"

    def tambah_kedua(self, pelanggan, resto, menu_item, harga, prioritas):
        oid = self._oid_berikutnya()
        p = Pesanan(oid, pelanggan, resto, menu_item, harga,
                    prioritas, 0, '', 'ANTRE')

        pencacah_a = Pencacah()
        t0a = _timer()
        if prioritas == 3:
            pos_a = len(self.array)
            self.array.append(p)
        elif prioritas == 2:
            pos_a = len(self.array) // 2
            self.array.insert(pos_a, p, pencacah_a)
        else:
            pos_a = 0
            self.array.insert(0, p, pencacah_a)
        t1a = _timer()

        pencacah_l = Pencacah()
        t0l = _timer()
        if prioritas == 3:
            pos_l = len(self.linklist)
            self.linklist.append(p)
        elif prioritas == 2:
            pos_l = len(self.linklist) // 2
            self.linklist.insert(pos_l, p, pencacah_l)
        else:
            pos_l = 0
            self.linklist.prepend(p)
        t1l = _timer()

        return (p,
                (pos_a, _ms(t0a, t1a), pencacah_a.n, "M1 - Array Tambah"),
                (pos_l, _ms(t0l, t1l), pencacah_l.n, "M1 - LinkList Tambah"))

    def hapus_array(self, indeks):
        pencacah = Pencacah()
        t0 = _timer()
        val = self.array.hapus(indeks, pencacah)
        t1 = _timer()
        return val, _ms(t0, t1), pencacah.n, "M1 - Array Hapus"

    def hapus_linklist(self, indeks):
        pencacah = Pencacah()
        t0 = _timer()
        val = self.linklist.hapus(indeks, pencacah)
        t1 = _timer()
        return val, _ms(t0, t1), pencacah.n, "M1 - LinkList Hapus"

    def pesanan_antre(self):
        for p in self.array:
            if p.status == 'ANTRE':
                yield p

    def jumlah_data(self):
        """Jumlah data di kedua struktur."""
        return len(self.array), len(self.linklist)
