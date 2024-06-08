
# coins/tasks.py
from celery import shared_task
from .coinmarketcap import CoinMarketCap

@shared_task
def get_crypto_data(coin_acronyms):
    cmc = CoinMarketCap()
    return cmc.get_crypto_data(coin_acronyms)
