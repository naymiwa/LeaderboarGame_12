import csv
import os
import random
import time

# =======================================================
# NAYLA: KONFIGURASI TEMA WARNA & UI (ANSI ESCAPE CODES)
# Digunakan untuk memberikan warna pada teks di terminal
# =======================================================
PINK = '\033[95m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m' # Mengembalikan warna terminal ke default
LEBAR_TERMINAL = 60

# =======================================================
# DEKLARASI VARIABEL GLOBAL & STRUKTUR DATA
# =======================================================
FILE_NAME = "ZTugasAkhir/data.csv"

# 1. LIST (Array Dinamis)
players = []        

# 2. STACK (Tumpukan - LIFO)
# Digunakan untuk menyimpan riwayat penghapusan data. 
history_stack = []  

# =======================================================
# NAJLA: FUNGSI BANTUAN UX (USER EXPERIENCE)
# =======================================================
def clear_screen():
    """Membersihkan layar terminal agar UI terlihat rapi saat pindah menu."""
    os.system('cls' if os.name == 'nt' else 'clear')

def jeda_kembali():
    """Memberikan jeda bagi user untuk membaca output sebelum kembali ke menu."""
    input(f"\n{CYAN}>>> Tekan [ENTER] untuk kembali ke menu utama...{RESET}")

def cetak_judul(judul):
    """Mencetak judul menu dengan format border yang posisinya persis di tengah."""
    clear_screen()
    print(PINK + "=" * LEBAR_TERMINAL + RESET)
    print(YELLOW + judul.center(LEBAR_TERMINAL) + RESET) # .center() untuk rata tengah presisi
    print(PINK + "=" * LEBAR_TERMINAL + RESET + "\n")

# =======================================================
# NAYLA: LOAD DATA (Membaca file CSV ke List)
# =======================================================
def load_data():
    players.clear() # Bersihkan list sebelum memuat data baru
    
    # Validasi dan pembuatan folder jika belum ada agar terhindar dari FileNotFoundError
    if not os.path.exists("ZTugasAkhir"):
        os.makedirs("ZTugasAkhir")

    # Jika file CSV belum ada, buat file baru beserta headernya
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["nama", "skor"])
        return

    # Membaca data dari CSV dan memasukkannya ke dalam list of dictionaries 'players'
    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            players.append({
                "nama": row["nama"],
                "skor": int(row["skor"]) # Konversi skor ke integer untuk keperluan sorting/kalkulasi
            })

# =======================================================
# NAJLA: SAVE DATA (File Handling / Menulis ke CSV)
# =======================================================
def save_data():
    try:
        with open(FILE_NAME, mode='w', newline='') as file:
            fieldnames = ['nama', 'skor']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader() # Menulis ulang header kolom
            
            # Memastikan seluruh nilai skor adalah integer murni sebelum disimpan
            for p in players:
                p['skor'] = int(p['skor'])
            
            writer.writerows(players) # Menulis seluruh isi list 'players' ke CSV
    except Exception as e:
        # Menangani error jika file sedang dibuka oleh program lain atau hak akses ditolak
        print(f"{RED}[!] Kesalahan: Gagal menyimpan data. Alasan: {e}{RESET}")

# =======================================================
# NAYLA & REZKI: PLAY GAME 
# =======================================================
def play_game():
    cetak_judul("A R E N A   T E B A K   A N G K A")
    
    player_name = input(f"{CYAN}Masukkan nama pemain: {RESET}").strip()
    if player_name == "":
        print(f"{RED}[!] Nama tidak boleh kosong.{RESET}")
        jeda_kembali()
        return
    
    print(f"\n{PINK}Halo {YELLOW}{player_name}{PINK}! Sistem telah memikirkan angka 1 - 10.{RESET}")
    print("Kamu punya 3 kali kesempatan untuk menebak.\n")
    
    # Menghasilkan angka acak dari 1 hingga 10
    angka_rahasia = random.randint(1, 10)
    kesempatan = 3
    skor = 0

    for i in range(1, kesempatan + 1):
        try:
            tebakan = int(input(f"Tebakan ke-{i}: "))
        except ValueError:
            # Mencegah program crash (force close) jika user menginput huruf/simbol
            print(f"{RED}[!] Masukkan angka yang valid!{RESET}")
            continue

        if tebakan == angka_rahasia:
            # Algoritma perhitungan skor: semakin cepat menebak, skor semakin tinggi
            skor = 100 - (i - 1) * 30
            print(f"\n{GREEN}🎉 LUAR BIASA! Tebakanmu benar!{RESET}")
            print(f"Skor yang kamu dapatkan: {YELLOW}{skor}{RESET}")
            break
        else:
            if i < kesempatan:
                # Memberikan petunjuk (clue) navigasi tebakan
                if tebakan < angka_rahasia:
                    print(f"{CYAN}Clue: Angka lebih BESAR dari {tebakan}{RESET}")
                else:
                    print(f"{CYAN}Clue: Angka lebih KECIL dari {tebakan}{RESET}")
            else:
                print(f"\n{RED}Game Over! Angka yang benar adalah: {angka_rahasia}{RESET}")
                print(f"Skor kamu: {YELLOW}0{RESET}")

    # Memanggil modul terpisah untuk menyimpan skor
    simpan_skor(player_name, skor)
    jeda_kembali()

# =======================================================
# NAJLA: SIMPAN SKOR
# =======================================================
def simpan_skor(nama, skor):
    """Menambahkan data pemain baru ke list global dan trigger save_data."""
    players.append({"nama": nama, "skor": skor})
    save_data() 
    print(f"{GREEN}[v] Skor berhasil disinkronkan ke database.{RESET}")

# =======================================================
# REZKI: TAMPILKAN LEADERBOARD (Implementasi Algoritma SORTING)
# =======================================================
def tampilkan_leaderboard():
    cetak_judul("L E A D E R B O A R D   S K O R")
    
    if not players:
        print(f"{CYAN}Belum ada data pemain di leaderboard.{RESET}".center(LEBAR_TERMINAL))
    else:
        # ALGORITMA SORTING:
        # Mengurutkan list 'players' berdasarkan *key* 'skor'.
        # reverse=True digunakan agar urutannya Descending (Skor terbesar di atas).
        sorted_players = sorted(players, key=lambda x: x['skor'], reverse=True)
        
        # Formatting output menjadi bentuk tabel yang rapi
        print(f"{YELLOW}{'PERINGKAT':<12} | {'NAMA PEMAIN':<25} | {'SKOR':<10}{RESET}")
        print("-" * LEBAR_TERMINAL)
        for idx, p in enumerate(sorted_players, 1):
            if idx == 1:
                # Memberikan highlight khusus (ikon mahkota) untuk Peringkat 1
                print(f"{GREEN}{'# '+str(idx):<12} | {p['nama']:<25} | {p['skor']:<10} 👑{RESET}")
            else:
                print(f"{'# '+str(idx):<12} | {p['nama']:<25} | {p['skor']:<10}")
    jeda_kembali()

# =======================================================
# NAJLA: CARI PEMAIN (Implementasi Algoritma SEARCHING)
# =======================================================
def cari_pemain():
    cetak_judul("P E N C A R I A N   P E M A I N")
    
    nama_dicari = input(f"{CYAN}Masukkan nama pemain yang ingin dicari: {RESET}").strip()
    hasil_pencarian = []

    # HAPUS fungsi .lower() di sini
    for pemain in players:
        if nama_dicari in pemain['nama']:
            hasil_pencarian.append(pemain)

    print("\n" + "-" * LEBAR_TERMINAL)
    if hasil_pencarian:
        print(f"{GREEN}Ditemukan {len(hasil_pencarian)} data yang cocok:{RESET}\n")
        for idx, p in enumerate(hasil_pencarian, 1):
            print(f"  {idx}. {YELLOW}{p['nama']}{RESET} - Skor: {CYAN}{p['skor']}{RESET}")
    else:
        print(f"{RED}Data dengan nama '{nama_dicari}' tidak ditemukan.{RESET}")
    print("-" * LEBAR_TERMINAL)
    jeda_kembali()

# =======================================================
# REZKI: UPDATE SKOR
# =======================================================
def update_skor():
    cetak_judul("U P D A T E   S K O R   P E M A I N")
    
    nama_dicari = input(f"{CYAN}Masukkan nama pemain secara spesifik: {RESET}").strip()

    # HAPUS fungsi .lower() di sini agar exact match (harus sama persis)
    for pemain in players:
        if pemain['nama'] == nama_dicari:
            try:
                skor_baru = int(input(f"Masukkan skor baru untuk {YELLOW}{pemain['nama']}{RESET}: "))
                pemain['skor'] = skor_baru
                save_data() # Sinkronisasi perubahan ke CSV
                print(f"\n{GREEN}[v] Skor untuk {pemain['nama']} berhasil diperbarui menjadi {skor_baru}.{RESET}")
            except ValueError:
                print(f"\n{RED}[!] Skor harus berupa angka. Update dibatalkan.{RESET}")
            jeda_kembali()
            return

    print(f"\n{RED}Pemain dengan nama '{nama_dicari}' tidak ditemukan. Update dibatalkan.{RESET}")
    jeda_kembali()

# =======================================================
# NAYLA: HAPUS PEMAIN & PUSH KE STACK RIWAYAT
# =======================================================
def hapus_pemain():
    cetak_judul("H A P U S   D A T A   P E M A I N")
    
    nama = input(f"{CYAN}Masukkan nama pemain yang akan dihapus: {RESET}").strip()
    
    # HAPUS fungsi .lower() di sini
    for p in players:
        if p["nama"] == nama:
            konfirmasi = input(f"Yakin ingin menghapus {YELLOW}{p['nama']}{RESET}? (y/n): ")
            if konfirmasi.lower() == 'y':
                history_stack.append(("Hapus", p.copy()))
                players.remove(p) # Hapus dari list utama
                save_data() # Update file CSV
                print(f"\n{GREEN}[v] Data berhasil dihapus dan disimpan ke riwayat.{RESET}")
            else:
                print(f"\n{CYAN}[-] Penghapusan dibatalkan.{RESET}")
            jeda_kembali()
            return
            
    print(f"\n{RED}[!] Pemain tidak ditemukan.{RESET}")
    jeda_kembali()

# =======================================================
# REZKI: TAMPILKAN RIWAYAT (Implementasi Struktur Data STACK)
# =======================================================
def tampilkan_riwayat():
    cetak_judul("R I W A Y A T   S Y S T E M   (LIFO)")
    
    if not history_stack:
        print(f"{CYAN}Belum ada riwayat penghapusan data.{RESET}".center(LEBAR_TERMINAL))
    else:
        # Menampilkan data Stack menggunakan reversed() 
        # untuk menyimulasikan sifat LIFO (Last In First Out).
        for idx, (aksi, data) in enumerate(reversed(history_stack), 1):
            print(f"{PINK}[{idx}]{RESET} Aksi: {RED}{aksi}{RESET} | Nama: {YELLOW}{data['nama']}{RESET} | Skor Lama: {data['skor']}")
    jeda_kembali()

# =======================================================
# MAIN MENU & ENTRY POINT
# =======================================================
def menu():
    """Merender antarmuka menu utama berbentuk kotak."""
    clear_screen()
    print(PINK + "╔" + "═" * (LEBAR_TERMINAL - 2) + "╗" + RESET)
    print(PINK + "║" + YELLOW + "M E N U   U T A M A   G A M E".center(LEBAR_TERMINAL - 2) + PINK + "║" + RESET)
    print(PINK + "╠" + "═" * (LEBAR_TERMINAL - 2) + "╣" + RESET)
    
    menu_items = [
        "1. Main Game Tebak Angka",
        "2. Tampilkan Leaderboard",
        "3. Cari Pemain",
        "4. Update Skor",
        "5. Hapus Pemain",
        "6. Tampilkan Riwayat Perubahan",
        "0. Keluar"
    ]
    
    for item in menu_items:
        print(PINK + "║" + CYAN + item.center(LEBAR_TERMINAL - 2) + PINK + "║" + RESET)
        
    print(PINK + "╚" + "═" * (LEBAR_TERMINAL - 2) + "╝" + RESET)

def main():
    """Fungsi utama yang menjalankan sistem navigasi program."""
    load_data() # Memuat data CSV ke memori saat program pertama kali dijalankan

    while True:
        menu()
        print(f"\n{YELLOW}Silakan pilih opsi navigasi:{RESET}")
        pilih = input(">>> ").strip()

        # Percabangan logika untuk mengarahkan pilihan user ke fungsi yang sesuai
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
            # Keluar dari program (Exit Point)
            clear_screen()
            print(f"{PINK}=" * LEBAR_TERMINAL + RESET)
            print(f"{YELLOW}Terima kasih telah menggunakan sistem Leaderboard Game!{RESET}".center(LEBAR_TERMINAL + 10))
            print(f"{PINK}=" * LEBAR_TERMINAL + RESET + "\n")
            break
        else:
            print(f"{RED}[!] Pilihan tidak valid. Silakan masukkan angka 0-6.{RESET}")
            time.sleep(1.5) # Memberi jeda sebentar sebelum menu dirender ulang

# Script entry point standar di Python
if __name__ == "__main__":
    main()
