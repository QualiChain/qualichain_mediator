import json
import logging
import sys

from sqlalchemy import create_engine, func, or_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from settings import ENGINE_STRING, SKILL_LEVEl_MAPPING

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
        self.engine = create_engine(ENGINE_STRING, pool_pre_ping=True)
        self.Base = automap_base()
        self.base = self.Base.prepare(self.engine, reflect=True)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.cvs = self.Base.classes.CVs
        # self.users = self.Base.classes.users
        self.skills = self.Base.classes.skills
        self.cv_skills = self.Base.classes.cv_skills
        self.jobs = self.Base.classes.jobs
        self.job_skills = self.Base.classes.job_skills
        # self.specialization = self.Base.classes.specialization
        self.user_applications = self.Base.classes.user_applications
        self.notification = self.Base.classes.notifications
        self.user_notification_preference = self.Base.classes.user_notification_preference


d = DataHandler()

country = 'Greece'
city = 'Athina'
state = 'Attiki'
specialization = 'Backend Developer'
organisation = 1
job_title = "Software Engineer"
message = "There is a new job opening that may interest you. Job title: {} ".format(job_title)
user_notification_preferences_obj = d.session.query(d.user_notification_preference).filter(
    or_(
        d.user_notification_preference.locations.contains(country),
        d.user_notification_preference.locations.contains(city),
        d.user_notification_preference.locations.contains(state)
    )).filter(d.user_notification_preference.specializations.contains(specialization)).filter(
    d.user_notification_preference.organisation == organisation).all()
user_ids = [user_notification_preference.user_id for user_notification_preference in user_notification_preferences_obj]

# for user_id in user_ids:
#     d.notification(
#         message=message,
#         user_id=user_id,
#             read= False
#     )

print(user_ids)

# job = d.jobs
# job_skills = d.job_skills
# user_applications = d.user_applications
# user_application = d.session.query(d.user_applications).filter_by(user_id=39, job_id=113)
# user_application.delete()
