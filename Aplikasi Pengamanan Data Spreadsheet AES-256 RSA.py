#PROGRAM APLIKASI PENGAMANAN DATA SPREADSHEET MENGGUNAKAN KRIPTOGRAFI HIBRIDA AES-256 DAN RSA

from customtkinter import *
from tkinter import filedialog, messagebox
import random
import string
import backend_rsa
import backend_file_processor

#--- Form ---
root = CTk()
root.title('Pengamanan Data Spreadsheet dengan AES-256 dan RSA')
root.geometry('1000x500')
set_appearance_mode("system")
set_default_color_theme("green")


# --- Frame Utama ---
frame_utama = CTkFrame(master = root, width = 800, height = 500)
frame_utama.propagate(False)

# --- Laman Home ---
def laman_home():
    frame_home = CTkFrame(master = frame_utama, width = 800, height = 500, fg_color="transparent")
    frame_home.propagate(False)
    
    # --- Widget Home ---
    label_judul = CTkLabel(master = frame_home, text = 'Pengamanan Data Spreadsheet Menggunakan Kriptografi Hibrida', font = ('Montserrat', 18, 'bold'))
    label_judul.place(x=120, y=50)
    label_judul = CTkLabel(master = frame_home, text = 'Advanced Encryption Standard-256 dan Rivest-Shamir-Adleman', font = ('Montserrat', 18, 'bold'))
    label_judul.place(x=120, y=75)
    label_keterangan = CTkLabel(master = frame_home, text = 'Terdapat 3 jenis program:', font = ('Montserrat', 14, 'bold'))
    label_keterangan.place(x=140, y=125)
    label_pembangkitankunci = CTkLabel(master = frame_home, text = '1. Pembangkitan Kunci', font = ('Montserrat', 12))
    label_pembangkitankunci.place(x=140, y=155)
    label_enkripsi = CTkLabel(master = frame_home, text = '2. Enkripsi', font = ('Montserrat', 12))
    label_enkripsi.place(x=140, y=185)
    label_dekripsi = CTkLabel(master = frame_home, text = '3. Dekripsi', font = ('Montserrat', 12))
    label_dekripsi.place(x=140, y=215)
    label_penutup = CTkLabel(master = frame_home, text = 'Silakan pilih salah satu program pada tombol di samping.', font = ('Montserrat', 12))
    label_penutup.place(x=140, y=245)

    frame_home.pack(side = 'left')

# --- Laman Pembangkitan Kunci ---
def laman_pembangkitankunci():
    frame_pembangkitankunci = CTkFrame(master=frame_utama, width=800, height=500, fg_color="transparent")
    frame_pembangkitankunci.propagate(False)

    def tampilkan_help_pembangkitan_kunci():
        # Membuat jendela pop-up baru
        jendela_help = CTkToplevel()
        jendela_help.title("Petunjuk - Pembangkitan Kunci")
        jendela_help.geometry("550x450")
        jendela_help.resizable(False, False)
        
        jendela_help.attributes("-topmost", True)
        
        jendela_help.grab_set()

        # Judul Pop-up
        label_judul_help = CTkLabel(master=jendela_help, text="Petunjuk Pembangkitan Kunci RSA", font=('Montserrat', 16, 'bold'))
        label_judul_help.pack(pady=(20, 15))

        # Isi Teks Petunjuk
        teks_petunjuk = (
            "Program pembangkitan kunci berfungsi untuk menghasilkan sepasang kunci (Kunci Publik dan Kunci Privat) "
            "menggunakan algoritma RSA. Berikut adalah langkah-langkah penggunaannya:\n\n"
            
            "1. Menentukan Nilai P₁ dan P₂\n"
            "   Algoritma RSA membutuhkan dua buah bilangan prima (P₁ dan P₂). Anda memiliki dua pilihan:\n"
            "   • Manual: Ketik angka bilangan prima pada kolom P₁ dan P₂.\n"
            "   • Otomatis: Klik tombol 'Generate Bilangan' agar sistem memilihkan bilangan prima secara acak untuk Anda.\n\n"
            
            "2. Membangkitkan Kunci\n"
            "   • Setelah nilai P₁ dan P₂ terisi, klik tombol 'Bangkitkan Kunci'.\n"
            "   • Sistem akan melakukan komputasi matematis dan menampilkan hasil Kunci Publik dan Kunci Privat "
            "pada panel di bawah.\n\n"
            
            "3. Menyimpan Kunci (Penting)\n"
            "   • Sangat disarankan untuk menyimpan kunci yang telah dibangkitkan agar tidak hilang.\n"
            "   • Klik tombol 'Simpan' di bawah masing-masing hasil kunci untuk menyimpannya "
            "dalam format file teks (*.txt).\n"
            "   • Kunci Publik akan Anda gunakan nanti pada tahap Enkripsi dokumen.\n"
            "   • Kunci Privat akan Anda gunakan nanti pada tahap Dekripsi dokumen. Jaga kerahasiaan Kunci Privat Anda."
        )

        # Kotak Teks (Read-only)
        textbox_help = CTkTextbox(master=jendela_help, width=480, height=280, font=('Montserrat', 12), wrap="word")
        textbox_help.pack(padx=20, pady=5)
        textbox_help.insert("0.0", teks_petunjuk)
        textbox_help.configure(state="disabled")

        # Tombol Tutup
        btn_tutup = CTkButton(master=jendela_help, text="Mengerti", font=('Montserrat', 12, 'bold'), width=120, command=jendela_help.destroy)
        btn_tutup.pack(pady=(15, 10))
    
    # --- Fungsi Penghubung ---
    def isi_otomatis():
        # panggil fungsi
        p1 = backend_rsa.generate_prime_number()
        p2 = backend_rsa.generate_prime_number()

        # Update GUI
        entry_p1.delete(0, END)
        entry_p1.insert(0, str(p1))

        entry_p2.delete(0, END)
        entry_p2.insert(0, str(p2))

        messagebox.showinfo("Info", "Bilangan Prima berhasil di-generate!")
    
    def proses_kunci():
        # ambil input dari GUI
        str_p1 = entry_p1.get()
        str_p2 = entry_p2.get()

        if not str_p1 or not str_p2:
            messagebox.showwarning("Peringatan", "Harap isi P1 dan P2!")
            return
            
        try:
            p_int = int(str_p1)
            q_int = int(str_p2)
            
            sukses, hasil = backend_rsa.generate_rsa_keys(p_int, q_int)
            
            if sukses:
                pub, priv = hasil
                
                # Tampilkan ke GUI
                entry_pub.configure(state="normal")
                entry_pub.delete(0, END)
                entry_pub.insert(0, pub)
                entry_pub.configure(state="readonly")
                
                entry_priv.configure(state="normal")
                entry_priv.delete(0, END)
                entry_priv.insert(0, priv)
                entry_priv.configure(state="readonly")
                
                messagebox.showinfo("Sukses", "Kunci RSA berhasil dibangkitkan!")
            else:
                messagebox.showerror("Gagal", hasil) # Tampilkan pesan error dari backend
                
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka!")
    
    def simpan_kunci_pub():
        pub = entry_pub.get()

        if not pub:
            messagebox.showwarning("Info", "Bangkitkan kunci terlebih dahulu.")
            return
        
        f_pub = filedialog.asksaveasfile(
            mode='w', 
            defaultextension=".txt", 
            filetypes=[("Text Files", "*.txt")],
            title="Simpan Kunci Publik",
            initialfile="Kunci_Publik.txt"
        )
        if f_pub:
            f_pub.write(pub)
            f_pub.close()
            messagebox.showinfo("Sukses", "Kunci publik berhasil disimpan.")

    def simpan_kunci_priv():
        priv = entry_priv.get()

        if not priv:
            messagebox.showwarning("Info", "Bangkitkan kunci terlebih dahulu.")
            return
        
        f_priv = filedialog.asksaveasfile(
            mode='w', 
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Simpan Kunci Privat",
            initialfile="Kunci_Privat.txt"
        )
        if f_priv:
            f_priv.write(priv)
            f_priv.close()
            messagebox.showinfo("Sukses", "Kunci privat berhasil disimpan.")

    # --- Widget Pembangkitan Kunci ---
    
    ## Judul Halaman
    label_judulpembangkitankunci = CTkLabel(master=frame_pembangkitankunci, text='Pembangkitan Kunci', font=('Montserrat', 20, 'bold'))
    label_judulpembangkitankunci.place(relx=0.5, y=30, anchor='center')
    # Button Help
    btn_help = CTkButton(master=frame_pembangkitankunci, text='?', font=('Montserrat', 12, 'bold'), width=20, height=20, command=tampilkan_help_pembangkitan_kunci)
    btn_help.place(x=515, y=20)

    ## Input P1
    label_p1 = CTkLabel(master=frame_pembangkitankunci, text='Bilangan Prima P₁', font=('Montserrat', 12))
    label_p1.place(x=150, y=100)
    entry_p1 = CTkEntry(master=frame_pembangkitankunci, width=300, placeholder_text="Input")
    entry_p1.place(x=350, y=100)

    ## Input P2
    label_p2 = CTkLabel(master=frame_pembangkitankunci, text='Bilangan Prima P₂', font=('Montserrat', 12))
    label_p2.place(x=150, y=140)
    entry_p2 = CTkEntry(master=frame_pembangkitankunci, width=300, placeholder_text="Input")
    entry_p2.place(x=350, y=140)

    ## Tombol Aksi
    # Tombol 1: Generate Bilangan
    button_generate = CTkButton(master=frame_pembangkitankunci, text='Generate Bilangan', font=('Montserrat', 12, 'bold'), width=140, height=35, command=isi_otomatis)
    button_generate.place(x=250, y=190)

    # Tombol 2: Bangkitkan Kunci (Core Process: Hitung n, totient, e, d)
    button_proses = CTkButton(master=frame_pembangkitankunci, text='Bangkitkan Kunci', font=('Montserrat', 12, 'bold'), width=140, height=35, command=proses_kunci)
    button_proses.place(x=400, y=190)

    ## Separator
    label_separator = CTkLabel(master=frame_pembangkitankunci, text='.'*200, text_color="gray")
    label_separator.place(relx=0.5, y=240, anchor='center')

    ## Output Kunci Publik
    label_pub = CTkLabel(master=frame_pembangkitankunci, text='Kunci Publik (e, n)', font=('Montserrat', 12))
    label_pub.place(x=150, y=270)
    entry_pub = CTkEntry(master=frame_pembangkitankunci, width=300, placeholder_text="Output (e, n)")
    entry_pub.place(x=150, y=300)
    btn_simpan_kunci_pub = CTkButton(master=frame_pembangkitankunci, text='Simpan', font=('Montserrat', 12, 'bold'), width=100, height=30, command=simpan_kunci_pub)
    btn_simpan_kunci_pub.place(x=460, y=300)

    ## Output Kunci Privat
    label_priv = CTkLabel(master=frame_pembangkitankunci, text='Kunci Privat (d, n)', font=('Montserrat', 12))
    label_priv.place(x=150, y=340)
    entry_priv = CTkEntry(master=frame_pembangkitankunci, width=300, placeholder_text="Output (d, n)")
    entry_priv.place(x=150, y=370)
    btn_simpan_kunci_priv = CTkButton(master=frame_pembangkitankunci, text='Simpan', font=('Montserrat', 12, 'bold'), width=100, height=30, command=simpan_kunci_priv)
    btn_simpan_kunci_priv.place(x=460, y=370)

    frame_pembangkitankunci.pack(fill="both", expand=True)

# --- Laman Enkripsi ---
def laman_enkripsi():
    frame_enkripsi = CTkFrame(master=frame_utama, width=800, height=500, fg_color="transparent")
    frame_enkripsi.propagate(False)

    ## Window Help Enkripsi
    def tampilkan_help_enkripsi():
        jendela_help = CTkToplevel()
        jendela_help.title("Petunjuk - Enkripsi")
        jendela_help.geometry("550x500")
        jendela_help.resizable(False, False)
        jendela_help.attributes("-topmost", True)
        jendela_help.grab_set()

        label_judul_help = CTkLabel(master=jendela_help, text="Petunjuk Proses Enkripsi Dokumen", font=('Montserrat', 16, 'bold'))
        label_judul_help.pack(pady=(20, 15))

        teks_petunjuk = (
            "Program enkripsi digunakan untuk mengamankan data spreadsheet menggunakan metode hibrida "
            "AES-256 dan RSA. Berikut langkah-langkahnya:\n\n"
            
            "1. Memilih Dokumen Spreadsheet\n"
            "   Klik tombol 'Cari' pada panel Spreadsheet untuk memilih file (.xlsx) yang ingin diamankan. "
            "Aplikasi akan mengenkripsi teks, formula, dan gambar di dalamnya.\n\n"
            
            "2. Memasukkan Kunci Publik RSA\n"
            "   Masukkan Kunci Publik yang telah Anda bangkitkan sebelumnya. Format kunci harus "
            "berupa dua bilangan bulat yang dipisahkan koma (e,n).\n\n"
            
            "3. Menentukan Kunci AES\n"
            "   • Masukkan kunci rahasia pada kolom Kunci AES.\n"
            "   • Jika kunci kurang dari 32 karakter, sistem secara otomatis akan menambahkan karakter "
            "acak (huruf, angka, simbol) hingga tepat 32 karakter.\n"
            "   • Kunci ini akan digunakan untuk mengenkripsi konten spreadsheet.\n"
            "   • Kunci ini juga bisa dibangkitkan secara otomatis oleh sistem dengan menekan tombol "
            "'Generate Kunci AES', yang akan menghasilkan kunci AES acak dengan panjang 32 karakter.\n\n"

            "4. Menjalankan Enkripsi\n"
            "   Klik tombol 'Enkripsi'. Sistem akan mengenkripsi data spreadsheet sehingga mengubah data sel menjadi format heksadesimal' "
            "dan gambar menjadi noise pixel.\n\n"
            
            "5. Menyimpan Hasil\n"
            "   Setelah sukses, gunakan tombol 'Simpan' pada panel bawah untuk mengunduh:\n"
            "   • File Spreadsheet Terenkripsi.\n"
            "   • Kunci AES Terenkripsi (32 blok bilangan bulat hasil enkripsi RSA)."
        )

        textbox_help = CTkTextbox(master=jendela_help, width=480, height=320, font=('Montserrat', 12), wrap="word")
        textbox_help.pack(padx=20, pady=5)
        textbox_help.insert("0.0", teks_petunjuk)
        textbox_help.configure(state="disabled")

        btn_tutup = CTkButton(master=jendela_help, text="Mengerti", font=('Montserrat', 12, 'bold'), width=120, command=jendela_help.destroy)
        btn_tutup.pack(pady=(15, 10))

    # Variabel Temp
    wb_terenkripsi = None
    kunci_aes_terenkripsi = None

    # --- Fungsi untuk Memilih File ---
    def cari_file_excel():
        filename = filedialog.askopenfilename(
            title="Pilih File Spreadsheet",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if filename:
            entry_file_input.delete(0, END)
            entry_file_input.insert(0, filename)

    def cari_kunci_publik():
        filename = filedialog.askopenfilename(
            title="Pilih Kunci Publik RSA",
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    isi_kunci = f.read().strip()
                    entry_pub_key.delete(0, END)
                    entry_pub_key.insert(0, isi_kunci)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca file kunci publik: {e}")

    def cari_kunci_aes():
        filename = filedialog.askopenfilename(
            title="Pilih Kunci AES",
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    isi_kunci = f.read().strip()
                entry_aes_key.delete(0, END)
                entry_aes_key.insert(0, isi_kunci)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca file AES: {e}")

    def generate_random_aes():
        # 1. Bangkitkan 32 karakter acak
        karakter = string.ascii_letters + string.digits + string.punctuation
        kunci_str = ''.join(random.choice(karakter) for _ in range(32))
        
        # 2. Masukkan ke dalam kotak Entry di layar
        entry_aes_key.configure(state="normal")
        entry_aes_key.delete(0, 'end')
        entry_aes_key.insert(0, kunci_str)
        
        # 3. Munculkan Pop-up Konfirmasi
        simpan = messagebox.askyesno(
            title="Simpan Kunci", 
            message="Kunci AES berhasil digenerate!\n\nSimpan kunci ke dalam file?"
        )
        
        # 4. Logika jika pengguna memilih 'Yes'
        if simpan:
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                initialfile="Kunci_AES.txt",
                title="Simpan Kunci AES"
            )
            
            if path: # Jika user tidak menekan tombol 'Cancel' pada jendela penyimpanan
                try:
                    with open(path, 'w') as f:
                        f.write(kunci_str)
                    messagebox.showinfo("Sukses", "Kunci AES berhasil disimpan.")
                except Exception as e:
                    messagebox.showerror("Error", f"Gagal menyimpan kunci:\n{e}")
                
    def jalankan_enkripsi():
        nonlocal wb_terenkripsi, kunci_aes_terenkripsi

        path_excel = entry_file_input.get()
        kunci_aes_input = entry_aes_key.get()
        kunci_publik_input = entry_pub_key.get()

        if not path_excel or not kunci_aes_input or not kunci_publik_input:
            messagebox.showwarning("Peringatan", "Harap isi semua kolom (File, Kunci AES, dan Kunci RSA)!")
            return
        
        # 1. LOGIKA PADDING KUNCI AES
        # Jika panjang kurang dari 32, tambahkan karakter ascii di belakangnya
        if len(kunci_aes_input) < 32:
            sisa = 32 - len(kunci_aes_input)
            karakter_pad = string.ascii_letters + string.digits + string.punctuation            
            pad = ''.join(random.choice(karakter_pad) for i in range(sisa))
            kunci_aes_input += pad
            entry_aes_key.delete(0, END)
            entry_aes_key.insert(0, kunci_aes_input)
        # Jika lebih dari 32, potong dan ambil 32 karakter pertama saja
        elif len(kunci_aes_input) > 32:
            kunci_aes_input = kunci_aes_input[:32]
            entry_aes_key.delete(0, END)
            entry_aes_key.insert(0, kunci_aes_input)
            
        # Ubah string kunci AES menjadi bytes untuk diproses backend
        aes_key_bytes = kunci_aes_input.encode('utf-8')
            
        # 3. PANGGIL BACKEND
        sukses, hasil = backend_file_processor.proses_enkripsi_dokumen(path_excel, kunci_publik_input, aes_key_bytes)

        if sukses:
            wb_terenkripsi, kunci_aes_terenkripsi = hasil
                
            entry_output_spreadsheet.configure(state="normal")
            entry_output_spreadsheet.delete(0, END)
            entry_output_spreadsheet.insert(0, "Spreadsheet terenkripsi siap disimpan")
            entry_output_spreadsheet.configure(state="readonly")

            entry_output_kunci_aes.configure(state="normal")
            entry_output_kunci_aes.delete(0, END)
            entry_output_kunci_aes.insert(0, kunci_aes_terenkripsi)
            entry_output_kunci_aes.configure(state="readonly")
            
            messagebox.showinfo("Sukses", f"Proses enkripsi telah berhasil")
        else:
            messagebox.showerror("Gagal", f"Enkripsi gagal:\n{hasil}")

    # --- Widget GUI ---
    
    ## Judul
    label_judul = CTkLabel(master=frame_enkripsi, text='Enkripsi', font=('Montserrat', 20, 'bold'))
    label_judul.place(relx=0.5, y=30, anchor='center')
    ## Button help
    btn_help = CTkButton(master=frame_enkripsi, text='?', font=('Montserrat', 12, 'bold'), width=20, height=20, command=tampilkan_help_enkripsi)
    btn_help.place(x=450, y=20)

    ## 1. Input File Spreadsheet
    label_file = CTkLabel(master=frame_enkripsi, text='Pilih File Spreadsheet', font=('Montserrat', 12))
    label_file.place(x=150, y=80)
    entry_file_input = CTkEntry(master=frame_enkripsi, width=300, placeholder_text="Lokasi file *.xlsx...")
    entry_file_input.place(x=350, y=80)
    btn_cari_file = CTkButton(master=frame_enkripsi, text="...", width=30, command=cari_file_excel)
    btn_cari_file.place(x=660, y=80)

    ## 2. Input Kunci AES
    label_aes = CTkLabel(master=frame_enkripsi, text='Masukkan Kunci AES', font=('Montserrat', 12))
    label_aes.place(x=150, y=120)
    entry_aes_key = CTkEntry(master=frame_enkripsi, width=300, placeholder_text="Kunci 32 karakter (256-bit)")
    entry_aes_key.place(x=350, y=120)
    btn_cari_keyAES = CTkButton(master=frame_enkripsi, text="...", width=30, command=cari_kunci_aes)
    btn_cari_keyAES.place(x=660, y=120)

    ## 3. Input Kunci Publik RSA
    label_pub = CTkLabel(master=frame_enkripsi, text='Masukkan Kunci Publik (e,n)', font=('Montserrat', 12))
    label_pub.place(x=150, y=160)
    entry_pub_key = CTkEntry(master=frame_enkripsi, width=300, placeholder_text="Kunci publik RSA")
    entry_pub_key.place(x=350, y=160)
    btn_cari_keyPub = CTkButton(master=frame_enkripsi, text="...", width=30, command=cari_kunci_publik)
    btn_cari_keyPub.place(x=660, y=160)

    ## Tombol Aksi (Generate AES & Proses)
    btn_gen_aes = CTkButton(master=frame_enkripsi, text='Generate Kunci AES', font=('Montserrat', 12, 'bold'), width=140, height=35, command=generate_random_aes)
    btn_gen_aes.place(x=200, y=210)
    btn_proses = CTkButton(master=frame_enkripsi, text='Proses Enkripsi', font=('Montserrat', 12, 'bold'), width=140, height=35, command=jalankan_enkripsi)
    btn_proses.place(x=360, y=210)

    ## Separator
    label_separator = CTkLabel(master=frame_enkripsi, text='.'*200, text_color="gray")
    label_separator.place(relx=0.5, y=260, anchor='center')

    ## Output file spreadsheet terenkripsi
    label_output_spreadsheet = CTkLabel(master=frame_enkripsi, text='File Spreadsheet Terenkripsi:', font=('Montserrat', 12))
    label_output_spreadsheet.place(x=150, y=290)
    entry_output_spreadsheet = CTkEntry(master=frame_enkripsi, width=300, placeholder_text="Output file...")
    entry_output_spreadsheet.place(x=150, y=320)
    btn_simpan_file_spreadsheet = CTkButton(master=frame_enkripsi, text='Simpan', font=('Montserrat', 12, 'bold'), width=100, height=30, command=lambda: simpan_spreadsheet_terenkripsi())
    btn_simpan_file_spreadsheet.place(x=460, y=320)

    ## Output kunci AES terenkripsi
    label_output_kunci_aes = CTkLabel(master=frame_enkripsi, text='Kunci AES Terenkripsi:', font=('Montserrat', 12))
    label_output_kunci_aes.place(x=150, y=360)
    entry_output_kunci_aes = CTkEntry(master=frame_enkripsi, width=300, placeholder_text="Output kunci...")
    entry_output_kunci_aes.place(x=150, y=390)
    btn_simpan_kunci_aes = CTkButton(master=frame_enkripsi, text='Simpan', font=('Montserrat', 12, 'bold'), width=100, height=30, command=lambda: simpan_kunci_aes_terenkripsi())
    btn_simpan_kunci_aes.place(x=460, y=390)

    frame_enkripsi.pack(fill="both", expand=True)

    def simpan_spreadsheet_terenkripsi():        
        if wb_terenkripsi is None:
            messagebox.showwarning("Peringatan", "Lakukan tahapan proses enkripsi terlebih dahulu.")
            return
        # 1. Ambil path dari file yang dipilih di input
        path_input = entry_file_input.get()
        
        # 2. Logika penentuan nama file default
        if path_input:
            nama_file_asli = os.path.basename(path_input)
            nama_tanpa_ekstensi = os.path.splitext(nama_file_asli)[0]
            nama_file_default = f"{nama_tanpa_ekstensi}_terenkripsi.xlsx"
        else:
            nama_file_default = "Dokumen_Terenkripsi.xlsx"

        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            initialfile=nama_file_default
        )
        if path:
            try:
                wb_terenkripsi.save(path)
                entry_output_spreadsheet.configure(state="normal")
                entry_output_spreadsheet.delete(0, END)
                entry_output_spreadsheet.insert(0, path)
                entry_output_spreadsheet.configure(state="readonly")
                messagebox.showinfo("Sukses", "File Spreadsheet Terenkripsi berhasil diamankan dan disimpan.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan file: {e}")

    def simpan_kunci_aes_terenkripsi():
        if kunci_aes_terenkripsi is None:
            messagebox.showwarning("Peringatan", "Lakukan tahapan proses enkripsi terlebih dahulu.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialfile="Kunci_AES_Terenkripsi.txt"
        )
        if path:
            try:
                with open(path, 'w') as f:
                    f.write(kunci_aes_terenkripsi)
                messagebox.showinfo("Sukses", "Kunci AES Terenkripsi berhasil disimpan.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan kunci: {e}")

# --- Laman Dekripsi ---
def laman_dekripsi():
    frame_dekripsi = CTkFrame(master=frame_utama, width=800, height=500, fg_color="transparent")
    frame_dekripsi.propagate(False)

    def tampilkan_help_dekripsi():
        jendela_help = CTkToplevel()
        jendela_help.title("Petunjuk - Dekripsi")
        jendela_help.geometry("550x500")
        jendela_help.resizable(False, False)
        jendela_help.attributes("-topmost", True)
        jendela_help.grab_set()

        label_judul_help = CTkLabel(master=jendela_help, text="Petunjuk Proses Dekripsi Dokumen", font=('Montserrat', 16, 'bold'))
        label_judul_help.pack(pady=(20, 15))

        teks_petunjuk = (
            "Program dekripsi digunakan untuk memulihkan dokumen spreadsheet yang telah terenkripsi "
            "ke bentuk aslinya. Berikut langkah-langkahnya:\n\n"
            
            "1. Memilih Dokumen Terenkripsi\n"
            "   Klik tombol 'Cari' untuk memilih file spreadsheet (.xlsx) yang telah terenkripsi'.\n\n"
            
            "2. Memasukkan Kunci AES Terenkripsi\n"
            "   Masukkan rentetan 32 blok bilangan bulat yang dipisahkan tanda hubung (-) yang Anda "
            "dapatkan dari file hasil enkripsi sebelumnya.\n\n"
            
            "3. Memasukkan Kunci Privat RSA\n"
            "   Masukkan Kunci Privat RSA Anda dengan format dua bilangan bulat yang dipisahkan koma (d,n). "
            "Kunci ini diperlukan untuk membuka Kunci AES di atas.\n\n"
            
            "4. Menjalankan Dekripsi\n"
            "   Klik tombol 'Dekripsi'. Sistem akan mendekripsi Kunci AES menggunakan RSA, kemudian "
            "menggunakannya untuk mendekripsi setiap sel dan gambar.\n\n"
            
            "5. Menyimpan Hasil\n"
            "   Setelah sukses, kolom kunci AES akan menampilkan karakter kunci asli. "
            "Gunakan tombol 'Simpan' untuk mengunduh:\n"
            "   • File Spreadsheet Asli.\n"
            "   • File teks berisi Kunci AES asli."
        )

        textbox_help = CTkTextbox(master=jendela_help, width=480, height=320, font=('Montserrat', 12), wrap="word")
        textbox_help.pack(padx=20, pady=5)
        textbox_help.insert("0.0", teks_petunjuk)
        textbox_help.configure(state="disabled")

        btn_tutup = CTkButton(master=jendela_help, text="Mengerti", font=('Montserrat', 12, 'bold'), width=120, command=jendela_help.destroy)
        btn_tutup.pack(pady=(15, 10))

    wb_hasil_dekripsi = None
    kunci_aes_hasil_dekripsi = None

    # --- Fungsi Helper untuk Memilih File ---
    def cari_file_terenkripsi():
        filename = filedialog.askopenfilename(
            title="Pilih File Spreadsheet Terenkripsi",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if filename:
            entry_input_spreadsheet_enc.delete(0, END)
            entry_input_spreadsheet_enc.insert(0, filename)

    def cari_kunci_aes_enc():
        filename = filedialog.askopenfilename(
            title="Pilih Kunci AES Terenkripsi",
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    kunci_aes_enc = f.read().strip()
                entry_aes_enc.delete(0, END)
                entry_aes_enc.insert(0, kunci_aes_enc)
            except Exception as e:
                messagebox.showerror(("Error", f"Gagal membaca file kunci AES terenkripsi: {e}"))
    
    def cari_kunci_privat():
        filename = filedialog.askopenfilename(
            title="Pilih Kunci Privat RSA",
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    kunci_privat = f.read().strip() 
                    entry_kunci_privat.delete(0, END)
                    entry_kunci_privat.insert(0, kunci_privat)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca file kunci publik: {e}")
    
    # --- FUNGSI INTEGRASI BACKEND ---
    def jalankan_dekripsi():
        nonlocal wb_hasil_dekripsi, kunci_aes_hasil_dekripsi

        path_excel_enc = entry_input_spreadsheet_enc.get()
        kunci_aes_enc = entry_aes_enc.get()
        kunci_privat_rsa = entry_kunci_privat.get()

        if not path_excel_enc or not kunci_aes_enc or not kunci_privat_rsa:
            messagebox.showwarning("Peringatan", "Harap lengkapi ketiga file input yang dibutuhkan!")
            return

        # Panggil Backend
        sukses, hasil = backend_file_processor.proses_dekripsi_dokumen(path_excel_enc, kunci_privat_rsa, kunci_aes_enc)

        if sukses:
            wb_hasil_dekripsi, kunci_aes_hasil_dekripsi = hasil

            entry_output_spreadsheet.configure(state="normal")
            entry_output_spreadsheet.delete(0, END)
            entry_output_spreadsheet.insert(0, "Spreadsheet terdekripsi siap disimpan")
            entry_output_spreadsheet.configure(state="readonly")

            entry_output_kunci_aes.configure(state="normal")
            entry_output_kunci_aes.delete(0, END)
            entry_output_kunci_aes.insert(0, kunci_aes_hasil_dekripsi)
            entry_output_kunci_aes.configure(state="readonly")
                
            messagebox.showinfo("Sukses", f"Proses dekripsi berhasil.")
        else:
            messagebox.showerror("Gagal", f"Proses Dekripsi gagal:\n{hasil}")

    # --- Widget GUI ---

    ## Judul Halaman
    label_judul = CTkLabel(master=frame_dekripsi, text='Dekripsi', font=('Montserrat', 20, 'bold'))
    label_judul.place(relx=0.5, y=30, anchor='center')
    ## Button help
    btn_help = CTkButton(master=frame_dekripsi, text='?', font=('Montserrat', 12, 'bold'), width=20, height=20, command=tampilkan_help_dekripsi)
    btn_help.place(x=450, y=20)

    ## 1. Input File Spreadsheet Terenkripsi
    label_file_enc = CTkLabel(master=frame_dekripsi, text='Pilih File Spreadsheet Terenkripsi', font=('Montserrat', 12))
    label_file_enc.place(x=120, y=80)
    entry_input_spreadsheet_enc = CTkEntry(master=frame_dekripsi, width=300, placeholder_text="Lokasi file *.xlsx terenkripsi...")
    entry_input_spreadsheet_enc.place(x=350, y=80)
    btn_cari_file = CTkButton(master=frame_dekripsi, text="...", width=30, command=cari_file_terenkripsi)
    btn_cari_file.place(x=660, y=80)

    ## 2. Input Kunci AES Terenkripsi
    label_aes_enc = CTkLabel(master=frame_dekripsi, text='Masukkan Kunci AES Terenkripsi', font=('Montserrat', 12))
    label_aes_enc.place(x=120, y=120)
    entry_aes_enc = CTkEntry(master=frame_dekripsi, width=300, placeholder_text="Kunci AES terenkripsi")
    entry_aes_enc.place(x=350, y=120)
    btn_cari_aes = CTkButton(master=frame_dekripsi, text="...", width=30, command=cari_kunci_aes_enc)
    btn_cari_aes.place(x=660, y=120)

    ## 3. Input Kunci Privat RSA
    label_priv = CTkLabel(master=frame_dekripsi, text='Masukkan Kunci Privat (d,n)', font=('Montserrat', 12))
    label_priv.place(x=120, y=160)
    entry_kunci_privat = CTkEntry(master=frame_dekripsi, width=300, placeholder_text="Kunci privat RSA")
    entry_kunci_privat.place(x=350, y=160)
    btn_cari_priv = CTkButton(master=frame_dekripsi, text="...", width=30, command=cari_kunci_privat)
    btn_cari_priv.place(x=660, y=160)

    ## Tombol Proses Dekripsi
    btn_proses = CTkButton(master=frame_dekripsi, text='Proses Dekripsi', font=('Montserrat', 12, 'bold'), width=160, height=35, command=jalankan_dekripsi)
    btn_proses.place(relx=0.5, y=220, anchor='center')

    ## Separator
    label_separator = CTkLabel(master=frame_dekripsi, text='.'*200, text_color="gray")
    label_separator.place(relx=0.5, y=250, anchor='center')

    ## Output Spreadsheet Terdekripsi
    label_output_spreadsheet = CTkLabel(master=frame_dekripsi, text='File Spreadsheet Terdekripsi:', font=('Montserrat', 12))
    label_output_spreadsheet.place(x=150, y=280)
    entry_output_spreadsheet = CTkEntry(master=frame_dekripsi, width=300, placeholder_text="Output file...")
    entry_output_spreadsheet.place(x=150, y=310)
    btn_simpan_file_spreadsheet = CTkButton(master=frame_dekripsi, text='Simpan', font=('Montserrat', 12, 'bold'), width=100, height=30, command=lambda: simpan_spreadsheet_terdekripsi())
    btn_simpan_file_spreadsheet.place(x=460, y=310)

    ## Output Kunci AES Terdekripsi
    label_output_kunci_aes = CTkLabel(master=frame_dekripsi, text='Kunci AES Terdekripsi:', font=('Montserrat', 12))
    label_output_kunci_aes.place(x=150, y=350)
    entry_output_kunci_aes = CTkEntry(master=frame_dekripsi, width=300, placeholder_text="Output kunci...")
    entry_output_kunci_aes.place(x=150, y=380)
    btn_simpan_file_kunci = CTkButton(master=frame_dekripsi, text='Simpan', font=('Montserrat', 12, 'bold'), width=100, height=30, command=lambda: simpan_kunci_aes_terdekripsi())
    btn_simpan_file_kunci.place(x=460, y=380)

    frame_dekripsi.pack(fill="both", expand=True)

    def simpan_spreadsheet_terdekripsi():
        if wb_hasil_dekripsi is None:
            messagebox.showwarning("Peringatan", "Lakukan proses dekripsi terlebih dahulu.")
            return
            
        path_input = entry_input_spreadsheet_enc.get()
        # Logika penamaan: dokumen_terenkripsi_terdekripsi.xlsx atau dokumen_terdekripsi.xlsx
        nama_asli = os.path.basename(path_input)
        nama_clean = os.path.splitext(nama_asli)[0].replace("_terenkripsi", "")
        nama_default = f"{nama_clean}_terdekripsi.xlsx"
            
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            initialfile=nama_default
        )
        if path:
            try:
                wb_hasil_dekripsi.save(path)
                entry_output_spreadsheet.configure(state="normal")
                entry_output_spreadsheet.delete(0, END)
                entry_output_spreadsheet.insert(0, path)
                entry_output_spreadsheet.configure(state="readonly")
                messagebox.showinfo("Sukses", "File Spreadsheet berhasil disimpan.")
            except PermissionError:
                messagebox.showerror("Akses Ditolak", "Tutup file Excel yang bersangkutan sebelum menyimpan.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan: {e}")

    def simpan_kunci_aes_terdekripsi():
        if kunci_aes_hasil_dekripsi is None:
            messagebox.showwarning("Peringatan", "Lakukan proses dekripsi terlebih dahulu.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialfile="Kunci_AES_terdekripsi.txt"
        )
        if path:
            try:
                with open(path, 'w') as f:
                    f.write(kunci_aes_hasil_dekripsi)
                messagebox.showinfo("Sukses", "Kunci AES asli berhasil disimpan.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan: {e}")

# --- Fungsi sembunyikan frame ---
def sembunyikan_frame():
    for frame in frame_utama.winfo_children():
        frame.destroy()

# --- Fungsi munculkan frame ---
def munculkan(laman):
    sembunyikan_frame()
    laman()

# --- frame pilihan program ---
frame_pilihan = CTkFrame(master = root, width = 200, height = 500, fg_color = ("#EAEAEA","#333333"))
frame_pilihan.propagate(False)

# --- Pilihan Program ---
label_PilihanProgram = CTkLabel(master = frame_pilihan, text = 'Pilihan Program', font = ('Montserrat', 14, 'bold'))
label_PilihanProgram.place(x = 45, y = 5)
btn_home = CTkButton(master = frame_pilihan, text = 'Home', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command = lambda: munculkan(laman_home))
btn_home.place(x = 20, y = 70)
button_pembangkitankunci = CTkButton(master = frame_pilihan, text = 'Pembangkitan Kunci', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command = lambda: munculkan(laman_pembangkitankunci))
button_pembangkitankunci.place(x = 20, y = 120)
button_enkripsi = CTkButton(master = frame_pilihan, text = 'Enkripsi', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command = lambda: munculkan(laman_enkripsi))
button_enkripsi.place(x = 20, y = 170)
button_dekripsi = CTkButton(master = frame_pilihan, text = 'Dekripsi', font = ('Montserrat', 12), width = 160, height = 30, corner_radius= 10, command=lambda: munculkan(laman_dekripsi))
button_dekripsi.place(x = 20, y = 220)
label_watermark = CTkLabel(master=frame_pilihan, text="2209397 - M Rizqi Winnel A", font = ('Montserrat', 12))
label_watermark.place(x=15, y=460)

frame_pilihan.pack(side = 'left')
frame_utama.pack(side = 'left')
laman_home()

root.mainloop()