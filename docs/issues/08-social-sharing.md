# Isu 8: Implementasi Tombol Berbagi (Share) Menggunakan API Bawaan

**Latar Belakang:**
Pesan-pesan ini ditujukan untuk dibagikan. Cara berbagi yang paling natural di perangkat mobile adalah menggunakan dialog berbagi (share sheet) bawaan sistem operasi.

**Permintaan:**
Tambahkan sebuah tombol "Bagikan" yang akan memicu Web Share API (`navigator.share`) jika didukung oleh browser.

**Detail Implementasi:**
1.  **Tombol:** Buat sebuah tombol "Bagikan" atau ikon berbagi di halaman pesan.
2.  **JavaScript:** Tambahkan skrip JavaScript untuk menangani klik pada tombol tersebut.
3.  **Web Share API:**
    - Skrip akan memeriksa apakah `navigator.share` tersedia.
    - Jika tersedia, panggil `navigator.share()` dengan data yang relevan.
    - **Penting:** `text` yang dibagikan haruslah teks yang diberi notasi khusus untuk dijadikan gambar (lihat Isu #7).
      ```javascript
      navigator.share({
        title: '{{ post.metadata.title }}',
        text: '[Teks dari notasi di Isu #7]', // Teks yang akan dibagikan
        url: window.location.href
      })
      ```
    - Ini akan membuka dialog berbagi bawaan di Android, iOS, dan platform lain yang mendukung.
4.  **Fallback (Opsional):**
    - Jika `navigator.share` tidak didukung (misalnya di browser desktop), bisa disediakan tautan berbagi manual sebagai alternatif, atau sembunyikan tombol tersebut.
