import json
import logging
import sys

from schema_validator import CValidator

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class DataHandler(object):
    """This object is used to receive CVs from rabbitMQ Consumer"""

    def __init__(self):
        self.validator = CValidator()

    def receive_data(self, ch, method, properties, body):
        """This function is enabled when a message is received from CV Consumer"""
        cv_instance = json.loads(body)
        is_valid = self.validator.evaluate(cv_instance, instance_category='cv')
        log.info(is_valid)