import telebot as tb
import logging
from datetime import datetime
import pytz
import os
import json
from google_currency import convert
import requests
import pandas as pd
import apis_key



# Keys
# api_key_bot = os.environ['KEY_BOT_HEROKU']
# api_key_clima = os.environ['KEY_CLIMA_HEROKU']
# api_key_clima = apis_key.api_key_clima
# api_key_bot = apis_key.api_bot
api_key_bot = os.environ['KEY_BOT_RENDER']
api_key_clima = os.environ['KEY_CLIMA_RENDER']

# Bot
bot = tb.TeleBot(api_key_bot)  # Heroku Config Vars

logger = tb.logger
tb.logger.setLevel(logging.DEBUG)  # Outputs messages to console INFO / DEBUG / NOTSET / WARNING / ERROR / CRITICAL


# Bem-vindo(a)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Bem-vindo(a) {message.from_user.username}!")
    ad_text = """
    Esta é uma demonstração de um bot no Telegram para ser inserido no meu LinkedIn e Github:
    [LinkedIn](www.linkedin.com/in/antxara/)
    [GitHub](https://github.com/Antxj) 
        """
    bot.send_message(message.chat.id, text=ad_text, parse_mode="markDown", disable_web_page_preview=True)

    with open('usersinfo/users_start.csv', 'a') as csv:
        texto = f'{message.from_user.id},{message.from_user.first_name}, {message.from_user.username}\n'
        csv.write(texto)
        users_start_data = pd.read_csv('usersinfo/users_start.csv')
        print(users_start_data.head())


# Recebendo arquivos e etc...
@bot.message_handler(content_types=["audio", "sticker", "document", "photo", "video", "location", "contact", "video_note"])
def content_types(message):
    bot.send_message(message.chat.id, 'Pô to meio cansado...manda texto aí.')


# Cotação do dólar
@bot.message_handler(regexp="dolar|dólar|usd")
def currency2(message):
    currency_dic = json.loads(convert('usd', 'brl', 1))  # json to dic
    resultado_currency = currency_dic['amount'].replace(".", ",")
    bot.send_message(message.chat.id, f'Cotação atual do dólar:\nR${resultado_currency}')


# Informações
@bot.message_handler(regexp="infos|info")
def userinfo(message):
    bot.send_message(message.chat.id, f"Seu nome no telegram é: {message.from_user.first_name}")
    bot.send_message(message.chat.id, f"Seu usuário no telegram é: {message.from_user.username}")
    bot.send_message(message.chat.id, f"Está é uma conversa do tipo: {message.chat.type}")
    bot.send_message(message.chat.id, f"Seu chatID é:\n{message.chat.id}")
    bot.send_message(message.chat.id, f"Seu ID é:\n{message.from_user.id}")


# Data hoje
@bot.message_handler(regexp="data|hoje|hj")
def hoje(message):
    tz = pytz.timezone('America/Sao_Paulo')
    brasil_hoje = datetime.now(tz).strftime("%d/%m/%Y")
    bot.send_message(message.chat.id, f'Hoje é dia:\n{brasil_hoje}')


# Hora atual
@bot.message_handler(regexp="hora|agora|horário|now|horario")
def agora(message):
    tz = pytz.timezone('America/Sao_Paulo')
    brasil_now = datetime.now(tz).strftime("%Hh%Mm")
    bot.send_message(message.chat.id, f'Agora são:\n{brasil_now}')


# Clima
@bot.message_handler(commands=['clima'])
def handle_clima(message):
    msgclima = bot.send_message(message.chat.id, 'Quer saber o clima de qual cidade?')
    bot.register_next_step_handler(msgclima, step_Set_Clima)


def step_Set_Clima(message):
    cidade = message.text
    requisition = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key_clima}&lang=pt_br')  # 200 = Válida / 404  = Inválida

    if requisition.status_code != 200:
        cidade = cidade.capitalize()
        bot.send_message(message.chat.id, f'Desculpa, não encontrei a cidade: {cidade}, tente novamente:\n/clima')

    else:
        requisicao_dic = requisition.json()
        temperatura = requisicao_dic['main']['temp'] - 273.15
        descricao = requisicao_dic['weather'][0]['description']
        sensacaotermica = requisicao_dic['main']['feels_like'] - 273.15
        resposta_clima = f'''O clima em {cidade.capitalize()}:\n
Temperatura: {temperatura:.2f}°C
Céu: {descricao.capitalize()}
Sensação térmica de: {sensacaotermica:.2f}°C'''
        bot.send_message(message.chat.id, resposta_clima)


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
    bot.send_message(message.chat.id, 'Impressionante né?\nSe quiser ver todas, acesse:\n'
                                      'https://webbtelescope.org/resource-gallery/images')


# Ideia ao criador
@bot.message_handler(commands=["ideia"])
def handle_deia(message):
    msgideia = bot.send_message(message.chat.id, 'Qual sua a ideia?')
    bot.register_next_step_handler(msgideia, step_Set_Ideia)


def step_Set_Ideia(message):
    ideiatexto = message.text
    id_criador = 1317880277  # Meu ID.
    bot.send_message(id_criador, f'Ideia enviada pelo {message.from_user.username} ({message.from_user.first_name}), '
                                 f'ID: {message.from_user.id}:\n{ideiatexto}')
    bot.send_message(message.chat.id, 'Obrigado, sua ideia foi enviada ao criador, espero que ele goste!')
    with open('usersinfo/users_ideias.csv', 'a') as csv:
        texto = f'{message.from_user.id},{message.from_user.first_name}, {message.from_user.username}, {ideiatexto}\n'
        csv.write(texto)
        users_ideias_data = pd.read_csv('usersinfo/users_ideias.csv')
        print(users_ideias_data.head())


# Enviar mensagem
@bot.message_handler(commands=["privado"])
def sendrivado(message):
    id_destino = message.chat.id
    bot.send_message(id_destino, "Oi! Eu sou um bot!")


# Criador, eu :)
@bot.message_handler(commands=['criador'])
def send_criador(message):
    add_text = """Meu primeiro 'Hello World!' foi graças a este indivíduo:    
[LinkedIn](www.linkedin.com/in/antxara/)
[GitHub](https://github.com/Antxj) 
Obrigado!
        """
    bot.send_message(message.chat.id, text=add_text, parse_mode="markDown", disable_web_page_preview=True)


# Menu padrão se não bater com nada
def verificar(message):
    return True


@bot.message_handler(func=verificar)
def responder(message):
    texto = f'''

Interagindo por comandos, clique:

/clima - Confira o clima em uma cidade.
/fotos - Receber fotos do Telescópio Espacial James Webb.
/docs - Receber um documento.
/audio - Receber um áudio. 
/video - Receber um vídeo. 
/privado - Receber uma mensagem do bot.
/criador - Criador do bot.
/ideia - Enviar uma ideia ao criador do bot.


Interagindo por palavras, envie por exemplo:

-Cotação do dólar:
dólar, usd, dolar.

-Hora atual:
hora, agora, horário, horario.

-Data atual:
data, hoje, hj.

-Informações do usuário no Telegram:
info, infos.
'''
    bot.send_message(message.chat.id, texto)


# Sempre aguardando interação
bot.infinity_polling()

# bot.send_message(1317880277, 'Hi! I\'m a Bot!')
# bot5727655671
