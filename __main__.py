import os
import telebot

# Код полностью чист! Бот возьмет токен из скрытой памяти Google
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(
        message.chat.id,
        "🎮 **Добро пожаловать в магазин TonPures!**\n\n"
        "Здесь вы можете приобрести Telegram Stars, Premium подписку и proxy! 💎\n\n"
        "👇 Нажмите кнопку **МАГАЗИН** в левом нижнем углу экрана!",
        parse_mode='Markdown'
    )

if __name__ == "__main__":
    bot.infinity_polling()
