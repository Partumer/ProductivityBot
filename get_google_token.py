"""
Вспомогательный скрипт для получения Google Refresh Token.

Использование:
1. Скачайте credentials.json из Google Cloud Console
2. Поместите его в корень проекта
3. Запустите: python get_google_token.py
4. Скопируйте выведенные значения в .env файл
"""
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    if not os.path.exists('credentials.json'):
        print("❌ Файл credentials.json не найден!")
        print("Скачайте его из Google Cloud Console и поместите в корень проекта.")
        return
    
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    print("\n" + "="*60)
    print("✅ Успешно получены credentials!")
    print("="*60)
    print("\nДобавьте следующие строки в ваш .env файл:\n")
    print(f"GOOGLE_CLIENT_ID={creds.client_id}")
    print(f"GOOGLE_CLIENT_SECRET={creds.client_secret}")
    print(f"GOOGLE_REFRESH_TOKEN={creds.refresh_token}")
    print("\n" + "="*60)

if __name__ == '__main__':
    main()


