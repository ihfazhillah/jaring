# Isu 11: Dukungan Jalankan Skrip dengan Jalur Konfigurasi Kustom

## Deskripsi

Saat ini, skrip kemungkinan besar membaca konfigurasi dari file `config.yaml` yang berada di lokasi default. Untuk meningkatkan fleksibilitas dan memungkinkan penggunaan konfigurasi yang berbeda tanpa memodifikasi file asli, kita perlu menambahkan kemampuan untuk menentukan jalur file konfigurasi kustom saat menjalankan skrip.

Ini akan sangat berguna untuk:
-   Pengembangan di lingkungan yang berbeda (development, staging, production).
-   Menjalankan skrip dengan setelan khusus untuk tujuan pengujian atau debugging.
-   Mengelola beberapa proyek yang menggunakan skrip yang sama tetapi dengan konfigurasi yang berbeda.

## Kriteria Penerimaan

-   Skrip harus menerima argumen baris perintah (misalnya, `--config` atau `-c`) untuk menentukan jalur ke file konfigurasi.
-   Jika argumen jalur konfigurasi tidak diberikan, skrip harus tetap menggunakan file `config.yaml` di lokasi default (misalnya, di root proyek).
-   Skrip harus dapat menangani kesalahan jika file konfigurasi yang ditentukan tidak ditemukan atau tidak valid.
-   Prioritas pembacaan konfigurasi: argumen baris perintah > lokasi default.
