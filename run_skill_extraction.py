from clients.postgres_client import PostgresClient
from extraction_pipeline.execute_pipeline import Executor
from settings import JOB_NAMES, SAVE_IN_FILE
from utils import query_creator

if __name__ == "__main__":
    # try:

    print("Initialize Table extracted_skill", flush=True)

    pg_client = PostgresClient()
    pg_client.initialize_extracted_skills_model()

    for key in JOB_NAMES.keys():

        print("Extract skills for: {}".format(key), flush=True)
        job_post_ids = query_creator(JOB_NAMES[key], key)
        print(job_post_ids)

        if job_post_ids:
            executor = Executor(job_post_ids)
            executor.execution_stage(job_name=key, save_in_file=SAVE_IN_FILE)
        break

    # except Exception as ex:
    #     print(ex, flush=True)
