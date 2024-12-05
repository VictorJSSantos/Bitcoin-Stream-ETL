from datetime import datetime
import time


from load.FireHose_load import *
from extract.requisition import *

i = 0
while True:
    price, currency = get_data()
    hora = datetime.now()
    hora = hora.strftime("%Y-%m-%d %H:%M:%S")
    delivery_stream_name = "PUT-S3-btc-etl-2"
    # print(price, currency, hora)
    records = {"price": price, "currency": currency, "time": hora}
    # Envia o dado para o Firehose
    response = put_record_to_firehose(delivery_stream_name, records)
    # print(response)
    time.sleep(1)

    # Implementando condição de saída do loop While arbitrariamente.
    i += 1
    if i == 5:
        break
