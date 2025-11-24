"""Интеграция с Google Calendar API."""
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REFRESH_TOKEN,
    TIMEZONE,
)

logger = logging.getLogger(__name__)

# Области доступа для Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    """
    Создает и возвращает сервис Google Calendar API.
    
    Returns:
        Объект сервиса Google Calendar API
    """
    creds = Credentials(
        token=None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
    )
    
    # Обновляем токен, если нужно
    if creds.expired:
        creds.refresh(Request())
    
    service = build("calendar", "v3", credentials=creds)
    return service


def create_event(event_data: Dict) -> Optional[str]:
    """
    Создает событие в Google Calendar.
    
    Args:
        event_data: Словарь с полями:
            - title: название события
            - date: дата в формате YYYY-MM-DD
            - time: время в формате HH:MM
            - description: описание
            - duration_minutes: длительность в минутах
            
    Returns:
        ID созданного события или None в случае ошибки
    """
    try:
        # Парсим дату и время
        date_str = event_data["date"]
        time_str = event_data["time"]
        duration_minutes = event_data.get("duration_minutes", 60)
        
        # Создаем datetime объекты
        start_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        
        # Форматируем для Google Calendar API (RFC3339)
        start_time = start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        end_time = end_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Формируем тело события
        event_body = {
            "summary": event_data["title"],
            "description": event_data.get("description", event_data["title"]),
            "start": {
                "dateTime": start_time,
                "timeZone": TIMEZONE,
            },
            "end": {
                "dateTime": end_time,
                "timeZone": TIMEZONE,
            },
        }
        
        # Создаем событие
        service = get_calendar_service()
        event = service.events().insert(calendarId="primary", body=event_body).execute()
        
        logger.info(f"Событие создано: {event.get('id')}")
        return event.get("id")
        
    except HttpError as e:
        logger.error(f"Ошибка Google Calendar API: {e}", exc_info=True)
        logger.error(f"Детали ошибки: {e.error_details if hasattr(e, 'error_details') else 'N/A'}")
        return None
    except ValueError as e:
        logger.error(f"Ошибка парсинга даты/времени: {e}", exc_info=True)
        logger.error(f"Данные события: {event_data}")
        return None
    except Exception as e:
        logger.error(f"Неожиданная ошибка при создании события: {e}", exc_info=True)
        logger.error(f"Данные события: {event_data}")
        return None

