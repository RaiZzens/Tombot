import os
from telegram import Bot
from telegram.ext import Application, CommandHandler

# Bot-Token aus den Umgebungsvariablen holen
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Funktion für /start-Befehl
async def start(update, context):
    await update.message.reply_text('Hallo! Ich bin dein Telegram Bot.')

# Application und Dispatcher einrichten
application = Application.builder().token(TOKEN).build()

# Befehl /start hinzufügen
start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

# Bot starten
application.run_polling()
