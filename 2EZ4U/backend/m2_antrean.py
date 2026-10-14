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

class Stack:
    def __init__(self):
        self._data = [None] * 4
        self._size = 0
        self._kapasitas = 4

    def _tumbuh(self):
        kap_baru = self._kapasitas * 2
        baru = [None] * kap_baru
        for i in range(self._size):
            baru[i] = self._data[i]
        self._data = baru
        self._kapasitas = kap_baru

    def push(self, nilai):
        if self._size == self._kapasitas:
            self._tumbuh()
        self._data[self._size] = nilai
        self._size += 1

    def pop(self):
        if self._size == 0:
            return None
        self._size -= 1
        val = self._data[self._size]
        self._data[self._size] = None
        return val

    def peek(self):
        if self._size == 0:
            return None
        return self._data[self._size - 1]

    def kosong(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]
            
def _prioritas_op(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def _tokenisasi(ekspresi):
    tokens = []
    i = 0
    s = ekspresi.strip()
    while i < len(s):
        ch = s[i]
        if ch == ' ':
            i += 1
            continue
        if ch.isdigit():
            mulai = i
            while i < len(s) and s[i].isdigit():
                i += 1
            tokens.append(s[mulai:i])
        elif ch in '+-*/()':
            tokens.append(ch)
            i += 1
        else:
            i += 1
    return tokens


def ke_postfix(ekspresi):
    t0 = _timer()
    tokens = _tokenisasi(ekspresi)
    stack = Stack()
    output = []
    tabel = []
    langkah = 0

    for token in tokens:
        langkah += 1
        no = f"1.{langkah}"

        if token.isdigit():
            output.append(token)
            tabel.append((no, token, "Operand -> output",
                          _stack_str(stack), ' '.join(output)))

        elif token == '(':
            stack.push(token)
            tabel.append((no, token, "Kurung buka -> push stack",
                          _stack_str(stack), ' '.join(output)))

        elif token == ')':
            while not stack.kosong() and stack.peek() != '(':
                op = stack.pop()
                output.append(op)
            if not stack.kosong() and stack.peek() == '(':
                stack.pop()  
            tabel.append((no, token, "Kurung tutup -> pop sampai '('",
                          _stack_str(stack), ' '.join(output)))

        elif token in '+-*/':
            while (not stack.kosong() and
                   stack.peek() != '(' and
                   _prioritas_op(stack.peek()) >= _prioritas_op(token)):
                op = stack.pop()
                output.append(op)
            stack.push(token)
            tabel.append((no, token, "Operator -> pop yg >= lalu push",
                          _stack_str(stack), ' '.join(output)))

    while not stack.kosong():
        langkah += 1
        no = f"1.{langkah}"
        op = stack.pop()
        output.append(op)
        tabel.append((no, "-", f"Sisa stack -> pop '{op}'",
                      _stack_str(stack), ' '.join(output)))

    postfix_str = ' '.join(output)
    t1 = _timer()
    return postfix_str, tabel, _ms(t0, t1), "M2 - Postfix"


def hitung_postfix(postfix_str, tabel_sebelumnya=None):
    
    t0 = _timer()
    tokens = postfix_str.strip().split()
    stack = Stack()
    tabel = list(tabel_sebelumnya) if tabel_sebelumnya else []
    langkah = 0
    galat = None

    for token in tokens:
        langkah += 1
        no = f"2.{langkah}"

        if token.lstrip('-').isdigit():
            stack.push(int(token))
            tabel.append((no, token, "Angka -> push",
                          _stack_nilai_str(stack), ""))

        elif token in '+-*/':
            if len(stack) < 2:
                galat = "Ekspresi tidak valid: kurang operand"
                tabel.append((no, token, f"ERROR: {galat}",
                              _stack_nilai_str(stack), ""))
                break

            b = stack.pop() 
            a = stack.pop() 

            if token == '+':
                hasil_op = a + b
            elif token == '-':
                hasil_op = a - b
            elif token == '*':
                hasil_op = a * b
            elif token == '/':
                if b == 0:
                    galat = "Pembagian nol tidak diperbolehkan"
                    tabel.append((no, token, f"ERROR: {galat}",
                                  _stack_nilai_str(stack), ""))
                    break
                hasil_op = a / b
                if hasil_op == int(hasil_op):
                    hasil_op = int(hasil_op)

            stack.push(hasil_op)
            tabel.append((no, token,
                          f"pop {b} dan {a} -> {a}{token}{b} = {hasil_op}",
                          _stack_nilai_str(stack),
                          f"<- TOTAL Rp {hasil_op:,}".replace(',', '.') if langkah == len(tokens) else ""))
        else:
            galat = f"Token tidak dikenali: '{token}'"
            tabel.append((no, token, f"ERROR: {galat}",
                          _stack_nilai_str(stack), ""))
            break

    t1 = _timer()

    if galat:
        return None, tabel, _ms(t0, t1), "M2 - Postfix", galat

    if len(stack) != 1:
        galat = "Ekspresi tidak valid: terlalu banyak operand"
        return None, tabel, _ms(t0, t1), "M2 - Postfix", galat

    hasil = stack.pop()
    return hasil, tabel, _ms(t0, t1), "M2 - Postfix", None


def _stack_str(stack):
    items = []
    for item in stack:
        items.append(str(item))
    return ' '.join(items) if items else 'kosong'


def _stack_nilai_str(stack):
    items = []
    for item in stack:
        items.append(str(item))
    return ' '.join(items) if items else 'kosong'

class AntreanNaif:
    def __init__(self):
        self._data = [None] * 8
        self._size = 0
        self._kapasitas = 8
        self.total_geseran = 0  

    def _tumbuh(self):
        """Gandakan kapasitas saat penuh."""
        kap_baru = self._kapasitas * 2
        baru = [None] * kap_baru
        for i in range(self._size):
            baru[i] = self._data[i]
        self._data = baru
        self._kapasitas = kap_baru

    def enqueue(self, nilai):
        if self._size == self._kapasitas:
            self._tumbuh()
        self._data[self._size] = nilai
        self._size += 1

    def dequeue(self):
        if self._size == 0:
            return None, 0
        val = self._data[0]
        geseran = self._size - 1
        for i in range(self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        self.total_geseran += geseran
        return val, geseran

    def enqueue_depan(self, nilai):
        if self._size == self._kapasitas:
            self._tumbuh()
        for i in range(self._size, 0, -1):
            self._data[i] = self._data[i - 1]
        self._data[0] = nilai
        self._size += 1

    def hapus_belakang(self):
        if self._size == 0:
            return None
        self._size -= 1
        val = self._data[self._size]
        self._data[self._size] = None
        return val

    def kosong(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]

class AntreanMelingkar:
    def __init__(self, kapasitas=16):
        self.data = [None] * kapasitas
        self.front = 0
        self.rear = 0
        self.count = 0
        self._kapasitas = kapasitas

    def _tumbuh(self):
        kap_baru = self._kapasitas * 2
        baru = [None] * kap_baru
        idx = self.front
        for i in range(self.count):
            baru[i] = self.data[idx]
            idx = (idx + 1) % self._kapasitas
        self.data = baru
        self.front = 0
        self.rear = self.count
        self._kapasitas = kap_baru

    def enqueue(self, nilai):
        if self.count == self._kapasitas:
            self._tumbuh()
        self.data[self.rear] = nilai
        self.rear = (self.rear + 1) % self._kapasitas
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            return None
        val = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self._kapasitas
        self.count -= 1
        return val

    def enqueue_depan(self, nilai):
        if self.count == self._kapasitas:
            self._tumbuh()
        self.front = (self.front - 1) % self._kapasitas
        self.data[self.front] = nilai
        self.count += 1

    def hapus_belakang(self):
        if self.count == 0:
            return None
        self.rear = (self.rear - 1) % self._kapasitas
        val = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return val

    def kosong(self):
        return self.count == 0

    def __len__(self):
        return self.count

    def __iter__(self):
        idx = self.front
        for _ in range(self.count):
            yield self.data[idx]
            idx = (idx + 1) % self._kapasitas

    @property
    def kapasitas(self):
        return self._kapasitas

    def stats(self):
        """Statistik antrean melingkar: (front, rear, count, kapasitas)."""
        return (self.front, self.rear, self.count, self._kapasitas)

class ManajerAntrean:
    def __init__(self):
        self.naif = AntreanNaif()
        self.circular = AntreanMelingkar()
        self._undo_stack = Stack()
        self._redo_stack = Stack()
        self._manajer_pesanan = None 
        self.terakhir_aksi = None

    def set_manajer_pesanan(self, mp):
        self._manajer_pesanan = mp

    def muat_antrean(self, pesanan_antre):
        t0 = _timer()
        jumlah = 0
        for p in pesanan_antre:
            self.naif.enqueue(p)
            self.circular.enqueue(p)
            jumlah += 1
        t1 = _timer()
        return jumlah, _ms(t0, t1), "M2 - Antrean"

    def enqueue(self, pesanan):
        t0 = _timer()
        self.naif.enqueue(pesanan)
        self.circular.enqueue(pesanan)

        aksi = ("ENQUEUE", pesanan)
        self._undo_stack.push(aksi)
        self.terakhir_aksi = aksi
        self._kosongkan_redo()

        t1 = _timer()
        return (f"Enqueue {pesanan.oid} berhasil. "
                f"Naif: {len(self.naif)} | Circular: {len(self.circular)}",
                _ms(t0, t1), "M2 - Antrean")

    def dequeue_naif(self, k=1):
        t0 = _timer()
        keluar = []
        geseran_sesi = 0

        for _ in range(k):
            val_naif, ges = self.naif.dequeue()
            if val_naif is None:
                break
            keluar.append(val_naif)
            geseran_sesi += ges
        t1 = _timer()

        for _ in range(len(keluar)):
            self.circular.dequeue()

        if keluar:
            daftar_copy = list(keluar)
            aksi = ("DEQUEUE", daftar_copy)
            self._undo_stack.push(aksi)
            self.terakhir_aksi = aksi
            self._kosongkan_redo()

        info_c = (self.circular.front, self.circular.rear,
                  self.circular.kapasitas, len(self.circular))
        return (keluar, geseran_sesi, _ms(t0, t1), info_c,
                "M2 - Dequeue Naif")

    def dequeue_circular(self, k=1):
        t0 = _timer()
        keluar = []

        for _ in range(k):
            val_circ = self.circular.dequeue()
            if val_circ is None:
                break
            keluar.append(val_circ)
        t1 = _timer()
        
        for _ in range(len(keluar)):
            self.naif.dequeue()

        if keluar:
            daftar_copy = list(keluar)
            aksi = ("DEQUEUE", daftar_copy)
            self._undo_stack.push(aksi)
            self.terakhir_aksi = aksi
            self._kosongkan_redo()

        info_c = (self.circular.front, self.circular.rear,
                  self.circular.kapasitas, len(self.circular))
        return (keluar, 0, _ms(t0, t1), info_c,
                "M2 - Dequeue Circular")

    def undo_last(self):
        t0 = _timer()
        if self._undo_stack.kosong():
            t1 = _timer()
            return ("Tumpukan undo kosong, tidak ada yang dibatalkan.",
                    _ms(t0, t1), "M2 - Undo")

        aksi = self._undo_stack.pop()
        tipe, data = aksi

        if tipe == "ENQUEUE":
            self.naif.hapus_belakang()
            self.circular.hapus_belakang()
            self._redo_stack.push(aksi)
            pesan = f"Undo ENQUEUE {data.oid}: dihapus dari belakang kedua antrean."

        elif tipe == "DEQUEUE":
            for i in range(len(data) - 1, -1, -1):
                self.naif.enqueue_depan(data[i])
                self.circular.enqueue_depan(data[i])
            self._redo_stack.push(aksi)
            oids = ', '.join(p.oid for p in data)
            pesan = (f"Undo DEQUEUE: {len(data)} pesanan ({oids}) "
                     f"dikembalikan ke depan kedua antrean.")

        elif tipe == "ORDER":
            if self._manajer_pesanan is not None:
                idx_a = len(self._manajer_pesanan.array) - 1
                idx_l = len(self._manajer_pesanan.linklist) - 1
                if idx_a >= 0:
                    self._manajer_pesanan.array.hapus(idx_a)
                if idx_l >= 0:
                    self._manajer_pesanan.linklist.hapus(idx_l)
            self._redo_stack.push(aksi)
            pesan = f"Undo ORDER {data.oid}: pesanan dihapus."
        else:
            pesan = f"Tipe aksi tidak dikenal: {tipe}"

        t1 = _timer()
        return pesan, _ms(t0, t1), "M2 - Undo"

    def redo_last(self):
        t0 = _timer()
        if self._redo_stack.kosong():
            t1 = _timer()
            return ("Tumpukan redo kosong, tidak ada yang diulang.",
                    _ms(t0, t1), "M2 - Redo")

        aksi = self._redo_stack.pop()
        tipe, data = aksi

        if tipe == "ENQUEUE":
            self.naif.enqueue(data)
            self.circular.enqueue(data)
            self._undo_stack.push(aksi)
            pesan = f"Redo ENQUEUE {data.oid}: ditambahkan kembali."

        elif tipe == "DEQUEUE":
            for _ in data:
                self.naif.dequeue()
                self.circular.dequeue()
            self._undo_stack.push(aksi)
            oids = ', '.join(p.oid for p in data)
            pesan = f"Redo DEQUEUE: {len(data)} pesanan ({oids}) dikeluarkan lagi."

        elif tipe == "ORDER":
            if self._manajer_pesanan is not None:
                p = data
                pri = p.prioritas
                if pri == 3:
                    self._manajer_pesanan.array.append(p)
                    self._manajer_pesanan.linklist.append(p)
                elif pri == 2:
                    mid_a = len(self._manajer_pesanan.array) // 2
                    mid_l = len(self._manajer_pesanan.linklist) // 2
                    self._manajer_pesanan.array.insert(mid_a, p)
                    self._manajer_pesanan.linklist.insert(mid_l, p)
                else:
                    self._manajer_pesanan.array.insert(0, p)
                    self._manajer_pesanan.linklist.prepend(p)
            self._undo_stack.push(aksi)
            pesan = f"Redo ORDER {data.oid}: pesanan ditambahkan kembali."
        else:
            pesan = f"Tipe aksi tidak dikenal: {tipe}"

        t1 = _timer()
        return pesan, _ms(t0, t1), "M2 - Redo"

    def catat_order(self, pesanan):
        self._undo_stack.push(("ORDER", pesanan))
        self._kosongkan_redo()

    def _kosongkan_redo(self):
        while not self._redo_stack.kosong():
            self._redo_stack.pop()

    def history(self):
        undo_list = []
        for item in self._undo_stack:
            tipe, data = item
            if tipe == "DEQUEUE":
                desc = f"DEQUEUE {len(data)} pesanan"
            elif tipe == "ENQUEUE":
                desc = f"ENQUEUE {data.oid}"
            elif tipe == "ORDER":
                desc = f"ORDER {data.oid}"
            else:
                desc = str(item)
            undo_list.append((tipe, desc))

        redo_list = []
        for item in self._redo_stack:
            tipe, data = item
            if tipe == "DEQUEUE":
                desc = f"DEQUEUE {len(data)} pesanan"
            elif tipe == "ENQUEUE":
                desc = f"ENQUEUE {data.oid}"
            elif tipe == "ORDER":
                desc = f"ORDER {data.oid}"
            else:
                desc = str(item)
            redo_list.append((tipe, desc))

        return undo_list, redo_list

    def stats(self):
        return (len(self.naif), len(self.circular),
                self.circular.kapasitas,
                self.naif.total_geseran,
                len(self._undo_stack), len(self._redo_stack))

def hitung_struk(ekspresi):
    t0 = _timer()
    postfix_str, tabel_konversi, _, _ = ke_postfix(ekspresi)
    hasil, tabel_lengkap, _, _, galat = hitung_postfix(postfix_str, tabel_konversi)
    t1 = _timer()
    return postfix_str, hasil, tabel_lengkap, _ms(t0, t1), "M2 - Postfix", galat


def hitung(postfix):
    hasil, _, _, _, galat = hitung_postfix(postfix)
    if galat:
        raise ValueError(galat)
    return hasil
    
stack = Stack
queue = AntreanMelingkar
