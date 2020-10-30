
from extraction_pipeline.execute_courses_extraction_pipeline import CourseSkillExtractionExecutor

from settings import SAVE_IN_FILE, COURSES_TABLE, ENGINE_STRING

import pandas as pd
from sqlalchemy import create_engine


if __name__ == "__main__":

    # engine = create_engine(ENGINE_STRING)
    # index = 0
    # select_query = 'SELECT id, course_title from {}'.format(COURSES_TABLE)
    # courses = pd.read_sql_query(select_query, engine)
    #
    # for ind in courses.index:
    executor = CourseSkillExtractionExecutor([])
    executor.execution_stage(save_in_file=SAVE_IN_FILE)

