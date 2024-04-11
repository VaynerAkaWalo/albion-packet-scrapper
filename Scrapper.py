from AlbiPy import sniffing_thread
from AlbiPy import HEADERS
from time import sleep
import logging
import sys

banner = """
  ,---.  ,--.,--.  ,--.,--------.,--.  ,--. ,-----. ,--.   ,--.  ,---. ,--. ,--. 
 /  O  \\ |  ||  ,'.|  |'--.  .--'|  ,'.|  |'  .-.  '|  |   |  | /  O  \\ \\ `.' /  
|  .-.  ||  ||  |' '  |   |  |   |  |' '  ||  | |  ||  |.'.|  ||  .-.  | \\   /   
|  | |  ||  ||  | `   |   |  |   |  | `   |'  '-'  '|   ,'.   ||  | |  |  |  |    
`--' `--'`--'`--'  `--'   `--'   `--'  `--' `-----' '--'   '--'`--' `--'  `--'    
                                                                                  
Albion-packet-scrapper (v2.13.7)
Definitly not Powered by Spring Boot
"""
print(banner)

logger = logging.getLogger()
FORMAT = '%(asctime)s %(levelname)s %(process)d [%(processName)s] %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)


thread = sniffing_thread()
thread.start()


def main():
    logger.info("essa")
    try:
        while True:
                logger.info("Waiting three seconds...")
                sleep(3)

                logger.info("Fetching recorded orders...")
                orders = thread.get_data()

                logger.info("Obtained %s orders", orders.__len__())
                for order in orders:
                    logger.info(",".join(list(map(str, order.data)))+"\n")
    except:
        thread.stop()
    finally:
        logger.info("\nThread stopped!")


if __name__ == '__main__':
    main()
