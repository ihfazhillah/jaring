# Isu 4: File Konfigurasi Terpusat

**Latar Belakang:**
Saat ini, beberapa konfigurasi seperti path ke konten, nama situs, dan teks footer di-hardcode di dalam skrip `jaring.py` atau templat.

**Permintaan:**
Buat sebuah file konfigurasi terpusat (misalnya `config.json` atau `config.yaml`) untuk mengelola pengaturan global situs.

**Pengaturan yang Perlu Dimasukkan:**
- `content_path`: Path ke direktori yang berisi file-file markdown.
- `template_path`: Path ke direktori templat.
- `output_path`: Path ke direktori keluaran.
- `site_name`: Nama situs yang akan ditampilkan di judul dan header.
- `footer_text`: Teks yang akan ditampilkan di footer.

**Keuntungan:**
- Memudahkan pengguna untuk mengubah pengaturan tanpa harus mengedit kode Python.
- Membuat skrip lebih fleksibel dan dapat digunakan kembali.
