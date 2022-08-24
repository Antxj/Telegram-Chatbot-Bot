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


# Bem-vindo(a)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Bem-vindo(a) {message.from_user.username}!")


# Recebendo arquivos e etc
@bot.message_handler(content_types=["audio", "sticker", "document", "photo", "video", "location", "contact", "video_note"])
def content_types(message):
    bot.send_message(message.chat.id, 'Pô to meio cansado...manda texto aí.')


# Informações
@bot.message_handler(regexp="infos|info")
def userinfo(message):
    bot.send_message(message.chat.id, f"Seu nome no telegram é: {message.from_user.first_name}")
    bot.send_message(message.chat.id, f"Seu usuário no telegram é: {message.from_user.username}")
    bot.send_message(message.chat.id, f"Está é uma conversa do tipo: {message.chat.type}")
    bot.send_message(message.chat.id, f"Seu ID é:\n{message.chat.id}")


# Data hoje
@bot.message_handler(regexp="data|hoje")
def hoje(message):
    tz = pytz.timezone('America/Sao_Paulo')
    brasil_hoje = datetime.now(tz).strftime("%d/%m/%Y")
    bot.send_message(message.chat.id, f'Hoje é dia:\n{brasil_hoje}')


# Hora atual
@bot.message_handler(regexp="hora|agora")
def agora(message):
    tz = pytz.timezone('America/Sao_Paulo')
    brasil_now = datetime.now(tz).strftime("%Hh%Mm")
    bot.send_message(message.chat.id, f'Agora são:\n{brasil_now}')


# Vídeo
@bot.message_handler(commands=["video"])
def videos(message):
    # sendVideo
    video = open('media/videosample.mp4', 'rb')
    bot.send_video(message.chat.id, video)


# Documentos
@bot.message_handler(commands=["docs"])
def docs(message):
    bot.send_message(message.chat.id, 'Segue a papelada...')
    # sendDocument
    pdf_file = open('media/arquivopdf.pdf', 'rb')
    bot.send_document(message.chat.id, pdf_file)
    docx_file = open('media/demo.docx', 'rb')
    bot.send_document(message.chat.id, docx_file)


# Áudio
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


# Fotos
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


# Cotação do dólar
@bot.message_handler(commands=["dolar"])
def currency2(message):
    currency_dic = json.loads(convert('usd', 'brl', 1))  # json to dic
    resultado_currency = currency_dic['amount'].replace(".", ",")
    bot.send_message(message.chat.id, f'Cotação atual do dólar:\nR${resultado_currency}')


# Menu padrão se não bater com nada
def verificar(message):
    return True


@bot.message_handler(func=verificar)
def responder(message):
    texto = rf'''
    Olá,
    
Esta é uma demonstração simples de um bot no Telegram:

Interagindo por comandos, clique:

/fotos - Receber fotos do Telescópio Espacial James Webb.
/docs - Receber um documento.
/audio - Receber um áudio. 
/video - Receber um vídeo. 
/dolar - Ver a cotação do dólar.\
/Família - Testando, aguarde...

Interagindo por palavras, envie por exemplo:

Hora
Data
Info
Agora

      '''
    bot.send_message(message.chat.id, texto)


# Sempre aguardando interação
bot.infinity_polling()
