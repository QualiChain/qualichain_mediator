import re

import pandas as pd
from sqlalchemy import create_engine

from settings import ENGINE_STRING, STOP_WORDS, COURSES_TABLE


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
            select_query = 'SELECT course_description, course_title from "{}" WHERE id in {}'.format(COURSES_TABLE,
                                                                                                     tuple_ids)
        else:
            select_query = 'SELECT course_description, course_title from {}'.format(COURSES_TABLE)

        courses = pd.read_sql_query(select_query, self.engine)
        return courses

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
