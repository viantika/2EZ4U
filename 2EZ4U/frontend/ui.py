import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys

from backend.m1_pesanan import (
    ManajerPesanan,
    Pesanan,
    format_harga,
    format_waktu,
)
from backend.m2_antrean import (
    ManajerAntrean,
    hitung_struk,
)
from backend.m3_laporan import (
    ManajerLaporan,
    BATAS_INSERTION,
)


def format_ms(ms_val):
    s = f"{ms_val:.2f}".replace('.', ',')
    return f"{s} ms"


class App2EZ4U(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("2EZ4U Food Delivery - Blackpink Edition")
        self.geometry("1180x760")
        self.minsize(1000, 680)

        self.mp = ManajerPesanan()
        self.ma = ManajerAntrean()
        self.ma.set_manajer_pesanan(self.mp)
        self.ml = ManajerLaporan()

        self.menu_aktif = None
        self._sedang_proses = False

        self._atur_gaya()
        self._bangun_ui()
        self._pilih_menu("LOAD")

    def _atur_gaya(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.c_bg_dark = "#09090d"        # Pitch Black / Obsidian
        self.c_card_dark = "#14141c"      # Dark Charcoal Panel
        self.c_sidebar_dark = "#0f0f15"   # Sidebar Charcoal
        self.c_menu_btn = "#191923"       # Tombol Menu Normal
        self.c_menu_border = "#3a1329"    # Border Wine Subtle
        self.c_pink_hot = "#ff2d75"       # Electric Hot Pink (Aksen Utama)
        self.c_pink_hover = "#f43f5e"     # Rose Pink (Hover)
        self.c_pink_deep = "#be185d"      # Deep Magenta / Border
        self.c_pink_soft = "#fbcfe8"      # Soft Pastel Pink
        self.c_pink_luminous = "#f472b6"  # Luminous Neon Pink (Teks Info/Output)
        self.c_pink_err = "#ff4d6d"       # Vibrant Red-Pink (Galat)
        self.c_text_white = "#ffffff"     # Putih Bersih
        self.c_text_muted = "#a1a1aa"     # Abu-abu Lembut

        self.configure(bg=self.c_bg_dark)
        self.style.configure(".", background=self.c_card_dark, foreground=self.c_text_white, font=("Segoe UI", 10))

        # 1. Header Frame & Label
        self.style.configure("Header.TFrame", background="#060609")
        self.style.configure("Header.TLabel", background="#060609", foreground=self.c_pink_hot, font=("Segoe UI", 13, "bold"))
        self.style.configure("SubHeader.TLabel", background="#060609", foreground=self.c_pink_soft, font=("Segoe UI", 9))

        # 2. PanedWindow
        self.style.configure("TPanedwindow", background=self.c_bg_dark)

        # 3. Cards / LabelFrame
        self.style.configure("TLabelframe", background=self.c_card_dark, relief="solid", borderwidth=1, bordercolor=self.c_pink_deep)
        self.style.configure("TLabelframe.Label", background=self.c_card_dark, foreground=self.c_pink_hot, font=("Segoe UI", 9, "bold"))

        # 4. Treeview (Tabel Data)
        self.style.configure("Treeview.Heading",
                             font=("Segoe UI", 9, "bold"),
                             background="#271022",
                             foreground=self.c_pink_hot,
                             relief="flat")
        self.style.configure("Treeview",
                             background=self.c_card_dark,
                             foreground=self.c_pink_soft,
                             fieldbackground=self.c_card_dark,
                             rowheight=25,
                             font=("Segoe UI", 9))
        self.style.map("Treeview",
                       background=[("selected", self.c_pink_hot)],
                       foreground=[("selected", "#ffffff")])

        # 5. Tombol Aksi Utama (Hot Pink)
        self.style.configure("Aksi.TButton",
                             font=("Segoe UI", 9, "bold"),
                             background=self.c_pink_hot,
                             foreground="#ffffff",
                             padding=(14, 5),
                             relief="flat")
        self.style.map("Aksi.TButton",
                       background=[("active", self.c_pink_hover), ("pressed", self.c_pink_deep)],
                       foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])

        # 6. Checkbutton & Entry & Combobox
        self.style.configure("TCheckbutton", background=self.c_card_dark, foreground=self.c_pink_soft, font=("Segoe UI", 9))
        self.style.map("TCheckbutton", background=[("active", self.c_card_dark)], foreground=[("active", self.c_pink_hot)])

        self.style.configure("TEntry", fieldbackground="#1f1f2b", foreground="#ffffff", insertcolor=self.c_pink_hot)
        self.style.configure("TCombobox", fieldbackground="#1f1f2b", foreground="#ffffff")

    def _bangun_ui(self):
        # 1. Header Atas
        header_frame = ttk.Frame(self, style="Header.TFrame", padding=(16, 9))
        header_frame.pack(fill="x", side="top")

        lbl_title = ttk.Label(header_frame, text="2EZ4U Food Delivery  ★ ", style="Header.TLabel")
        lbl_title.pack(anchor="w")

        lbl_sub = ttk.Label(header_frame, text="Struktur Data & Analisa Algoritma (M1 - Array & LinkedList | M2 - Stack & Queue | M3 - Sort & Search)", style="SubHeader.TLabel")
        lbl_sub.pack(anchor="w")

        # Kontainer Utama (Kiri dan Kanan)
        main_paned = ttk.PanedWindow(self, orient="horizontal")
        main_paned.pack(fill="both", expand=True, padx=8, pady=4)

        # 2. Panel Kiri (Menu Navigasi dengan Scrollbar)
        left_container = ttk.Frame(main_paned, width=270)
        main_paned.add(left_container, weight=1)

        canvas_menu = tk.Canvas(left_container, bg=self.c_sidebar_dark, highlightthickness=1, highlightbackground=self.c_menu_border)
        sb_menu = ttk.Scrollbar(left_container, orient="vertical", command=canvas_menu.yview)
        self.menu_inner_frame = ttk.Frame(canvas_menu)

        self.menu_inner_frame.bind(
            "<Configure>",
            lambda e: canvas_menu.configure(scrollregion=canvas_menu.bbox("all"))
        )
        canvas_window = canvas_menu.create_window((0, 0), window=self.menu_inner_frame, anchor="nw")
        canvas_menu.configure(xscrollcommand=None, yscrollcommand=sb_menu.set)

        def _on_canvas_configure(event):
            canvas_menu.itemconfig(canvas_window, width=event.width)
        canvas_menu.bind("<Configure>", _on_canvas_configure)

        sb_menu.pack(side="right", fill="y")
        canvas_menu.pack(side="left", fill="both", expand=True)

        self._buat_daftar_menu(self.menu_inner_frame)

        # 3. Panel Kanan (Form Parameter, Hasil, dan Treeview)
        right_container = ttk.Frame(main_paned)
        main_paned.add(right_container, weight=4)

        # Sub-panel form input & deskripsi
        self.card_form = ttk.LabelFrame(right_container, text=" Parameter Operasi ", padding=10)
        self.card_form.pack(fill="x", side="top", pady=(0, 4))

        self.lbl_judul_menu = ttk.Label(self.card_form, text="Judul Menu", font=("Segoe UI", 11, "bold"), foreground=self.c_pink_hot)
        self.lbl_judul_menu.pack(anchor="w")

        self.lbl_deskripsi_menu = ttk.Label(self.card_form, text="Deskripsi aksi menu.", font=("Segoe UI", 9), foreground=self.c_pink_soft)
        self.lbl_deskripsi_menu.pack(anchor="w", pady=(1, 6))

        # Kontainer dinamis untuk input widgets
        self.form_inputs_frame = ttk.Frame(self.card_form)
        self.form_inputs_frame.pack(fill="x", pady=2)

        # Label status/pesan hasil eksekusi (multi-line)
        self.lbl_ringkasan_hasil = ttk.Label(self.card_form, text="", font=("Segoe UI", 9, "bold"), foreground=self.c_pink_luminous, justify="left")
        self.lbl_ringkasan_hasil.pack(anchor="w", pady=(4, 2))

        # Sub-panel Tabel Hasil
        tabel_frame = ttk.LabelFrame(right_container, text=" Hasil ", padding=4)
        tabel_frame.pack(fill="both", expand=True)

        # Scrollbar tabel
        sb_y = ttk.Scrollbar(tabel_frame, orient="vertical")
        sb_x = ttk.Scrollbar(tabel_frame, orient="horizontal")

        self.tree = ttk.Treeview(tabel_frame, show="headings", yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        sb_y.config(command=self.tree.yview)
        sb_x.config(command=self.tree.xview)

        sb_y.pack(side="right", fill="y")
        sb_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        # 4. Bagian Bawah (Panel COMMAND & Status Bar dengan Catatan Edukatif)
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill="x", side="bottom", padx=8, pady=(0, 4))

        # Panel COMMAND (Terminal Pink Gelap)
        cmd_card = ttk.LabelFrame(bottom_frame, text=" COMMAND ", padding=4)
        cmd_card.pack(fill="x", pady=(2, 3))

        cmd_sb = ttk.Scrollbar(cmd_card, orient="vertical")
        self.txt_command = tk.Text(cmd_card, height=4, font=("Consolas", 9), bg="#07070b", fg=self.c_pink_luminous,
                                   insertbackground=self.c_pink_hot, relief="solid", bd=1, yscrollcommand=cmd_sb.set)
        cmd_sb.config(command=self.txt_command.yview)
        cmd_sb.pack(side="right", fill="y")
        self.txt_command.pack(fill="x", expand=True)
        self.txt_command.config(state="disabled")

        # Baris Status & Catatan Edukatif (Blackpink Glow)
        status_container = ttk.Frame(bottom_frame)
        status_container.pack(fill="x", pady=(1, 0))

        self.lbl_badge = tk.Label(status_container, text="[Siap]", bg=self.c_pink_hot, fg="#ffffff",
                                  font=("Segoe UI", 8, "bold"), padx=9, pady=3, relief="flat")
        self.lbl_badge.pack(side="left", padx=(0, 6))

        self.catatan_frame = tk.Frame(status_container, bg="#1a0b18", bd=1, relief="solid", highlightbackground=self.c_pink_deep, highlightthickness=1)
        self.catatan_frame.pack(side="left", fill="x", expand=True)

        self.lbl_catatan = tk.Label(self.catatan_frame,
                                    text="Silakan muat dataset terlebih dahulu melalui menu DATA -> Load",
                                    bg="#1a0b18", fg=self.c_pink_soft, font=("Segoe UI", 9),
                                    anchor="w", padx=8, pady=3)
        self.lbl_catatan.pack(fill="x")

    def _buat_daftar_menu(self, parent):
        daftar_grup = [
            ("DATA", [
                ("Load", "LOAD"),
            ]),
            ("M1 - DATA PESANAN", [
                ("ARRAY - LIHAT PESANAN", "ARR_LIHAT"),
                ("ARRAY - TAMBAH PESANAN REGULER", "ARR_TAMBAH_REG"),
                ("ARRAY - TAMBAH PESANAN PRIORITAS", "ARR_TAMBAH_PRI"),
                ("ARRAY - TAMBAH PESANAN VIP", "ARR_TAMBAH_VIP"),
                ("ARRAY - HAPUS PESANAN", "ARR_HAPUS"),
                ("LINKEDLIST - LIHAT PESANAN", "LL_LIHAT"),
                ("LINKEDLIST - TAMBAH PESANAN REGULER", "LL_TAMBAH_REG"),
                ("LINKEDLIST - TAMBAH PESANAN PRIORITAS", "LL_TAMBAH_PRI"),
                ("LINKEDLIST - TAMBAH PESANAN VIP", "LL_TAMBAH_VIP"),
                ("LINKEDLIST - HAPUS PESANAN", "LL_HAPUS"),
            ]),
            ("M2 - STACK DAN QUEUE", [
                ("STACK - POSTFIX (MESIN KASIR)", "STACK_POSTFIX"),
                ("STACK - UNDO", "STACK_UNDO"),
                ("STACK - REDO", "STACK_REDO"),
                ("QUEUE - ENQUEUE", "QUEUE_ENQUEUE"),
                ("QUEUE - DEQUEUE NAIF", "QUEUE_DEQ_NAIF"),
                ("QUEUE - DEQUEUE CIRCULAR", "QUEUE_DEQ_CIRC"),
            ]),
            ("M3 - SORT DAN SEARCH", [
                ("SORT - INSERTION SORT", "SORT_INSERTION"),
                ("SORT - MERGE SORT", "SORT_MERGE"),
                ("SEARCH - LINEAR SEARCH", "SEARCH_LINEAR"),
                ("SEARCH - BINARY SEARCH", "SEARCH_BINARY"),
            ]),
        ]

        self.tombol_menu_dict = {}

        for nama_grup, items in daftar_grup:
            lbl = tk.Label(parent, text=nama_grup, font=("Segoe UI", 8, "bold"), fg=self.c_pink_hot, bg=self.c_sidebar_dark, anchor="w", pady=3)
            lbl.pack(fill="x", padx=6, pady=(6, 0))

            for label_tombol, kode_menu in items:
                btn = tk.Button(
                    parent,
                    text=f"  {label_tombol}",
                    font=("Segoe UI", 8),
                    anchor="w",
                    bg=self.c_menu_btn,
                    fg="#f4f4f5",
                    relief="flat",
                    activebackground=self.c_pink_hot,
                    activeforeground="#ffffff",
                    padx=4,
                    pady=2,
                    command=lambda k=kode_menu: self._pilih_menu(k)
                )
                btn.pack(fill="x", padx=4, pady=1)
                if kode_menu not in self.tombol_menu_dict:
                    self.tombol_menu_dict[kode_menu] = btn

    def catat_command(self, cmd_nama, modul_singkat, waktu_ms, catatan_edukatif=None):
        waktu_str = format_ms(waktu_ms)
        baris = f"{cmd_nama:<24} -> {modul_singkat:<22} {waktu_str}\n"

        self.txt_command.config(state="normal")
        self.txt_command.insert("1.0", baris)
        self.txt_command.config(state="disabled")

        self.lbl_badge.config(text=f"[{modul_singkat}]  {waktu_str}")

        if catatan_edukatif:
            self.lbl_catatan.config(text=catatan_edukatif)

    def _bersihkan_form(self):
        for w in self.form_inputs_frame.winfo_children():
            w.destroy()
        self.lbl_ringkasan_hasil.config(text="")

    def _bersihkan_tabel(self, kolom_list, judul_list=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.tree["columns"] = kolom_list
        if judul_list is None:
            judul_list = kolom_list

        for col, heading in zip(kolom_list, judul_list):
            self.tree.heading(col, text=heading)
            if col in ("#", "no", "langkah"):
                self.tree.column(col, width=45, anchor="center")
            elif col in ("oid", "prioritas", "masuk", "selesai", "status", "kolom"):
                self.tree.column(col, width=85, anchor="center")
            elif col in ("harga",):
                self.tree.column(col, width=95, anchor="e")
            elif col in ("pelanggan", "resto", "menu"):
                self.tree.column(col, width=150, anchor="w")
            elif col in ("tindakan", "output", "isi"):
                self.tree.column(col, width=220, anchor="w")
            elif col in ("stack",):
                self.tree.column(col, width=110, anchor="w")
            else:
                self.tree.column(col, width=110, anchor="w")

    def _tampilkan_pesanan_ke_tabel(self, daftar_pesanan, mulai_no=1):
        kolom = ["#", "oid", "pelanggan", "resto", "menu", "harga", "prioritas", "masuk", "selesai", "status"]
        self._bersihkan_tabel(kolom, ["#", "oid", "pelanggan", "resto", "menu", "harga", "prioritas", "masuk", "selesai", "status"])

        for i, p in enumerate(daftar_pesanan):
            pri_str = "1 (VIP)" if p.prioritas == 1 else ("2 (Prioritas)" if p.prioritas == 2 else "3 (Reguler)")
            self.tree.insert("", "end", values=(
                mulai_no + i,
                p.oid,
                p.pelanggan,
                p.resto,
                p.menu,
                format_harga(p.harga),
                pri_str,
                format_waktu(p.t_masuk_detik),
                format_waktu(p.t_selesai_detik),
                p.status
            ))

    def _tampilkan_tabel_kv(self, rincian_kv):
        self._bersihkan_tabel(["kolom", "isi"], ["kolom", "isi"])
        for k, v in rincian_kv:
            self.tree.insert("", "end", values=(k, v))

    def _validasi_muat_data(self):
        if not self.mp.sudah_dimuat:
            messagebox.showwarning("Perhatian", "Data belum dimuat! Silakan klik menu 'DATA -> Load' terlebih dahulu.")
            return False
        return True

    def _pilih_menu(self, kode):
        self.menu_aktif = kode
        self._bersihkan_form()

        # Highlight tombol aktif dengan Hot Pink
        for k, btn in self.tombol_menu_dict.items():
            if k == kode:
                btn.config(bg=self.c_pink_hot, fg="#ffffff", font=("Segoe UI", 8, "bold"))
            else:
                btn.config(bg=self.c_menu_btn, fg="#f4f4f5", font=("Segoe UI", 8))

        # Routing ke pembuat form masing-masing
        if kode == "LOAD":
            self._form_load()
        elif kode in ("ARR_LIHAT", "LL_LIHAT"):
            self._form_lihat(kode)
        elif kode in ("ARR_TAMBAH_REG", "ARR_TAMBAH_PRI", "ARR_TAMBAH_VIP",
                      "LL_TAMBAH_REG", "LL_TAMBAH_PRI", "LL_TAMBAH_VIP"):
            self._form_tambah(kode)
        elif kode in ("ARR_HAPUS", "LL_HAPUS"):
            self._form_hapus(kode)
        elif kode == "STACK_POSTFIX":
            self._form_postfix()
        elif kode in ("STACK_UNDO", "STACK_REDO"):
            self._form_undo_redo(kode)
        elif kode == "QUEUE_ENQUEUE":
            self._form_enqueue()
        elif kode in ("QUEUE_DEQ_NAIF", "QUEUE_DEQ_CIRC"):
            self._form_dequeue(kode)
        elif kode in ("SORT_INSERTION", "SORT_MERGE"):
            self._form_sort(kode)
        elif kode in ("SEARCH_LINEAR", "SEARCH_BINARY"):
            self._form_search(kode)

    def _form_load(self):
        self.lbl_judul_menu.config(text="DATA: Muat Dataset Pesanan")
        self.lbl_deskripsi_menu.config(text="Memuat 200.000 baris pesanan dari data/pesanan.csv ke memori Array & LinkedList buatan sendiri.")
        self.lbl_catatan.config(text="Dynamic Array menggandakan kapasitas 2x lipat (amortized O(1)) agar mampu menampung 200.000 pesanan.")

        btn_load = ttk.Button(self.form_inputs_frame, text="MULAI MUAT DATASET (200.000)", style="Aksi.TButton", command=self._aksi_load)
        btn_load.pack(side="left", padx=4, pady=4)

        if self.mp.sudah_dimuat:
            self.lbl_ringkasan_hasil.config(text=f"✓ Data sudah dimuat: {len(self.mp.array):,} baris pesanan siap digunakan.", foreground=self.c_pink_luminous)

    def _aksi_load(self):
        if self._sedang_proses:
            return
        self._sedang_proses = True
        self.lbl_ringkasan_hasil.config(text="Sedang memuat dataset 200.000 baris...", foreground=self.c_pink_soft)
        self.update_idletasks()

        def _worker():
            csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "pesanan.csv")
            if not os.path.exists(csv_path):
                self.after(0, lambda: messagebox.showerror("Galat", f"File {csv_path} tidak ditemukan!"))
                self._sedang_proses = False
                return

            jumlah, waktu_ms, modul = self.mp.muat_csv(csv_path)
            pesanan_antre_iter = self.mp.pesanan_antre()
            j_antre, w_antre, _ = self.ma.muat_antrean(pesanan_antre_iter)

            def _selesai():
                self._sedang_proses = False
                msg = f"✓ Berhasil memuat {jumlah:,} baris dalam {format_ms(waktu_ms)}! ({j_antre:,} berstatus ANTRE masuk antrean)"
                self.lbl_ringkasan_hasil.config(text=msg, foreground=self.c_pink_luminous)
                self.catat_command("load_dataset", "DATA - load", waktu_ms,
                                   "Dynamic Array menggandakan kapasitas 2x lipat (amortized O(1)) agar mampu menampung 200.000 pesanan.")
                data_awal = self.mp.array.slice(0, 15)
                self._tampilkan_pesanan_ke_tabel(data_awal, mulai_no=1)

            self.after(0, _selesai)

        threading.Thread(target=_worker, daemon=True).start()

    def _form_lihat(self, kode):
        is_arr = "ARR" in kode
        tipe = "Array" if is_arr else "LinkedList"
        self.lbl_judul_menu.config(text=f"{tipe}: lihat pesanan ke-i")
        self.lbl_deskripsi_menu.config(text=f"Melihat pesanan pada indeks ke-i di struktur data {tipe}.")

        if is_arr:
            self.lbl_catatan.config(text="Akses pesanan ke-i pada Array beroperasi O(1) via penunjuk memori langsung.")
        else:
            self.lbl_catatan.config(text="Akses pesanan ke-i pada Linked List menelusuri simpul demi simpul dari head sehingga berbiaya O(i).")

        f_in = ttk.Frame(self.form_inputs_frame)
        f_in.pack(fill="x")

        ttk.Label(f_in, text="Indeks ke-i:").pack(side="left", padx=4)
        ent_idx = ttk.Entry(f_in, width=10)
        ent_idx.insert(0, "0")
        ent_idx.pack(side="left", padx=4)

        ttk.Button(f_in, text="LIHAT", style="Aksi.TButton",
                   command=lambda: self._aksi_lihat(kode, ent_idx.get())).pack(side="left", padx=8)

    def _aksi_lihat(self, kode, str_idx):
        if not self._validasi_muat_data():
            return
        try:
            idx = int(str_idx)
        except ValueError:
            self.lbl_ringkasan_hasil.config(text="⚠️ Galat: Indeks harus berupa bilangan bulat!", foreground=self.c_pink_err)
            return

        total_len = len(self.mp.array) if "ARR" in kode else len(self.mp.linklist)
        if idx < 0 or idx >= total_len:
            self.lbl_ringkasan_hasil.config(text=f"⚠️ Galat: Indeks di luar rentang valid (0 s.d. {total_len - 1:,})!", foreground=self.c_pink_err)
            return

        is_arr = "ARR" in kode
        if is_arr:
            hasil, waktu_ms, info, modul = self.mp.lihat_array(idx, 10)
            cmd_nama = f"array_get_{idx}"
            modul_singkat = "M1 - array"
            note = f"Akses elemen indeks {idx} pada Array selesai dalam O(1) konstan."
        else:
            hasil, waktu_ms, info, modul = self.mp.lihat_linklist(idx, 10)
            cmd_nama = f"linkedlist_get_{idx}"
            modul_singkat = "M1 - linkedlist"
            note = f"Akses elemen indeks {idx} pada Linked List menelusuri {idx:,} simpul secara bertahap."

        self._tampilkan_pesanan_ke_tabel(hasil, mulai_no=idx + 1)
        self.lbl_ringkasan_hasil.config(text=f"✓ Menampilkan {len(hasil)} pesanan mulai indeks {idx} (Waktu: {format_ms(waktu_ms)})", foreground=self.c_pink_luminous)
        self.catat_command(cmd_nama, modul_singkat, waktu_ms, note)

    def _form_tambah(self, kode):
        is_arr = "ARR" in kode
        struktur = "Array" if is_arr else "LinkedList"
        pri = 1 if "VIP" in kode else (2 if "PRI" in kode else 3)

        if pri == 3:
            judul = f"{struktur}: pesanan REGULER, masuk paling belakang"
            deskripsi = "pesanan biasa mengantre di susunan paling belakang"
            catatan = "Pesanan reguler selalu menempel di belakang, jadi O(1) pada kedua versi. Perbedaannya baru muncul saat dequeue."
        elif pri == 2:
            judul = f"{struktur}: pesanan PRIORITAS, menyerobot ke tengah"
            deskripsi = "pesanan prioritas disisipkan di indeks n//2 barisan"
            catatan = "Pesanan prioritas menyerobot ke tengah (indeks n//2). Array menggeser n/2 elemen, sedangkan LinkedList menelusuri n/2 simpul."
        else:
            judul = f"{struktur}: pesanan VIP, langsung ke urutan pertama"
            deskripsi = "pesanan VIP langsung ke urutan pertama"
            catatan = "Pesanan VIP langsung ke indeks 0. Array harus menggeser seluruh n elemen (O(n)), sedangkan LinkedList hanya mengubah pointer head (O(1))."

        self.lbl_judul_menu.config(text=judul)
        self.lbl_deskripsi_menu.config(text=deskripsi)
        self.lbl_catatan.config(text=catatan)

        f_in = ttk.Frame(self.form_inputs_frame)
        f_in.pack(fill="x")

        ttk.Label(f_in, text="Nama pelanggan").grid(row=0, column=0, sticky="w", padx=4, pady=2)
        ent_pelanggan = ttk.Entry(f_in, width=22)
        ent_pelanggan.insert(0, "Jennie" if pri == 3 else ("Jisoo" if pri == 2 else "Lisa"))
        ent_pelanggan.grid(row=0, column=1, padx=4, pady=2)

        ttk.Label(f_in, text="Resto").grid(row=0, column=2, sticky="w", padx=4, pady=2)
        ent_resto = ttk.Entry(f_in, width=18)
        ent_resto.insert(0, "kafe-teknik")
        ent_resto.grid(row=0, column=3, padx=4, pady=2)

        ttk.Label(f_in, text="Menu").grid(row=1, column=0, sticky="w", padx=4, pady=2)
        ent_menu = ttk.Entry(f_in, width=22)
        ent_menu.insert(0, "roti-bakar")
        ent_menu.grid(row=1, column=1, padx=4, pady=2)

        ttk.Label(f_in, text="Harga (Rp)").grid(row=1, column=2, sticky="w", padx=4, pady=2)
        ent_harga = ttk.Entry(f_in, width=18)
        ent_harga.insert(0, "12000")
        ent_harga.grid(row=1, column=3, padx=4, pady=2)

        # Checkbox sinkronkan ke kedua struktur
        var_kedua = tk.BooleanVar(value=True)
        cb_kedua = ttk.Checkbutton(f_in, text="Sinkronkan & Bandingkan Keduanya (Array & LinkedList)", variable=var_kedua)
        cb_kedua.grid(row=2, column=0, columnspan=4, sticky="w", padx=4, pady=3)

        btn_tambah = ttk.Button(f_in, text="TAMBAH", style="Aksi.TButton",
                                command=lambda: self._aksi_tambah(kode, pri, ent_pelanggan.get(), ent_resto.get(), ent_menu.get(), ent_harga.get(), var_kedua.get()))
        btn_tambah.grid(row=3, column=0, columnspan=2, sticky="w", padx=4, pady=4)

    def _aksi_tambah(self, kode, prioritas, pelanggan, resto, menu_item, str_harga, sinkron_kedua):
        if not self._validasi_muat_data():
            return
        if not pelanggan.strip() or not resto.strip() or not menu_item.strip():
            self.lbl_ringkasan_hasil.config(text="⚠️ Galat: Nama pelanggan, resto, dan menu tidak boleh kosong!", foreground=self.c_pink_err)
            return
        try:
            harga = int(str_harga)
            if harga < 0:
                raise ValueError
        except ValueError:
            self.lbl_ringkasan_hasil.config(text="⚠️ Galat: Harga harus berupa angka positif!", foreground=self.c_pink_err)
            return

        if sinkron_kedua:
            p, res_arr, res_ll = self.mp.tambah_kedua(pelanggan, resto, menu_item, harga, prioritas)
            pos_a, w_a, ges_a, mod_a = res_arr
            pos_l, w_l, tra_l, mod_l = res_ll

            self.ma.enqueue(p)

            msg = (f"{p.oid} masuk ke barisan pada KEDUA struktur data.\n"
                   f"Panjang sekarang: array {len(self.mp.array):,}, linkedlist {len(self.mp.linklist):,}.")
            self.lbl_ringkasan_hasil.config(text=msg, foreground=self.c_pink_luminous)

            if prioritas == 3:
                catatan = "Pesanan reguler selalu menempel di belakang, jadi O(1) pada kedua versi. Perbedaannya baru muncul saat dequeue."
            elif prioritas == 2:
                catatan = "Pesanan prioritas menyerobot ke tengah (indeks n//2). Array menggeser n/2 elemen, sedangkan LinkedList menelusuri n/2 simpul."
            else:
                catatan = "Pesanan VIP langsung ke urutan pertama (indeks 0). Array menggeser seluruh elemen, LinkedList hanya mengubah satu penunjuk."

            self.catat_command("array_insert", "M1 - array", w_a, catatan)
            self.catat_command("linkedlist_insert", "M1 - linkedlist", w_l, catatan)

            rincian = [
                ("oid", p.oid),
                ("pelanggan", p.pelanggan),
                ("resto", p.resto),
                ("menu", p.menu),
                ("harga", format_harga(p.harga)),
                ("prioritas", str(p.prioritas)),
                ("masuk", format_waktu(p.t_masuk_detik)),
                ("selesai", "-"),
                ("status", p.status),
            ]
            self._tampilkan_tabel_kv(rincian)
        else:
            is_arr = "ARR" in kode
            if is_arr:
                p, pos, waktu_ms, geseran, modul = self.mp.tambah_array(pelanggan, resto, menu_item, harga, prioritas)
                cmd_nama = "array_insert"
                mod_singkat = "M1 - array"
            else:
                p, pos, waktu_ms, geseran, modul = self.mp.tambah_linklist(pelanggan, resto, menu_item, harga, prioritas)
                cmd_nama = "linkedlist_insert"
                mod_singkat = "M1 - linkedlist"

            self.ma.catat_order(p)
            self.lbl_ringkasan_hasil.config(text=f"{p.oid} berhasil disisipkan di posisi {pos:,}.", foreground=self.c_pink_luminous)
            self.catat_command(cmd_nama, mod_singkat, waktu_ms)
            rincian = [
                ("oid", p.oid),
                ("pelanggan", p.pelanggan),
                ("resto", p.resto),
                ("menu", p.menu),
                ("harga", format_harga(p.harga)),
                ("prioritas", str(p.prioritas)),
                ("masuk", format_waktu(p.t_masuk_detik)),
                ("selesai", "-"),
                ("status", p.status),
            ]
            self._tampilkan_tabel_kv(rincian)

    def _form_hapus(self, kode):
        is_arr = "ARR" in kode
        tipe = "Array" if is_arr else "LinkedList"
        self.lbl_judul_menu.config(text=f"{tipe}: hapus pesanan ke-i")
        self.lbl_deskripsi_menu.config(text=f"Menghapus pesanan di indeks ke-i dari struktur data {tipe}.")

        if is_arr:
            self.lbl_catatan.config(text="Menghapus di indeks 0 pada Array menggeser seluruh sisa elemen ke kiri (O(n)).")
        else:
            self.lbl_catatan.config(text="Menghapus simpul pada LinkedList memerlukan penelusuran O(i) sebelum mengubah pointer next.")

        f_in = ttk.Frame(self.form_inputs_frame)
        f_in.pack(fill="x")

        ttk.Label(f_in, text="Indeks ke-i yang dihapus:").pack(side="left", padx=4)
        ent_idx = ttk.Entry(f_in, width=12)
        ent_idx.insert(0, "0")
        ent_idx.pack(side="left", padx=4)

        ttk.Button(f_in, text="HAPUS", style="Aksi.TButton",
                   command=lambda: self._aksi_hapus(kode, ent_idx.get())).pack(side="left", padx=10)

    def _aksi_hapus(self, kode, str_idx):
        if not self._validasi_muat_data():
            return
        try:
            idx = int(str_idx)
        except ValueError:
            self.lbl_ringkasan_hasil.config(text="⚠️ Galat: Indeks harus berupa bilangan bulat!", foreground=self.c_pink_err)
            return

        total_len = len(self.mp.array) if "ARR" in kode else len(self.mp.linklist)
        if idx < 0 or idx >= total_len:
            self.lbl_ringkasan_hasil.config(text=f"⚠️ Galat: Indeks di luar rentang valid (0 s.d. {total_len - 1:,})!", foreground=self.c_pink_err)
            return

        is_arr = "ARR" in kode
        if is_arr:
            val, waktu_ms, stat, modul = self.mp.hapus_array(idx)
            cmd_nama = f"array_delete_{idx}"
            mod_singkat = "M1 - array"
            note = f"Hapus indeks {idx} pada Array menggeser {stat:,} elemen."
        else:
            val, waktu_ms, stat, modul = self.mp.hapus_linklist(idx)
            cmd_nama = f"linkedlist_delete_{idx}"
            mod_singkat = "M1 - linkedlist"
            note = f"Hapus indeks {idx} pada LinkedList menelusuri {stat:,} simpul."

        self.lbl_ringkasan_hasil.config(text=f"✓ Pesanan {val.oid} ({val.pelanggan}) berhasil dihapus dari { 'Array' if is_arr else 'LinkedList' }.", foreground=self.c_pink_luminous)
        self.catat_command(cmd_nama, mod_singkat, waktu_ms, note)
        self._tampilkan_pesanan_ke_tabel([val], mulai_no=idx + 1)

    def _form_postfix(self):
        self.lbl_judul_menu.config(text="Stack: hitung struk lewat postfix")
        self.lbl_deskripsi_menu.config(text="Struk ditulis infix (dihitung dua tahap dengan stack: tahap 1 Infix menjadi postfix, tahap 2 postfix dievaluasi)")
        self.lbl_catatan.config(text="Baris 1.x adalah tahap konversi, baris 2.x tahap evaluasi. Tahap 1 menahan operator di stack sampai gilirannya tiba. Tahap 2 menumpuk angka, dan setiap operator mengambil dua nilai teratas. Operand kanan selalu keluar lebih dulu.")

        f_in = ttk.Frame(self.form_inputs_frame)
        f_in.pack(fill="x")

        ttk.Label(f_in, text="Struk belanja (infix)").pack(side="left", padx=4)
        ent_struk = ttk.Entry(f_in, width=45)
        ent_struk.insert(0, "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
        ent_struk.pack(side="left", padx=4)

        ttk.Button(f_in, text="HITUNG", style="Aksi.TButton",
                   command=lambda: self._aksi_postfix(ent_struk.get())).pack(side="left", padx=8)

    def _aksi_postfix(self, ekspresi):
        if not ekspresi.strip():
            self.lbl_ringkasan_hasil.config(text="⚠️ Galat: Ekspresi struk tidak boleh kosong!", foreground=self.c_pink_err)
            return

        postfix_str, hasil, tabel_langkah, waktu_ms, modul, galat = hitung_struk(ekspresi)

        if galat:
            self.lbl_ringkasan_hasil.config(text=f"⚠️ Galat Evaluasi: {galat}", foreground=self.c_pink_err)
            self.catat_command("stack_postfix", "M2 - stack", waktu_ms)
            return

        total_rp = format_harga(hasil)
        msg = (f"Struk: {ekspresi}\n"
               f"Postfix: {postfix_str}\n"
               f"TOTAL : Rp {total_rp}")
        self.lbl_ringkasan_hasil.config(text=msg, foreground=self.c_pink_luminous)

        catatan = "Baris 1.x adalah tahap konversi, baris 2.x tahap evaluasi. Tahap 1 menahan operator di stack sampai gilirannya tiba. Tahap 2 menumpuk angka, dan setiap operator mengambil dua nilai teratas. Operand kanan selalu keluar lebih dulu."
        self.catat_command("stack_postfix", "M2 - stack", waktu_ms, catatan)

        kolom = ["langkah", "token", "tindakan", "stack", "output"]
        self._bersihkan_tabel(kolom, ["langkah", "token", "tindakan", "stack", "output"])

        for row in tabel_langkah:
            self.tree.insert("", "end", values=row)

    def _form_undo_redo(self, kode):
        is_undo = kode == "STACK_UNDO"
        if is_undo:
            judul = "Stack: batalkan aksi antrean terakhir"
            deskripsi = "Mengambil catatan teratas tumpukan undo, lalu menjalankan kebalikannya. Aksi terakhirlah yang dibatalkan lebih dulu."
            btn_text = "UNDO"
            catatan = "Kebalikan dari enqueue adalah membuang elemen paling belakang, jadi O(1) pada kedua antrean."
        else:
            judul = "Stack: kerjakan lagi aksi yang dibatalkan"
            deskripsi = "Mengambil catatan teratas tumpukan redo, lalu mengerjakan ulang aksi aslinya. Aksi baru apa pun mengosongkan tumpukan ini."
            btn_text = "REDO"
            catatan = "Redo mengerjakan ULANG aksi aslinya, bukan kebalikannya, lalu mengembalikan catatannya ke tumpukan undo supaya bisa dibatalkan lagi."

        self.lbl_judul_menu.config(text=judul)
        self.lbl_deskripsi_menu.config(text=deskripsi)
        self.lbl_catatan.config(text=catatan)

        f_in = ttk.Frame(self.form_inputs_frame)
        f_in.pack(fill="x")

        btn_cmd = self._aksi_undo if is_undo else self._aksi_redo
        ttk.Button(f_in, text=btn_text, style="Aksi.TButton", command=btn_cmd).pack(side="left", padx=4)

    def _aksi_undo(self):
        pesan, waktu_ms, modul = self.ma.undo_last()
        stats = self.ma.stats()
        catatan = "Kebalikan dari enqueue adalah membuang elemen paling belakang, jadi O(1) pada kedua antrean."

        aksi = getattr(self.ma, 'terakhir_aksi', None)
        if aksi:
            tipe, data = aksi
            if tipe == "ENQUEUE":
                p_item = data
                res_teks = (f"Pembatalan enqueue: {p_item.oid} dikeluarkan lagi dari belakang.\n"
                            f"Panjang antrean sekarang: naif {stats[0]:,}, circular {stats[1]:,}. tumpukan undo tersisa {stats[4]} catatan.")
                self.lbl_ringkasan_hasil.config(text=res_teks, foreground=self.c_pink_luminous)
                self._tampilkan_tabel_antrean_pesanan([p_item])
            elif tipe == "DEQUEUE":
                res_teks = (f"Pembatalan dequeue: {len(data)} pesanan dikembalikan ke depan antrean.\n"
                            f"Panjang antrean sekarang: naif {stats[0]:,}, circular {stats[1]:,}. tumpukan undo tersisa {stats[4]} catatan.")
                self.lbl_ringkasan_hasil.config(text=res_teks, foreground=self.c_pink_luminous)
                self._tampilkan_tabel_antrean_pesanan(data)
            else:
                self.lbl_ringkasan_hasil.config(text=pesan, foreground=self.c_pink_luminous)
        else:
            self.lbl_ringkasan_hasil.config(text=pesan, foreground=self.c_pink_hover)

        self.catat_command("stack_undo", "M2 - stack", waktu_ms, catatan)

    def _aksi_redo(self):
        pesan, waktu_ms, modul = self.ma.redo_last()
        stats = self.ma.stats()
        catatan = "Redo mengerjakan ULANG aksi aslinya, bukan kebalikannya, lalu mengembalikan catatannya ke tumpukan undo supaya bisa dibatalkan lagi."

        aksi = getattr(self.ma, 'terakhir_aksi', None)
        if aksi and "kosong" not in pesan.lower():
            tipe, data = aksi
            if tipe == "ENQUEUE":
                p_item = data
                res_teks = (f"Enqueue dikerjakan lagi: {p_item.oid} masuk kembali ke belakang.\n"
                            f"Panjang antrean sekarang: naif {stats[0]:,}, circular {stats[1]:,}. Tumpukan undo {stats[4]}, redo {stats[5]}.")
                self.lbl_ringkasan_hasil.config(text=res_teks, foreground=self.c_pink_luminous)
                self._tampilkan_tabel_antrean_pesanan([p_item])
            elif tipe == "DEQUEUE":
                res_teks = (f"Dequeue dikerjakan lagi: {len(data)} pesanan dikeluarkan lagi.\n"
                            f"Panjang antrean sekarang: naif {stats[0]:,}, circular {stats[1]:,}. Tumpukan undo {stats[4]}, redo {stats[5]}.")
                self.lbl_ringkasan_hasil.config(text=res_teks, foreground=self.c_pink_luminous)
                self._tampilkan_tabel_antrean_pesanan(data)
            else:
                self.lbl_ringkasan_hasil.config(text=pesan, foreground=self.c_pink_luminous)
        else:
            self.lbl_ringkasan_hasil.config(text=pesan, foreground=self.c_pink_hover)

        self.catat_command("stack_redo", "M2 - stack", waktu_ms, catatan)

    def _tampilkan_tabel_antrean_pesanan(self, daftar_pesanan):
        """Menampilkan pesanan pada antrean (tabel format #, oid, pelanggan, resto, menu)."""
        kolom = ["#", "oid", "pelanggan", "resto", "menu"]
        self._bersihkan_tabel(kolom, ["#", "oid", "pelanggan", "resto", "menu"])
        for i, p in enumerate(daftar_pesanan, 1):
            self.tree.insert("", "end", values=(i, p.oid, p.pelanggan, p.resto, p.menu))

    def _form_enqueue(self):
        self.lbl_judul_menu.config(text="Queue: pesanan baru masuk ke belakang")
        self.lbl_deskripsi_menu.config(text="Menambah pesanan di ujung belakang kedua antrean sekaligus, yang naif maupun yang circular.")
        self.lbl_catatan.config(text="Enqueue selalu menempel di belakang, jadi O(1) pada kedua versi. Perbedaannya baru muncul saat dequeue.")

        f_in = ttk.Frame(self.form_inputs_frame)
        f_in.pack(fill="x")

        ttk.Label(f_in, text="Nama pelanggan").grid(row=0, column=0, sticky="w", padx=4, pady=2)
        ent_pelanggan = ttk.Entry(f_in, width=22)
        ent_pelanggan.insert(0, "Rosé")
        ent_pelanggan.grid(row=0, column=1, padx=4, pady=2)

        ttk.Label(f_in, text="Resto").grid(row=0, column=2, sticky="w", padx=4, pady=2)
        ent_resto = ttk.Entry(f_in, width=18)
        ent_resto.insert(0, "kafe-teknik")
        ent_resto.grid(row=0, column=3, padx=4, pady=2)

        ttk.Label(f_in, text="Menu").grid(row=1, column=0, sticky="w", padx=4, pady=2)
        ent_menu = ttk.Entry(f_in, width=22)
        ent_menu.insert(0, "roti-bakar")
        ent_menu.grid(row=1, column=1, padx=4, pady=2)

        ttk.Label(f_in, text="Harga (Rp)").grid(row=1, column=2, sticky="w", padx=4, pady=2)
        ent_harga = ttk.Entry(f_in, width=18)
        ent_harga.insert(0, "12000")
        ent_harga.grid(row=1, column=3, padx=4, pady=2)

        btn_enq = ttk.Button(f_in, text="ENQUEUE", style="Aksi.TButton",
                             command=lambda: self._aksi_enqueue(ent_pelanggan.get(), ent_resto.get(), ent_menu.get(), ent_harga.get()))
        btn_enq.grid(row=2, column=0, columnspan=2, sticky="w", padx=4, pady=4)

    def _aksi_enqueue(self, pelanggan, resto, menu_item, str_harga):
        if not self._validasi_muat_data():
            return
        try:
            harga = int(str_harga)
        except ValueError:
            self.lbl_ringkasan_hasil.config(text="⚠️ Galat: Harga harus angka!", foreground=self.c_pink_err)
            return

        oid = self.mp._oid_berikutnya()
        p = Pesanan(oid, pelanggan, resto, menu_item, harga, 3, 0, '', 'ANTRE')
        self.mp.array.append(p)
        self.mp.linklist.append(p)

        pesan, waktu_ms, modul = self.ma.enqueue(p)

        res_teks = (f"{oid} masuk ke barisan paling belakang pada KEDUA antrean.\n"
                    f"Panjang sekarang: naif {len(self.ma.naif):,}, circular {len(self.ma.circular):,}.")
        self.lbl_ringkasan_hasil.config(text=res_teks, foreground=self.c_pink_luminous)

        catatan = "Enqueue selalu menempel di belakang, jadi O(1) pada kedua versi. Perbedaannya baru muncul saat dequeue."
        self.catat_command("queue_enqueue", "M2 - queue", waktu_ms, catatan)

        rincian = [
            ("oid", p.oid),
            ("pelanggan", p.pelanggan),
            ("resto", p.resto),
            ("menu", p.menu),
            ("harga", format_harga(p.harga)),
            ("prioritas", str(p.prioritas)),
            ("masuk", format_waktu(p.t_masuk_detik)),
            ("selesai", "-"),
            ("status", p.status),
        ]
        self._tampilkan_tabel_kv(rincian)

    def _form_dequeue(self, kode):
        is_naif = kode == "QUEUE_DEQ_NAIF"
        if is_naif:
            judul = "Queue naif: ambil dari depan dengan menggeser isi"
            deskripsi = "Mengambil indeks 0 lalu menggeser seluruh sisa isi satu petak ke kiri. Biayanya O(n) setiap kali."
            catatan = "Mengambil indeks 0 memaksa seluruh sisa isi bergeser satu petak ke kiri, jadi O(n) per dequeue. Bandingkan waktunya dengan menu DEQUEUE CIRCULAR."
        else:
            judul = "Queue circular: ambil dari depan dengan memajukan penunjuk"
            deskripsi = "Hanya penunjuk front yang maju, memakai sisa bagi terhadap kapasitas. Isi larik tidak digeser sama sekali."
            catatan = "Yang berpindah hanya penunjuk front, memakai sisa bagi terhadap kapasitas. Isi larik tidak disentuh sama sekali, jadi biayanya O(1) berapa pun panjang antreannya."

        self.lbl_judul_menu.config(text=judul)
        self.lbl_deskripsi_menu.config(text=deskripsi)
        self.lbl_catatan.config(text=catatan)

        f_in = ttk.Frame(self.form_inputs_frame)
        f_in.pack(fill="x")

        ttk.Label(f_in, text="Berapa kali dequeue").pack(side="left", padx=4)
        ent_k = ttk.Entry(f_in, width=8)
        ent_k.insert(0, "2")
        ent_k.pack(side="left", padx=4)

        ttk.Button(f_in, text="DEQUEUE", style="Aksi.TButton",
                   command=lambda: self._aksi_dequeue(kode, ent_k.get())).pack(side="left", padx=10)

    def _aksi_dequeue(self, kode, str_k):
        if not self._validasi_muat_data():
            return
        try:
            k = int(str_k)
            if k <= 0:
                raise ValueError
        except ValueError:
            self.lbl_ringkasan_hasil.config(text="⚠️ Galat: Nilai k harus berupa bilangan bulat positif!", foreground=self.c_pink_err)
            return

        is_naif = kode == "QUEUE_DEQ_NAIF"
        if is_naif:
            daftar, geseran, waktu_ms, info_c, modul = self.ma.dequeue_naif(k)
            sisa = len(self.ma.naif)
            rata_ges = geseran // len(daftar) if daftar else 0
            res_teks = (f"{len(daftar)} pesanan keluar dari depan antrean naif.\n"
                        f"Total {geseran:,} elemen digeser, rata-rata {rata_ges:,} geseran per dequeue.\n"
                        f"Sisa antrean naif {sisa:,}.")
            catatan = f"Mengambil indeks 0 memaksa seluruh sisa isi bergeser satu petak ke kiri, jadi O(n) per dequeue. Panjang antrean saat itu {sisa+len(daftar):,}, dan begitu pula kira-kira geseran yang terjadi. Bandingkan waktunya dengan menu DEQUEUE CIRCULAR."
            cmd_nama = "queue_dequeue_naive"
            mod_singkat = "M2 - queue naif"
        else:
            daftar, geseran, waktu_ms, info_c, modul = self.ma.dequeue_circular(k)
            front, rear, kap, count = info_c
            res_teks = (f"{len(daftar)} pesanan keluar dari depan antrean circular.\n"
                        f"Tidak ada elemen yang digeser, front sekarang {front}, rear {rear}, kapasitas {kap:,}.\n"
                        f"Sisa antrean circular {count:,}.")
            catatan = "Yang berpindah hanya penunjuk front, memakai sisa bagi terhadap kapasitas. Isi larik tidak disentuh sama sekali, jadi biayanya O(1) berapa pun panjang antreannya."
            cmd_nama = "queue_dequeue_circular"
            mod_singkat = "M2 - queue circular"

        self.lbl_ringkasan_hasil.config(text=res_teks, foreground=self.c_pink_luminous)
        self.catat_command(cmd_nama, mod_singkat, waktu_ms, catatan)

        kolom = ["#", "oid", "pelanggan", "resto", "menu", "masuk"]
        self._bersihkan_tabel(kolom, ["#", "oid", "pelanggan", "resto", "menu", "masuk"])
        for i, p in enumerate(daftar, 1):
            self.tree.insert("", "end", values=(
                i,
                p.oid,
                p.pelanggan,
                p.resto,
                p.menu,
                format_waktu(p.t_masuk_detik)
            ))

    def _form_sort(self, kode):
        is_ins = kode == "SORT_INSERTION"
        if is_ins:
            judul = "Sort: insertion sort, O(n²)"
            deskripsi = "Setiap elemen digeser mundur sampai menemukan tempatnya. Sederhana, tetapi kerjanya tumbuh kuadratik."
            catatan = "Setiap elemen digeser mundur sampai menemukan tempatnya, jadi biayanya tumbuh kuadratik: melipatduakan jumlah baris membuat kerjanya kira-kira empat kali lipat. Jalankan SORT - MERGE SORT pada jumlah dan kunci yang sama, lalu bandingkan angka perbandingannya."
            default_n = "10"
        else:
            judul = "Sort: merge sort, O(n log n)"
            deskripsi = "Larik dibelah dua terus-menerus, lalu potongan yang sudah terurut disatukan kembali."
            catatan = "Larik dibelah dua terus-menerus lalu potongan yang sudah terurut disatukan kembali. Kedalaman belahannya log n dan tiap lapis menyentuh n elemen, jadi O(n log n). Hasilnya sama persis dengan insertion sort karena keduanya stabil."
            default_n = "4000"

        self.lbl_judul_menu.config(text=judul)
        self.lbl_deskripsi_menu.config(text=deskripsi)
        self.lbl_catatan.config(text=catatan)

        f_in = ttk.Frame(self.form_inputs_frame)
        f_in.pack(fill="x")

        ttk.Label(f_in, text="Jumlah baris diurutkan").pack(side="left", padx=4)
        ent_n = ttk.Entry(f_in, width=10)
        ent_n.insert(0, default_n)
        ent_n.pack(side="left", padx=4)

        ttk.Label(f_in, text="Diurutkan menurut").pack(side="left", padx=(10, 4))
        cb_kunci = ttk.Combobox(f_in, values=["harga", "oid", "selesai"], state="readonly", width=10)
        cb_kunci.set("harga" if is_ins else "oid")
        cb_kunci.pack(side="left", padx=4)

        ttk.Button(f_in, text="URUTKAN", style="Aksi.TButton",
                   command=lambda: self._aksi_sort(kode, ent_n.get(), cb_kunci.get())).pack(side="left", padx=10)

    def _aksi_sort(self, kode, str_n, kunci):
        if not self._validasi_muat_data():
            return
        try:
            n = int(str_n)
            if n <= 0:
                raise ValueError
        except ValueError:
            self.lbl_ringkasan_hasil.config(text="⚠️ Galat: Jumlah baris (n) harus berupa bilangan bulat positif!", foreground=self.c_pink_err)
            return

        is_ins = kode == "SORT_INSERTION"
        if is_ins and n > BATAS_INSERTION:
            msg_tolak = f"DITOLAK: batasnya {BATAS_INSERTION:,} baris, pakai merge sort untuk data penuh"
            self.lbl_ringkasan_hasil.config(text=msg_tolak, foreground=self.c_pink_err)
            messagebox.showwarning("Ditolak", msg_tolak)
            self.catat_command("insertion_sort", "M3 - insertion sort", 0, "Batas insertion sort 20.000 baris.")
            return

        if self._sedang_proses:
            return
        self._sedang_proses = True
        self.lbl_ringkasan_hasil.config(text=f"Sedang mengurutkan {n:,} baris...", foreground=self.c_pink_soft)
        self.update_idletasks()

        def _worker():
            if is_ins:
                hasil, banding, pindah, waktu_ms, modul, galat = self.ml.sort_insertion(self.mp, kunci, n)
                cmd_nama = "insertion_sort"
                mod_singkat = "M3 - insertion sort"
                catatan = "Setiap elemen digeser mundur sampai menemukan tempatnya, jadi biayanya tumbuh kuadratik: melipatduakan jumlah baris membuat kerjanya kira-kira empat kali lipat. Jalankan SORT - MERGE SORT pada jumlah dan kunci yang sama, lalu bandingkan angka perbandingannya."
            else:
                hasil, banding, pindah, waktu_ms, modul, galat = self.ml.sort_merge(self.mp, kunci, n)
                cmd_nama = "merge_sort"
                mod_singkat = "M3 - merge sort"
                catatan = "Larik dibelah dua terus-menerus lalu potongan yang sudah terurut disatukan kembali. Kedalaman belahannya log n dan tiap lapis menyentuh n elemen, jadi O(n log n). Hasilnya sama persis dengan insertion sort karena keduanya stabil."

            def _selesai():
                self._sedang_proses = False
                if galat:
                    self.lbl_ringkasan_hasil.config(text=f"⚠️ {galat}", foreground=self.c_pink_err)
                    return

                res_teks = (f"{len(hasil):,} pesanan diurutkan menurut {kunci}.\n"
                            f"{banding:,} perbandingan, {pindah:,} pemindahan.")
                self.lbl_ringkasan_hasil.config(text=res_teks, foreground=self.c_pink_luminous)
                self.catat_command(cmd_nama, mod_singkat, waktu_ms, catatan)

                # Tabel 6 kolom: #, oid, harga, selesai, resto, menu
                kolom = ["#", "oid", "harga", "selesai", "resto", "menu"]
                self._bersihkan_tabel(kolom, ["#", "oid", "harga", "selesai", "resto", "menu"])
                for i, p in enumerate(hasil[:100], 1):
                    self.tree.insert("", "end", values=(
                        i,
                        p.oid,
                        format_harga(p.harga),
                        format_waktu(p.t_selesai_detik),
                        p.resto,
                        p.menu
                    ))

            self.after(0, _selesai)

        threading.Thread(target=_worker, daemon=True).start()

    def _form_search(self, kode):
        is_lin = kode == "SEARCH_LINEAR"
        if is_lin:
            judul = "Search: linear search, O(n)"
            deskripsi = "Memeriksa pesanan satu per satu dari depan. Tidak menuntut data terurut."
            catatan = "Data tidak perlu terurut, tetapi setiap pesanan diperiksa satu per satu dari depan. Kasus terburuk menyentuh seluruh 200.000 baris."
        else:
            judul = "Search: binary search, O(log n)"
            deskripsi = "Membuang separuh sisa daftar pada setiap perbandingan. Menuntut daftar yang sudah terurut menurut oid."
            catatan = "Setiap perbandingan membuang separuh sisa daftar, jadi 200.000 baris habis dalam paling banyak 18 langkah. Syaratnya daftar harus SUDAH terurut menurut kunci yang dicari; di sini terurut menurut oid."

        self.lbl_judul_menu.config(text=judul)
        self.lbl_deskripsi_menu.config(text=deskripsi)
        self.lbl_catatan.config(text=catatan)

        f_in = ttk.Frame(self.form_inputs_frame)
        f_in.pack(fill="x")

        ttk.Label(f_in, text="Nomor pesanan (oid)").pack(side="left", padx=4)
        ent_oid = ttk.Entry(f_in, width=15)
        ent_oid.insert(0, "O-137442")
        ent_oid.pack(side="left", padx=4)

        ttk.Button(f_in, text="CARI", style="Aksi.TButton",
                   command=lambda: self._aksi_search(kode, ent_oid.get())).pack(side="left", padx=10)

    def _aksi_search(self, kode, str_oid):
        if not self._validasi_muat_data():
            return
        oid_clean = str_oid.strip()
        if not oid_clean:
            self.lbl_ringkasan_hasil.config(text="⚠️ Galat: Nomor pesanan (OID) tidak boleh kosong!", foreground=self.c_pink_err)
            return

        is_lin = kode == "SEARCH_LINEAR"
        if is_lin:
            idx, p, banding, waktu_ms, modul = self.ml.cari_linear(self.mp, oid_clean)
            info_cache = ""
            cmd_nama = "linear_search"
            mod_singkat = "M3 - linear search"
            catatan = f"Data tidak perlu terurut, tetapi setiap pesanan diperiksa satu per satu dari depan. Kasus terburuk menyentuh seluruh {len(self.mp.array):,} baris."
        else:
            idx, p, banding, waktu_ms, modul, info_cache = self.ml.cari_binary(self.mp, oid_clean)
            cmd_nama = "binary_search"
            mod_singkat = "M3 - binary search"
            catatan = "Setiap perbandingan membuang separuh sisa daftar, jadi 200.000 baris habis dalam paling banyak 18 langkah. Syaratnya daftar harus SUDAH terurut menurut kunci yang dicari; di sini terurut menurut oid."

        if idx == -1 or p is None:
            self.lbl_ringkasan_hasil.config(text=f"Pesanan {oid_clean} TIDAK DITEMUKAN. ({banding:,} perbandingan)", foreground=self.c_pink_err)
            self.catat_command(cmd_nama, mod_singkat, waktu_ms, catatan)
            self._bersihkan_tabel(["kolom", "isi"], ["kolom", "isi"])
            return

        total_baris = len(self.mp.array)
        if is_lin:
            res_teks = (f"Ditemukan pada indeks {idx:,}.\n"
                        f"{banding:,} perbandingan.")
        else:
            res_teks = ""
            if info_cache:
                res_teks += f"{info_cache}\n"
            res_teks += (f"Ditemukan pada baris ke-{idx + 1:,} dari {total_baris:,} baris.\n"
                         f"{banding:,} perbandingan, bandingkan dengan linear search.")

        self.lbl_ringkasan_hasil.config(text=res_teks, foreground=self.c_pink_luminous)
        self.catat_command(cmd_nama, mod_singkat, waktu_ms, catatan)

        rincian = [
            ("oid", p.oid),
            ("pelanggan", p.pelanggan),
            ("resto", p.resto),
            ("menu", p.menu),
            ("harga", format_harga(p.harga)),
            ("prioritas", str(p.prioritas)),
            ("masuk", format_waktu(p.t_masuk_detik)),
            ("selesai", format_waktu(p.t_selesai_detik)),
            ("status", p.status),
        ]
        self._tampilkan_tabel_kv(rincian)


def jalankan_aplikasi():
    app = App2EZ4U()
    app.mainloop()


if __name__ == "__main__":
    jalankan_aplikasi()
