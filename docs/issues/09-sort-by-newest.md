# Isu 9: Urutkan Pesan Berdasarkan Tanggal Terbaru

**Latar Belakang:**
Saat ini, urutan pesan di halaman indeks tidak diurutkan secara spesifik, kemungkinan berdasarkan urutan pembacaan file dari sistem operasi. Hal ini membuat pesan-pesan terbaru tidak selalu muncul di atas.

**Permintaan:**
Urutkan daftar pesan di semua halaman indeks sehingga pesan dengan tanggal terbaru (paling baru) muncul di paling atas.

**Detail Implementasi:**
1.  **Parsing Tanggal:** Saat mem-parsing file, tanggal dari `id` atau mungkin dari field `date` khusus di frontmatter perlu diubah menjadi objek tanggal yang bisa dibandingkan.
2.  **Pengurutan:** Sebelum me-render templat `index.html`, daftar `posts` harus diurutkan dalam urutan menurun (descending) berdasarkan tanggal.
3.  **Contoh di `jaring.py`:**
    ```python
    # Setelah parsing semua post
    posts.sort(key=lambda p: p['metadata']['id'], reverse=True)

    # Kemudian baru render template
    html = render_html(template_env, "index.html", {"posts": posts, ...})
    ```
    *(Catatan: Pengurutan berdasarkan `id` string akan berfungsi jika format tanggalnya konsisten YYYY-MM-DD)*.
