from extraction_pipeline.execute_pipeline import Executor
from settings import JOB_NAMES
from utils import query_creator

if __name__ == "__main__":
    try:

        save_in_file = False
        for key in JOB_NAMES.keys():

            print("Extract skills for: {}".format(key), flush=True)
            job_post_ids = query_creator(JOB_NAMES[key], key)

            if job_post_ids:
                executor = Executor(job_post_ids)
                executor.execution_stage(job_name=key, save_in_file=save_in_file)

    except Exception as ex:
        print(ex, flush=True)
