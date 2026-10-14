Fokus utama dari (M1) dalam proyek aplikasi "2EZ4U" ini adalah mempelajari dan membandingkan performa antara dua struktur data dasar: Array (Larik) dan Linked List (Rantai). Poin-poin penting mengenai apa saja yang dikerjakan pada M1:
1.	Menyimpan Data yang Sama di Dua Struktur Sekaligus. Backend membaca data pesanan, lalu menyimpannya secara bersamaan ke dalam struktur Array dan Linked List buatan sendiri.
2.	Mengimplementasikan 5 Operasi Utama. Kedua struktur data tersebut harus mampu melayani lima operasi yang persis sama agar kinerjanya dapat diadu langsung melalui antarmuka Tkinter:
   - Melihat pesanan ke-i (buka detail pesanan).
   - Menambah pesanan REGULER (masuk ke barisan paling belakang).
   - Menambah pesanan PRIORITAS (menyerobot ke tengah barisan).
   - Mnambah pesanan VIP (langsung ke urutan pertama).
   - Menghapus pesanan ke-i (mencabut pesanan dari antrean).
3.	Menganalisis Perbedaan Kompleksitas Waktu (O notation). M1 memperlihatkan keunggulan dan kelemahan masing-masing struktur berdasarkan letak penyisipannya. Misalnya, Linked List sangat efisien untuk penambahan VIP (O(1)) karena tinggal mengubah penunjuk (pointer) tanpa menggeser data, sementara Array membutuhkan proses penggeseran elemen yang lebih mahal (O(n)).
  M1 bertujuan membuktikan secara praktis bagaimana pemilihan struktur data (Array vs Linked List) memengaruhi kecepatan eksekusi program saat menangani data dalam jumlah besar (200.000 baris).

Fokus utama dari M2 dalam proyek "2EZ4U" adalah implementasi Stack (Tumpukan) dan Queue (Antrean) serta fitur pendukungnya seperti undo/redo dan mesin kasir berbasis notasi postfix. 
1. Stack untuk Mesin Kasir (Infix ke Postfix)
	- Mengubah struk belanja dari bentuk infix (misalnya: (3*12000)+(2*8500)-5000) menjadi postfix menggunakan stack operator. 
	- Mengevaluasi hasil postfix tersebut menggunakan stack angka untuk mendapatkan total harga belanja secara akurat. 
2. Stack untuk Fitur Undo dan Redo
	- Mencatat setiap aksi yang mengubah keadaan (seperti order, enqueue, dequeue) ke dalam tumpukan undo beserta informasi pembalikannya. 
	- Tombol undo_last() berfungsi membatalkan aksi terakhir, sedangkan redo_last() mengerjakan ulang aksi yang sempat dibatalkan (dengan aturan tumpukan redo harus dikosongkan jika ada aksi baru). 
3. Perbandingan Queue (Antrean Naif vs Antrean Melingkar)
	- Queue Naif: Menggunakan larik biasa di mana proses dequeue mengambil elemen indeks 0 dan memaksa seluruh sisa elemen bergeser ke kiri, menghasilkan biaya O(n). 
	- Queue Melingkar (Circular Queue): Menggunakan penunjuk front, rear, dan count (atau kapasitas) dengan operasi modulo, sehingga proses melayani pesanan cukup memajukan penunjuk front tanpa menggeser elemen sama sekali (O(1)). 
4. Menu Utama M2 di Backend (m2_antrean.py)
	Membangun kelas-kelas dasar untuk stack, queue naif, dan queue melingkar yang kemudian dihubungkan ke antarmuka Tkinter untuk memperlihatkan perbandingan waktu serta jumlah pergeseran secara langsung. 