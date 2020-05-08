import json

import requests

from extraction_pipeline.execute_pipeline import Executor

if __name__ == "__main__":
    data = {
        "query": "bool_query",
        "index": "my_index",
        "min_score": 4,
        "_source": ["id"],
        "should": [
            {"multi_match": {
                "query": "ui/ux",
                "fields": ["title", "requirements"],
                "type": "phrase",
                "slop": 2}
            },
            {"multi_match": {
                "query": "ux/ui",
                "fields": ["title", "requirements"],
                "type": "phrase",
                "slop": 2}
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url='http://127.0.0.1:5000/ask/storage', headers=headers, data=json.dumps(data))
    job_post_ids = [res['_source']['id'] for res in response.json()]
    job_name = 'ui/ux designer'


    # job_post_ids = [1, 367, 363, 369, 372, 374, 376, 377, 378, 420, 437, 364, 366, 415, 1374, 6, 7, 368, 365, 371, 397,
    #                 370]
    executor = Executor(job_post_ids)
    executor.execution_stage(job_name=job_name)
