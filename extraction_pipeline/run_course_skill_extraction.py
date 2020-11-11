import sys

sys.path.append('../')
from extraction_pipeline.courses.execute_courses_extraction_pipeline import CourseSkillExtractionExecutor

from settings import SAVE_IN_FILE


if __name__ == "__main__":
    executor = CourseSkillExtractionExecutor([])
    courses = executor.courses
    courses_length = len(courses)

    for execution in range(0, courses_length - 1):
        executor.iterate(execution)

