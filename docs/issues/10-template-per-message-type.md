# Isu 10: Dukungan Template Berdasarkan Tipe Pesan/Konten

## Deskripsi

Saat ini, tampilan untuk pesan (message) kemungkinan besar ditangani oleh template umum seperti `message.html` atau `message-detail.html`. Untuk mendukung fleksibilitas dan skalabilitas di masa depan, kita perlu memperkenalkan konsep "tipe pesan" atau "tipe konten" yang memungkinkan setiap tipe memiliki template tampilannya sendiri.

Ini akan memungkinkan kita untuk:
-   Menampilkan berbagai jenis konten (misalnya, "artikel", "event", "kutipan") dengan tata letak dan gaya yang berbeda tanpa memodifikasi template default.
-   Memudahkan penambahan tipe konten baru di masa mendatang.

## Kriteria Penerimaan

-   Sistem harus dapat mengidentifikasi tipe pesan/konten dari data yang diproses.
-   Harus ada mekanisme untuk memetakan tipe pesan/konten ke file template HTML tertentu (misalnya, `type_artikel.html` untuk tipe "artikel", `type_event.html" untuk tipe "event").
-   Jika tidak ada template spesifik yang ditemukan untuk suatu tipe, sistem harus kembali menggunakan template default (misalnya, `message.html`).
-   Struktur file template harus jelas dan mudah dikelola.
