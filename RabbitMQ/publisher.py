from loguru import logger
from connection import ConnectionClient


def start_publisher():
    client = ConnectionClient()
    try:
        connection = client.get_connection()
    except Exception as e:
        logger.error(f'connection to tasks queue failed with error: {e}')
        raise e
    
    logger.info(f'connection to tasks queue created: {connection}')
    while True:
        pass


if __name__ == "__main__":
    try:
        start_publisher()
    except KeyboardInterrupt:
        logger.warning("stopped publisher by keyboard interruption")