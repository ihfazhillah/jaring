# Rencana Implementasi Isu 11: Dukungan Jalankan Skrip dengan Jalur Konfigurasi Kustom

## Tujuan
Memungkinkan skrip `jaring.py` untuk menerima argumen baris perintah untuk menentukan jalur file konfigurasi kustom, dengan fallback ke `config.yaml` default jika tidak ada argumen yang diberikan.

## Detail Implementasi

1.  **Modifikasi `main()` (jaring.py):**
    *   **Import `argparse`:** Tambahkan `import argparse` di bagian atas file `jaring.py`.
    *   **Inisialisasi Parser:** Di awal fungsi `main()`, inisialisasi `ArgumentParser`:
        ```python
        parser = argparse.ArgumentParser(description="Generate a static site from markdown files.")
        ```
    *   **Tambahkan Argumen Konfigurasi:** Tambahkan argumen untuk jalur konfigurasi:
        ```python
        parser.add_argument(
            "--config",
            "-c",
            type=str,
            default="config.yaml", # Default path to config file
            help="Path to the custom configuration file (default: config.yaml)"
        )
        ```
    *   **Parse Argumen:** Parse argumen yang diberikan:
        ```python
        args = parser.parse_args()
        config_path = args.config
        ```
    *   **Logika Pemuatan Konfigurasi:** Ubah bagian pemuatan konfigurasi untuk menggunakan `config_path`:
        ```python
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at '{config_path}'.")
            exit(1) # Keluar dari skrip dengan error
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file '{config_path}': {e}")
            exit(1) # Keluar dari skrip dengan error
        ```

2.  **Penanganan Kesalahan:**
    *   Implementasikan blok `try-except` untuk menangani `FileNotFoundError` jika jalur konfigurasi kustom tidak valid.
    *   Tambahkan penanganan `yaml.YAMLError` untuk kasus file konfigurasi yang tidak valid secara sintaksis.
    *   Berikan pesan kesalahan yang informatif kepada pengguna.

## Pengujian

1.  **Unit Test untuk Argumen Parsing:**
    *   Simulasikan pemanggilan skrip dengan `--config custom.yaml` dan verifikasi bahwa `config_path` diatur dengan benar.
    *   Simulasikan pemanggilan tanpa argumen dan verifikasi bahwa `config_path` default ke `config.yaml`.
2.  **Integrasi Test:**
    *   Buat file `custom_config.yaml` dengan beberapa pengaturan yang berbeda.
    *   Jalankan skrip dengan `python jaring.py --config custom_config.yaml` dan verifikasi bahwa pengaturan dari `custom_config.yaml` digunakan.
    *   Jalankan skrip tanpa argumen dan verifikasi bahwa `config.yaml` default digunakan.
    *   Jalankan skrip dengan jalur ke file yang tidak ada dan verifikasi bahwa skrip keluar dengan pesan kesalahan yang sesuai.
    *   Jalankan skrip dengan jalur ke file YAML yang rusak dan verifikasi penanganan kesalahan.
