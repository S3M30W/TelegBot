import json
import requests
from config import keys


class APIException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не смог обработать валюту {quote}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не смог обработать валюту {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не смог обработать количество валюты {amount}!')

        if int(amount) < 0:
            raise APIException('Колличество валюты не может быть ниже нуля!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount
