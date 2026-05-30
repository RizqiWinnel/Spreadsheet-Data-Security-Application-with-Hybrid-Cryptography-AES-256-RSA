# backend_rsa.py
from Crypto.Util.number import getPrime, inverse, GCD, isPrime
import random
import math

def generate_prime_number(bits=1024):
    return getPrime(bits)

def generate_rsa_keys(p1, p2):
    try:
        # Validasi Input
        if p1 == p2:
            return False, "Nilai P₁ dan P₂ tidak boleh sama!"
        
        if not isPrime(p1) or not isPrime(p2):
            return False, "Nilai bilangan yang anda masukkan bukan bilangan prima. Mohon masukkan P₁ dan P₂ bilangan prima"
        
        # 1. Hitung n (Modulus)
        n = p1 * p2
        
        # 2. Hitung phi
        phi = (p1 - 1) * (p2 - 1)
        
        # 3. Tentukan e
        while True:
            e = random.randrange(1, phi-1)
            if GCD(e, phi) == 1:
                break
            
        # 4. Hitung d (Private Exponent)
        d = inverse(e, phi)
        
        # 5. Ubah ke String
        n_str = str(n)
        e_str = str(e)
        d_str = str(d)
        
        # Format string untuk output GUI
        pub_key = f"{e_str},{n_str}"
        priv_key = f"{d_str},{n_str}"
        
        return True, (pub_key, priv_key)
        
    except Exception as e:
        return False, str(e)
    
# --- Tambahan untuk Enkripsi/Dekripsi Kunci AES ---

def encrypt_rsa(aes_key_bytes, public_key_str):
    """
    Memecah Kunci AES 32-byte menjadi 32 blok terpisah,
    mengenkupsi tiap blok dengan RSA.
    """
    try:
        # 1. Pisah Kunci Publik "e,n"
        e_str, n_str = public_key_str.split(',')
        e = int(e_str)
        n = int(n_str)
        
        cipher_blocks = []
        
        # 2. Iterasi per byte (Total 32 perulangan)
        for m in aes_key_bytes:
            # Nilai 'byte' di Python secara otomatis adalah integer 0-255
            if m >= n:
                return False, "Modulus n terlalu kecil untuk mengenkripsi nilai byte (n harus > 255)."
                
            # 3. Rumus Enkripsi RSA untuk tiap blok: C = m^e mod n
            c = pow(m, e, n)
            
            cipher_blocks.append(str(c))
            
        # 5. Gabungkan 32 blok dengan tanda hubung (-)
        cipher_key_str = "-".join(cipher_blocks)
        
        return True, cipher_key_str
        
    except Exception as e:
        return False, str(e)

def decrypt_rsa(cipher_key_str, private_key_str):
    """
    Mendekripsi 32 blok Heksadesimal kembali menjadi Kunci AES utuh (Bytes).
    """
    try:
        # 1. Pisah Kunci Privat "d,n"
        d_str, n_str = private_key_str.split(',')
        d = int(d_str)
        n = int(n_str)
        
        # 2. Pisahkan ciphertext berdasarkan tanda hubung
        cipher_blocks_str = cipher_key_str.split('-')
        
        # Validasi sederhana
        if len(cipher_blocks_str) != 32:
            return False, "Format ciphertext RSA tidak valid atau tidak berjumlah 32 blok."
        
        plain_bytes_list = bytearray()
        
        # 3. Iterasi dekripsi per blok
        for cipher_str in cipher_blocks_str:
            # Konversi ke integer
            c = int(cipher_str)

            # Rumus Dekripsi RSA: M = C^d mod n
            m = pow(c, d, n)
            
            # Masukkan hasil ke dalam array byte
            plain_bytes_list.append(m)
            
        # 4. Kembalikan sebagai format bytes utuh
        return True, bytes(plain_bytes_list)
        
    except Exception as e:
        return False, str(e)