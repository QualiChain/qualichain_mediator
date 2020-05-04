import re

import pandas as pd
from sqlalchemy import create_engine

from settings import ENGINE_STRING, JOB_POSTS_TABLE, STOP_WORDS


class JobPostSkillExtractor(object):
    """This Class is used to take job posts and feed them to Dobie"""

    def __init__(self):
        self.engine = create_engine(ENGINE_STRING)
        self.index = 0

    def get_job_posts(self, ids=[]):
        """
        This function is used to get job_posts table from DB

        :return: job_posts table
        """
        if ids:
            tuple_ids = tuple(ids)
            select_query = 'SELECT requirements from "{}" WHERE id in {}'.format(JOB_POSTS_TABLE, tuple_ids)
        else:
            select_query = 'SELECT requirements from requirements'

        job_posts = pd.read_sql_query(select_query, self.engine)
        return job_posts

    @staticmethod
    def remove_stop_words(job_requirements):
        """
        This function is used to remove stop words from job post requirements
        description

        :param job_requirements: job requirements text
        :return: job requirements without stopwords
        """
        split_txt = job_requirements.split()
        removed_txt = [word for word in split_txt if word not in STOP_WORDS]
        return " ".join(removed_txt)

    def process_job_requirements(self, job_posts_fraction):
        """
        This function receives a job posts data frame, which is a part of the original table
        and preprocess the stored job requirements

        :param job_posts_fraction: pandas data frame
        :return: processed requirements
        """
        # raw_requirements = job_posts_fraction['requirements'].map(
        #     lambda requirement: re.sub(r"[^a-zA-Z0-9]+", ' ', requirement)
        # )
        raw_requirements = job_posts_fraction['requirements']
        removed_stop_words = raw_requirements.map(self.remove_stop_words)
        stipped_from_whitespaces = removed_stop_words.map(
            lambda requirement: requirement.strip()
        )

        processed_requirements = " ".join(stipped_from_whitespaces)
        return processed_requirements
