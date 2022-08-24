import json
from google_currency import convert


def currency(moeda1, moeda2):
    currency_dic = json.loads(convert(f'{moeda1}', f'{moeda2}', 1))  # json to dic
    currency = currency_dic['amount'].replace(".", ",")
    # print(f'R${currency}')




