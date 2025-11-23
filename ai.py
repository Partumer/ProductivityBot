"""Парсинг событий из текста через OpenAI ChatGPT."""
import json
import logging
from typing import Dict, Optional

from openai import OpenAI

from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


def parse_event(text: str) -> Optional[Dict]:
    """
    Парсит текст сообщения и извлекает информацию о событии.
    
    Args:
        text: Текст сообщения от пользователя
        
    Returns:
        Словарь с полями: title, date, time, description, duration_minutes
        или None в случае ошибки
    """
    prompt = """You are an event parser for my calendar. Extract meeting information and return strict JSON.
You understand both Russian and English languages.

Format:
{
  "title": "",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "description": "",
  "duration_minutes": 60
}

Rules:
- Date format: YYYY-MM-DD
- Time format: HH:MM (24-hour format)
- If duration is not specified — set 60 minutes
- If description is missing — duplicate the title
- Return only JSON, no additional text
- Understand relative dates like "tomorrow", "завтра", "after tomorrow", "послезавтра", "today", "сегодня"

User text:
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Используем gpt-4o-mini (исправлено с gpt-4.1-mini)
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            temperature=0,
            response_format={"type": "json_object"}  # Принудительно JSON формат
        )
        
        content = response.choices[0].message.content.strip()
        
        # Парсим JSON
        event_data = json.loads(content)
        
        # Валидация обязательных полей
        required_fields = ["title", "date", "time"]
        for field in required_fields:
            if field not in event_data:
                logger.error(f"Отсутствует обязательное поле: {field}")
                return None
        
        # Устанавливаем значения по умолчанию
        if "description" not in event_data or not event_data["description"]:
            event_data["description"] = event_data["title"]
        
        if "duration_minutes" not in event_data:
            event_data["duration_minutes"] = 60
        
        return event_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON: {e}", exc_info=True)
        logger.error(f"Ответ от OpenAI: {content if 'content' in locals() else 'N/A'}")
        return None
    except Exception as e:
        logger.error(f"Ошибка при вызове OpenAI API: {e}", exc_info=True)
        return None

