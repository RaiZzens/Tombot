import os
import openai
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters

# Tokens
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Füge deinen OpenAI API-Schlüssel in Render hinzu

# Überprüfen, ob die Tokens geladen wurden
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN ist nicht gesetzt. Bitte füge es als Umgebungsvariable hinzu.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY ist nicht gesetzt. Bitte füge es als Umgebungsvariable hinzu.")

openai.api_key = OPENAI_API_KEY

# Funktion für den /start-Befehl
async def start(update: Update, context):
    await update.message.reply_text("Hallo! Ich bin ein KI-gestützter Bot. Frag mich alles, was du möchtest!")

# Funktion für die Nachrichtenantwort mit GPT
async def antwort(update: Update, context):
    user_message = update.message.text.strip()  # Entfernt unnötige Leerzeichen
    await update.message.reply_text("Einen Moment, ich denke nach ...")

    try:
        # Anfrage an die OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Oder gpt-4, falls du es nutzen möchtest
            messages=[
                {"role": "system", "content": "Du bist ein freundlicher und hilfreicher Chatbot."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,  # Begrenze die Antwortlänge
            temperature=0.7  # Kreativitätslevel
        )
        bot_reply = response['choices'][0]['message']['content'].strip()
        await update.message.reply_text(bot_reply)
    except openai.error.OpenAIError as e:  # Spezifische Fehler von OpenAI abfangen
        await update.message.reply_text("Entschuldigung, es gab ein Problem mit der KI-Anfrage. Versuche es später erneut.")
        print(f"OpenAI Fehler: {e}")
    except Exception as e:  # Allgemeine Fehler abfangen
        await update.message.reply_text("Entschuldigung, es gab einen unerwarteten Fehler. 😢")
        print(f"Allgemeiner Fehler: {e}")

# Application und Dispatcher einrichten
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Befehle und Nachrichtenhandler hinzufügen
application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, antwort))

# Bot starten
if __name__ == "__main__":
    print("Bot wird gestartet...")
    application.run_polling()

