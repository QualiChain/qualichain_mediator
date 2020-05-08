import json

import requests

from extraction_pipeline.execute_pipeline import Executor
from settings import JOB_NAMES, QUERY_EXECUTOR_URL
from utils import query_creator

if __name__ == "__main__":
    for key in JOB_NAMES.keys():
        job_post_ids = query_creator(JOB_NAMES[key], key)
        executor = Executor(job_post_ids)
        executor.execution_stage(job_name=key, save_in_file=True)
