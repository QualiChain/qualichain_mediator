from celery import Celery

from clients.dobie_client import send_data_to_dobie
from clients.fuseki_server import FusekiServer
from utils import parse_dobie_response

app = Celery('qualichain_mediator')
app.config_from_object('settings', namespace='CELERY_')


@app.task()
def send_dobie_input(message):
    """
    This task is used to received job posting text and feed DOBIE component
    """
    fuseki_server = FusekiServer()
    dobie_response = send_data_to_dobie(message)

    if dobie_response.status_code == 200:

        extracted_skills_xml = dobie_response.text
        saro_data = parse_dobie_response(extracted_skills_xml)

        if saro_data:
            fuseki_server.update_dataset(saro_data)


@app.task()
def query_fuseki_async(message):
    """
    This function is used to query fuseki server
    """
    sparql_query = message["query"]

    fuseki = FusekiServer()
    response = fuseki.query_fuseki_server(sparql_query)

    if response.status_code == 200:
        print(response.json(), flush=True)
    else:
        print("some error occurred", flush=True)
