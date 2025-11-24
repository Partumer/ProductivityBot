"""
Вспомогательный скрипт для получения Google Refresh Token.

Использование:
1. Скачайте credentials.json из Google Cloud Console
2. Поместите его в корень проекта
3. Запустите: python3 get_google_token.py
4. Скопируйте выведенные значения в .env файл
"""
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import sys

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    if not os.path.exists('credentials.json'):
        print("❌ Файл credentials.json не найден!")
        print("Скачайте его из Google Cloud Console и поместите в корень проекта.")
        return
    
    try:
        print("🔄 Запускаю локальный сервер для авторизации...")
        print("📝 Откроется браузер - войдите в ваш Google аккаунт")
        print("⚠️  Если появится ошибка 'redirect_uri_mismatch', см. инструкцию в GOOGLE_SETUP.md (Шаг 4.5)\n")
        
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True)
    except Exception as e:
        if 'redirect_uri_mismatch' in str(e).lower() or '400' in str(e):
            print("\n❌ ОШИБКА: redirect_uri_mismatch")
            print("\n🔧 Решение:")
            print("1. Зайдите в Google Cloud Console → APIs & Services → Credentials")
            print("2. Найдите ваш OAuth 2.0 Client ID и нажмите на иконку редактирования")
            print("3. В разделе 'Authorized redirect URIs' добавьте:")
            print("   - http://localhost:8080/")
            print("   - http://localhost:8080")
            print("   - http://localhost/")
            print("   - http://127.0.0.1:8080/")
            print("   - http://127.0.0.1:8080")
            print("   - http://127.0.0.1/")
            print("4. Нажмите 'Save' и попробуйте снова")
            print("\n📖 Подробная инструкция: см. GOOGLE_SETUP.md (Шаг 4.5)")
        else:
            print(f"\n❌ Ошибка: {e}")
            print("Проверьте, что credentials.json правильный и все зависимости установлены.")
        sys.exit(1)
    
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


