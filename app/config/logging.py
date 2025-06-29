import logging
import sys
from datetime import datetime
from logging import StreamHandler


# Кольорові коди ANSI
class Colors:
    HEADER = "\033[95m"
    INFO = "\033[94m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    CRITICAL = "\033[41m"  # Червоний фон для CRITICAL
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DEBUG = "\033[37m"  # Світло-сірий для DEBUG


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Зберігаємо оригінальний levelname
        orig_levelname = record.levelname

        # Додаємо кольори залежно від рівня логування
        if record.levelno == logging.DEBUG:
            record.levelname = f"{Colors.DEBUG}{orig_levelname}{Colors.RESET}"
        elif record.levelno == logging.INFO:
            record.levelname = f"{Colors.INFO}{orig_levelname}{Colors.RESET}"
        elif record.levelno == logging.WARNING:
            record.levelname = f"{Colors.WARNING}{orig_levelname}{Colors.RESET}"
        elif record.levelno == logging.ERROR:
            record.levelname = f"{Colors.ERROR}{orig_levelname}{Colors.RESET}"
        elif record.levelno == logging.CRITICAL:
            record.levelname = (
                f"{Colors.CRITICAL}{Colors.BOLD}{orig_levelname}{Colors.RESET}"
            )

        # Формат дати
        dt_fmt = "%H:%M:%S %d-%m-%Y"  # Годинник:Хвилини:Секунди День-Місяць-Рік
        record.asctime = datetime.now().strftime(dt_fmt)

        # Вичисляємо довжину рядка, щоб вирівняти по правому краю
        log_line = f"{record.asctime} | {record.levelname}: {record.msg}"

        # Друкуємо повідомлення з вирівнюванням (можна змінювати ширину)
        total_length = 100  # Ширина всього рядка
        spaces_needed = total_length - len(log_line)
        return f"{log_line}{' ' * spaces_needed}"


def setup_logging():
    # Створюємо логер
    logger = logging.getLogger("mafia_bot")
    logger.setLevel(logging.DEBUG)  # Для виведення всіх рівнів логів

    # Створюємо handler для виводу в консоль
    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)  # Параметр DEBUG для всіх типів повідомлень

    # Створюємо форматтер
    formatter = ColoredFormatter(
        fmt="%(message)s",  # Ми змінимо формат в самому formatter
        datefmt="%H:%M:%S %d-%m-%Y",
    )

    # Застосовуємо форматтер до handler
    console_handler.setFormatter(formatter)

    # Добавляємо handler до логгеру
    logger.addHandler(console_handler)

    return logger


# Створюємо й експортуємо логгер
logger = setup_logging()
