import os
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Bot-Token aus den Umgebungsvariablen holen
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Funktion für /start-Befehl
def start(update, context):
    update.message.reply_text('Hallo! Ich bin dein Telegram Bot.')

# Updater und Dispatcher einrichten
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Befehl /start hinzufügen
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Bot starten
updater.start_polling()
updater.idle()
