import json
import logging
import sys

import pandas as pd
from schema_validator import CValidator
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from settings import ENGINE_STRING

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class DataHandler(object):
    """This object is used to receive CVs from rabbitMQ Consumer"""

    def __init__(self):
        self.validator = CValidator()

        self.engine = create_engine(ENGINE_STRING)
        self.Base = automap_base()
        self.base = self.Base.prepare(self.engine, reflect=True)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.cvs = self.Base.classes.CVs

    def receive_data(self, ch, method, properties, body):
        """This function is enabled when a message is received from CV Consumer"""
        data_payload = json.loads(body)
        if 'cv' in data_payload.keys():
            instance = data_payload['cv']
            is_valid = self.validator.evaluate(instance, instance_category='cv')
            if is_valid:
                log.info("The CV instance is valid")
                self.add_cv(**instance)
            else:
                log.info("The CV instance is not valid -- Abort")
        elif 'job' in data_payload.keys():
            instance = data_payload['job']
            is_valid = self.validator.evaluate(instance, instance_category='job')
            log.info(is_valid)
        else:
            log.info("Not valid payload send")

    def add_cv(self, **kwargs):
        """This function is used to add a new cv to Qualichain DB"""
        try:
            data = kwargs
            personURI = data['personURI']
            user_id = int(personURI.replace("qc:", ""))
            check_is_cv_exists = self.session.query(self.cvs).filter_by(user_id=user_id)

            if not check_is_cv_exists.scalar():
                new_cv = self.cvs(
                    user_id=user_id,
                    target_sector=data['targetSector'] if 'targetSector' in data.keys() else None,
                    description=data['description'] if 'description' in data.keys() else None,
                    work_history=data['workHistory'],
                    education=data['education']
                )
                self.session.add(new_cv)
                self.session.commit()
            else:
                log.info("CV for user with ID: {} already exists".format(user_id))
        except Exception as ex:
            log.error(ex)
