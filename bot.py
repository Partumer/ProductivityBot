"""Telegram-бот для создания событий в Google Calendar."""
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from ai import parse_event
from google_calendar import create_event
from config import TELEGRAM_TOKEN

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    await update.message.reply_text(
        "Привет! Напиши мне о событии, например:\n"
        "«встретиться с Петей завтра в 19:00»\n"
        "или\n"
        "«meeting with John tomorrow at 7 PM»\n"
        "Я создам событие в твоём календаре."
    )


async def process_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает текстовое сообщение и создает событие в календаре.
    
    Args:
        update: Объект обновления от Telegram
        context: Контекст бота
    """
    user_text = update.message.text
    user_id = update.effective_user.id
    
    if not user_text or not user_text.strip():
        await update.message.reply_text("Пожалуйста, отправь текстовое сообщение.")
        return
    
    # Показываем, что бот обрабатывает запрос
    await update.message.reply_text("Обрабатываю запрос...")
    
    try:
        # Парсим событие через OpenAI
        event_data = parse_event(user_text)
        
        if not event_data:
            logger.warning(f"Не удалось распознать событие для пользователя {user_id}. Текст: {user_text}")
            await update.message.reply_text(
                "Извини, произошла ошибка при обработке запроса. "
                "Попробуй написать более подробно, например:\n"
                "«встретиться с Петей завтра в 19:00»\n"
                "или\n"
                "«meeting with John tomorrow at 7 PM»"
            )
            return
        
        # Создаем событие в Google Calendar
        event_id = create_event(event_data)
        
        if not event_id:
            logger.error(f"Не удалось создать событие в календаре для пользователя {user_id}. Данные: {event_data}")
            await update.message.reply_text(
                "Извини, произошла ошибка при создании события в календаре."
            )
            return
        
        # Формируем ответ пользователю
        date_str = event_data["date"]
        time_str = event_data["time"]
        title = event_data["title"]
        
        # Форматируем дату для читаемости
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d.%m.%Y")
        except Exception as e:
            logger.warning(f"Ошибка форматирования даты: {e}")
            formatted_date = date_str
        
        response = (
            f"✅ Событие добавлено: {title}\n"
            f"📅 Дата: {formatted_date}\n"
            f"🕐 Время: {time_str}"
        )
        
        await update.message.reply_text(response)
        logger.info(f"Событие успешно создано для пользователя {user_id}: {title} на {date_str} {time_str}")
        
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке запроса пользователя {user_id}: {e}", exc_info=True)
        await update.message.reply_text(
            "Извини, произошла ошибка. Попробуй позже или напиши более подробно."
        )


def main():
    """Запуск бота."""
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, process_event)
    )
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

