import math
import time

import pandas
from bs4 import BeautifulSoup

from clients.dobie_client import send_data_to_dobie, dobie_second_version
from extraction_pipeline.job_post_extraction_pipeline import JobPostSkillExtractor
from settings import BATCH_SIZE, TIME_BETWEEN_REQUESTS, QUALICHAIN_DB_ENGINE_STRING
from tasks import extract_skills_async
from utils import handle_raw_annotation, save_extracted_skills, translate_v2dobie_output


class Executor(object):

    def __init__(self, job_post_ids):
        self.index = 0
        self.extractor = JobPostSkillExtractor()
        self.job_posts = self.extractor.get_job_posts(ids=job_post_ids)
        self.qualichain_skills = pandas.read_sql_table('skills', QUALICHAIN_DB_ENGINE_STRING)

    @staticmethod
    def calculate_execution(job_posts_length):
        """
        This function is used to calculate number of executions

        :param job_posts_length: job posts length
        :return:
        """
        number_of_executions = math.floor(job_posts_length / BATCH_SIZE)
        integral_executions = number_of_executions * BATCH_SIZE
        executions_modulo = job_posts_length - integral_executions
        return number_of_executions, integral_executions, executions_modulo

    @staticmethod
    def prepare_dobie_input(processed_requirements):
        """
        This function is used to format the proper Dobie input

        :param processed_requirements: processed requirements
        :return: proper dobie input
        """
        job_description = {"tasks":
            [{
                "label": "95671c903a5b97a9",
                "jobDescription": processed_requirements
            }]
        }
        return job_description

    def get_fraction_requirements(self, START, STOP):
        """
        This function is used to take fractions of job post dataframe according to START, STOP indices
        then send data to Dobie

        :param START: START index
        :param STOP: STOP index
        :return: return dobie response
        """
        job_posts_fraction = self.job_posts.iloc[START:STOP]
        processed_requirements = self.extractor.process_job_requirements(job_posts_fraction)

        dobie_input = self.prepare_dobie_input(processed_requirements)
        dobie_response = dobie_second_version(dobie_input)
        # dobie_response = send_data_to_dobie(dobie_input)
        return dobie_response

    def pipe_dobie_results(self, START, STOP, save=False, job_name='sample_job_name'):
        """
        This function is used to take job posts fractions and handle Dobie Response output
        :param START: START index
        :param STOP: STOP index
        :param save: if True save file in CSV format
        :param job_name: filename to save results
        :return: None
        """
        dobie_response = self.get_fraction_requirements(START, STOP)
        dobie_status_code = dobie_response.status_code

        print('Response from Dobie: {}'.format(dobie_status_code))
        if dobie_status_code == 200:
            output = dobie_response.text
            skill_results = translate_v2dobie_output(output, job_name)
            print(skill_results)
        else:
            print("Dobie status code: {}".format(dobie_status_code))
            # extracted_skills = handle_raw_annotation(output, job_name)

            # if save:
            #     save_extracted_skills(extracted_skills, job_name)

    def execution_stage(self, job_name, save_in_file=False):
        """This is pipeline's execution stage"""
        index = 0

        job_posts_length = len(self.job_posts)
        number_of_executions, integral_executions, executions_modulo = self.calculate_execution(job_posts_length)

        for execution in range(0, number_of_executions):
            START = index
            STOP = index + BATCH_SIZE

            print('Execution No: {}'.format(execution))
            print('Job posts Index Range: {}-{}'.format(START, STOP))
            self.pipe_dobie_results(START, STOP, save=save_in_file, job_name=job_name)

            index = index + BATCH_SIZE
            time.sleep(TIME_BETWEEN_REQUESTS)
            break

        if executions_modulo:
            START = integral_executions
            STOP = job_posts_length

            print('Last Execution')
            print('Job posts Index Range: {}-{}'.format(START, STOP))
            self.pipe_dobie_results(START, STOP, save=save_in_file, job_name=job_name)
