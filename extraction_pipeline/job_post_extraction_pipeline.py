import pandas as pd
from sqlalchemy import create_engine

from settings import ENGINE_STRING, JOB_POSTS_TABLE


class JobPostSkillExtractor(object):
    """This Class is used to take job posts and feed them to Dobie"""

    def __init__(self):
        self.engine = create_engine(ENGINE_STRING)
        self.index = 0

    def get_job_posts(self):
        """
        This function is used to get job_posts table from DB

        :return: job_posts table
        """
        SELECT_QUERY = 'SELECT requirements from "{}"'.format(JOB_POSTS_TABLE)

        job_posts = pd.read_sql_query(SELECT_QUERY, self.engine)
        return job_posts

    # def process_job_requirements(self, job_posts_fraction):
    #
