import csv
import os
import random

# Menggunakan konstanta folder yang sudah ditentukan kelompokmu
FILE_NAME = "ZTugasAkhir/data.csv"

players = []        # List (data utama)
history_stack = []  # Stack (riwayat)

# ========================
# Nayla
# Load_Data
# =======================
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

# ========================
# Najla
# Save_Data
# ========================

def save_data():
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
# Nayla (Play_Game)
# Rezki (Tambah_Pemain)
# ========================

def play_game(player_name):
    print(f"Selamat datang, {player_name}! Ayo main tebak angka!")
    nama = input("Masukkan nama kamu: ").strip()

    if nama == "":
        print("Nama tidak boleh kosong. Silakan coba lagi.")
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

# ========================
# Najla
# Simpan_Skor
# ========================
def simpan_skor(nama, skor):
    # Logika untuk menambah pemain baru ke list global
    players.append({"nama": nama, "skor": skor})
    save_data() # Langsung simpan ke CSV setiap ada skor baru

# ========================
# Rezki
# Tampilkan_Leaderboard
# ========================
def tampilkan_leaderboard():
        # Menampilkan data yang ada di list players
    print("\n=== LEADERBOARD ===")
    if not players:
        print("Belum ada data pemain.")
        return
    for p in players:
        print(f"Nama: {p['nama']} | Skor: {p['skor']}")

# ========================
# Najla
# Cari_Pemain
# ========================
def cari_pemain():
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

# ========================
# Rezki
# Update_Skor
# ========================
def update_skor():
    print("\n=== FITUR UPDATE SKOR PEMAIN ===")
    nama_dicari = input("Masukkan nama pemain yang ingin diupdate skornya: ").strip()

    # Mencari pemain dengan nama yang cocok
    for pemain in players:
        if pemain['nama'].lower() == nama_dicari.lower():
            try:
                skor_baru = int(input(f"Masukkan skor baru untuk {pemain['nama']}: "))
                pemain['skor'] = skor_baru
                save_data()  # Simpan perubahan ke CSV
                print(f"Skor untuk {pemain['nama']} berhasil diperbarui.")
            except ValueError:
                print("Skor harus berupa angka. Update dibatalkan.")
            return

    print(f"Pemain dengan nama '{nama_dicari}' tidak ditemukan. Update dibatalkan.")

# ========================
# Nayla
# Hapus_Pemain
# ========================
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

# ========================
# Rezki
# Tampilkan_Riwayat
# ========================
def tampilkan_riwayat():
    print("\n=== RIWAYAT PERUBAHAN DATA ===")
    if not history_stack:
        print("Belum ada riwayat perubahan data.")
        return
    for idx, (aksi, data) in enumerate(history_stack, 1):
        print(f"{idx}. Aksi: {aksi} | Data: {data}")

# ========================
# Nayla (Load Game, Play Game, Hapus Pemain)
# Najla (Save Data, Cari Pemain)
# Rezki (Tampilkan Leaderboard, Update Skor, Tampilkan Riwayat)
# ========================

# ========================
# Menu Game
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
    print("6. Tampilkan Riwayat Perubahan Data")
    print("0. Keluar")

def main():
    load_data()

    while True:
        menu()
        pilih = input("Pilih menu: ")

        if pilih == "1":
            player_name = input("Masukkan nama pemain: ")
            play_game(player_name)
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
            print("Terima kasih telah bermain! Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()