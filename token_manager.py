import uuid
import requests
import base64
import warnings
import json
from urllib3.exceptions import InsecureRequestWarning

# Отключаем предупреждение о небезопасном соединении
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

# Ваши учетные данные
client_id = "13fae9d7-4cfe-4ab2-be7a-8669606e529e"
client_secret = "74c4d938-4d89-417d-a383-5f0aa781a9e2"

try:
    # Создаем ключ авторизации
    auth_data = f"{client_id}:{client_secret}"
    auth_key = base64.b64encode(auth_data.encode()).decode()

    # Генерируем UUID
    request_id = str(uuid.uuid4())

    # Отправляем запрос на получение токена
    response = requests.post(
        'https://ngw.devices.sberbank.ru:9443/api/v2/oauth',
        headers={
            'RqUID': request_id,
            'Authorization': f'Basic {auth_key}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        },
        data={
            'scope': 'GIGACHAT_API_PERS'
        },
        verify=False
    )
    
    # Выводим статус и ответ для отладки
    print(f"Статус ответа: {response.status_code}")
    print(f"Ответ сервера: {response.text}")
    
    # Проверяем успешность запроса
    response.raise_for_status()
    
    # Получаем токен
    data = response.json()
    if 'access_token' in data:
        token = data['access_token']
        print(f"\nПолученный токен:\n{token}")
        
        # Сохраняем токен в .env файл
        with open('.env', 'w') as f:
            f.write(f"GIGACHAT_TOKEN={token}")
    else:
        print(f"Ошибка: токен не найден в ответе")
        print(f"Содержимое ответа: {data}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {str(e)}")
except json.JSONDecodeError as e:
    print(f"Ошибка парсинга JSON: {str(e)}")
    print(f"Текст ответа: {response.text}")
except Exception as e:
    print(f"Неожиданная ошибка: {str(e)}")