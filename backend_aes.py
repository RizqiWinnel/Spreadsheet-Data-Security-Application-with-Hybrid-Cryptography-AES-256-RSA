# Backend AES

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_aes(data_bytes, key):
    """
    Mengenkripsi data (bytes) menggunakan AES-256 Mode ECB.
    Input: data (bytes), key (bytes)
    Output: ciphertext
    """
    try:
        # 1. Buat Cipher Object
        cipher = AES.new(key, AES.MODE_ECB)
        
        # 2. Lakukan Padding (Agar panjang data kelipatan 16 byte)
        data_padded = pad(data_bytes, AES.block_size)
        
        # 3. Enkripsi
        ciphertext = cipher.encrypt(data_padded)
        
        # 4. Kembalikan Ciphertext.
        return ciphertext
        
    except Exception as e:
        print(f"Error Enkripsi AES: {e}")
        return None

def decrypt_aes(encrypted_data, key):
    """
    Mendekripsi data AES-256.
    Input: ciphertext, key
    Output: data asli (bytes)
    """
    try:
        # 1. Buat Cipher Object
        cipher = AES.new(key, AES.MODE_ECB)
        
        # 2. Dekripsi dan Unpadding
        decrypted_padded = cipher.decrypt(encrypted_data)
        original_data = unpad(decrypted_padded, AES.block_size)
        
        return original_data
        
    except Exception as e:
        print(f"Error Dekripsi AES: {e}")
        return None