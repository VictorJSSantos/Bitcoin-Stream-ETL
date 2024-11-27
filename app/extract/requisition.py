import requests
from bs4 import BeautifulSoup


coin = "bitcoin"
url = f"https://www.google.com/search?q={coin}+price"


def get_data():
    """
    Envia um registro para um Delivery Stream do Kinesis Firehose.

    Args:
        delivery_stream_name (str): O nome do Delivery Stream.
        records (dict): O dado a ser enviado como um JSON.

    Returns:
        price (float), currency (str)
        price: Valor do Bitcoin cotado no momento
        currency: Moeda base para comparação monetária
    """
    try:
        response = requests.get(url)
    except:
        print(f"A chamada para requisição deu erro!")
        return None, None

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

    print(f"O preço é: {price}, e a moeda é:  {currency}")

    return price, currency
