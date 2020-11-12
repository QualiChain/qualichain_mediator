import time

import nltk
from nltk import tokenize

from clients.postgres_client import PostgresClient
from decorators import retry

nltk.download('punkt')

from clients.dobie_client import dobie_second_version
from extraction_pipeline.courses.courses_extraction_pipeline import CourseExtractor, SkillExtractor
from settings import NUM_OF_CHUKS, TIME_BETWEEN_CHUNKS
from utils import save_extracted_skills, handle_course_skill_annotation, chunkify


class CourseSkillExtractionExecutor(object):

    def __init__(self, courses_ids):
        self.index = 0
        self.extractor = CourseExtractor()
        self.courses = self.extractor.get_courses(ids=courses_ids)
        self.skill_extractor = SkillExtractor()

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

    def get_fraction_requirements(self, text, course_name):
        """
        This function is used to take fractions of courses dataframe then send data to Dobie

        :return: return dobie response
        """
        # course_description = self.courses.iloc[idx]
        processed_descriptions = self.extractor.process_course_description(text, course_name)
        dobie_input = self.prepare_dobie_input(processed_descriptions)
        dobie_response = dobie_second_version(dobie_input)
        return dobie_response

    def pipe_dobie_results(self, text, course_name, save=False, course_id='0'):
        """
        This function is used to take job posts fractions and handle Dobie Response output
        :param save: if True save file in CSV format
        :param course_name: filename to save results
        :return: None
        """
        dobie_response = self.get_fraction_requirements(text, course_name)
        dobie_status_code = dobie_response.status_code

        print('Response from Dobie: {}'.format(dobie_status_code))
        if dobie_status_code == 200:
            output = dobie_response
            extracted_skills = handle_course_skill_annotation(output, course_id)

            if save:
                save_extracted_skills(extracted_skills, course_id)
            return extracted_skills

    def store_chunk_skills(self, list_of_skills, course_id):
        """This function is used to store skills extracted from chunks"""
        unique_skills = list(set(list_of_skills))
        postgres_client = PostgresClient()

        for skill in unique_skills:

            skill_lowercase = skill.lower()
            skill_obj = self.skill_extractor.get_skills(skill_lowercase)

            if not skill_obj.empty:
                skill_id = skill_obj.iloc[0]['id']
                postgres_client.upsert_new_skill_per_course(
                    course_id=int(course_id),
                    skill_id=int(skill_id)
                )

        postgres_client.session.close()

    @retry(exception=Exception, n_tries=20, delay=15)
    def iterate(self, execution):

        course = self.courses.iloc[execution]
        course_id = course['id']
        course_name = course['name']
        print('Course Id: {} '.format(course_id))

        sentences = tokenize.sent_tokenize(course['description'])
        chunks = chunkify(sentences, NUM_OF_CHUKS)

        skills_of_chunks = []
        for chunk in chunks:
            joined_chunk = " ".join(chunk)
            extracted_skills = self.pipe_dobie_results(joined_chunk, course_name, course_id=course_id)
            skills_of_chunks = skills_of_chunks + extracted_skills
            time.sleep(TIME_BETWEEN_CHUNKS)

        self.store_chunk_skills(skills_of_chunks, course_id)
