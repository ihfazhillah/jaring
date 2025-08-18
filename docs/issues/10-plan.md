# Rencana Implementasi Isu 10: Dukungan Template Berdasarkan Tipe Pesan/Konten

## Tujuan
Mengimplementasikan sistem yang memungkinkan setiap tipe konten (misalnya, 'artikel', 'event') memiliki template HTML-nya sendiri, dengan fallback ke template default jika template spesifik tidak ditemukan.

## Detail Implementasi

1.  **Definisi Tipe Konten:**
    *   **Sumber Tipe:** Tipe konten akan didefinisikan dalam frontmatter file markdown. Contoh:
        ```yaml
        ---
        id: 1447-01-01-contoh-artikel
        title: Judul Artikel
        type: article # <-- Tambahkan field ini
        ---
        ```
    *   **Default Type:** Jika field `type` tidak ada di frontmatter, anggap sebagai tipe default (misalnya, 'message').

2.  **Modifikasi `parse_file` (jaring.py):**
    *   Pastikan fungsi `parse_file` membaca field `type` dari metadata frontmatter dan menyimpannya ke dalam dictionary `post` yang dikembalikan. Contoh: `post["metadata"]["type"]`.

3.  **Logika Pemilihan Template di `main()` (jaring.py):**
    *   Navigasi ke bagian `main()` di mana halaman pesan individual dibuat:
        ```python
        # Generate individual message pages
        for post in posts:
            # ... kode yang ada ...
            # html = render_html(template_env, "message.html", {"post": post, "depth": 1}) # <-- Baris ini akan dimodifikasi
            # ... kode yang ada ...
        ```
    *   Sebelum memanggil `render_html`, tentukan nama template yang akan digunakan:
        ```python
        # Dapatkan tipe konten, default ke 'message' jika tidak ada
        content_type = post["metadata"].get("type", "message")
        
        # Tentukan nama template berdasarkan tipe konten
        # Contoh: 'type_article.html', 'type_event.html', atau 'message.html'
        template_name = f"type_{content_type}.html" 
        
        # Coba dapatkan template spesifik, jika gagal, gunakan template default
        try:
            template_to_render = template_env.get_template(template_name)
        except jinja2.exceptions.TemplateNotFound:
            template_to_render = template_env.get_template("message.html") # Fallback template
            
        html = template_to_render.render({"post": post, "depth": 1})
        ```
    *   **Alternatif:** Bisa juga membuat fungsi pembantu baru, misalnya `get_template_for_type(content_type)` yang mengelola logika fallback.

4.  **Struktur File Template:**
    *   Buat template baru di folder `templates/` sesuai dengan tipe konten yang diharapkan (misalnya, `templates/type_article.html`, `templates/type_event.html`).
    *   Pastikan `message.html` tetap ada sebagai template fallback default.

## Pengujian

1.  **Unit Test untuk Pemilihan Template:**
    *   Buat test case yang memverifikasi bahwa template yang benar dipilih berdasarkan `type` di frontmatter.
    *   Test case untuk skenario di mana `type` tidak ada (harus menggunakan default).
    *   Test case untuk skenario di mana `type` ada tetapi template spesifik tidak ada (harus menggunakan fallback).
2.  **Integrasi Test:**
    *   Buat beberapa file markdown dengan `type` yang berbeda di frontmatter.
    *   Jalankan `main()` dan verifikasi bahwa halaman HTML yang dihasilkan menggunakan template yang sesuai.
    *   Verifikasi bahwa halaman tanpa `type` atau dengan `type` yang tidak ada templatenya menggunakan `message.html`.
