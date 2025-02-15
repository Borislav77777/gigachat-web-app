# GigaChat Web Application

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-username/gigachat-web-app.git
cd gigachat-web-app
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env и добавьте ваш токен:
```
GIGACHAT_TOKEN=ваш_токен_здесь
```

5. Запустите приложение:
```bash
python app.py
```
