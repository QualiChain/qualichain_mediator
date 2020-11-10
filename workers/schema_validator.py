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
        self.job_schema_json = 'schemas/job-schema.json'

        self.schema_dir = 'file:///{0}/'.format(
            os.path.dirname(os.path.realpath(self.cv_schema_json)).replace("\\", "/")
        )

    @staticmethod
    def file_loader(path):
        """This function is used to load files"""
        with open(path, 'r') as file:
            content = file.read()
        loaded_file = json.loads(content)
        return loaded_file

    def _cv_schema(self):
        """This function loads cv schema"""
        cv_schema = self.file_loader(path=self.cv_schema_json)
        return cv_schema

    def _job_schema(self):
        """This function is used to load job schema"""
        job_schema = self.file_loader(path=self.job_schema_json)
        return job_schema

    def evaluate(self, instance, instance_category):
        """This function is used to evaluate provided json instance"""
        if instance_category == 'cv':
            this_schema = self._cv_schema()
        else:
            this_schema = self._job_schema()

        resolver = RefResolver(self.schema_dir, this_schema)
        try:
            validate(instance, this_schema, resolver=resolver)
            return True
        except Exception as ex:
            log.error(ex)
            return False
