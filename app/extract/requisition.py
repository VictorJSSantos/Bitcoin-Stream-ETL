from bs4 import BeautifulSoup
import logging
import requests


# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

coin = "bitcoin"
url = f"https://www.google.com/search?q={coin}+price"


def get_data():
    """
    Envia um registro para um Delivery Stream do Kinesis Firehose.


    :param delivery_stream_name (str): O nome do Delivery Stream.
    :param records (dict): O dado a ser enviado como um JSON.

    Returns:
        price (float): Valor do Bitcoin cotado no momento
        currency (str): Moeda base para comparação monetária
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Lendo o soup temos essa parte a seguir de interessante para o nosso web scrapper:
        # <div><div><div><div class="BNeawe iBp4i AP7Wnd"><div><div class="BNeawe iBp4i AP7Wnd">552.390,72 Real brasileiro</div></div></div></div></div>
        infos = (
            soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"})
            .find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"})
            .text
        ).split(" ")
        price = infos[0]
        currency = infos[1]
        price = float(price.replace(".", "").replace(",", "."))
        return price, currency
    except Exception as e:
        logger.error(
            f"Ocorreu um erro para a extração da informação: {e}", exc_info=True
        )
        return None, None
