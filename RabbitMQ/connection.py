from os import getenv
from dotenv import load_dotenv

from pika import (
    ConnectionParameters, BlockingConnection, PlainCredentials
)

try:
    is_loaded = load_dotenv()
except Exception as e:
    raise e
finally:
    if not is_loaded:
        raise EnvironmentError


class ConnectionClient:
    def get_connection_parameters(self) -> ConnectionParameters:
        return ConnectionParameters(
            host=getenv('TASKS_QUEUE_HOST'),
            port=getenv('TASKS_QUEUE_PORT'),
            credentials=PlainCredentials(
                username=getenv('TASKS_QUEUE_USERNAME'), 
                password=getenv('TASKS_QUEUE_PASSWORD')
            )
        )

    def get_connection(self) -> BlockingConnection:
        parameters = self.get_connection_parameters()
        return BlockingConnection(parameters=parameters)