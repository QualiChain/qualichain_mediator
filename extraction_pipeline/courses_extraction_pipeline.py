import re

import pandas as pd
from sqlalchemy import create_engine

from settings import ENGINE_STRING, STOP_WORDS, COURSES_TABLE, SKILLS_TABLE


class CourseSkillExtractor(object):
    """This Class is used to take courses and feed them to Dobie"""

    def __init__(self):
        self.engine = create_engine(ENGINE_STRING)
        self.index = 0

    def get_courses(self, ids=[]):
        """
        This function is used to get courses table from DB

        :return: courses table
        """
        if ids:
            tuple_ids = tuple(ids)
            select_query = 'SELECT id, name, description from "{}" WHERE id in {}'.format(COURSES_TABLE,
                                                                                                     tuple_ids)
        else:
            select_query = 'SELECT id, name, description from {}'.format(COURSES_TABLE)

        courses = pd.read_sql_query(select_query, self.engine)
        return courses

    class SkillExtractor(object):
        """This Class is used to take skills from db"""

        def __init__(self):
            self.engine = create_engine(ENGINE_STRING)
            self.index = 0

        def get_skills(self, ids=[]):
            """
            This function is used to get skills table from DB

            :return: courses table
            """
            if ids:
                tuple_ids = tuple(ids)
                select_query = 'SELECT id, name  from "{}" WHERE id in {}'.format(
                    SKILLS_TABLE,
                    tuple_ids)
            else:
                select_query = 'SELECT id, name from {}'.format(SKILLS_TABLE)

            skills = pd.read_sql_query(select_query, self.engine)
            return skills

    @staticmethod
    def remove_stop_words(course_description):
        """
        This function is used to remove stop words from courses
        description

        :param course_description text
        :return: course_description without stopwords
        """
        split_txt = course_description.split()
        removed_txt = [word for word in split_txt if word not in STOP_WORDS]
        return " ".join(removed_txt)

    def process_course_description(self, course_descriptions_fraction):
        """
        This function receives a courses data frame, which is a part of the original table
        and preprocess the stored descriptions

        :param courses_fraction: pandas data frame
        :return: processed descriptions
        """

        raw_description = course_descriptions_fraction['course_description'] + ' ' + course_descriptions_fraction[
            'course_title']
        removed_stop_words = self.remove_stop_words(raw_description)
        stripped_from_whitespaces = removed_stop_words.strip()

        return stripped_from_whitespaces
