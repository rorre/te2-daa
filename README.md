# Tugas Eksperimen 2 DAA

## Struktur

- `dataset/`: Direktori dataset untuk digunakan `test.py`
- `bnb.py`: Implementasi Brand and Bound
- `dp.py`: Implementasi Dynamic Programming
- `test.py`: Python script untuk semua test, serta generator
- `result.py`: Python script untuk menampilkan semua hasil test
- `run.sh`: Melakukan test dengan dataset yang sudah ada
- `init.sh`: Melakukan generate dataset dan test

> [!WARNING]
>
> `run.sh` dan `init.sh` akan melakukan semua test **secara paralel**. Pastikan Anda menutup aplikasi-aplikasi
> untuk memastikan CPU Anda tidak _overloaded_.

### Struktur direktori dataset:

`[size]`: Ukuran data

- `dataset/[size]/dataset.json`: Dataset yang digunakan untuk test
- `dataset/[size]/result.json`: Hasil dari test terakhir

## Menjalankan

- Generate dataset dan test

```bash
sh init.sh
```

- Test dengan dataset yang sudah ada

```bash
sh run.sh
```
