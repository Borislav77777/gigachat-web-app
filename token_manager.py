import uuid
import requests
import base64
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self):
        # Ваши учетные данные
        self.client_id = "13fae9d7-4cfe-4ab2-be7a-8669606e529e"
        self.client_secret = "74c4d938-4d89-417d-a383-5f0aa781a9e2"  # Получите на developers.sber.ru
        self.token = None
        self.token_expires = None

    def get_token(self):
        # Проверяем, нужно ли обновить токен
        if self._is_token_expired():
            self._refresh_token()
        return self.token

    def _is_token_expired(self):
        if not self.token or not self.token_expires:
            return True
        # Обновляем токен за 1 минуту до истечения
        return datetime.now() >= self.token_expires - timedelta(minutes=1)

    def _refresh_token(self):
        try:
            # Создаем ключ авторизации
            auth_data = f"{self.client_id}:{self.client_secret}"
            auth_key = base64.b64encode(auth_data.encode()).decode()

            # Генерируем UUID для запроса
            request_id = str(uuid.uuid4())

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
                verify=False  # Только для тестирования!
            )

            data = response.json()
            self.token = data['access_token']
            # Устанавливаем время истечения токена (30 минут)
            self.token_expires = datetime.now() + timedelta(minutes=30)

        except Exception as e:
            print(f"Ошибка получения токена: {str(e)}")
            raise