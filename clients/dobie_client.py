import json

import requests
from requests.auth import HTTPBasicAuth
from rdflib import Graph
from requests.auth import HTTPBasicAuth

from settings import DOBIE_HOST, DOBIE_PASS, DOBIE_USERNAME
from settings import DOBIE_HOST, DOBIE_PORT, DOBIE_V2_SETTINGS


def send_data_to_dobie(job_description):
    """
    This function sends a POST request to the skill annotation tool (Dobie) providing it with the proper input.

    :param payload_dict: The json file used as input for dobie.
    :return: Return response text
    Examples:
        >>>send_data_to_dobie({"tasks":[{"label":"95671c903a5b97a9", "jobDescription":"job_text"}]})

    """
    url = "http://{}:{}/annotate".format(DOBIE_HOST, DOBIE_PORT)

    headers = {
        'Content-Type': "application/json",
        'Postman-Token': "53181693-dfea-47df-8a4e-2d7124aeb47a",
        'Cache-Control': "no-cache"
    }

    jsonified_data = json.dumps(job_description)
    response = requests.request("POST", url, data=jsonified_data, headers=headers)
    return response


def dobie_second_version(job_description):
    """This function implements a call to Dobie V2"""

    dobie_v2_url = 'https://demo.iais.fraunhofer.de/dobie/jsonData/jobPostNTUA'
    password = '5UxLtwaeJ8fK'
    user = DOBIE_V2_SETTINGS['user']

    headers = {
        "Content-Type": "application/json"
    }
    jsonified_data = json.dumps(job_description)

    response = requests.request(
        "POST",
        dobie_v2_url,
        data=jsonified_data,
        headers=headers,
        auth=HTTPBasicAuth(user, password)
    )
    return response
