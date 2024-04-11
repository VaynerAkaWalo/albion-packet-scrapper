from timeit import default_timer as timer
from AlbiPy import sniffing_thread
from time import sleep
import logging
import sys
import os
import threading

service_name = 'Albion-packet-scrapper'

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
        sleep(3)
        orders = thread.get_data()

        #    logger.info(",".join(list(map(str, order.data)))+"\n")


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
        logger.error(e.with_traceback())
    finally:
        thread.stop()
        thread.join()
        logger.info("Sniffing thread stopped")
        logger.info("Stopped %s after %f seconds", service_name, timer() - start_time)

