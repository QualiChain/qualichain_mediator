import json
import logging
import sys

from schema_validator import CValidator
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from settings import ENGINE_STRING, SKILL_LEVEl_MAPPING
from utils import store_job_to_elk, get_skills_from_payload

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class DataHandler(object):
    """DataHandler Object class
    This object is used to receive CVs from rabbitMQ Consumer

    Methods
    -------
    receive_date(ch, method, properties, body):
        This is the first method that distributes the incoming payloads to the other object methods
    store_cv_skills(skills, cv_id):
        This is the method that stores cv-skills relations
    add_cv(*kwargs):
        This function is used for adding a new CV
    store_job_skills(**kwargs):
        his is the method that stores job-skills relations
    add_job(**kwargs):
        This method is for adding a new Job instance
    transform_job_data(**kwargs):
        This method is for preparing the job data for elasticsearch insertion
    add_job_application(**kwargs):
        This function is for adding a new Job application instance
    """

    def __init__(self):
        self.validator = CValidator()

        self.engine = create_engine(ENGINE_STRING, pool_pre_ping=True)
        self.Base = automap_base()
        self.base = self.Base.prepare(self.engine, reflect=True)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.cvs = self.Base.classes.CVs
        self.users = self.Base.classes.users
        self.skills = self.Base.classes.skills
        self.cv_skills = self.Base.classes.cv_skills
        self.jobs = self.Base.classes.jobs
        self.job_skills = self.Base.classes.job_skills
        self.specialization = self.Base.classes.specialization
        self.user_applications = self.Base.classes.user_applications

    def receive_data(self, ch, method, properties, body):
        """This function is enabled when a message is received from CV Consumer"""
        data_payload = json.loads(body)
        if 'cv' in data_payload.keys():

            instance = data_payload['cv']
            if "status" in data_payload.keys():
                status = data_payload['status']
                if status == 'update':
                    self.update_cv(**instance)
                else:
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
        elif 'job_application' in data_payload.keys():
            instance = data_payload['job_application']
            is_valid = self.validator.evaluate(instance, instance_category='job_application')
            self.add_job_application(**instance)
        else:
            log.info("Not valid payload send")

    def _create_cv_skill_relation(self, skill_id, cv_id, skill_level):
        """This function is used for storing cv-skill relation"""
        new_cv_skill_relation = self.cv_skills(
            skill_id=skill_id,
            cv_id=cv_id,
            skil_level=skill_level
        )
        return new_cv_skill_relation

    def store_cv_skills(self, skills, cv_id, status='create'):
        """This function is used to store the provided as params skills to Qualichain DB"""
        try:
            for skill_obj in skills:
                skill_name = skill_obj['label']
                proficiency_level = skill_obj['proficiencyLevel']
                skill_level = SKILL_LEVEl_MAPPING[proficiency_level]

                if_skill_exists = self.session.query(self.skills).filter(
                    func.lower(self.skills.name) == skill_name.lower()
                )

                if if_skill_exists.first() is not None:
                    qualichain_skill = if_skill_exists.first()

                    if status == 'update':
                        cv_skill_relation = self.session.query(self.cv_skills).filter_by(
                            skill_id=qualichain_skill.id,
                            cv_id=cv_id
                        )
                        if cv_skill_relation.first() is not None:
                            cv_skill_relation.update(
                                skil_level=skill_level
                            )
                        else:
                            new_cv_skill_relation = self._create_cv_skill_relation(skill_id=qualichain_skill.id,
                                                                                   cv_id=cv_id,
                                                                                   skill_level=skill_level)
                            self.session.add(new_cv_skill_relation)
                    else:
                        new_cv_skill_relation = self._create_cv_skill_relation(skill_id=qualichain_skill.id,
                                                                               cv_id=cv_id,
                                                                               skill_level=skill_level)
                        self.session.add(new_cv_skill_relation)
            self.session.commit()
        except Exception as cv_ex:
            log.info(skills)
            self.session.rollback()
            log.error(cv_ex)
        finally:
            self.session.close()

    def add_cv(self, **kwargs):
        """This function is used to add a new cv to Qualichain DB"""
        try:
            data = kwargs
            personURI = data['personURI']
            user_id = int(data['userID'])
            cv_skills = data['skills']

            check_is_cv_exists = self.session.query(self.cvs).filter_by(user_id=user_id)

            if not check_is_cv_exists.scalar():
                new_cv = self.cvs(
                    user_id=user_id,
                    target_sector=data['targetSector'] if 'targetSector' in data.keys() else None,
                    description=data['description'] if 'description' in data.keys() else None,
                    work_history=data['workHistory'] if 'workHistory' in data.keys() else None,
                    education=data['education'] if 'education' in data.keys() else None
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
            self.session.rollback()
            log.error(ex)
        finally:
            self.session.close()

    def update_cv(self, **kwargs):
        """This method is used to update an existing CV to the DB"""
        # try:
        data = kwargs
        user_id = int(data['userID'])
        cv_skills = data['skills']

        cv = self.session.query(self.cvs).filter(user_id == user_id)
        if cv.first() is not None:
            cv.update(
                target_sector=data['targetSector'] if 'targetSector' in data.keys() else None,
                description=data['description'] if 'description' in data.keys() else None,
                work_history=data['workHistory'] if 'workHistory' in data.keys() else None,
                education=data['education'] if 'education' in data.keys() else None
            )
            self.session.commit()
        else:
            log.info("Abort incoming CV")
        log.info("this is hell")
        # except Exception as ex:
        #     self.session.rollback()
        #     log.error(ex)
        # finally:
        #     self.session.close()

    def store_job_skills(self, skills, job_id):
        """This function is used to store skills job information"""
        try:
            for skill_obj in skills:
                skill_name = skill_obj['label']

                if_skill_exists = self.session.query(self.skills).filter(
                    func.lower(self.skills.name) == skill_name.lower()
                )
                if if_skill_exists.first() is not None:
                    qualichain_skill = if_skill_exists.first()

                    new_job_skill_relation = self.job_skills(
                        skill_id=qualichain_skill.id,
                        job_id=job_id,
                    )
                    self.session.add(new_job_skill_relation)
            self.session.commit()
        except Exception as job_ex:
            log.info(skills)
            self.session.rollback()
            log.error(job_ex)
        finally:
            self.session.close()

    def add_job(self, **kwargs):
        """This function is used to add a new job to QualiChain DB"""
        try:
            data = kwargs
            job_id = int(data['id'].replace('Job', ''))
            job_skills = get_skills_from_payload(data)
            job_sector = data['specialization']

            check_if_job_exists = self.session.query(self.jobs).filter_by(id=job_id)
            check_specialization = self.session.query(self.specialization).filter_by(title=job_sector)

            # changes should be done here
            employer_id = None

            if not check_if_job_exists.scalar():
                if check_specialization.scalar():
                    specialization_id = check_specialization.first().id
                    new_job = self.jobs(
                        id=job_id,
                        title=data['label'],
                        creator_id=int(data['creator_id'].replace(":", '')),
                        # kbiz use user ids that already exist in QC DB
                        job_description=data['jobDescription'],
                        level=data['seniorityLevel'],  # seniority level in QC DB is different
                        country=data['country'],  # add country to Job schema
                        state=data['state'],  # add stare to Job schema
                        city=data['city'],  # add city to job schema
                        # employer=data['hiringOrganization'],
                        date=data['startDate'],
                        start_date=data['startDate'],
                        end_date=data['endDate'],
                        employment_type=data['contractType'],  # this field should me aligned with our data model
                        specialization_id=specialization_id
                        # sector value should be aligned with our specialization info
                    )
                    if employer_id:
                        new_job['employer_id'] = employer_id

                    self.session.add(new_job)
                    self.session.commit()

                    if job_skills:
                        self.store_job_skills(job_skills, job_id)
                    self.transform_job_data(data)
                else:
                    log.info("Specialization : {} does not exists".format(job_sector))
                    log.info(data)
            else:
                log.info("Job with ID: {} already exists".format(job_id))
        except Exception as ex:
            self.session.rollback()
            log.error(ex)
        finally:
            self.session.close()

    @staticmethod
    def transform_job_data(data):
        """This function is used to transform job data for elk storage"""
        job_skills = get_skills_from_payload(data)
        payload = {
            'title': data['label'],
            'jobDescription': data['jobDescription'],
            'level': data['seniorityLevel'],
            'date': data['startDate'],
            'startDate': data['startDate'],
            'endDate': data['endDate'],
            'creatorId': data['creator_id'],
            'employmentType': data['contractType'],
            'employer': data['hiringOrg'],
            'country': data['country'],
            'state': data['state'],
            'city': data['city'],
            'required_skills': []
        }
        if job_skills:
            for skill in job_skills:
                payload['required_skills'].append(skill['label'])
        store_job_to_elk(**payload)

    def add_job_application(self, **kwargs):
        """This function is used to store user job applications to Qualichain DB"""
        try:
            data = kwargs
            user_id = int(data['personURI'].
                          replace('qc', '').
                          replace(':', '')
                          )
            job_id = int(data['jobURI'].
                         replace('saro', '').
                         replace('Job', '').
                         replace(':', '')
                         )

            user_obj = self.session.query(self.users).filter_by(id=user_id)
            job_obj = self.session.query(self.jobs).filter_by(id=job_id)

            if user_obj.scalar() and job_obj.scalar():
                new_application = self.user_applications(
                    user_id=user_id,
                    job_id=job_id,
                    available=data['availability'],
                    exp_salary=data['expectedSalary']
                )
                self.session.add(new_application)
                self.session.commit()
            else:
                log.info("User or Job object not exist")

        except Exception as ex:
            log.info(kwargs)
            self.session.rollback()
            log.error(ex)
        finally:
            self.session.close()
