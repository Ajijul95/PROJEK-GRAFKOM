# Project PAA/Grafika Komputer - Peta Kota 2D, Dijkstra, Zoom, Scroll, dan Animasi Kendaraan

Project ini merupakan aplikasi simulasi peta kota 2D berbasis Python Tkinter. Program menampilkan struktur peta kota, jaringan jalan, pencarian rute menggunakan algoritma Dijkstra, navigasi tampilan peta, fitur zoom, serta animasi kendaraan yang dapat dikontrol menggunakan tombol Start dan Pause.

## Tujuan Project

Tujuan utama project ini adalah membuat simulasi peta kota sederhana yang dapat digunakan untuk menampilkan jalur perjalanan kendaraan dari titik awal menuju titik tujuan. Peta dibangun dari struktur jalan yang membentuk jaringan node dan edge. Jaringan tersebut kemudian digunakan oleh algoritma Dijkstra untuk mencari rute terpendek. Selain itu, pengguna dapat menggeser tampilan peta, memperbesar atau memperkecil skala tampilan, serta menjalankan dan menghentikan sementara animasi kendaraan.

## Fitur Utama

- Membuat struktur peta kota secara dinamis.
- Membentuk jaringan jalan yang terdiri dari node dan edge.
- Menampilkan area peta, jalan, bangunan, dan elemen lingkungan.
- Memilih titik awal dan titik tujuan.
- Mencari rute terpendek menggunakan algoritma Dijkstra.
- Menggeser tampilan peta menggunakan sistem navigasi/scroll/pan.
- Melakukan zoom in dan zoom out pada tampilan peta.
- Mengelola skala tampilan agar objek tetap proporsional saat diperbesar atau diperkecil.
- Menjalankan animasi kendaraan pada rute yang ditemukan.
- Mengontrol simulasi menggunakan tombol Start dan Pause.

## Teknologi yang Digunakan

- Python 3
- Tkinter
- Struktur program modular
- Algoritma Dijkstra
- Canvas 2D untuk visualisasi peta

Project ini tidak membutuhkan library eksternal tambahan karena menggunakan Tkinter yang umumnya sudah tersedia pada instalasi Python standar.

## Cara Menjalankan Program

1. Pastikan Python sudah terpasang di laptop/komputer.
2. Ekstrak file ZIP project.
3. Masuk ke folder runtime program gabungan:


4. Jalankan file utama:

```bash
python main.py
```

Jika menggunakan Windows dan perintah `python` tidak berjalan, coba gunakan:

```bash
py main.py
```

## Struktur Folder

```text
MODUL_TERPISAH_SESUAI_PEMBAGIAN_TUGAS/
│
├── 00_RUNTIME_PROGRAM_GABUNGAN_SIAP_JALAN/
│   ├── main.py
│   ├── analisis_kompleksitas.py
│   ├── ANALISIS_KOMPLEKSITAS.md
│   ├── algo/
│   ├── map/
│   └── ui/
│
├── 01_MODUL_AKBAR_RIZKI_LINGGA_STRUKTUR_PETA_JARINGAN_JALAN/
│   ├── source_full/
│   ├── cuplikan_kode_kunci.py
│   └── README.md
│
├── 02_MODUL_FARHAN_DWI_SAPUTRA_NAVIGASI_SCROLL_PETA/
│   ├── source_full/
│   ├── cuplikan_kode_kunci.py
│   └── README.md
│
├── 03_MODUL_MUHAMMAD_AL_FIKRY_AKBAR_ZOOM_SKALA_TAMPILAN/
│   ├── source_full/
│   ├── cuplikan_kode_kunci.py
│   └── README.md
│
├── 04_MODUL_AZIZUL_RIZKY_MAHADI_PENCARIAN_RUTE_START_TUJUAN/
│   ├── source_full/
│   ├── cuplikan_kode_kunci.py
│   └── README.md
│
└── 05_MODUL_AL_ADLHU_SODRI_NIWRAD_ANIMASI_KENDARAAN_KONTROL_SIMULASI/
    ├── source_full/
    ├── cuplikan_kode_kunci.py
    └── README.md
```

## Pembagian Tugas Anggota

### 1. Akbar Rizki Lingga

Bertanggung jawab dalam perancangan struktur peta dan pembentukan jaringan jalan secara dinamis.

Fokus pekerjaan:

- Membuat struktur dasar peta kota.
- Membentuk jalan luar dan jalan dalam.
- Membuat variasi bentuk jalan agar tampilan tidak kaku.
- Membentuk node dan edge dari jaringan jalan.
- Menyiapkan struktur peta agar dapat digunakan oleh fitur pencarian rute.

File yang berkaitan:

- `map/grid_kota.py`
- `map/utils.py`
- `map/grid/grid_kota.py`
- `map/grid/roads.py`
- `map/grid/clip.py`
- `map/grid/vector.py`
- `map/grid/buildings.py`
- `map/grid/nature.py`

### 2. Farhan Dwi Saputra

Bertanggung jawab dalam pengembangan sistem navigasi peta, khususnya fitur pergeseran tampilan atau scroll/pan.

Fokus pekerjaan:

- Mengatur pergeseran tampilan peta.
- Menghubungkan input pengguna dengan pergerakan kamera.
- Membantu pengguna melihat bagian peta yang berbeda.
- Menjaga agar posisi tampilan tetap nyaman saat peta digeser.

File yang berkaitan:

- `map/kamera.py`
- `ui/app.py`

### 3. Muhammad Al-Fikry Akbar

Bertanggung jawab dalam implementasi fitur zoom serta pengelolaan skala tampilan peta.

Fokus pekerjaan:

- Membuat fitur zoom in dan zoom out.
- Membatasi nilai zoom agar tidak terlalu kecil atau terlalu besar.
- Mengatur konversi koordinat layar ke koordinat dunia peta.
- Menjaga ukuran tampilan objek agar tetap sesuai ketika peta diperbesar atau diperkecil.

File yang berkaitan:

- `map/kamera.py`
- `ui/app.py`

### 4. Azizul Rizky Mahadi

Bertanggung jawab dalam pengembangan sistem pencarian rute dan pengaturan posisi awal serta tujuan.

Fokus pekerjaan:

- Menentukan titik awal dan titik tujuan.
- Mengubah data jalan menjadi graph.
- Menjalankan algoritma Dijkstra untuk mencari rute terpendek.
- Menampilkan hasil rute pada peta.

File yang berkaitan:

- `algo/dijkstra.py`
- `algo/pencarian.py`
- `ui/app.py`

### 5. Al Adlhu Sodri Niwrad

Bertanggung jawab dalam pengembangan animasi pergerakan kendaraan dan kontrol simulasi.

Fokus pekerjaan:

- Menampilkan kendaraan pada peta.
- Menggerakkan kendaraan mengikuti rute yang ditemukan.
- Menambahkan kontrol simulasi.
- Menambahkan tombol Start untuk menjalankan animasi.
- Menambahkan tombol Pause untuk menghentikan sementara animasi.
- Menjaga agar animasi dapat dilanjutkan kembali dari posisi terakhir.

File yang berkaitan:

- `ui/app.py`
- `map/render/renderer.py`
- `map/kamera.py`


## Alur Kerja Program

1. Program dijalankan melalui `main.py`.
2. Aplikasi membuat jendela utama menggunakan Tkinter.
3. Peta kota dibentuk dari modul struktur peta.
4. Jalan-jalan pada peta diubah menjadi jaringan node dan edge.
5. Pengguna menentukan titik awal dan titik tujuan.
6. Sistem menjalankan algoritma Dijkstra untuk mencari rute terpendek.
7. Rute hasil pencarian ditampilkan pada peta.
8. Pengguna dapat melakukan zoom dan scroll untuk melihat peta dengan lebih jelas.
9. Ketika tombol Start ditekan, kendaraan bergerak mengikuti rute.
10. Ketika tombol Pause ditekan, kendaraan berhenti sementara di posisi terakhir.
11. Ketika tombol Start ditekan kembali, kendaraan melanjutkan animasi dari posisi terakhir.

```
