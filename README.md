# Sistem Penjadwalan Otomatis Menggunakan Algoritma Genetika

Sistem Penjadwalan Otomatis adalah aplikasi berbasis Web yang dirancang untuk menyusun jadwal perkuliahan secara optimal tanpa bentrok menggunakan metode Algoritma Genetika. Aplikasi ini dibangun dengan bahasa pemrograman Python dan menggunakan Streamlit sebagai antarmuka pengguna yang interaktif dan mudah digunakan.

## ✨ Fitur Utama

- **Optimasi Tanpa Bentrok (Zero Conflict)**: Meminimalkan dan mencegah tabrakan jadwal pada waktu mengajar dosen, waktu kuliah kelas mahasiswa, dan penggunaan kapasitas ruangan.
- **Dukungan Team Teaching (Merged Cells)**: Mampu membaca dan memproses kelas yang diampu oleh tim dosen (Ketua dan Anggota) dari sel Excel yang digabungkan (*merged cells*), memastikan tidak ada satupun anggota tim yang jadwalnya berbenturan.
- **Penyaringan Kelas MBKM Otomatis**: Mendeteksi dan mengecualikan kelas berskema MBKM (Merdeka Belajar Kampus Merdeka) secara otomatis dari penjadwalan fisik kampus.
- **Eksperimen Parameter Fleksibel**: Pengaturan ukuran populasi, jumlah generasi, batas *auto-restart*, probabilitas *crossover*, dan *mutation rate* dapat diubah secara dinamis melalui UI Web untuk menangani skala data yang padat.
- **Ekspor Hasil ke Excel**: Jadwal terbaik yang ditemukan oleh algoritma dapat diunduh langsung dalam bentuk berkas spreadsheet `.xlsx` yang rapi dan terurut berdasarkan hari dan waktu.

## 📂 Struktur Direktori

```text
├── data_parser.py       # Modul untuk membaca, membersihkan, dan mengekstrak data dari Excel
├── penjadwalan_ga.py    # Modul utama Algoritma Genetika dan Antarmuka Web Streamlit
├── requirements.txt     # Daftar pustaka (library) Python yang dibutuhkan
├── .gitignore           # Daftar berkas dan folder yang diabaikan oleh Git
└── README.md            # Dokumentasi repositori proyek
```

## ⚙️ Prasyarat Sistem
Sebelum menjalankan aplikasi, pastikan perangkat Anda sudah terpasang:
Python versi 3.9 atau yang lebih baru
PIP (Python Package Installer)

## 🚀 Langkah Instalasi dan Penggunaan
Kloning Repositori
Unduh repositori ini ke dalam mesin lokal Anda:
