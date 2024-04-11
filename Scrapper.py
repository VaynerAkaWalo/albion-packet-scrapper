import time
from timeit import default_timer as timer
from AlbiPy import sniffing_thread
from AlbiPy import HEADERS
from time import sleep
import logging
import sys
import os

banner = """
  ,---.  ,--.,--.  ,--.,--------.,--.  ,--. ,-----. ,--.   ,--.  ,---. ,--. ,--. 
 /  O  \\ |  ||  ,'.|  |'--.  .--'|  ,'.|  |'  .-.  '|  |   |  | /  O  \\ \\ `.' /  
|  .-.  ||  ||  |' '  |   |  |   |  |' '  ||  | |  ||  |.'.|  ||  .-.  | \\   /   
|  | |  ||  ||  | `   |   |  |   |  | `   |'  '-'  '|   ,'.   ||  | |  |  |  |    
`--' `--'`--'`--'  `--'   `--'   `--'  `--' `-----' '--'   '--'`--' `--'  `--'    
                                                                                  
Albion-packet-scraper (v2.13.7)
Definitely not Powered by Spring Boot
"""

logger = logging.getLogger("Scrapper")
FORMAT = '%(asctime)s %(levelname)s %(process)d [%(processName)s] %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)


thread = sniffing_thread()

def main():
    try:
        while False:
                logger.info("Waiting three seconds...")
                sleep(3)

                logger.info("Fetching recorded orders...")
                orders = thread.get_data()

                logger.info("Obtained %s orders", orders.__len__())
                 # for order in orders:
                 #    logger.info(",".join(list(map(str, order.data)))+"\n")
    except Exception as e:
        logger.error(e.with_traceback())
        thread.stop()
    finally:
        logger.info("Thread stopped!")

if __name__ == '__main__':
    start_time = timer()
    print(banner)
    logger.info("Starting Albion-Packet-Scraper with PID %s (%s)", os.getpid(), os.getcwd())
    logger.info("Starting service [Sniffer thread]")
    logger.info("Started Albion-Packet-Scrapper in %f seconds", timer() - start_time)
    thread.start()
    main()
    logger.info("Stopped Albion-Packet-Scrapper after %f", timer() - start_time)
