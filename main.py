import telebot as tb
import logging
from datetime import datetime
import os

import currency


KEY_BOT_HEROKU = os.environ['KEY_BOT_HEROKU']

# Bot
bot = tb.TeleBot(KEY_BOT_HEROKU)  # Heroku Config Vars

# bot = tb.TeleBot(api_bot.api_bot)  # Pycharm local
# import api_bot

logger = tb.logger
tb.logger.setLevel(logging.DEBUG)  # Outputs messages to console INFO / DEBUG / NOTSET / WARNING / ERROR / CRITICAL


# Por escrita
@bot.message_handler(regexp="dolar")
def currency2(message):
    bot.send_message(message.chat.id, f'Cotação atual do dólar: {currency.currency("usd", "brl")}.')


@bot.message_handler(regexp="infos")
def userinfo(message):
    bot.send_message(message.chat.id, f"Seu nome no telegram é: {message.from_user.first_name}.")
    bot.send_message(message.chat.id, f"Seu usuário no telegram é: {message.from_user.username}.")


@bot.message_handler(regexp="data")
def hora_data(message):
    hoje = datetime.now().strftime("Hoje é dia: %d/%m/%Y.")
    bot.send_message(message.chat.id, f'{hoje}')


@bot.message_handler(regexp="hora")
def agorahora(message):
    agorahora = datetime.now().strftime("Agora são: %Hh%Mm.")
    bot.send_message(message.chat.id, f'{agorahora}')


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
