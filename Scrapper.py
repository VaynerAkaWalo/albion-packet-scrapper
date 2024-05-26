import json
from timeit import default_timer as timer
from AlbiPy import sniffing_thread
from time import sleep
import logging
import sys
import os
import threading
import requests
import traceback

from requests.exceptions import InvalidJSONError

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
    orders = []
    while True:
        try:
            orders.append((thread.get_data().parsed_orders()))
            if sys.argv[1] == "debug" and orders.__len__():
                logger.info(str(orders).replace("\'", "\"").replace("False", "false").replace("None", "null"))
        except IndexError:
            orders = []

        if orders.__len__() > 100:
            sendOrders(orders)
            orders = []

        sleep(5)


def sendOrders(orders):
    try:
        response = requests.post(URL, json=orders)
        if response.status_code == 201:
            json_response = response.json()
            logger.info("Successfully posted %s orders, %s failed", json_response['Succeed'].__len__(), json_response.get('failed', []).__len__())
        else:
            logger.error("Failed to post orders, status code %d", response.status_code)
    except InvalidJSONError as e:
        logger.error("Invalid json error %s", e)
        pass


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
        logger.error(e.__str__())
        print(traceback.format_exc())
    finally:
        thread.stop()
        thread.join()
        logger.info("Sniffing thread stopped")
        logger.info("Stopped %s after %f seconds", service_name, timer() - start_time)
