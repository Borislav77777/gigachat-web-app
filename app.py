from flask import Flask, request, jsonify, render_template
from gigachat import GigaChat
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='templates')

GIGACHAT_TOKEN = os.getenv('GIGACHAT_TOKEN')

@app.route('/')
def home():
    return render_template('index.html', token=GIGACHAT_TOKEN)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
