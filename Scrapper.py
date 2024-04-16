import json
from timeit import default_timer as timer
from AlbiPy import sniffing_thread
from time import sleep
import logging
import sys
import os
import threading
import requests

service_name = 'Albion-packet-scrapper'
URL = "https://blamedevs.com:8443/albion-rmt-backend/api/v1/marketdata"

banner = """
  ,---.  ,--.,--.  ,--.,--------.,--.  ,--. ,-----. ,--.   ,--.  ,---. ,--. ,--. 
 /  O  \\ |  ||  ,'.|  |'--.  .--'|  ,'.|  |'  .-.  '|  |   |  | /  O  \\ \\ `.' /  
|  .-.  ||  ||  |' '  |   |  |   |  |' '  ||  | |  ||  |.'.|  ||  .-.  | \\   /   
|  | |  ||  ||  | `   |   |  |   |  | `   |'  '-'  '|   ,'.   ||  | |  |  |  |    
`--' `--'`--'`--'  `--'   `--'   `--'  `--' `-----' '--'   '--'`--' `--'  `--'    
                                                                                  
Albion-packet-scraper (v2.13.7)
Definitely not Powered by Spring Boot
"""

threading.current_thread().name='Main   '
logger = logging.getLogger()
FORMAT = '%(asctime)s %(levelname)s %(process)d [%(threadName)s] %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)


thread = sniffing_thread()


def scraping():
    while True:
        orders = thread.get_data()
        if(orders.logs.__len__() == 0):
            sleep(3)
            continue

        sendOrders(orders.parsed_orders())

        #    logger.info(",".join(list(map(str, order.data)))+"\n")


def sendOrders(orders):
    response = requests.post(URL, json=json.loads(orders))
    json_response = response.json()
    logger.info(json_response)
    # logger.info("Successfully posted %s orders, %s failed", json_response['Succeed'].__len__(), json_response['failed'].__len__())


if __name__ == '__main__':
    start_time = timer()
    print(banner)
    logger.info("Starting %s with PID %s (%s)", service_name, os.getpid(), os.getcwd())
    logger.info("Starting service [Sniffer thread]")
    logger.info("Started %s in %f seconds", service_name,  timer() - start_time)
    try:
        thread.start()
        scraping()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(e.__traceback__)
    finally:
        thread.stop()
        thread.join()
        logger.info("Sniffing thread stopped")
        logger.info("Stopped %s after %f seconds", service_name, timer() - start_time)

