import openai
import telebot
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

# Inicia o servidor Flask para manter o serviço vivo no Render
keep_alive()

# Carrega as variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

@bot.message_handler(func=lambda message: True)
def responder_com_ia(message):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4o",
            max_tokens=300,
            temperature=0.5,
            messages=[
                {"role": "system", "content": "Você é um tutor de matemática para estudantes de Ciências Econômicas. Responda com explicações claras e objetivas."},
                {"role": "user", "content": message.text}
            ]
        )
        texto_resposta = resposta['choices'][0]['message']['content']
        bot.reply_to(message, texto_resposta)
    except Exception as e:
        bot.reply_to(message, f"Erro: {e}")

print("Bot rodando no Render.")
bot.polling()
