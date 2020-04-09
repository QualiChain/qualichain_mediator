import json

import requests

from clients.fuseki_server import FusekiServer
from settings import DOBIE_HOST, DOBIE_PORT
from utils import parse_dobie_response

fuseki = FusekiServer()



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

job_description = {"tasks":
                       [{
                           "label":"95671c903a5b97a9",
                           "jobDescription": "Linux, Matlab, Python, C++, C#, computer science, office365, sql server 2008, .Net"
                       }]
}
dobie_extracted_skills = send_data_to_dobie(job_description).text

skills = parse_dobie_response(dobie_extracted_skills)

if skills:
    print(skills)
    response = fuseki.update_dataset(skills)
    print(response.reason)
    print(response.status_code)