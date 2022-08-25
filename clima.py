import apis_key
import requests

api_key_clima = apis_key.api_key_clima

# api_key_clima = os.environ['KEY_BOT_HEROKU']


cidade = 'brasilia'
cidade = cidade.lower()




def clima(cidade):
    requisicao = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key_clima}&lang=pt_br')  # 200 = Válida / 404  = Inválida

    if requisicao != 200:
        bot.send_message(message.chat.id, f'Desculpa, não encontrei a cidade: {cidade}, desisto!')

    else:
        requisicao_dic = requisicao.json()
        # print(requisicao_dic_atual)

        temperatura = requisicao_dic['main']['temp'] - 273.15
        descricao = requisicao_dic['weather'][0]['description']
        sensacaotermica = requisicao_dic['main']['feels_like'] - 273.15

        bot.send_message(message.chat.id, f'O tempo em {cidade.capitalize()}:')
        bot.send_message(message.chat.id, f'Temperatura: {temperatura:.2f}°C')
        bot.send_message(message.chat.id, f'Céu: {descricao.capitalize()}')
        bot.send_message(message.chat.id, f'Sensação térmica de: {sensacaotermica:.2f}°C')




