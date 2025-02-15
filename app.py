from flask import Flask, request, jsonify
from gigachat import GigaChat
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)

# Получаем токен из переменных окружения
GIGACHAT_TOKEN = os.getenv('GIGACHAT_TOKEN')

giga = GigaChat(credentials=GIGACHAT_TOKEN, verify_ssl_certs=False)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        response = giga.chat(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7,
            max_tokens=2000
        )
        return jsonify({
            'response': response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
