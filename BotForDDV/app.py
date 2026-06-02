from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv() # Загружает переменные из файла .env

app = Flask(__name__)
CORS(app)

# ЗАМЕНИТЕ НА СВОИ ДАННЫЕ
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return None


@app.route('/send', methods=['POST'])
def handle_form():
    data = request.get_json()

    name = data.get('name', 'Не указано')
    phone = data.get('phone', 'Не указано')
    work_type = data.get('work_type', 'Не указано')
    address = data.get('address', 'Не указано')
    comment = data.get('comment', 'Нет комментария')

    message = f"""🔔 <b>Новая заявка с сайта!</b>

👤 <b>Имя:</b> {name}
📞 <b>Телефон:</b> {phone}
🔧 <b>Вид работы:</b> {work_type}
📍 <b>Адрес:</b> {address}
📝 <b>Комментарий:</b> {comment}"""

    result = send_telegram_message(message)

    if result and result.get('ok'):
        return jsonify({"success": True, "message": "Заявка отправлена!"})
    else:
        return jsonify({"success": False, "message": "Ошибка отправки"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)