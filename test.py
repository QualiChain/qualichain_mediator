import json
import math
import re
import time

import requests
import pandas as pd
from sqlalchemy import create_engine

stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


def remove_stop_words(txt):
    split_txt = txt.split()
    removed_txt = [word for word in split_txt if word not in stop_words]
    return " ".join(removed_txt)


def send_data_to_dobie(job_description):
    """
    This function sends a POST request to the skill annotation tool (Dobie) providing it with the proper input.
    :param payload_dict: The json file used as input for dobie.
    :return:
    Return response text
    Examples:
    >>>send_data_to_dobie({"tasks":[{"label":"95671c903a5b97a9", "jobDescription":"job_text"}]})

    """
    url = "http://{}:{}/annotate".format("qualichain.epu.ntua.gr", "9006")

    headers = {
        'Content-Type': "application/json",
        'Postman-Token': "53181693-dfea-47df-8a4e-2d7124aeb47a",
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST", url, data=json.dumps(job_description), headers=headers)
    return response


ENGINE_STRING = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format('admin', 'admin', 'qualichain.epu.ntua.gr', 5432,
                                                              'api_db')
TABLE = 'job_post'
engine = create_engine(ENGINE_STRING)

job_posts = pd.read_sql_query('SELECT requirements from "job_post"', engine)
job_posts_length = len(job_posts)

batch_size = 50
index = 0
executions = math.floor(job_posts_length / batch_size)

for execution in range(0, executions):
    print('Execution: {}'.format(execution))
    print('Job Posts Index: {}-{}'.format(index, index + batch_size))

    job_posts_fraction = job_posts.iloc[index:index + batch_size]

    raw_requirements = job_posts_fraction['requirements'].map(lambda x: re.sub(r"[^a-zA-Z0-9]+", ' ', x)).map(
        remove_stop_words)

    requirements = " ".join(raw_requirements)

    job_description = {"tasks":
        [{
            "label": "95671c903a5b97a9",
            "jobDescription": requirements
        }]
    }

    dobie_response = send_data_to_dobie(job_description)
    print(dobie_response.text)

    index = index + 50
    time.sleep(10)
