import csv
import os
import random

# Menggunakan konstanta folder yang sudah ditentukan kelompokmu
FILE_NAME = "ZTugasAkhir/data.csv"

players = []        # List (data utama)
history_stack = []  # Stack (riwayat)

# ========================
# FILE HANDLING
# ========================
def load_data():
    players.clear()

    # Memastikan folder ZTugasAkhir ada agar tidak error saat save
    if not os.path.exists("ZTugasAkhir"):
        os.makedirs("ZTugasAkhir")

    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["nama", "skor"])
        return

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            players.append({
                "nama": row["nama"],
                "skor": int(row["skor"])
            })

def save_data():
    """
    Fungsi milik Najla: Menyimpan seluruh data pemain dari list ke file CSV.
    Mengimplementasikan File Handling untuk penyimpanan permanen.
    """
    try:
        with open(FILE_NAME, mode='w', newline='') as file:
            fieldnames = ['nama', 'skor']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            
            # Memastikan skor adalah integer sebelum disimpan agar data konsisten
            for p in players:
                p['skor'] = int(p['skor'])
            
            writer.writerows(players)
            
        print(f" [OK] Data telah disinkronkan ke {FILE_NAME}.")
    except Exception as e:
        print(f" Kesalahan: Gagal menyimpan data. Alasan: {e}")

# ========================
# GAME TEBAK ANGKA
# ========================
def play_game():
    print("\n=== GAME TEBAK ANGKA ===")
    nama = input("Masukkan nama pemain: ").strip()

    if nama == "":
        print("Nama tidak boleh kosong!")
        return

    angka_rahasia = random.randint(1, 10)
    kesempatan = 3
    skor = 0

    for i in range(1, kesempatan + 1):
        try:
            tebakan = int(input(f"Tebakan ke-{i}: "))
        except ValueError:
            print("Masukkan angka!")
            continue

        if tebakan == angka_rahasia:
            skor = 100 - (i - 1) * 30
            print("🎉 Tebakan benar!")
            break
        else:
            if i < kesempatan:
                if tebakan < angka_rahasia:
                    print("Clue: Angka lebih besar")
                else:
                    print("Clue: Angka lebih kecil")
            else:
                print(f"Game Over! Angka yang benar: {angka_rahasia}")

    simpan_skor(nama, skor)

def simpan_skor(nama, skor):
    # Logika untuk menambah pemain baru ke list global
    players.append({"nama": nama, "skor": skor})
    save_data() # Langsung simpan ke CSV setiap ada skor baru

# ========================
# CRUD & FITUR DATA
# ========================
def tampilkan_leaderboard():
    # Menampilkan data yang ada di list players
    print("\n=== LEADERBOARD ===")
    if not players:
        print("Belum ada data pemain.")
        return
    for p in players:
        print(f"Nama: {p['nama']} | Skor: {p['skor']}")

def cari_pemain():
    """
    Fungsi milik Najla: Mencari data pemain tertentu berdasarkan nama.
    Mengimplementasikan algoritma Linear Search.
    """
    print("\n=== FITUR PENCARIAN PEMAIN ===")
    nama_dicari = input("Masukkan nama pemain yang ingin dicari: ").strip()

    hasil_pencarian = []

    # Iterasi Linear Search untuk mencocokkan nama
    for pemain in players:
        if nama_dicari.lower() in pemain['nama'].lower():
            hasil_pencarian.append(pemain)

    if hasil_pencarian:
        print(f"\nDitemukan {len(hasil_pencarian)} data yang cocok:")
        print("-" * 30)
        for idx, p in enumerate(hasil_pencarian, 1):
            print(f"{idx}. Nama: {p['nama']} | Skor: {p['skor']}")
        print("-" * 30)
    else:
        print(f"\n Data dengan nama '{nama_dicari}' tidak ditemukan.")

def update_skor():
    # Fitur ini bisa dikembangkan nanti
    pass

def hapus_pemain():
    nama = input("Nama pemain yang akan dihapus: ")
    for p in players:
        if p["nama"].lower() == nama.lower():
            history_stack.append(("Hapus", p.copy()))
            players.remove(p)
            save_data()
            print("Data berhasil dihapus.")
            return
    print("Pemain tidak ditemukan.")

def tampilkan_riwayat():
    # Fitur riwayat dari stack
    pass

# ========================
# MENU
# ========================
def menu():
    print("\n" + "="*20)
    print("      MENU GAME")
    print("="*20)
    print("1. Main Game Tebak Angka")
    print("2. Tampilkan Leaderboard")
    print("3. Cari Pemain")
    print("4. Update Skor")
    print("5. Hapus Pemain")
    print("6. Lihat Riwayat")
    print("0. Keluar")

def main():
    load_data()

    while True:
        menu()
        pilih = input("Pilih menu: ")

        if pilih == "1":
            play_game()
        elif pilih == "2":
            tampilkan_leaderboard()
        elif pilih == "3":
            cari_pemain()
        elif pilih == "4":
            update_skor()
        elif pilih == "5":
            hapus_pemain()
        elif pilih == "6":
            tampilkan_riwayat()
        elif pilih == "0":
            print("Program selesai. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()