import csv

def save_data(data_pemain, nama_file='data.csv'):
    """
    Fungsi untuk menyimpan seluruh data pemain dari list ke file CSV.
    Mengimplementasikan File Handling untuk penyimpanan permanen.
    """
    try:
        # Membuka file dengan mode 'w' (write) untuk memperbarui seluruh isi file
        # newline='' digunakan untuk mencegah adanya baris kosong tambahan di Windows
        with open(nama_file, mode='w', newline='') as file:
            # Menentukan nama kolom sesuai dengan atribut: nama dan skor
            fieldnames = ['nama', 'skor']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Menulis header (nama kolom) di baris pertama
            writer.writeheader()
            
            # Menulis seluruh baris data dari list data_pemain
            writer.writerows(data_pemain)
            
        print(f" Berhasil: Data telah disinkronkan ke {nama_file}.")
        
    except Exception as e:
        # Validasi input/error handling agar program tidak crash jika terjadi kegagalan file
        print(f" Kesalahan: Gagal menyimpan data. Alasan: {e}")