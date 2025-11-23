"""
Скрипт для проверки конфигурации перед запуском бота.
"""
import os
import sys

def check_env_file():
    """Проверяет наличие и содержимое .env файла."""
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("Создайте файл .env на основе .env.example")
        return False
    
    print("✅ Файл .env найден")
    return True

def check_env_variables():
    """Проверяет наличие всех необходимых переменных окружения."""
    required_vars = [
        'TELEGRAM_TOKEN',
        'OPENAI_API_KEY',
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET',
        'GOOGLE_REFRESH_TOKEN',
    ]
    
    # Загружаем переменные из .env файла
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
    
    missing_vars = []
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            missing_vars.append(var)
            print(f"❌ {var} не установлена")
        else:
            # Показываем только первые и последние символы для безопасности
            masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
            print(f"✅ {var} установлена ({masked})")
    
    if missing_vars:
        print(f"\n❌ Отсутствуют переменные: {', '.join(missing_vars)}")
        return False
    
    print("\n✅ Все необходимые переменные установлены")
    return True

def check_optional_vars():
    """Проверяет опциональные переменные."""
    tz = os.environ.get('TZ', 'Europe/Berlin')
    print(f"ℹ️  Часовой пояс: {tz}")

def check_imports():
    """Проверяет, что все необходимые библиотеки установлены."""
    required_modules = [
        'telegram',
        'openai',
        'googleapiclient',
        'google.auth',
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'telegram':
                import telegram
            elif module == 'openai':
                import openai
            elif module == 'googleapiclient':
                import googleapiclient
            elif module == 'google.auth':
                import google.auth
            print(f"✅ Модуль {module} установлен")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ Модуль {module} не установлен")
    
    if missing_modules:
        print(f"\n❌ Установите недостающие модули: pip install -r requirements.txt")
        return False
    
    return True

def main():
    print("=" * 60)
    print("Проверка конфигурации бота")
    print("=" * 60)
    print()
    
    all_ok = True
    
    print("1. Проверка файла .env...")
    if not check_env_file():
        all_ok = False
    print()
    
    print("2. Проверка переменных окружения...")
    if not check_env_variables():
        all_ok = False
    check_optional_vars()
    print()
    
    print("3. Проверка установленных модулей...")
    if not check_imports():
        all_ok = False
    print()
    
    print("=" * 60)
    if all_ok:
        print("✅ Все проверки пройдены! Можно запускать бота: python3 bot.py")
    else:
        print("❌ Есть проблемы с конфигурацией. Исправьте их перед запуском.")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())

