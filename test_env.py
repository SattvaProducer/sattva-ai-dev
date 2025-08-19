from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

# Проверяем каждую переменную отдельно
api_key = os.getenv('DEEPSEEK_API_KEY')
app_secret = os.getenv('APP_SECRET')

print('API ключ:', repr(api_key))  # repr покажет точное значение
print('Секрет:', repr(app_secret))

# Альтернативный способ проверки
print('\nПроверка через os.environ:')
print('API ключ:', repr(os.environ.get('DEEPSEEK_API_KEY')))
print('Секрет:', repr(os.environ.get('APP_SECRET')))
