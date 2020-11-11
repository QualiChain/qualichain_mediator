import time


from clients.dobie_client import send_data_to_dobie
from extraction_pipeline.courses.courses_extraction_pipeline import CourseExtractor
from settings import TIME_BETWEEN_REQUESTS
from utils import save_extracted_skills, handle_course_skill_annotation


class CourseSkillExtractionExecutor(object):

    def __init__(self, courses_ids):
        self.index = 0
        self.extractor = CourseExtractor()
        self.courses = self.extractor.get_courses(ids=courses_ids)

    @staticmethod
    def prepare_dobie_input(processed_course_description):
        """
        This function is used to format the proper Dobie input

        :param processed_course_description: processed course description
        :return: proper dobie input
        """
        course_description = {"tasks":
            [{
                "label": "95671c903a5b97a9",
                "jobDescription": processed_course_description
            }]
        }
        return course_description

    def get_fraction_requirements(self, idx):
        """
        This function is used to take fractions of courses dataframe then send data to Dobie

        :return: return dobie response
        """
        course_description = self.courses.iloc[idx]
        processed_descriptions = self.extractor.process_course_description(course_description)
        dobie_input = self.prepare_dobie_input(processed_descriptions)
        dobie_response = send_data_to_dobie(dobie_input)
        return dobie_response

    def pipe_dobie_results(self, idx, save=False, course_id='0'):
        """
        This function is used to take job posts fractions and handle Dobie Response output
        :param save: if True save file in CSV format
        :param course_name: filename to save results
        :return: None
        """
        dobie_response = self.get_fraction_requirements(idx)
        dobie_status_code = dobie_response.status_code

        print('Response from Dobie: {}'.format(dobie_status_code))
        if dobie_status_code == 200:
            output = dobie_response
            extracted_skills = handle_course_skill_annotation(output, course_id)

            if save:
                save_extracted_skills(extracted_skills, course_id)

    def execution_stage(self, save_in_file=False):
        """This is pipeline's execution stage"""

        courses_length = len(self.courses)

        for execution in range(0, courses_length-1):
            print('Course Id: {} '.format(self.courses.iloc[execution]['id']))
            self.pipe_dobie_results(execution, save=save_in_file, course_id=self.courses.iloc[execution]['id'])
            time.sleep(TIME_BETWEEN_REQUESTS)
