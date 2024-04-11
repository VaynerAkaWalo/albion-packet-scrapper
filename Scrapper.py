from AlbiPy import sniffing_thread
from AlbiPy import HEADERS
from time import sleep

thread = sniffing_thread()
thread.start()

try:
    while True:
        print("Waiting three seconds...")
        sleep(3)

        print("Fetching recorded orders...")
        orders = thread.get_data()

        print("Writing recorded orders")
        for order in orders:
            print(",".join(list(map(str, order.data)))+"\n")
except KeyboardInterrupt:
    pass

