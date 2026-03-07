import csv
import os
import random

FILE_NAME = "ZTugasAkhir/data.csv"

players = []        # List (data utama)
history_stack = []  # Stack (riwayat)

# ========================
# FILE HANDLING
# ========================
def load_data():
    players.clear()

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
    # TODO: simpan data players ke file CSV
    pass


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
    # TODO: tambah skor pemain atau buat pemain baru
    pass


# ========================
# CRUD & FITUR DATA
# ========================
def tampilkan_leaderboard():
    # TODO: tampilkan ranking pemain berdasarkan skor
    pass


def cari_pemain():
    # TODO: cari pemain berdasarkan nama
    pass


def update_skor():
    # TODO: update skor pemain
    pass


def hapus_pemain():
    nama = input("Nama pemain: ")

    for p in players:
        if p["nama"].lower() == nama.lower():
            history_stack.append(("Hapus", p.copy()))
            players.remove(p)
            save_data()
            print("Data dihapus.")
            return

    print("Pemain tidak ditemukan.")


def tampilkan_riwayat():
    # TODO: tampilkan history dari stack
    pass


# ========================
# MENU
# ========================
def menu():
    print("\n===== MENU =====")
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
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()