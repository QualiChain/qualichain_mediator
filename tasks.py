from celery import Celery

from clients.dobie_client import send_data_to_dobie
from clients.fuseki_server import FusekiServer

app = Celery('qualichain_mediator')
app.config_from_object('settings', namespace='CELERY_')


@app.task()
def send_dobie_input(message):
    """
    This task is used to received job posting text and feed DOBIE component
    """
    extracted_skills = send_data_to_dobie(message)
    print(extracted_skills, flush=True)
    return extracted_skills


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
