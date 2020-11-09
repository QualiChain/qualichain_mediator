import json
import logging
import os
import sys

from jsonschema import RefResolver, validate

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class CValidator(object):
    """This class is used to validate CV jsons"""

    def __init__(self):
        self.cv_schema_json = 'schemas/cv-schema.json'
        self.schema_dir = 'file:///{0}/'.format(
            os.path.dirname(os.path.realpath(self.cv_schema_json)).replace("\\", "/")
        )

    def _schema(self):
        """This function loads cv schema"""
        with open(self.cv_schema_json, 'r') as file:
            cv_schema_data = file.read()
        cv_schema = json.loads(cv_schema_data)
        return cv_schema

    def evaluate(self, instance):
        """This function is used to evaluate provided json instance"""
        cv_schema = self._schema()
        resolver = RefResolver(self.schema_dir, cv_schema)
        try:
            validate(instance, cv_schema, resolver=resolver)
            return True
        except Exception as ex:
            log.error(ex)
            return False
