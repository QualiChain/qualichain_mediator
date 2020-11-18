import os
import sys
import time

from decorators import retry

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from clients.postgres_client import PostgresClient
from extraction_pipeline.job_posts.execute_pipeline import Executor
from settings import JOB_NAMES, SAVE_IN_FILE
from utils import query_creator


@retry(exception=Exception, n_tries=20, delay=15)
def job_extraction_runner(key, postgres_client):
    postgres_client.delete_job_skill(job=key)

    print("Extract skills for: {}".format(key), flush=True)
    job_post_ids = query_creator(JOB_NAMES[key], key)
    print(job_post_ids)

    if job_post_ids:
        executor = Executor(job_post_ids)
        executor.execution_stage(job_name=key, save_in_file=SAVE_IN_FILE)


if __name__ == "__main__":

    print("Initialize Table extracted_skill", flush=True)

    pg_client = PostgresClient()
    pg_client.initialize_extracted_skills_model()

    for key in JOB_NAMES.keys():
        job_extraction_runner(key, pg_client)
        time.sleep(15)

    # except Exception as ex:
    #     print(ex, flush=True)
