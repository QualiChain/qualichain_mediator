import json
import logging
import sys

from schema_validator import CValidator
from sqlalchemy import create_engine, func, or_
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
    update_cv(**kwargs):
        This function is used to update a user's CV
    delete_cv(**kwargs):
        This function is used to delete a specific CV
    store_job_skills(**kwargs):
        his is the method that stores job-skills relations
    add_job(**kwargs):
        This method is for adding a new Job instance
    update_job(**kwargs):
        This method is used for updating Job instanses stored to the DB
    delete_job(**kwargs):
        This method is used for deleting Job instances stored in Qualichain RDBMS
    transform_job_data(**kwargs):
        This method is for preparing the job data for elasticsearch insertion
    add_job_application(**kwargs):
        This function is for adding a new Job application instance
    delete_job_application(**kwargs):
        This function is for deleting Job application instances stored in Qualichain RDBMS

    Examples
    --------
    >>> data_handler = DataHandler()

    `Send CV data`
    >>> payload = {'cv': ${cv}, 'status': 'create/update'}

    `Send Job data`
    >>> payload = {'job': ${job}, 'status': 'create/update'}

    `Send Job-application data`
    >>> payload = {'job-application': ${job-application}, 'status': 'create/update'}

    >>> data_handler.receive_data(payload)
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
        self.notification = self.Base.classes.notifications
        self.user_notification_preference = self.Base.classes.user_notification_preference
        self.recruitment_organisations = self.Base.classes.recruitment_organisation
        self.user_recruitment_organisation = self.Base.classes.user_recruitment_organisations

    def receive_data(self, ch, method, properties, body):
        """This function is enabled when a message is received from CV Consumer"""
        data_payload = json.loads(body)
        log.info(data_payload)
        if 'cv' in data_payload.keys():
            instance = data_payload['cv']
            if "status" in data_payload.keys():
                status = data_payload['status']
                if status == 'update':
                    self.update_cv(**instance)
                elif status == 'delete':
                    self.delete_cv(**instance)
                elif status == 'create':
                    is_valid = self.validator.evaluate(instance, instance_category='cv')
                    if is_valid:
                        log.info("The CV instance is valid")
                        self.add_cv(**instance)
                    else:
                        log.info("The CV instance is not valid -- Abort!")
            else:
                log.info("No correct status -- Abort!")
        elif 'job' in data_payload.keys():
            instance = data_payload['job']
            if "status" in data_payload.keys():
                status = data_payload['status']
                if status == 'update':
                    self.update_job(**instance)
                elif status == 'delete':
                    self.delete_job(**instance)
                elif status == 'create':
                    is_valid = self.validator.evaluate(instance, instance_category='job')
                    if is_valid:
                        log.info("The Job instance is valid")
                        self.add_job(**instance)
                    else:
                        log.info("The Job instance is not valid -- Abort!")
            else:
                log.info("No valid status key -- Abort!")
        elif 'job_application' in data_payload.keys():
            instance = data_payload['job_application']
            if "status" in data_payload.keys():
                status = data_payload['status']
                if status == 'delete':
                    self.delete_job_application(**instance)
                elif status == 'create':
                    is_valid = self.validator.evaluate(instance, instance_category='job_application')
                    if is_valid:
                        self.add_job_application(**instance)
                    else:
                        log.info("Not valid payload send")
            else:
                log.info("No valid status key -- Abort!")

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
                            cv_skill_relation.update({
                                'skil_level': skill_level
                            })
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
        try:
            data = kwargs
            user_id = int(data['userID'])
            cv_skills = data['skills']

            cv = self.session.query(self.cvs).filter(user_id == user_id)
            if cv.first() is not None:
                cv.update({
                    'target_sector': data['targetSector'] if 'targetSector' in data.keys() else None,
                    'description': data['description'] if 'description' in data.keys() else None,
                    'work_history': data['workHistory'] if 'workHistory' in data.keys() else None,
                    'education': data['education'] if 'education' in data.keys() else None
                })
                self.session.commit()
                cv_id = cv.first().id
                if cv_skills:
                    log.info("Create cv - skills relations")
                    self.store_cv_skills(cv_skills, cv_id, status='update')
                else:
                    log.info("No skills for current CV")
            else:
                log.info("Abort incoming CV")
            log.info("Successfully updated CV for userID: {}".format(user_id))
        except Exception as ex:
            self.session.rollback()
            log.error(ex)
        finally:
            self.session.close()

    def delete_cv(self, **kwargs):
        """This function is used to delete cv instances stored in Qualichain RDBMS"""
        try:
            data = kwargs
            cv_instance = self.session.query(self.cvs).filter_by(
                user_id=data['user_id']
            )
            cv_skills = self.session.query(self.cv_skills).filter_by(
                cv_id=cv_instance[0].id
            )
            cv_skills.delete()
            cv_instance.delete()
            self.session.commit()
        except Exception as ex:
            log.error(ex)
            self.session.rollback()
        finally:
            self.session.close()

    def store_job_skills(self, skills, job_id, status='create'):
        """This function is used to store skills job information"""
        try:
            for skill_obj in skills:
                skill_name = skill_obj['label']

                if_skill_exists = self.session.query(self.skills).filter(
                    func.lower(self.skills.name) == skill_name.lower()
                )
                if if_skill_exists.first() is not None:
                    qualichain_skill = if_skill_exists.first()
                    if status == 'update':
                        job_skill_relation = self.session.query(self.job_skills).filter_by(
                            skill_id=qualichain_skill.id,
                            job_id=job_id
                        )
                        if job_skill_relation.first() is None:
                            new_job_skill_relation = self.job_skills(
                                skill_id=qualichain_skill.id,
                                job_id=job_id,
                            )
                            self.session.add(new_job_skill_relation)
                    else:
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

    def create_internal_new_job_application_notification(self, **kwargs):
        """This function is used to create a notification for the job creator when a new application is created for that job"""
        try:
            job_title = kwargs['job_title']
            user_name = kwargs['user_name']
            creator_id = kwargs['creator_id']
            message = "The user '{}' has applied for the job '{}' ". \
                format(user_name, job_title)

            new_notification = self.notification(
                message=message,
                user_id=creator_id,
                read=False
            )
            self.session.add(new_notification)
            # self.session.commit()
        except Exception as ex:
            log.info("Error in the creation of an new job application notification")


    def create_internal_mobility_notification(self, **kwargs):
        """This function is used to create a notification when a new position inside an organisation is create (internal reallocation)"""
        # country = kwargs['country']
        # city = kwargs['city']
        # state = kwargs['state']
        # specialization_name = kwargs['specialization_name']
        try:
            organisation = kwargs['organisation']
            job_title = kwargs['job_title']

            message = "There is a new job position opening inside your organisation. Title: {} ". \
                format(job_title)

            user_notification_preferences_obj = self.session.query(self.user_notification_preference).filter(
                self.user_notification_preference.internal_reallocation_availability == True).all()
            notif_user_ids = [user_notification_preference.user_id for user_notification_preference in
                              user_notification_preferences_obj]

            user_rec_org_obj = self.session.query(self.user_recruitment_organisation).filter(
                self.user_recruitment_organisation.organisation_id == organisation).all()
            org_user_ids = [user_organisation.user_id for user_organisation in
                            user_rec_org_obj]

            user_ids = list(set(notif_user_ids).intersection(org_user_ids))

            for user_id in user_ids:
                new_notification = self.notification(
                    message=message,
                    user_id=user_id,
                    read=False
                )
                self.session.add(new_notification)
            # self.session.commit()
        except Exception as ex:
            log.info("Error in the creation of an internal mobility notification")

    def create_user_job_notification(self, **kwargs):
        """This function is used to create a notification when a new job is consumed from Mediator"""
        country = kwargs['country']
        city = kwargs['city']
        state = kwargs['state']
        specialization_name = kwargs['specialization_name']
        organisation = kwargs['organisation']
        job_title = kwargs['job_title']

        message = "There is a new job opening that may interest you. Title: {} ". \
            format(job_title)

        user_notification_preferences_obj = self.session.query(self.user_notification_preference).filter(
            or_(
                self.user_notification_preference.locations.contains(country),
                self.user_notification_preference.locations.contains(city),
                self.user_notification_preference.locations.contains(state)
            )).filter(self.user_notification_preference.specializations.contains(specialization_name)).filter(
            self.user_notification_preference.organisation == organisation).all()
        user_ids = [user_notification_preference.user_id for user_notification_preference in
                    user_notification_preferences_obj]
        for user_id in user_ids:
            new_notification = self.notification(
                message=message,
                user_id=user_id,
                read=False
            )
            self.session.add(new_notification)
        # self.session.commit()

    def add_job(self, **kwargs):
        """This function is used to add a new job to QualiChain DB"""
        try:
            data = kwargs
            job_id = int(data['id'].replace('Job', ''))
            job_skills = get_skills_from_payload(data)
            job_sector = data['specialization']

            check_if_job_exists = self.session.query(self.jobs).filter_by(id=job_id)
            check_specialization = self.session.query(self.specialization).filter_by(title=job_sector)

            if 'hiringOrg' in data.keys() and data['hiringOrg'] is not None:
                employer_id = self.session.query(self.recruitment_organisations).filter_by(
                    title=data['hiringOrg']).first().id
            else:
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
                        employer_id=employer_id,
                        date=data['startDate'],
                        start_date=data['startDate'],
                        end_date=data['endDate'],
                        employment_type=data['contractType'],  # this field should me aligned with our data model
                        specialization_id=specialization_id
                        # sector value should be aligned with our specialization info
                    )

                    self.session.add(new_job)
                    self.create_user_job_notification(
                        country=data['country'],
                        city=data['city'],
                        state=data['state'],
                        specialization_name=check_specialization.first().title,
                        job_title=data['label'],
                        organisation=employer_id
                    )
                    self.create_internal_mobility_notification(
                        job_title=data['label'],
                        organisation=employer_id
                    )
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

    def update_job(self, **kwargs):
        """This function is used to update to the database consumed Jobs"""
        try:
            data = kwargs
            job_id = int(data['id'].replace('Job', ''))
            job_skills = get_skills_from_payload(data)
            job_sector = data['specialization']

            check_specialization = self.session.query(self.specialization).filter_by(title=job_sector)

            # changes should be done here
            employer_id = None

            if check_specialization.first() is not None:
                specialization_id = check_specialization.first().id
                job = self.session.query(self.jobs).filter(id == job_id)
                if job.first() is not None:
                    log.info("Successfully updated job with ID:{}".format(job_id))
                    job.update({
                        'id': job_id,
                        'title': data['label'],
                        'creator_id': int(data['creator_id'].replace(":", '')),
                        'job_description': data['jobDescription'],
                        'level': data['seniorityLevel'],
                        'country': data['country'],
                        'state': data['state'],
                        'city': data['city'],
                        'date': data['startDate'],
                        'start_date': data['startDate'],
                        'end_date': data['endDate'],
                        'employment_type': data['contractType'],  # this field should me aligned with our data model
                        'specialization_id': specialization_id
                    })
                self.session.commit()
                if job_skills:
                    self.store_job_skills(job_skills, job_id, status='update')
                log.info("Successfully updated job with ID:{}".format(job_id))
            else:
                log.info("Abort")
        except Exception as ex:
            self.session.rollback()
            log.error(ex)
        finally:
            self.session.close()

    def delete_job(self, **kwargs):
        """This function is used to delete stored Job objects"""
        data = kwargs
        try:
            job_instance = self.session.query(self.jobs).filter_by(
                id=data['job_id']
            )
            job_skills = self.session.query(self.job_skills).filter_by(
                job_id=job_instance[0].id
            )

            job_skills.delete()
            job_instance.delete()

            self.session.commit()
        except Exception as ex:
            log.error(ex)
            self.session.rollback()
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
            log.info(data)
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
            job_creator_id = job_obj.first().creator_id

            if user_obj.scalar() and job_obj.scalar():
                new_application = self.user_applications(
                    user_id=user_id,
                    job_id=job_id,
                    available=data['availability'],
                    exp_salary=data['expectedSalary']
                )
                self.session.add(new_application)
                self.create_internal_new_job_application_notification(
                    job_title=job_obj.first().title,
                    user_name=user_obj.first().fullName,
                    creator_id=job_creator_id
                )
                self.session.commit()
            else:
                log.info("User or Job object not exist")

        except Exception as ex:
            log.info(kwargs)
            self.session.rollback()
            log.error(ex)
        finally:
            self.session.close()

    def delete_job_application(self, **kwargs):
        """This function is used to remove job applications stored to QualiChain DB"""
        try:
            data = kwargs
            user_application = self.session.query(self.user_applications).filter_by(
                user_id=data['user_id'],
                job_id=data['job_id']
            )
            user_application.delete()
            self.session.commit()
        except Exception as ex:
            log.error(ex)
            log.info(kwargs)
            self.session.rollback()
        finally:
            self.session.close()
