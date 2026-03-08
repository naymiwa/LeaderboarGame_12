def cari_pemain(data_pemain):
    """
    Fungsi untuk mencari data pemain tertentu berdasarkan nama.
    Mengimplementasikan algoritma Linear Search pada struktur data List.
    """
    print("\n=== FITUR PENCARIAN PEMAIN ===")
    nama_dicari = input("Masukkan nama pemain yang ingin dicari: ").strip()

    # Inisialisasi variabel untuk menyimpan hasil pencarian
    hasil_pencarian = []

    # Melakukan iterasi melalui List yang berisi Dictionary pemain
    for pemain in data_pemain:
        # Pencarian dilakukan secara case-insensitive agar lebih user-friendly
        # Menggunakan pencarian 'partial match' (nama yang mengandung kata kunci)
        if nama_dicari.lower() in pemain['nama'].lower():
            hasil_pencarian.append(pemain)

    # Menampilkan hasil pencarian
    if hasil_pencarian:
        print(f"\nDitemukan {len(hasil_pencarian)} data yang cocok:")
        print("-" * 30)
        # Menampilkan hasil dalam format yang rapi
        for idx, p in enumerate(hasil_pencarian, 1):
            print(f"{idx}. Nama: {p['nama']} | Skor Tertinggi: {p['skor']}")
        print("-" * 30)
    else:
        # Validasi jika data yang dicari tidak ada dalam sistem
        print(f"\n Data dengan nama '{nama_dicari}' tidak ditemukan dalam leaderboard.")