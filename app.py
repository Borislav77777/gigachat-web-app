from flask import Flask, request, jsonify, render_template
from gigachat import GigaChat
import uuid
import base64
import requests
import os

app = Flask(__name__)

# Данные для авторизации
CLIENT_ID = "13fae9d7-4cfe-4ab2-be7a-8669606e529e"
CLIENT_SECRET = "74c4d938-4d89-417d-a383-5f0aa781a9e2"

def get_token():
    # Создаем ключ авторизации
    auth_data = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_key = base64.b64encode(auth_data.encode()).decode()
    
    # Генерируем UUID для запроса
    request_id = str(uuid.uuid4())
    
    # Запрос на получение токена
    response = requests.post(
        'https://ngw.devices.sberbank.ru:9443/api/v2/oauth',
        headers={
            'RqUID': request_id,
            'Authorization': f'Basic {auth_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'scope': 'GIGACHAT_API_PERS'
        },
        verify=False
    )
    
    return response.json()['access_token']

def get_gigachat():
    token = get_token()
    return GigaChat(credentials=token, verify_ssl_certs=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        # Получаем новый экземпляр GigaChat с актуальным токеном
        giga = get_gigachat()
        
        # Отправляем запрос
        response = giga.chat([{
            "role": "user",
            "content": user_message
        }])
        
        return jsonify({
            'response': response.choices[0].message.content
        })
    except Exception as e:
        print(f"Ошибка: {str(e)}")  # Для отладки
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)