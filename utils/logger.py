import logging
import os
from datetime import datetime
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """Formatter kustom untuk menambahkan warna pada level log."""
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        record.levelname = f"{log_color}{record.levelname:<8}{Style.RESET_ALL}"
        return super().format(record)

def setup_logger(log_level: str = "INFO") -> logging.Logger:
    """Mengatur logger untuk output konsol dan file."""
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger('FairblockBot')
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    logger.handlers.clear()

    # Formatter untuk konsol
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    # Formatter untuk file
    log_filename = f"logs/bot_{datetime.now().strftime('%Y-%m-%d')}.log"
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s'
    )
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
