from bs4 import BeautifulSoup
import logging
import requests


# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

url = f"https://api.coindesk.com/v1/bpi/currentprice.json"
headers = {
    "Content-Type": "application/json",
}


def get_data():
    """
    Sends a request to the Coindesk API to get bitcoin price
    compared to the USD value.

    Returns:
        price (float): Bitcoin price in comparison to USD price.
        currency (str): Currency that is being compared to.
    """
    try:
        response = requests.get(url, headers=headers)
        response = response.json()
        currency = response["bpi"]["USD"]["code"]
        price = response["bpi"]["USD"]["rate_float"]
        return price, currency
    except Exception as e:
        logger.error(
            f"Ocorreu um erro para a extração da informação: {e}", exc_info=True
        )
        return None, None
