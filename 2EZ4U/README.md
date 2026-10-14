# Proyek "2EZ4U APP"
**Studi Kasus Proyek Akhir Struktur Data & Analisa Algoritma (EC234303)**  
*Program Sarjana, Departemen Teknik Komputer, FTEIC - Institut Teknologi Sepuluh Nopember (ITS)*  
*Dosen Pengampu: Ir. Arta Kusuma Hernanda, S.T., M.T.*

---

## 1. Deskripsi Proyek

**2EZ4U App** adalah engine backend dan antarmuka desktop untuk sistem layanan pengantaran makanan dan barang (*delivery service* menyerupai versi mini dari GoFood, GrabFood, atau ShopeeFood). Proyek ini dirancang untuk menangani beban data berskala besar (200.000 entri pesanan) dengan mengimplementasikan struktur data dan algoritma klasik buatan sendiri tanpa memanfaatkan fungsi-fungsi instan bawaan bahasa pemrograman.

### Aturan Main & Batasan Kritis
Sesuai panduan proyek:
1. **Dilarang menggunakan pustaka instan**: Tidak menggunakan `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, `collections.*`, literal `{}` kosong/isi, maupun comprehension dict/set.
2. **List Python murni sebagai petak memori mentah (*raw array*)**: Semua operasi penambahan, pergeseran (*shift*), dan alokasi ulang memori diimplementasikan manual secara Object-Oriented Programming (OOP).
3. **Pencatatan Perbandingan Objektif**: Jumlah perbandingan (*comparisons*) dan pergeseran/pemindahan (*moves/shifts*) dicatat menggunakan kelas `Pencacah` mandiri agar evaluasi komputasi tidak bias oleh perbedaan spesifikasi perangkat keras.

---

## 2. Struktur Repositori

```text
2EZ4U/
|-- README.md             <- Laporan teknis lengkap & dokumentasi proyek
|-- app.py                <- Entry point utama ("python app.py")
|-- bench_m3.py           <- Skrip pengujian benchmark skala n vs perbandingan
|-- generate_csv.py       <- Skrip generator data sintetis 200.000 pesanan
|
|-- data/
|   |-- pesanan.csv       <- Dataset 200.000 baris pesanan
|   `-- peta.csv          <- Graf koneksi restoran dan gedung kampus
|
|-- backend/
|   |-- __init__.py
|   |-- m1_pesanan.py     <- M1: Array Dinamis & Singly Linked List
|   |-- m2_antrean.py     <- M2: Stack (Postfix, Undo/Redo) & Queue (Naif & Circular)
|   `-- m3_laporan.py     <- M3: Insertion Sort, Merge Sort, Linear & Binary Search
|
|-- frontend/
|   |-- __init__.py
|   `-- ui.py             <- Antarmuka desktop Tkinter 3 panel terintegrasi
|
`-- tests/
    |-- __init__.py
    |-- test_m1.py        <- Unit test M1 (Array & Linked List)
    |-- test_m2.py        <- Unit test M2 (Stack, Postfix, Queue, Undo/Redo)
    `-- test_m3.py        <- Unit test M3 (Sorting, Searching, Stabilitas, Aturan)
```

---

## 3. Pembahasan Teknis Milestone 1 s/d Milestone 3

### 3.1 Milestone 1: Array Dinamis vs Singly Linked List (`backend/m1_pesanan.py`)

Data pesanan disimpan secara berdampingan pada dua struktur data:
1. **`Array` (Larik Dinamis)**: Mengalokasikan blok memori berukuran tetap. Ketika kapasitas penuh, dialokasikan blok baru sebesar $2\times$ kapasitas sebelumnya (*doubling strategy*), seluruh elemen disalin, lalu blok lama dibuang. Hal ini menjamin biaya penambahan di akhir (*append*) bernilai **amortized $O(1)$**.
2. **`LinkList` (Singly Linked List)**: Tiap pesanan dibungkus simpul `Node` dengan atribut pointer `next`. Memiliki pointer `head` (depan) dan `tail` (belakang) sehingga penambahan di ujung depan (*prepend*) dan belakang (*append*) bernilai $O(1)$ konstan.

#### Perbandingan 3 Aturan Bisnis Penyisipan:
| Jenis Pesanan | Posisi Sisip | Kompleksitas Array | Kompleksitas Linked List | Mekanisme Komputasi |
| :--- | :--- | :---: | :---: | :--- |
| **REGULER (3)** | Paling belakang | $O(1)$ amortized | $O(1)$ | Menempel di ujung akhir; Linked List langsung memanfaatkan pointer `tail`. |
| **PRIORITAS (2)** | Tengah barisan ($n/2$) | $O(n)$ | $O(n)$ | Array menggeser $\approx 100.000$ elemen ke kanan; Linked List menelusuri $\approx 100.000$ simpul lalu menyambungkan pointer `next`. |
| **VIP (1)** | Urutan pertama (indeks 0) | $O(n)$ | $O(1)$ | Array wajib menggeser seluruh $200.000$ elemen ke kanan; Linked List hanya mengubah pointer `head = new_node`. |

---

### 3.2 Milestone 2: Stack & Queue (`backend/m2_antrean.py`)

#### A. Mesin Kasir Infix ke Postfix & Evaluasi
Struk kasir seperti `( 3 * 12000 ) + ( 2 * 8500 ) - 5000` diproses dalam 2 tahap menggunakan `Stack`:
1. **Konversi Infix $\to$ Postfix (Algoritma Shunting-Yard)**:
   - Token angka berdigit banyak (misal `12000`) disatukan dalam satu token utuh.
   - Operand langsung diteruskan ke string keluaran.
   - Operator `*` dan `/` memiliki presedensi lebih tinggi (2) dibanding `+` dan `-` (1).
   - Tanda kurung buka `(` didorong ke stack; tanda kurung tutup `)` mem-pop stack hingga bertemu `(`.
2. **Evaluasi Postfix**:
   - Angka didorong ke stack nilai.
   - Saat operator ditemukan, dua operand teratas di-pop: **operand kanan ($b$) keluar lebih dahulu, baru operand kiri ($a$)**, lalu dihitung $a - b$ atau $a / b$. Urutan pop ini mutlak krusial untuk menjaga kebenaran operasi non-komutatif.

#### B. Antrean: Naif vs Melingkar (Circular)
- **`AntreanNaif`**: Mengambil elemen indeks 0 via pergeseran seluruh sisa elemen ke kiri. Untuk $20.000$ antrean, melayani 1 pelanggan membutuhkan $19.999$ pergeseran memori ($O(n)$ per dequeue).
- **`AntreanMelingkar`**: Menggunakan penunjuk `front` dan `rear` berputar dengan operasi modulo `(idx + 1) % kapasitas`. Elemen keluar dalam $O(1)$ konstan tanpa pergeseran memori sama sekali (0 elemen digeser).

> **Mengapa Harus Ada Atribut `count` pada Antrean Melingkar?**  
> Jika antrean melingkar hanya menyimpan penunjuk `front` dan `rear`, kondisi **antrean kosong** (`front == rear`) dan kondisi **antrean penuh** (`front == rear` setelah memutar penuh) bernilai identik dan ambigu.  
> Terdapat dua pendekatan baku: (1) Menyisakan 1 slot kosong, atau (2) Menyimpan pencacah `count`. Kami memilih **menyimpan pencacah `count`** karena:
> 1. Memanfaatkan kapasitas array $100\%$ tanpa membuang 1 slot memori.
> 2. Pengecekan `count == 0` (kosong) dan `count == kapasitas` (penuh) sangat eksplisit, deterministik, dan mempermudah logika ekspansi buffer memori $2\times$ secara aman.

#### C. Mekanisme Undo & Redo (Dua Stack)
- Setiap mutasi antrean (`ENQUEUE` atau `DEQUEUE`) di-push ke `undo_stack` bersama salinan data pesanan terkait.
- **Aksi Undo `DEQUEUE`**: Mengembalikan pesanan yang keluar ke **DEPAN antrean** (bukan belakang) dengan urutan semula.
- **Aksi Undo `ENQUEUE`**: Mengeluarkan pesanan yang baru masuk dari belakang antrean.
- **Pengosongan Redo Stack**: Begitu pengguna melakukan aksi baru, `redo_stack` **wajib dikosongkan**. Hal ini mencegah percabangan riwayat (*history divergence*) yang dapat merusak integritas urutan antrean.

---

### 3.3 Milestone 3: Sorting & Searching (`backend/m3_laporan.py`)

#### A. Algoritma Pengurutan (Sorting)
1. **Insertion Sort**: Beroperasi di tempat (*in-place*) dengan kompleksitas rata-rata $O(n^2)$. Dibuat stabil dengan syarat penggeseran memakai operator lebih besar (`>`), bukan `>=`. Untuk mencegah antarmuka grafis *freeze/hang*, pesanan dengan $n > 20.000$ baris **secara otomatis ditolak** dengan pesan edukatif.
2. **Merge Sort**: Beroperasi secara rekursif membagi array menjadi dua bagian ($O(n \log n)$). Penggabungan (*merge*) dijamin stabil dengan menggunakan operator pembanding `<=` agar elemen sub-array kiri selalu didahulukan saat memiliki kunci sama.

#### B. Algoritma Pencarian (Searching)
1. **Linear Search ($O(n)$)**: Memeriksa elemen satu per satu dari awal. Tidak menuntut data terurut.
2. **Binary Search ($O(\log n)$)**: Menuntut data terurut menurut kunci `oid`. Setiap perbandingan mengeliminasi separuh ruang pencarian ($\le 18$ perbandingan pada $200.000$ data). Indeks terurut dibangun satu kali (*one-time indexing*) menggunakan Merge Sort.

---

## 4. Hasil Benchmark Eksperimental

Data di bawah ini diperoleh secara riil dari eksekusi skrip `bench_m3.py` pada dataset $200.000$ baris `data/pesanan.csv`:

### 4.1 Tabel Skala $n$ vs Perbandingan dan Waktu Pengurutan

| $n$ (Baris) | Insertion Sort (Perbandingan) | Merge Sort (Perbandingan) | Waktu Insertion (ms) | Waktu Merge (ms) |
| :---: | :---: | :---: | :---: | :---: |
| **1.000** | 236.597 | 8.604 | 43,91 ms | 2,48 ms |
| **2.000** | 935.340 | 19.251 | 173,77 ms | 5,62 ms |
| **4.000** | 3.699.256 | 42.294 | 714,80 ms | 13,89 ms |
| **8.000** | 14.875.579 | 92.438 | 3.467,47 ms | 54,05 ms |

#### Analisis Rasio Pertumbuhan:
- **Insertion Sort**: Ketika $n$ dilipatduakan ($2\times$), perbandingan bertambah $\approx 3,95\times - 4,02\times$ lipat (mendekati teori kuadratik $2^2 = 4$).
- **Merge Sort**: Ketika $n$ dilipatduakan ($2\times$), perbandingan bertambah $\approx 2,19\times - 2,24\times$ lipat (mendekati teori linearitmik $\frac{2n \log 2n}{n \log n}$).

```text
GRAFIK PERTUMBUHAN JUMLAH PERBANDINGAN:
n = 1.000:
  Merge    : [█] (8.604)
  Insertion: [██████] (236.597)
n = 2.000:
  Merge    : [██] (19.251)
  Insertion: [████████████████████████] (935.340)
n = 4.000:
  Merge    : [████] (42.294)
  Insertion: [████████████████████████████████████████████████████████████████] (3.699.256)
n = 8.000:
  Merge    : [█████████] (92.438)
  Insertion: [>>>> TUMBUH KUADRATIK MELEWATI SKALA LAYAR >>>>] (14.875.579)
```

### 4.2 Benchmark Pencarian: Linear vs Binary Search (OID `O-008000` pada 200.000 Data)

| Parameter | Linear Search ($O(n)$) | Binary Search ($O(\log n)$) | Rasio Efisiensi |
| :--- | :---: | :---: | :---: |
| **Jumlah Perbandingan** | 8.000 kali | 15 kali | **$533,3\times$ lebih sedikit** |
| **Waktu Eksekusi** | 1,8737 ms | 0,0279 ms | **$\approx 67\times$ lebih cepat** |
| **Persyaratan Data** | Bebas (acak / tidak terurut) | Wajib terurut menurut OID | - |

---

## 5. Cara Menjalankan

### Persyaratan Lingkungan
- Python versi 3.11 atau lebih baru (direkomendasikan Python 3.12+).
- Pustaka standar `tkinter` (bawaan instalasi Python Windows/macOS/Linux).

### 1. Menjalankan Aplikasi Utama (GUI Tkinter)
```bash
python app.py
```
*Langkah:* Klik menu **DATA $\to$ Load** untuk memuat dataset 200.000 baris. Setelah selesai, seluruh fitur M1, M2, dan M3 siap digunakan secara interaktif.

### 2. Menjalankan Skrip Benchmark Skala M3
```bash
python bench_m3.py
```

### 3. Menjalankan Seluruh Unit Test (88 Uji Mandiri)
```bash
python -m unittest discover tests
```

---

## 6. Checklist Verifikasi Kelulusan (M1 s/d M3)

- [x] **M1**: Struktur `Array` dinamis buatan sendiri dengan doubling capacity $2\times$ (amortized $O(1)$).
- [x] **M1**: Struktur `LinkList` dengan pointer `head` dan `tail` ($O(1)$ append & prepend).
- [x] **M1**: Tiga aturan bisnis penambahan pesanan (Reguler, Prioritas $n/2$, VIP indeks 0).
- [x] **M1**: Fitur lihat dan hapus pesanan ke-$i$ di kedua struktur.
- [x] **M2**: Struktur `Stack` LIFO buatan sendiri di atas larik raw.
- [x] **M2**: Evaluasi struk belanja kasir Infix $\to$ Postfix (Shunting-Yard) dengan multi-digit tokenizer.
- [x] **M2**: Evaluasi postfix dengan penanganan urutan pop yang benar untuk operator non-komutatif.
- [x] **M2**: Antrean Naif ($O(n)$ geser) vs Antrean Melingkar ($O(1)$ circular pointer modulo).
- [x] **M2**: Penanganan kondisi batas antrean melingkar dengan atribut `count`.
- [x] **M2**: Fitur Undo & Redo dua tumpukan dengan pengosongan tumpukan redo pada aksi baru.
- [x] **M3**: `insertion_sort` stabil di tempat dengan pelaporan jumlah perbandingan & pemindahan.
- [x] **M3**: `merge_sort` stabil rekursif dengan pelaporan jumlah perbandingan & pemindahan.
- [x] **M3**: Insertion sort secara ramah menolak input $n > 20.000$ baris agar UI tidak hang.
- [x] **M3**: `linear_search` $O(n)$ dan `binary_search` $O(\log n)$ teruji pada 4 kasus batas (tengah, kiri, kanan, tidak ada, larik kosong).
- [x] **Aturan Integritas**: 0 penggunaan `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, `collections.*`, maupun `{}` literal di backend.
- [x] **Antarmuka Desktop**: Tkinter terintegrasi 3 bagian (navigasi kiri, parameter & tabel kanan, panel COMMAND & catatan edukatif bawah).
