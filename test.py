import json
import math
import re
import time

import requests
import pandas as pd
from sqlalchemy import create_engine

from clients.dobie_client import send_data_to_dobie
from settings import ENGINE_STRING
from utils import remove_stop_words

engine = create_engine(ENGINE_STRING)

job_posts = pd.read_sql_query('SELECT requirements from "job_post"', engine)
job_posts_length = len(job_posts)

batch_size = 50
index = 0
executions = math.floor(job_posts_length / batch_size)
executions_modulo = job_posts_length - executions*batch_size
print(executions_modulo)

##########

# job_posts_length = len(job_posts)
# index = 0
#
# number_of_executions = math.floor(job_posts_length / BATCH_SIZE)
# executions_modulo = job_posts_length - number_of_executions * BATCH_SIZE
#
# for execution in range(0, number_of_executions):
#     START = index
#     STOP = index + BATCH_SIZE
#
#     print('Execution No: {}'.format(execution))
#     print('Job posts Index Range: {}-{}').format(START, STOP)
#
#     job_posts_fraction = job_posts.iloc[START:STOP]

#########

# for execution in range(0, executions):
#     print('Execution: {}'.format(execution))
#     print('Job Posts Index: {}-{}'.format(index, index + batch_size))
#
#     job_posts_fraction = job_posts.iloc[index:index + batch_size]
#
#     raw_requirements = job_posts_fraction['requirements'].map(lambda x: re.sub(r"[^a-zA-Z0-9]+", ' ', x)).map(
#         remove_stop_words)
#
#     requirements = " ".join(raw_requirements)
#
#     job_description = {"tasks":
#         [{
#             "label": "95671c903a5b97a9",
#             "jobDescription": requirements
#         }]
#     }
#
#     dobie_response = send_data_to_dobie(job_description)
#     print(dobie_response.text)
#
#     index = index + 50
#     time.sleep(10)
