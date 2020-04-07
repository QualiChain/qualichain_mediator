import requests
import urllib.parse

from settings import FUSEKI_SERVER_HOST, FUSEKI_SERVER_PORT, FUSEKI_SERVER_DATASET


def query_fuseki_server(sparql_query):
    """
    This function is used to generate queries against SARO dataset

    :param sparql_query: provided SPARQL query
    :return: SPARQL query output
    """
    FUSEKI_SERVER_BASE_URL = "http://{}:{}".format(
        FUSEKI_SERVER_HOST,
        FUSEKI_SERVER_PORT
    )
    query_endpoint = urllib.parse.urljoin(
        FUSEKI_SERVER_BASE_URL,
        FUSEKI_SERVER_DATASET
    )
    params = {'query': sparql_query}
    response = requests.get(url=query_endpoint, params=params)
    # print(response.json())


sparql_query = """SELECT ?subject ?predicate ?object
WHERE {
  ?subject ?predicate ?object
}
LIMIT 100000"""

query_fuseki_server(sparql_query)


def update_dataset(data):
    """
    This function is used to update SARO dataset

    :param data: provided data
    :return: response from Fuseki Server
    """
    headers = {'Content-Type': 'text/turtle;charset=utf-8'}
    FUSEKI_SERVER_BASE_URL = "http://{}:{}".format(
        FUSEKI_SERVER_HOST,
        FUSEKI_SERVER_PORT
    )
    update_data_endpoint = urllib.parse.urljoin(
        FUSEKI_SERVER_BASE_URL,
        "{}/{}".format(FUSEKI_SERVER_DATASET,"data?default")
    )
    response = requests.post(
        url=update_data_endpoint,
        headers=headers,
        data=data
    )
    return response


data = """
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix saro: <http://w3id.org/saro#> .
@prefix esco: <http://data.europa.eu/esco/model#> .

saro:netty a saro:Product ;
	 saro:icCoreTo saro:ICT ;
	 rdfs:label "netty" .

saro:rdbms a saro:Topic ;
	 saro:icCoreTo saro:ICT ;
	 rdfs:label "rdbms" .

saro:rubyOnRails a saro:Tool ;
	 saro:icCoreTo saro:ICT ;
	 rdfs:label "ruby on rails" ."""

update_dataset(data)