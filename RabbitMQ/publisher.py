from os import getenv
from datetime import datetime

from connection import ConnectionClient

from loguru import logger
from pika.adapters.blocking_connection import BlockingChannel


def declare_queue(channel: BlockingChannel) -> None:
    queue_name = getenv("TASKS_QUEUE_MAIN_QUEUE_NAME")
    try:
        channel.queue_declare(queue=queue_name)
        logger.success(f"declared queue {queue_name} for channel {channel}")
    except Exception as e:
        logger.error(f"failed declare queue {queue_name} for channel {channel} with error: {e}")
        raise e


def publish_message(channel: BlockingChannel) -> None:
    now, queue = str(datetime.now()), getenv("TASKS_QUEUE_MAIN_QUEUE_NAME")
    try:
        channel.basic_publish(
            exchange="", routing_key=queue, body=f"published at {now}"
        )
        logger.success(f"published message to channel {channel} at {now}")
    except Exception as e:
        logger.error(f"failed publish message with error: {e}")
        raise e
    return


def kick_off_publisher():
    client = ConnectionClient()
    # create a connection to tasks queue
    try:
        connection = client.get_connection()
    except Exception as e:
        logger.error(f"connection to tasks queue failed with error: {e}")
        raise e
    
    # perform a channel creation within an opened connection
    with connection as cnn:
        logger.success(f"connection to tasks queue created: {cnn}")
        logger.info(f"connection is open: {cnn.is_open}")

        # create a channel
        try:
            channel = cnn.channel()
        except Exception as e:
            logger.error(f"channel creation failed with error: {e}")
            raise e
        
        # perform a channel actions
        with channel as chn:
            logger.success(f"channel in connection is created: {chn}")
            logger.info(f"channel is open: {chn.is_open}")

            declare_queue(channel=chn)
            publish_message(channel=chn)

            while True:
                pass


if __name__ == "__main__":
    try:
        kick_off_publisher()
    except KeyboardInterrupt:
        logger.warning("stopped publisher by keyboard interruption")