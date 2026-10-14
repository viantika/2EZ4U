"""
Aplikasi '2EZ4U Food Delivery'
Struktur Data & Analisa Algoritma (M1 - M3)

Jalankan:
    python app.py
"""
import sys
import os

# Pastikan folder project berada pada sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from frontend.ui import jalankan_aplikasi

if __name__ == "__main__":
    jalankan_aplikasi()
