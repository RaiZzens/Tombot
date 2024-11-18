import os
import openai
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters

# Tokens
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Füge deinen OpenAI API-Schlüssel in Render hinzu
openai.api_key = OPENAI_API_KEY

# Funktion für den /start-Befehl
async def start(update: Update, context):
    await update.message.reply_text("Hallo! Ich bin ein KI-gestützter Bot. Frag mich alles, was du möchtest!")

# Funktion für die Nachrichtenantwort mit GPT
async def antwort(update: Update, context):
    user_message = update.message.text
    await update.message.reply_text("Einen Moment, ich denke nach ...")

    # Anfrage an die OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Oder gpt-4, wenn verfügbar
            messages=[
                {"role": "system", "content": "Du bist ein freundlicher und hilfreicher Chatbot."},
                {"role": "user", "content": user_message}
            ],
        )
        bot_reply = response['choices'][0]['message']['content']
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text("Entschuldigung, ich konnte deine Nachricht nicht verarbeiten. 😢")
        print(f"Fehler: {e}")

# Application und Dispatcher einrichten
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Befehle und Nachrichtenhandler hinzufügen
application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, antwort))

# Bot starten
application.run_polling()
