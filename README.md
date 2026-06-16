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
1. Kloning Repositori
Unduh repositori ini ke dalam mesin lokal Anda:
```text
git clone [https://github.com/username/nama-repositori.git](https://github.com/username/nama-repositori.git)
cd nama-repositori
```

2. Instalasi Pustaka Pendukung
Pasang semua dependensi yang diperlukan dengan menjalankan perintah berikut di terminal:
```text
pip install -r requirements.txt
```

3. Menjalankan Aplikasi
Eksekusi server lokal Streamlit untuk membuka antarmuka web:
```text
streamlit run penjadwalan_ga.py
```
Setelah perintah dijalankan, aplikasi akan otomatis terbuka di peramban (browser) Anda, biasanya pada alamat http://localhost:8501.

## 📊 Format Dokumen Masukan (Excel)
Untuk memastikan data dapat dibaca dengan benar oleh data_parser.py, berkas Excel (.xlsx) masukan wajib memiliki struktur 4 lembar kerja (sheets) dengan urutan berikut:
Sheet 1: Parameter Global
- Memuat informasi parameter operasional seperti waktu mulai, waktu selesai, dan durasi satuan SKS dalam menit.
Sheet 2: Data Ruangan
- Memuat daftar seluruh kode ruangan yang tersedia untuk digunakan sebagai tempat perkuliahan.
Sheet 3: Data Dosen
- Memuat nama lengkap dosen beserta daftar hari libur atau hari halangan mengajar mereka (dipisahkan dengan koma jika lebih dari satu hari).
Sheet 4: Data Mata Kuliah
- Memuat susunan kolom: Kurikulum, Kode Matakuliah, Nama Matakuliah (termasuk penanda kelas seperti (A) atau (MBKM)), Semester, SKS, dan Nama Dosen Pengampu. Mendukung format baris terpisah atau sel ter-merge untuk dosen anggota/tim.
