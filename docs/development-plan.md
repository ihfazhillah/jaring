# Rencana Pengembangan Jaring

Dokumen ini menguraikan rencana pengembangan untuk Jaring berdasarkan isu-isu yang telah diidentifikasi. Rencana ini dibagi menjadi beberapa fase untuk memastikan pengembangan yang terstruktur dan terkelola.

---

## Fase 1: Refactoring Fondasi & Konfigurasi

Tujuan fase ini adalah untuk merombak struktur dasar aplikasi, membuatnya lebih fleksibel, dan mempersiapkan untuk penambahan fitur di masa depan.

### 1. Implementasi File Konfigurasi (Isu #4)

- **Tujuan:** Memindahkan pengaturan yang di-hardcode ke dalam file konfigurasi eksternal.
- **Rencana Teknis:**
    1. Buat file `config.yaml` di root proyek.
    2. Isi dengan parameter: `site_name`, `footer_text`, `content_path`, `template_path`, `output_path`.
    3. Di `jaring.py`, gunakan library `PyYAML` untuk membaca `config.yaml` di awal eksekusi.
    4. Ganti semua variabel yang di-hardcode dengan nilai dari file konfigurasi.
- **File Terdampak:** `jaring.py`, `templates/base.html`.

### 2. Pengurutan Berdasarkan Tanggal Terbaru (Isu #9)

- **Tujuan:** Memastikan pesan di halaman indeks selalu ditampilkan dari yang terbaru hingga terlama.
- **Rencana Teknis:**
    1. Di `jaring.py`, setelah semua file markdown di-parse menjadi list `posts`.
    2. Gunakan `posts.sort(key=lambda p: p['metadata']['id'], reverse=True)` untuk mengurutkan list.
    3. Pengurutan ini diasumsikan aman karena format `id` (YYYY-MM-DD) mendukung pengurutan leksikografis.
- **File Terdampak:** `jaring.py`.

### 3. Hilangkan Konsep "Series" (Isu #6)

- **Tujuan:** Menyederhanakan struktur proyek dengan menghapus pengelompokan berdasarkan `series`.
- **Rencana Teknis:**
    1. Hapus field `series` dari semua file markdown di `examples/`.
    2. Di `jaring.py`:
        - Hapus logika untuk mengelompokkan post berdasarkan `series`.
        - Ubah path output untuk pesan menjadi `output/messages/[id].html`.
        - Hapus pembuatan halaman indeks per-seri.
    3. Di `templates/index.html`, sesuaikan tautan `href` untuk tidak lagi menyertakan direktori `series`.
    4. Di `templates/base.html`, perbarui logika `depth` karena struktur direktori menjadi lebih datar.
- **File Terdampak:** `jaring.py`, semua file `.md`, `templates/index.html`, `templates/base.html`.

---

## Fase 2: Fitur Inti & Peningkatan Konten

Tujuan fase ini adalah untuk membangun fitur-fitur utama yang meningkatkan cara pengguna menemukan dan mengonsumsi konten.

### 4. Implementasi Paginasi (Isu #2)

- **Tujuan:** Membatasi jumlah pesan per halaman untuk meningkatkan performa dan pengalaman pengguna.
- **Rencana Teknis:**
    1. Di `jaring.py`, setelah daftar `posts` diurutkan, bagi menjadi beberapa bagian (chunks) berisi 20 item.
    2. Buat beberapa file `index.html`, `page-2.html`, `page-3.html`, dst.
    3. Teruskan informasi halaman saat ini dan total halaman ke `index.html`.
    4. Di `templates/index.html`, tambahkan navigasi paginasi (misal: "Sebelumnya", "1, 2, 3", "Berikutnya").
- **File Terdampak:** `jaring.py`, `templates/index.html`.

### 5. Fungsionalitas Tag (Isu #5)

- **Tujuan:** Memberikan cara baru untuk mengkategorikan dan menemukan pesan.
- **Rencana Teknis:**
    1. Tambahkan field `tags` (berupa list) ke frontmatter beberapa file markdown contoh.
    2. Di `jaring.py`:
        - Buat struktur data untuk melacak semua tag dan pesan yang terkait dengan setiap tag.
        - Buat halaman indeks untuk setiap tag di `output/tags/[nama-tag].html`.
    3. Di `templates/message.html`, tampilkan daftar tag yang dimiliki pesan tersebut.
    4. Buat templat baru `templates/tag_index.html` untuk halaman daftar pesan per-tag.
- **File Terdampak:** `jaring.py`, `templates/message.html`, file-file `.md`.

---

## Fase 3: Pengalaman Pengguna & Fitur Lanjutan

Tujuan fase ini adalah untuk menyempurnakan interaksi pengguna dan menambahkan fitur-fitur canggih untuk berbagi dan presentasi konten.

### 6. Tombol Kembali (Isu #3)

- **Tujuan:** Memudahkan navigasi dari halaman pesan kembali ke halaman utama.
- **Rencana Teknis:**
    1. Di `templates/message.html`, tambahkan tautan "Kembali" di bagian atas, di bawah judul.
    2. Tautan ini harus mengarah ke `../index.html` (atau path relatif yang sesuai berdasarkan struktur baru).
- **File Terdampak:** `templates/message.html`.

### 7. Tampilkan Teks Penuh di Halaman Depan (Isu #1)

- **Tujuan:** Memberikan opsi untuk menampilkan konten penuh di halaman indeks.
- **Rencana Teknis:**
    1. Di `templates/index.html`, ganti `post.metadata.preview` dengan `post.html | safe`.
    2. Keputusan ini mungkin perlu ditinjau kembali setelah paginasi diimplementasikan, karena dampaknya terhadap panjang halaman akan berkurang.
- **File Terdampak:** `templates/index.html`.

### 8. Konversi Teks ke Gambar (Isu #7)

- **Tujuan:** Membuat gambar pratinjau secara otomatis dari teks.
- **Rencana Teknis:**
    1. Gunakan library `pictex` seperti yang disarankan. Tambahkan ke `requirements.txt`.
    2. Di `jaring.py`, saat mem-parse konten, gunakan regex untuk mencari notasi `[[...]]`.
    3. Ekstrak teks, lalu panggil `pictex` untuk menghasilkan gambar dari teks tersebut. Ini mungkin memerlukan konfigurasi template dan font untuk `pictex`.
    4. Simpan gambar ke `output/assets/images/`.
    5. Tambahkan path gambar ke data `post` untuk digunakan di `og:image`.
    6. Hapus notasi dari konten sebelum di-render sebagai HTML.
- **File Terdampak:** `jaring.py`, `requirements.txt`.

### 9. Implementasi Web Share API (Isu #8)

- **Tujuan:** Memungkinkan berbagi konten melalui dialog bawaan sistem operasi.
- **Rencana Teknis:**
    1. Di `templates/message.html`, tambahkan tombol "Bagikan" dan skrip JavaScript terkait.
    2. Skrip akan memanggil `navigator.share` dengan judul, URL, dan teks yang diekstrak dari Isu #7.
    3. Pastikan untuk menangani kasus di mana API tidak tersedia.
- **File Terdampak:** `templates/message.html`.
