import json

import requests

from extraction_pipeline.execute_pipeline import Executor
from settings import JOB_NAMES, QUERY_EXECUTOR_URL
from utils import query_creator

if __name__ == "__main__":
    for key in JOB_NAMES.keys():
        data, headers = query_creator(JOB_NAMES[key])

        response = requests.post(url=QUERY_EXECUTOR_URL, headers=headers, data=json.dumps(data))
        job_post_ids = [res['_source']['id'] for res in response.json()]
        job_name = key


        # job_post_ids = [1, 367, 363, 369, 372, 374, 376, 377, 378, 420, 437, 364, 366, 415, 1374, 6, 7, 368, 365, 371, 397,
        #                 370]
        executor = Executor(job_post_ids)
        executor.execution_stage(job_name=job_name, save_in_file=True)
