# Telegram-бот → ChatGPT → Google Calendar

Минимальная рабочая версия бота, который создаёт события в Google Calendar на основе текстовых сообщений.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните все переменные:

```bash
cp .env.example .env
```

**Необходимые переменные:**

- `TELEGRAM_TOKEN` - токен бота от @BotFather
- `OPENAI_API_KEY` - API ключ OpenAI
- `GOOGLE_CLIENT_ID` - Client ID из Google Cloud Console
- `GOOGLE_CLIENT_SECRET` - Client Secret из Google Cloud Console
- `GOOGLE_REFRESH_TOKEN` - Refresh Token для OAuth2
- `TZ` - часовой пояс (по умолчанию `Europe/Berlin`)

### 3. Получение Google Calendar credentials

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
2. Включите Google Calendar API
3. Создайте OAuth 2.0 Client ID (тип: Desktop app)
4. Скачайте credentials.json
5. Запустите скрипт для получения refresh token (см. раздел ниже)

### 4. Запуск бота

```bash
python bot.py
```

## 📝 Использование

Отправьте боту сообщение вида:
- "встретиться с Петей завтра в 19:00"
- "совещание 25 декабря в 14:30"
- "зубной врач послезавтра в 10:00"

Бот распарсит сообщение через ChatGPT и создаст событие в вашем Google Calendar.

## 🔧 Получение Google Refresh Token

Для получения refresh token выполните:

```python
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

# Сохраните refresh_token
print(f"GOOGLE_REFRESH_TOKEN={creds.refresh_token}")
print(f"GOOGLE_CLIENT_ID={creds.client_id}")
print(f"GOOGLE_CLIENT_SECRET={creds.client_secret}")
```

## 🐳 Деплой на Render

**📖 Подробная инструкция:** см. [RENDER_DEPLOY.md](RENDER_DEPLOY.md)

**⚡ Быстрый старт:** см. [QUICK_START_RENDER.md](QUICK_START_RENDER.md)

Кратко:
1. Загрузите код на GitHub
2. Создайте Background Worker на Render
3. Подключите репозиторий
4. Добавьте переменные окружения
5. Запустите деплой

Render автоматически обнаружит `Dockerfile` или используйте `Procfile` для Python.

## 📁 Структура проекта

```
project/
├── bot.py                 # Основной Telegram-бот
├── ai.py                  # Логика вызова OpenAI и парсинга JSON
├── calendar.py            # Интеграция с Google Calendar API
├── config.py              # Загрузка env-переменных
├── requirements.txt       # Зависимости Python
├── Dockerfile             # Для деплоя на Render
├── Procfile               # Для запуска worker на Render
├── .env.example           # Образец env файла
└── README.md              # Документация
```

## ⚠️ Примечания

- Бот использует модель `gpt-4o-mini` для парсинга событий
- По умолчанию длительность события - 60 минут
- Часовой пояс настраивается через переменную `TZ`
- Бот обрабатывает только текстовые сообщения


