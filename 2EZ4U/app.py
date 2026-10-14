import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from frontend.ui import jalankan_aplikasi

if __name__ == "__main__":
    jalankan_aplikasi()
