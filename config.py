import os
from dotenv import load_dotenv
from typing import Optional, Dict

# Memuat variabel dari file .env
load_dotenv()

class Config:
    """
    Kelas konfigurasi untuk menampung semua pengaturan bot.
    Memuat nilai dari environment variables.
    """
    # Konfigurasi Wallet
    PRIVATE_KEY: Optional[str] = os.getenv('PRIVATE_KEY')
    WALLET_ADDRESS: Optional[str] = os.getenv('WALLET_ADDRESS')
    RPC_URL: str = os.getenv('RPC_URL', 'https://rpc.testnet.fairyring.com')

    # Pengaturan Bot
    AUTO_CLAIM_INTERVAL: int = int(os.getenv('AUTO_CLAIM_INTERVAL', '60'))
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO').upper()
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', '30'))

    # URL API
    BASE_URLS: Dict[str, str] = {
        'website': 'https://www.fairblock.network/',
        'faucet': 'https://testnet-faucet.fairblock.network/',
        'bomb': 'https://bomb.fairblock.network/',
        'swap': 'https://swap.fairycow.fi',
        'docs': 'https://docs.fairblock.network/',
    }

    # Headers HTTP
    HEADERS: Dict[str, str] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
    }

    @classmethod
    def validate(cls) -> bool:
        """Memvalidasi apakah konfigurasi penting sudah diatur."""
        if not cls.PRIVATE_KEY:
            print("❌ ERROR: PRIVATE_KEY tidak ditemukan di file .env.")
            return False
        if len(cls.PRIVATE_KEY) != 64:
            print("❌ ERROR: PRIVATE_KEY harus terdiri dari 64 karakter (tanpa awalan 0x).")
            return False
        return True

    @classmethod
    def display(cls):
        """Menampilkan konfigurasi saat ini (menyembunyikan data sensitif)."""
        print("🔧 Konfigurasi Saat Ini:")
        print(f"   - RPC URL: {cls.RPC_URL}")
        print(f"   - Alamat Wallet: {cls.WALLET_ADDRESS or 'Akan dibuat dari Private Key'}")
        print(f"   - Interval Auto-Claim: {cls.AUTO_CLAIM_INTERVAL} menit")
        print(f"   - Private Key: {'✅ Dimuat' if cls.PRIVATE_KEY else '❌ KOSONG'}")
