import telebot as tb
import logging
from datetime import datetime
import pytz
import json
from google_currency import convert
import requests


# Keys
import os
api_key_bot = os.environ['KEY_BOT']  # Heroku Config Vars
api_key_clima = os.environ['KEY_CLIMA']  # Heroku Config Vars

# import apis_key
# api_key_clima = apis_key.api_key_clima
# api_key_bot = apis_key.api_bot

# Bot
bot = tb.TeleBot(api_key_bot)
logger = tb.logger
tb.logger.setLevel(logging.INFO)  # Outputs messages to console INFO / DEBUG / NOTSET / WARNING / ERROR / CRITICAL


# Salvar membros
class Cliente:
    def __init__(self, user_id, user_firstname, user_username):
        self.user_id = user_id
        self.user_firstname = user_firstname
        self.user_username = user_username

    def salvar_cliente_start(self):
        membros_data = {
        "UserID": self.user_id,
        "FirstName": self.user_firstname,
        "Username": self.user_username
        }
        with open("usersinfo/users_start.json", "a", encoding='utf-8') as arquivo:
            json.dump(membros_data, arquivo, ensure_ascii=False)
            arquivo.write(',\n')

    def salvar_cliente_ideia(self, ideiatexto):
        membros_data = {
        "UserID": self.user_id,
        "FirstName": self.user_firstname,
        "Username": self.user_username,
        "Ideia": ideiatexto
        }
        with open("usersinfo/users_ideias.json", "a", encoding='utf-8') as arquivo:
            json.dump(membros_data, arquivo, ensure_ascii=False)
            arquivo.write(',\n')


# Bem-vindo(a)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Bem-vindo(a) {message.from_user.first_name}!")
    ad_text = """
Esta é uma demonstração de um bot no Telegram para ser inserido no meu LinkedIn e Github:
[LinkedIn](www.linkedin.com/in/antxara/)
[GitHub](https://github.com/Antxj)

Clique em /menu para ver as opções!
"""
    bot.send_message(message.chat.id, text=ad_text, parse_mode="markDown", disable_web_page_preview=True)

    cliente = Cliente(message.from_user.id, message.from_user.first_name, message.from_user.username)
    cliente.salvar_cliente_start()


# Recebendo arquivos e etc...
@bot.message_handler(content_types=["audio", "sticker", "document",
                                    "photo", "video", "location", "contact", "video_note"])
def content_types(message):
    bot.send_message(message.chat.id, 'Ainda não consigo entender esse tipo de coisa...manda um /menu.')


# Cotação do dólar
@bot.message_handler(commands=['dolar'])
def currency2(message):
    currency_dic = json.loads(convert('usd', 'brl', 1))  # json to dic
    print(currency_dic)
    resultado_currency = currency_dic['amount'].replace(".", ",")
    print(resultado_currency)
    bot.send_message(message.chat.id, f'Cotação atual do dólar:\nR${resultado_currency}')


# CEP
@bot.message_handler(commands=['cep'])
def handle_cep(message):
    msgcep = bot.send_message(message.chat.id, 'Qual o CEP?')
    bot.register_next_step_handler(msgcep, step_set_cep)


def step_set_cep(message):  # https://viacep.com.br/
    cep_indicado = message.text
    cep_indicado = cep_indicado.replace('.', '').replace('-', '').replace(' ', '')
    link = f'https://viacep.com.br/ws/{cep_indicado}/json/'
    erro = 'erro'

    if len(cep_indicado) == 8 and cep_indicado.isnumeric():
        requisicao = requests.get(link)
        dict_requisicao = requisicao.json()
        if erro in dict_requisicao:
            print(f"Yes, key: '{erro}' exists in dictionary")
            bot.send_message(message.chat.id, 'CEP não encontrado, tente novamente: /cep')
            raise KeyError('Error: CEP não existe.')
        else:
            pass
        cidade = dict_requisicao['localidade']
        uf = dict_requisicao['uf']
        logradouro = dict_requisicao['logradouro']
        bairro = dict_requisicao['bairro']
        cep = dict_requisicao['cep']
        complemento = dict_requisicao['complemento']
        resultado_cep = (f"""
Cidade: {cidade}
UF: {uf}
Logradouro: {logradouro}
Bairro: {bairro}
Complemento: {complemento}
CEP: {cep}
    """)
        bot.send_message(message.chat.id, resultado_cep)

    else:
        bot.send_message(message.chat.id, 'CEP inválido, tente novamente: /cep')




# Informações
@bot.message_handler(commands=['infos'])
def userinfo(message):
    bot.send_message(message.chat.id, f"""
Seu nome no telegram é: {message.from_user.first_name}.
Seu usuário no telegram é: {message.from_user.username}.
Está é uma conversa do tipo: {message.chat.type}.
Seu ID é: {message.from_user.id}.
""")


# Data hoje
@bot.message_handler(commands=['hoje'])
def hoje(message):
    tz = pytz.timezone('America/Sao_Paulo')
    brasil_hoje = datetime.now(tz).strftime("%d/%m/%Y")
    bot.send_message(message.chat.id, f'Hoje é dia:\n{brasil_hoje}')


# Hora atual
@bot.message_handler(commands=['hora'])
def agora(message):
    tz = pytz.timezone('America/Sao_Paulo')
    brasil_now = datetime.now(tz).strftime("%Hh%Mm")
    bot.send_message(message.chat.id, f'Agora são:\n{brasil_now}')


# Clima
@bot.message_handler(commands=['clima'])
def handle_clima(message):
    msgclima = bot.send_message(message.chat.id, 'Quer saber o clima de qual cidade?')
    bot.register_next_step_handler(msgclima, step_set_clima)


def step_set_clima(message):
    cidade = message.text
    requisition = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&'
        f'appid={api_key_clima}&lang=pt_br')  # 200 = Válida / 404  = Inválida

    if requisition.status_code != 200:
        cidade = cidade.capitalize()
        bot.send_message(message.chat.id, f'Desculpa, não encontrei a cidade "{cidade}", tente novamente:\n/clima')

    else:
        requisicao_dic = requisition.json()
        temperatura = requisicao_dic['main']['temp'] - 273.15
        descricao = requisicao_dic['weather'][0]['description']
        sensacaotermica = requisicao_dic['main']['feels_like'] - 273.15
        resposta_clima = f'''
O clima em {cidade.capitalize()}:\n
Temperatura: {temperatura:.2f}°C
Céu: {descricao.capitalize()}
Sensação térmica de: {sensacaotermica:.2f}°C
'''
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
    bot.register_next_step_handler(msgideia, step_set_ideia)


def step_set_ideia(message):
    ideiatexto = message.text
    id_criador = 1317880277  # Meu ID.
    bot.send_message(id_criador, f'Ideia enviada pelo {message.from_user.first_name} ({message.from_user.username}), '
                                 f'ID: {message.from_user.id}:\n{ideiatexto}')
    bot.send_message(message.chat.id, 'Obrigado, sua ideia foi enviada ao criador, espero que ele goste!')

    cliente = Cliente(message.from_user.id, message.from_user.first_name, message.from_user.username)
    cliente.salvar_cliente_ideia(ideiatexto)


# Enviar mensagem
@bot.message_handler(commands=["privado"])
def sendprivado(message):
    id_destino = message.chat.id
    bot.send_message(id_destino, "Oi! Eu sou um bot!")


# Criador, eu :)
@bot.message_handler(commands=['criador'])
def send_criador(message):
    add_text = """
Meu primeiro 'Hello World!' foi graças a este indivíduo:    
[LinkedIn](www.linkedin.com/in/antxara/)
[GitHub](https://github.com/Antxj) 
Obrigado!
        """
    bot.send_message(message.chat.id, text=add_text, parse_mode="markDown", disable_web_page_preview=True)


# Menu
@bot.message_handler(commands=["menu"])
def menu(message):
    texto_menu = f'''

    Clique na opção desejada:

    /dolar - Cotação do dólar
    /clima - Confira o clima em uma cidade.
    /cep - Descobrir endereço pelo CEP.

    /fotos - Receber fotos do Telescópio Espacial James Webb.
    /docs - Receber um documento.
    /audio - Receber um áudio. 
    /video - Receber um vídeo. 

    /hora - Hora atual.
    /hoje - Data de hoje.

    /infos - Informações do usuário no Telegram
    /privado - Receber uma mensagem do bot.
    /criador - Criador do bot.

    /ideia - Enviar uma ideia ao criador do bot.

    '''
    bot.send_message(message.chat.id, texto_menu)


# Mensagem padrão se não bater com nada.
def verificar(message):
    return True


@bot.message_handler(func=verificar)
def responder(message):
    texto_geral = f'''
Hmm.. não entendi.
Clique em ou envie /menu para ver as opções.
    '''
    bot.send_message(message.chat.id, texto_geral)


# Sempre aguardando interação
bot.infinity_polling()

# bot.send_message(1317880277, 'Hi! I\'m a Bot!')
# bot5727655671

