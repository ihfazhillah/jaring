# Isu 6: Hilangkan Konsep "Series"

**Latar Belakang:**
Saat ini, semua pesan dikelompokkan berdasarkan `series`. Hal ini menciptakan struktur direktori `output/<series>/...` dan memerlukan field `series` di setiap file markdown.

**Permintaan:**
Sederhanakan struktur dengan menghilangkan konsep `series`.

**Detail Implementasi:**
- Hapus field `series` dari frontmatter.
- Ubah struktur output menjadi lebih datar, misalnya:
  - `/index.html` (halaman utama)
  - `/messages/[id].html` (halaman pesan)
- Skrip `jaring.py` perlu dimodifikasi secara signifikan untuk tidak lagi mengelompokkan berdasarkan seri.
- Ini akan menjadi perubahan besar (breaking change) pada struktur dan logika aplikasi.
