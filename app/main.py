from datetime import datetime
import time


from load.FireHose_load import *
from extract.utils.requisition import *

i = 0
while True:
    price, moeda_parametro = get_data()
    hora = datetime.now()
    hora = hora.strftime("%Y-%m-%d %H:%M:%S")
    delivery_stream_name = "PUT-S3-btc-etl-2"
    print(price, moeda_parametro, hora)
    records = {"price": price, "currency": moeda_parametro, "time": hora}
    # Envia o dado para o Firehose
    response = put_record_to_firehose(delivery_stream_name, records)
    print(response)
    time.sleep(10)
    i += 1
    if i == 12:
        break
