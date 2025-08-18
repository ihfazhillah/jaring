# Isu 7: Notasi Khusus untuk Konversi Teks ke Gambar

**Latar Belakang:**
Untuk setiap pesan, dibutuhkan sebuah gambar pratinjau (preview) dan gambar untuk Open Graph (og:image) agar saat dibagikan di media sosial terlihat menarik. Membuat gambar ini secara manual untuk setiap pesan tidak efisien.

**Permintaan:**
Buat sebuah sistem dengan notasi khusus di dalam konten markdown untuk secara otomatis menghasilkan gambar dari sebagian teks.

**Detail Implementasi:**
1.  **Notasi:** Gunakan notasi `!img{teks yang akan dijadikan gambar}`. Notasi `[[...]]` dihindari karena sering digunakan untuk internal link di banyak sistem.
2.  **Fleksibilitas Notasi:** Notasi ini harus dapat diparse dengan benar di mana pun ia berada dalam teks: di awal baris, di tengah baris, di akhir baris, atau bahkan mencakup beberapa baris.
3.  **Contoh:**
    ```
    aku makan ikan
    !img{ikannya enak sekali}
    hore hore hore
    ```
4.  **Proses di Skrip:**
    - Saat mem-parsing file markdown, skrip harus mendeteksi notasi `!img{...}`.
    - Teks di dalam notasi (`ikannya enak sekali`) diekstrak.
    - Teks ini kemudian dikonversi menjadi sebuah file gambar (misalnya `.png`) menggunakan library `pictex`. Proses ini mungkin memerlukan template gambar latar dan pemilihan font.
    - Gambar yang dihasilkan disimpan di direktori `output/assets/images/`.
5.  **Penggunaan Gambar:**
    - Path ke gambar yang baru dibuat ini akan digunakan sebagai nilai untuk `preview` dan `og:image` di metadata halaman HTML.
6.  **Tampilan di Konten:**
    - Teks yang diberi notasi khusus tersebut harus tetap ditampilkan sebagai teks biasa di dalam konten pesan. Notasi `!img{` dan `}` harus dihilangkan.
    - Dari contoh di atas, hasil teksnya adalah:
      ```
      aku makan ikan
      ikannya enak sekali
      hore hore hore
      ```
