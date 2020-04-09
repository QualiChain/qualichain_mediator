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
                           "jobDescription": "Moving Mobility Forward Aptiv is making mobility real. We are at the forefront of solving mobility toughest challenges. We have the people, experience, know-how and confidence to turn ideas into solutions. Solutions that move our world from what now to what next, while connecting us like never before. To us, nothing is impossible when you have the people with the passion to make anything possible. Mobility has the power to change the world, and we have the power to change mobility. Join our Innovative Team. Want to do more than just imagine the ways our world will move tomorrow? Here your opportunity. Join the technology company that is transforming the future of mobility today. About Aptiv Aptiv is a global technology company that develops safer, greener and more connected solutions, which enable the future of mobility. Matlab, Python, Linux, C++   "
                       }]
}
dobie_extracted_skills = send_data_to_dobie(job_description).text
skills = parse_dobie_response(dobie_extracted_skills)

if skills:
    fuseki.update_dataset(skills)