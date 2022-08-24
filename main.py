import telebot as tb
import logging
from datetime import datetime
import pytz
import os
import json
from google_currency import convert

# Bot
api_key_bot = os.environ['KEY_BOT_HEROKU']
bot = tb.TeleBot(api_key_bot)  # Heroku Config Vars

logger = tb.logger
tb.logger.setLevel(logging.DEBUG)  # Outputs messages to console INFO / DEBUG / NOTSET / WARNING / ERROR / CRITICAL


# Recebendo diferente de texto e comando
@bot.message_handler(content_types=["audio", "sticker", "document", "photo", "video", "location", "contact", "video_note"])
def content_types(message):
    bot.reply_to(message.chat.id, 'Pô to meio cansado...manda texto.')


# Cotação do dólar
@bot.message_handler(regexp="dolar")
def currency2(message):
    currency_dic = json.loads(convert('usd', 'brl', 1))  # json to dic
    resultado_currency = currency_dic['amount'].replace(".", ",")
    bot.send_message(message.chat.id, f'Cotação atual do dólar:\nR${resultado_currency}')


@bot.message_handler(regexp="infos")
def userinfo(message):
    bot.send_message(message.chat.id, f"Seu nome no telegram é: {message.from_user.first_name}.\n")
    bot.send_message(message.chat.id, f"Seu usuário no telegram é: {message.from_user.username}.")
    bot.send_message(message.chat.id, f"Está é uma conversa: {message.chat.type}.")


@bot.message_handler(regexp="data")
def hoje(message):
    tz = pytz.timezone('America/Sao_Paulo')
    brasil_hoje = datetime.now(tz).strftime("%d/%m/%Y")
    bot.send_message(message.chat.id, f'Hoje é dia:\n{brasil_hoje}')


@bot.message_handler(regexp="hora")
def agora(message):
    tz = pytz.timezone('America/Sao_Paulo')
    brasil_now = datetime.now(tz).strftime("%Hh%Mm")
    bot.send_message(message.chat.id, f'Agora são:\n{brasil_now}')


# Comandos
@bot.message_handler(commands=["docs"])
def docs(message):
    bot.send_message(message.chat.id, 'Segue a papelada...')
    # sendDocument
    pdf_file = open('media/arquivopdf.pdf', 'rb')
    bot.send_document(message.chat.id, pdf_file)
    docx_file = open('media/demo.docx', 'rb')
    bot.send_document(message.chat.id, docx_file)


@bot.message_handler(commands=["audio"])
def audio(message):
    # sendAudio
    bot.send_message(message.chat.id, 'Enviando como Áudio:')
    audio_file = open('media/audiofile.mp3', 'rb')
    bot.send_audio(message.chat.id, audio_file)
    # sendVoice
    bot.send_message(message.chat.id, 'Enviando como Voz:')
    voice_file = open('media/voicesample.ogg', 'rb')
    bot.send_voice(message.chat.id, voice_file)


@bot.message_handler(commands=["fotos"])
def fotos(message):
    # sendPhoto
    foto_file = open('media/foto1.png', 'rb')
    foto_file2 = open('media/foto2.png', 'rb')
    foto_file3 = open('media/foto3.png', 'rb')
    bot.send_photo(message.chat.id, foto_file)
    bot.send_photo(message.chat.id, foto_file2)
    bot.send_photo(message.chat.id, foto_file3)
    bot.send_message(message.chat.id, 'Impressionante né?')
    bot.send_message(message.chat.id, 'Se quiser ver todas, acesse: https://webbtelescope.org/resource-gallery/images')


# Menu padrão se não bater com nada
def verificar(message):
    return True


@bot.message_handler(func=verificar)
def responder(message):
    texto = '''
    Olá,
    
Esta é uma demonstração simples de um bot no Telegram:

Interagindo por comandos, clique:

/docs - Receber os documentos.
/audio - Recebe um áudio. 
/fotos - Receber fotos do Telescópio Espacial James Webb.
    
Interagindo por palavras, envie por exemplo:

hora
data
dolar
infos
      '''
    bot.send_message(message.chat.id, texto)


# Sempre aguardando interação
bot.infinity_polling()
