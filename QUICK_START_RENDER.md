# ⚡ Быстрый старт на Render

## 🎯 Минимальные шаги для деплоя

### 1. Подготовьте токены (5 минут)

- **Telegram:** [@BotFather](https://t.me/BotFather) → `/newbot` → скопируйте токен
- **OpenAI:** [platform.openai.com](https://platform.openai.com/api-keys) → создайте ключ
- **Google:** См. подробную инструкцию в `RENDER_DEPLOY.md` (раздел "Google Calendar Credentials")

### 2. Загрузите код на GitHub (2 минуты)

```bash
# Если еще не создали репозиторий
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/ваш-username/ваш-репозиторий.git
git push -u origin main
```

### 3. Создайте сервис на Render (3 минуты)

1. Зайдите на [render.com](https://render.com/)
2. **New +** → **Background Worker**
3. Подключите GitHub репозиторий
4. Настройки:
   - **Name:** `telegram-calendar-bot`
   - **Environment:** `Docker` (или `Python 3`)
   - **Start Command:** `python bot.py` (если Python 3)

### 4. Добавьте переменные окружения (2 минуты)

В настройках сервиса → **Environment Variables** → добавьте:

```
TELEGRAM_TOKEN=ваш_токен
OPENAI_API_KEY=ваш_ключ
GOOGLE_CLIENT_ID=ваш_client_id
GOOGLE_CLIENT_SECRET=ваш_secret
GOOGLE_REFRESH_TOKEN=ваш_refresh_token
TZ=Europe/Berlin
```

### 5. Запустите деплой

Нажмите **"Create Background Worker"** и ждите завершения.

### 6. Проверьте работу

Откройте Telegram → найдите бота → `/start` → `встретиться завтра в 19:00`

---

## ✅ Готово!

Бот работает 24/7 на Render. Все логи доступны в панели Render → **Logs**.

**Подробная инструкция:** см. `RENDER_DEPLOY.md`

