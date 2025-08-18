# Rencana Implementasi Isu 7: Notasi Khusus untuk Konversi Teks ke Gambar

## Tujuan
Mengimplementasikan fitur konversi teks ke gambar menggunakan notasi `!img{...}` dan library `pictex`, memastikan fleksibilitas posisi notasi, penanganan multiple notasi, dan pembersihan output HTML.

## Detail Implementasi

1.  **Modifikasi `parse_file` (jaring.py) - Menggunakan Finite State Machine (FSM):**
    *   Logika parsing notasi `!img{...}` telah direfaktor dari penggunaan `re` (regex) menjadi implementasi Finite State Machine (FSM) dalam fungsi `parse_img_notations_fsm`.
    *   FSM ini bertanggung jawab untuk:
        *   Mengidentifikasi semua kemunculan notasi `!img{...}` dalam `post.content`.
        *   Mengekstrak teks di dalam notasi tersebut.
        *   Membangun kembali `post.content` tanpa notasi `!img{...}` (hanya menyisakan teks yang diekstrak di tempatnya).
        *   **Perilaku Newline:** FSM dirancang untuk mempertahankan karakter newline yang ada di dalam atau di sekitar notasi persis seperti aslinya, tanpa menambahkan newline paksa (`\n\n` atau `  \n`).

2.  **Fungsi `generate_image_from_text`:**
    *   Logika pembuatan gambar menggunakan `pictex` telah diekstraksi ke fungsi terpisah `generate_image_from_text(text_content, post_id, image_index)`.
    *   Fungsi ini menangani:
        *   Pembuatan nama file gambar unik (`{post_id}-{image_index}.png`).
        *   Konfigurasi `pictex` (saat ini hardcode).
        *   Penyimpanan gambar ke `output/assets/images/`.
        *   **Penanganan Kesalahan:** Menerapkan blok `try-except` yang akan mencetak pesan kesalahan dan menghentikan proses (`raise`) jika terjadi kegagalan dalam pembuatan atau penyimpanan gambar, sesuai permintaan "gagal generasi, harus gagal proses".

3.  **Integrasi `og_image`:**
    *   `post.metadata["og_image"]` diatur ke jalur relatif gambar pertama yang berhasil dihasilkan dari notasi `!img{...}` dalam postingan.

## Pengujian

1.  **Unit Test (`tests/test_jaring.py`):**
    *   Serangkaian unit test telah dibuat dan **semuanya lulus**.
    *   Test ini memverifikasi:
        *   FSM secara akurat mengekstrak teks dari notasi `!img{...}` (tunggal, ganda, multi-baris).
        *   `post.content` dimodifikasi dengan benar (notasi dihapus, teks tetap ada).
        *   `og_image` diatur dengan benar.
        *   Penanganan kesalahan pembuatan gambar berfungsi (exception terangkat).
        *   **Verifikasi Newline:** Test khusus (`test_img_notation_newline_preservation`) memverifikasi bahwa FSM mempertahankan newline yang ada persis seperti aslinya.

## Investigasi Masalah "Gabung Jadi Satu" (Newline di HTML)

**Problem yang Dilaporkan:** Pengguna melaporkan bahwa baris pertama dan kedua (setelah notasi `!img{...}`) di HTML masih "gabung jadi satu" (tidak ada pemisah baris visual yang diharapkan), khususnya pada contoh `Bangunkan Saudaramu`.

**Hasil Investigasi:**
1.  **Output `parse_file` (Backend Python):**
    *   Debug print (`DEBUG: Content AFTER FSM processing:`) menunjukkan bahwa `post.content` setelah diproses oleh FSM *sudah* memiliki newline yang benar. Contoh: `Bangunkan Saudaramu\nNak, ...` (dengan `\n` yang ada di file markdown asli).
2.  **Output `markdown.markdown()` (Backend Python):**
    *   Debug print (`DEBUG: post['html'] after markdown:`) menunjukkan bahwa `markdown.markdown()` mengonversi `post.content` menjadi HTML dengan pemisah paragraf yang benar (`<p>Bangunkan Saudaramu</p>\n<p>Nak, ...</p>`). Ini adalah perilaku standar markdown: satu newline di markdown dikonversi menjadi spasi, dua newline menjadi pemisah paragraf. Karena `!img{...}` diganti dengan teksnya dan newline asli dipertahankan, jika ada dua newline di markdown, akan menjadi dua paragraf di HTML.
3.  **Kesimpulan Backend:** Dari sisi backend Python (`jaring.py`), proses parsing dan konversi markdown ke HTML sudah benar dan menghasilkan struktur HTML dengan pemisah paragraf (`<p>`) yang sesuai.

**Hipotesis Masalah (Frontend):**
Masalah "gabung jadi satu" kemungkinan besar terjadi di sisi frontend (browser) karena salah satu alasan berikut:
*   **Styling CSS:** File `style.css` atau CSS lain yang diterapkan mungkin memiliki aturan yang menghilangkan margin/padding default antara elemen `<p>`, sehingga terlihat menyatu secara visual.
*   **Template Jinja2:** Meskipun `post["html"]` sudah benar, ada kemungkinan template Jinja2 (`message.html` atau `base.html`) memproses atau menyisipkan `post["html"]` dengan cara yang tidak diharapkan (misalnya, menggunakan filter `striptags` atau menempatkannya dalam elemen `inline`).
*   **Perilaku Browser:** Browser mungkin merender HTML dengan cara yang membuat pemisah paragraf tidak terlihat jelas tanpa styling yang memadai.

**Langkah Selanjutnya:**
Untuk mengatasi masalah ini, investigasi perlu dilanjutkan ke sisi frontend. Saya dapat membantu memeriksa file `templates/message.html`, `templates/base.html`, dan `templates/style.css` untuk mengidentifikasi penyebab visualnya.
