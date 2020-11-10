import sys

sys.path.append('../')
from extraction_pipeline.execute_courses_extraction_pipeline import CourseSkillExtractionExecutor

from settings import SAVE_IN_FILE


if __name__ == "__main__":
    executor = CourseSkillExtractionExecutor([])
    executor.execution_stage(save_in_file=SAVE_IN_FILE)

