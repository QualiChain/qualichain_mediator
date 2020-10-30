import json

import requests
from requests.auth import HTTPBasicAuth

from settings import DOBIE_HOST, DOBIE_PASS, DOBIE_USERNAME


def send_data_to_dobie(job_description):
    """
    This function sends a POST request to the skill annotation tool (Dobie) providing it with the proper input.
    :param payload_dict: The json file used as input for dobie.
    :return:
    Return response text
    Examples:
    >>>send_data_to_dobie({"tasks":[{"label":"95671c903a5b97a9", "jobDescription":"job_text"}]})

    """
    url = "https://{}/dobie/jsonData/jobPostNTUA".format(DOBIE_HOST)

    headers = {
        'Authorization': 'Basic dXNlcjo1VXhMdHdhZUo4Zks=',
        'Content-Type': 'application/json'
    }
    print(job_description)
    jsonified_data = json.dumps(job_description)
    response = requests.request('POST', url, headers=headers, data=jsonified_data)
    return response
