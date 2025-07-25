import hashlib
import json
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class EncryptionHelper:
    """Kelas helper untuk operasi enkripsi AES-256."""

    @staticmethod
    def _derive_key(timestamp: int) -> bytes:
        """Membuat kunci enkripsi 32-byte dari timestamp."""
        key_material = f"fairblock_secret_{timestamp}".encode('utf-8')
        return hashlib.sha256(key_material).digest()

    @staticmethod
    def encrypt(message: str, unlock_timestamp: int) -> dict:
        """Enkripsi pesan menggunakan kunci yang berasal dari timestamp."""
        try:
            key = EncryptionHelper._derive_key(unlock_timestamp)
            cipher = AES.new(key, AES.MODE_CBC)
            message_bytes = message.encode('utf-8')
            padded_bytes = pad(message_bytes, AES.block_size)
            encrypted_bytes = cipher.encrypt(padded_bytes)
            
            # Encode ke Base64 untuk transfer yang aman
            iv_b64 = base64.b64encode(cipher.iv).decode('utf-8')
            encrypted_data_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
            
            return {
                "success": True,
                "iv": iv_b64,
                "encrypted_data": encrypted_data_b64,
                "unlock_timestamp": unlock_timestamp
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def decrypt(encrypted_data_b64: str, iv_b64: str, unlock_timestamp: int) -> dict:
        """Dekripsi pesan menggunakan kunci yang berasal dari timestamp."""
        try:
            key = EncryptionHelper._derive_key(unlock_timestamp)
            iv = base64.b64decode(iv_b64)
            encrypted_data = base64.b64decode(encrypted_data_b64)
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_padded_bytes = cipher.decrypt(encrypted_data)
            decrypted_bytes = unpad(decrypted_padded_bytes, AES.block_size)
            
            return {
                "success": True,
                "decrypted_message": decrypted_bytes.decode('utf-8')
            }
        except (ValueError, KeyError) as e:
            return {"success": False, "error": f"Dekripsi gagal. Kunci atau data salah: {e}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
