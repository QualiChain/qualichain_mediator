import json

from schema_validator import CValidator


class CVHandler(object):
    """This object is used to receive CVs from rabbitMQ Consumer"""

    def __init__(self):
        self.validator = CValidator()

    def receive_cv_data(self, ch, method, properties, body):
        """This function is enabled when a message is received from CV Consumer"""
        cv_instance = json.loads(body)
        is_valid = self.validator.evaluate(cv_instance)
        print(is_valid)