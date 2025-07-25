import asyncio
import json
from colorama import Fore, Style, init

from fairblock_bot import FairblockBot
from config import Config

# Inisialisasi colorama
init(autoreset=True)

class BotInterface:
    """Kelas antarmuka untuk interaksi dengan pengguna."""
    
    def __init__(self):
        try:
            self.bot = FairblockBot()
        except ValueError as e:
            print(f"{Fore.RED}{e}")
            self.bot = None

    def display_banner(self):
        """Menampilkan banner bot."""
        banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                     🔮 FAIRBLOCK BOT 🔮                      ║
║          Antarmuka Interaktif untuk Testnet Fairblock        ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """
        print(banner)

    def display_menu(self):
        """Menampilkan menu opsi."""
        menu = f"""
{Fore.GREEN}Pilih Aksi:{Style.RESET_ALL}
  1. 🪙  Klaim Faucet
  2. 💣  Tanam Time Bomb
  3. 💳  Cek Saldo Wallet
  4. 🖥️  Monitor Status Demo Apps
  
  9. 🤖  Mulai Auto-Claim Faucet
 10. 🛑  Hentikan Auto-Claim Faucet

  0. 🚪  Keluar
"""
        print(menu)

    async def handle_choice(self, choice: str):
        """Menangani pilihan pengguna."""
        if choice == '1':
            result = await self.bot.claim_faucet()
            print(json.dumps(result, indent=2))
        elif choice == '2':
            message = input("Masukkan pesan rahasia untuk bomb: ")
            try:
                hours = int(input("Berapa jam dari sekarang bomb akan terbuka? (contoh: 1): "))
                if hours <= 0:
                    print(f"{Fore.RED}Jumlah jam harus positif.")
                    return
                result = await self.bot.plant_time_bomb(message, hours)
                print(json.dumps(result, indent=2))
            except ValueError:
                print(f"{Fore.RED}Input jam tidak valid.")
        elif choice == '3':
            balance = await self.bot.get_wallet_balance()
            if balance['success']:
                print(f"{Fore.GREEN}Saldo Wallet: {balance['balance_eth']} ETH")
            else:
                print(f"{Fore.RED}Gagal cek saldo: {balance['error']}")
        elif choice == '4':
            status = await self.bot.monitor_demos()
            for name, data in status.items():
                status_color = Fore.GREEN if data['online'] else Fore.RED
                print(f"  - {name:<15} | Status: {status_color}{'ONLINE' if data['online'] else 'OFFLINE':<8}{Style.RESET_ALL} | Kode: {data['status_code']} | Waktu: {data['response_time_ms']}ms")
        elif choice == '9':
            self.bot.start_auto_claim()
        elif choice == '10':
            self.bot.stop_auto_claim()
        elif choice == '0':
            return False
        else:
            print(f"{Fore.RED}Pilihan tidak valid.")
        return True

    async def run(self):
        """Menjalankan loop utama bot."""
        if not self.bot:
            return

        self.display_banner()
        Config.display()
        print("-" * 62)

        running = True
        while running:
            self.display_menu()
            choice = input(f"{Fore.YELLOW}Masukkan pilihan Anda: {Style.RESET_ALL}").strip()
            running = await self.handle_choice(choice)
            if running:
                input(f"\n{Fore.CYAN}Tekan Enter untuk kembali ke menu...{Style.RESET_ALL}")
        
        await self.bot.cleanup()
        print(f"{Fore.MAGENTA}Bot dihentikan. Sampai jumpa!")

async def main():
    """Fungsi main asinkron."""
    interface = BotInterface()
    await interface.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nKeluar dari program.")
