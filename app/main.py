import time


from load.FireHose_load import *
from extract.utils.requisition import *

i = 0
while True:
    price, moeda_parametro = get_data()
    send_data(price, moeda_parametro)
    time.sleep(5)
    if i == 10:
        break
