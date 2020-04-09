import urllib.parse

import requests

from settings import FUSEKI_SERVER_HOST, FUSEKI_SERVER_PORT, FUSEKI_SERVER_DATASET


class FusekiServer(object):
    def __init__(self):
        self.FUSEKI_SERVER_BASE_URL = "http://{}:{}".format(
            FUSEKI_SERVER_HOST,
            FUSEKI_SERVER_PORT
        )

    def query_fuseki_server(self, sparql_query):
        """
        This function is used to generate queries against SARO dataset

        :param sparql_query: provided SPARQL query
        :return: response from Fuseki Server
        """
        query_endpoint = urllib.parse.urljoin(
            self.FUSEKI_SERVER_BASE_URL,
            FUSEKI_SERVER_DATASET
        )

        params = {'query': sparql_query}
        response = requests.get(
            url=query_endpoint,
            params=params
        )
        return response

    def update_dataset(self, data):
        """
        This function is used to update SARO dataset

        :param data: provided data
        :return: response from Fuseki Server
        """
        headers = {'Content-Type': 'text/turtle;charset=utf-8'}
        update_data_endpoint = urllib.parse.urljoin(
            self.FUSEKI_SERVER_BASE_URL,
            "{}/{}".format(FUSEKI_SERVER_DATASET, "data?default")
        )
        response = requests.post(
            url=update_data_endpoint,
            headers=headers,
            data=data
        )
        return response
