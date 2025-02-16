import uuid
import requests
import base64

# Ваши данные от API GigaChat (получите на developers.sber.ru)
client_id = "ваш_client_id"        # Замените на ваш ID
client_secret = "ваш_client_secret"  # Замените на ваш Secret

# Создаем ключ авторизации
auth_data = f"{client_id}:{client_secret}"
auth_key = base64.b64encode(auth_data.encode()).decode()

# Генерируем UUID
request_id = str(uuid.uuid4())

try:
    # Отправляем запрос на получение токена
    response = requests.post(
        'https://ngw.devices.sberbank.ru:9443/api/v2/oauth',
        headers={
            'RqUID': request_id,
            'Authorization': f'Basic {auth_key}'
        },
        data={
            'scope': 'GIGACHAT_API_PERS'
        },
        verify=False  # Только для тестирования
    )
    
    # Получаем токен
    token = response.json()['access_token']
    print(f"Ваш токен:\n{token}")
    
    # Сохраняем токен в .env файл
    with open('.env', 'w') as f:
        f.write(f"GIGACHAT_TOKEN={token}")
    
except Exception as e:
    print(f"Ошибка: {str(e)}")