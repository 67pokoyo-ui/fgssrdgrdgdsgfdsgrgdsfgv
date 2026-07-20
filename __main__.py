import os
import telebot
from flask import Flask, request

# Код чист! Бот возьмет токен из скрытых настроек Vercel
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(
        message.chat.id,
        "🎮 **Добро пожаловать в магазин TonPures!**\n\n"
        "Здесь вы можете приобрести Telegram Stars, Premium подписку и proxy! 💎\n\n"
        "👇 Нажмите кнопку **МАГАЗИН** в левом нижнем углу экрана!",
        parse_mode='Markdown'
    )

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    # Сервер сам автоматически привяжет вебхук к твоему боту
    bot.set_webhook(url="https://" + os.getenv("VERCEL_URL") + "/" + BOT_TOKEN)
    return "Вечный двигатель TonPures запущен!", 200
