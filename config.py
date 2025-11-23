"""Конфигурация проекта - загрузка переменных окружения."""
import os
from typing import Optional

# Загружаем переменные из .env файла, если он существует
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv не установлен, используем системные переменные


def get_env(key: str, default: Optional[str] = None) -> str:
    """Получить переменную окружения или вернуть default."""
    value = os.environ.get(key, default)
    if value is None:
        raise ValueError(f"Переменная окружения {key} не установлена")
    return value


# Telegram
TELEGRAM_TOKEN = get_env("TELEGRAM_TOKEN")

# OpenAI
OPENAI_API_KEY = get_env("OPENAI_API_KEY")

# Google Calendar
GOOGLE_CLIENT_ID = get_env("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = get_env("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN = get_env("GOOGLE_REFRESH_TOKEN")

# Часовой пояс
TIMEZONE = get_env("TZ", "Europe/Berlin")


