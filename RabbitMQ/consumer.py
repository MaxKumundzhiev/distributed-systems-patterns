from os import getenv
from datetime import datetime

from loguru import logger
from connection import ConnectionClient

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties, Basic 


def process(
    channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes
):
    logger.info(f"channel {channel}")
    logger.info(f"method {method}")
    logger.info(f"preperties {properties}")
    logger.info(f"body {body}")

    now = str(datetime.now())
    logger.success(f"processed message at {now}")
    channel.basic_ack(delivery_tag=method.delivery_tag)
    logger.success(f"sent ack to {method.delivery_tag}")


def consume_messages(channel: BlockingChannel) -> None:
    try:
        channel.basic_consume(
            queue=getenv("TASKS_QUEUE_MAIN_QUEUE_NAME"),
            on_message_callback=process
        )
    except Exception as e:
        logger.error(f"failed establish consumer for channel {channel} with error: {e}")
    
    try:
        logger.info("waiting for messages ...")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"failed to consume from channel {channel} with error: {e}")


def kick_off_consumer():
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
            consume_messages(channel=chn)


if __name__ == "__main__":
    try:
        kick_off_consumer()
    except KeyboardInterrupt:
        logger.warning("stopped consumer by keyboard interruption")