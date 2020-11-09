import logging
import sys

from clients.rabbitmq_client import RabbitMQClient
from settings import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_VHOST, APP_QUEUE
from workers.cv_handler import CVHandler

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def cv_consumer(queue):
    """This function is used to consume CV"""
    rabbitmq_client = RabbitMQClient()
    channel = rabbitmq_client.connection.channel()

    cv_handler = CVHandler()

    channel.basic_consume(
        queue=queue, on_message_callback=cv_handler.receive_cv_data, auto_ack=True)
    log.info(
        """
        RABBITMQ HOST: {host}
        RABBITMQ PORT: {port}
        RABBITMQ USER: {user}
        RABBITMQ PASSWORD: {password}
        RABBITMQ VIRTUAL HOST: {virtual_host}
        """.format(**{
            'host': RABBITMQ_HOST,
            'port': RABBITMQ_PORT,
            'user': RABBITMQ_USER,
            'password': '*' * len(RABBITMQ_PASSWORD),
            'virtual_host': RABBITMQ_VHOST
        })
    )
    log.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    cv_consumer(queue=APP_QUEUE)
