# Isu 5: Fungsionalitas Tag

**Latar Belakang:**
Selain pengelompokan berdasarkan seri, tidak ada cara lain untuk mengkategorikan atau menghubungkan pesan-pesan yang memiliki tema serupa.

**Permintaan:**
Tambahkan dukungan untuk `tags` (label) pada setiap pesan.

**Detail Implementasi:**
1.  **Frontmatter:** Tambahkan field `tags` di frontmatter setiap file markdown. Field ini bisa berisi daftar tag.
    ```yaml
    ---
    title: Judul Pesan
    series: nak
    tags:
      - sabar
      - keluarga
    ---
    ```
2.  **Halaman Pesan:** Tampilkan daftar tag yang dimiliki sebuah pesan di halaman detailnya.
3.  **Halaman per Tag:** Buat halaman indeks untuk setiap tag, yang berisi daftar semua pesan yang memiliki tag tersebut (misalnya `/tags/sabar.html`).
4.  **Daftar Semua Tag:** (Opsional) Buat satu halaman yang berisi daftar semua tag yang ada di situs.
