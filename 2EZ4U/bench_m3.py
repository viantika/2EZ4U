"""
Skrip benchmark M3: Pengujian skala n vs perbandingan.
Mengukur jumlah perbandingan dan waktu (ms) untuk:
- Insertion Sort vs Merge Sort (n = 1.000, 2.000, 4.000, 8.000)
- Linear Search vs Binary Search

Jalankan:
    python bench_m3.py
"""
import random
import os
import sys

# Pastikan path modul terdeteksi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.m1_pesanan import ManajerPesanan, format_harga
from backend.m3_laporan import (
    insertion_sort,
    merge_sort,
    linear_search,
    binary_search,
    Pencacah,
)


def jalankan_benchmark():
    print("=" * 75)
    print("BENCHMARK M3: PENGUJIAN SKALA N VS PERBANDINGAN & WAKTU (2EZ4U)")
    print("=" * 75)

    csv_path = os.path.join(os.path.dirname(__file__), "data", "pesanan.csv")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} tidak ditemukan!")
        return

    print("Memuat dataset dari pesanan.csv ...")
    mp = ManajerPesanan()
    total_data, waktu_load, _ = mp.muat_csv(csv_path)
    print(f"Selesai muat {total_data:,} baris dalam {waktu_load:.2f} ms.\n")

    # 1. Benchmark Sort
    ukuran_n = [1000, 2000, 4000, 8000]
    hasil_bench = []

    print("-" * 75)
    print(f"{'n':<8} | {'Insertion (Bandingan)':<22} | {'Merge (Bandingan)':<18} | {'Waktu Ins (ms)':<14} | {'Waktu Merge (ms)'}")
    print("-" * 75)

    for n in ukuran_n:
        # Ambil sampel data acak/asli sepanjang n
        sampel_ins = []
        sampel_merge = []
        for i in range(n):
            p = mp.array.get(i)
            sampel_ins.append(p)
            sampel_merge.append(p)

        pb_ins = Pencacah()
        pp_ins = Pencacah()
        _, b_ins, p_ins, w_ins, _, _ = insertion_sort(sampel_ins, "harga", pb_ins, pp_ins)

        pb_mrg = Pencacah()
        pp_mrg = Pencacah()
        _, b_mrg, p_mrg, w_mrg, _, _ = merge_sort(sampel_merge, "harga", pb_mrg, pp_mrg)

        hasil_bench.append((n, b_ins, b_mrg, w_ins, w_mrg))
        print(f"{n:<8} | {b_ins:<22,d} | {b_mrg:<18,d} | {w_ins:<14.2f} | {w_mrg:<14.2f}")

    print("-" * 75)
    print("Analisis Pertumbuhan Sort:")
    for i in range(1, len(hasil_bench)):
        n_prev, b_i_prev, b_m_prev, _, _ = hasil_bench[i - 1]
        n_curr, b_i_curr, b_m_curr, _, _ = hasil_bench[i]
        rasio_ins = b_i_curr / b_i_prev
        rasio_mrg = b_m_curr / b_m_prev
        print(f"- Dari n={n_prev} ke n={n_curr} (2x lipat):")
        print(f"  * Insertion Sort: {rasio_ins:.2f}x lipat (Teori O(n^2) mendekati 4.0x)")
        print(f"  * Merge Sort    : {rasio_mrg:.2f}x lipat (Teori O(n log n) mendekati 2.1x - 2.2x)")

    # 2. Benchmark Search
    print("\n" + "=" * 75)
    print("BENCHMARK PENCARIAN (OID: O-008000 pada 200.000 data)")
    print("=" * 75)

    target = "O-008000"
    data_penuh = mp.array.to_list()

    # Siapkan data terurut untuk binary search
    data_terurut, _, _, waktu_sort_awal, _, _ = merge_sort(list(data_penuh), "oid")

    # Linear Search
    idx_l, _, b_lin, w_lin, _ = linear_search(data_penuh, target)

    # Binary Search
    idx_b, _, b_bin, w_bin, _ = binary_search(data_terurut, target)

    print(f"Target OID       : {target}")
    print(f"Linear Search    : Indeks={idx_l}, Perbandingan={b_lin:,}, Waktu={w_lin:.4f} ms")
    print(f"Binary Search    : Indeks={idx_b}, Perbandingan={b_bin:,}, Waktu={w_bin:.4f} ms")
    print(f"Rasio Bandingan  : Linear Search butuh {b_lin / b_bin:.1f}x lebih banyak perbandingan daripada Binary Search!")
    print("=" * 75)


if __name__ == "__main__":
    jalankan_benchmark()
