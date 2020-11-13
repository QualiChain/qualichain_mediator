import json
import logging
import sys

from schema_validator import CValidator
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from settings import ENGINE_STRING, SKILL_LEVEl_MAPPING

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class DataHandler(object):
    """This object is used to receive CVs from rabbitMQ Consumer"""

    def __init__(self):
        self.validator = CValidator()

        self.engine = create_engine(ENGINE_STRING, pool_pre_ping=True)
        self.Base = automap_base()
        self.base = self.Base.prepare(self.engine, reflect=True)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.cvs = self.Base.classes.CVs
        self.skills = self.Base.classes.skills
        self.cv_skills = self.Base.classes.cv_skills
        self.jobs = self.Base.classes.jobs
        self.job_skills = self.Base.classes.job_skills

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
                log.info("The CV instance is not valid -- Abort!")
        elif 'job' in data_payload.keys():
            instance = data_payload['job']
            is_valid = self.validator.evaluate(instance, instance_category='job')
            if is_valid:
                log.info("The Job instance is valid")
                self.add_job(**instance)
            else:
                log.info("The Job instance is not valid -- Abort!")
        else:
            log.info("Not valid payload send")

    def store_cv_skills(self, skills, cv_id):
        """This function is used to store the provided as params skills to Qualichain DB"""
        for skill_obj in skills:
            skill_name = skill_obj['label']
            proficiency_level = skill_obj['proficiencyLevel']
            skill_level = SKILL_LEVEl_MAPPING[proficiency_level]

            if_skill_exists = self.session.query(self.skills).filter(
                func.lower(self.skills.name) == skill_name.lower()
            )
            if if_skill_exists.scalar():
                qualichain_skill = if_skill_exists.first()

                new_cv_skill_relation = self.cv_skills(
                    skill_id=qualichain_skill.id,
                    cv_id=cv_id,
                    skil_level=skill_level
                )
                self.session.add(new_cv_skill_relation)
        self.session.commit()

    def add_cv(self, **kwargs):
        """This function is used to add a new cv to Qualichain DB"""
        try:
            data = kwargs
            personURI = data['personURI']
            user_id = int(personURI.replace('qc:', ''))
            cv_skills = data['skills']

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
                new_cv_id = new_cv.id
                if cv_skills:
                    log.info("Create cv - skills relations")
                    self.store_cv_skills(cv_skills, new_cv_id)
                else:
                    log.info("No skills for current CV")
            else:
                log.info("CV for user with ID: {} already exists".format(user_id))
        except Exception as ex:
            log.error(ex)

    def store_job_skills(self, skills, job_id):
        """This function is used to store skills job information"""
        for skill_obj in skills:
            skill_name = skill_obj['label']

            if_skill_exists = self.session.query(self.skills).filter(
                func.lower(self.skills.name) == skill_name.lower()
            )
            if if_skill_exists.scalar():
                qualichain_skill = if_skill_exists.first()

                new_job_skill_relation = self.job_skills(
                    skill_id=qualichain_skill.id,
                    job_id=job_id,
                )
                self.session.add(new_job_skill_relation)
        self.session.commit()

    def add_job(self, **kwargs):
        """This function is used to add a new job to QualiChain DB"""
        try:
            data = kwargs
            job_id = int(data['id'].replace('saro:Job', ''))
            job_skills = data['skillReq']

            check_if_job_exists = self.session.query(self.jobs).filter_by(id=job_id)
            if not check_if_job_exists.scalar():
                log.info("Insert job")
                new_job = self.jobs(
                    id=job_id,
                    title=data['label'],
                    creator_id=int(data['creator_id']),  # kbiz use user ids that already exist in QC DB
                    job_description=data['jobDescription'],
                    level_value=data['seniorityLevel'],  # seniority level in QC DB is different
                    country=data['jobLocation'],  # add country to Job schema
                    state=data['jobLocation'],  # add stare to Job schema
                    city=data['jobLocation'],  # add city to job schema
                    employer="is missing",  # add employer to job schema
                    date=data['startDate'],
                    start_date=data['startDate'],
                    end_date=data['endDate'],
                    employment_value=data['contractType'],  # this field should me aligned with our data model
                    specialization_id=1  # sector value should be aligned with our specialization info
                )
                self.session.add(new_job)
                self.session.commit()

                if job_skills:
                    self.store_job_skills(job_skills, job_id)
            else:
                log.info("Job with ID: {} already exists".format(job_id))
        except Exception as ex:
            log.error(ex)
