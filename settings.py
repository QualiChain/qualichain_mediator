import os

# =================================
#   DOBIE SETTINGS
# =================================
DOBIE_HOST = os.environ.get('DOBIE_HOST', 'qualichain.epu.ntua.gr')
DOBIE_PORT = os.environ.get('DOBIE_PORT', 9006)


# =================================
#   FUSEKI SERVER SETTINGS
# =================================
FUSEKI_SERVER_HOST = os.environ.get('FUSEKI_SERVER_HOST', 'localhost')
FUSEKI_SERVER_PORT = os.environ.get('FUSEKI_SERVER_PORT', 3030)
FUSEKI_SERVER_DATASET = os.environ.get('FUSEKI_SERVER_DATASET', 'saro')

# =================================
#   RABBITMQ SETTINGS
# =================================
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'qualichain.epu.ntua.gr')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', 5672)
RABBITMQ_VHOST = os.environ.get('RABBITMQ_VHOST', '/')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'rabbitmq')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'rabbitmq')

# =================================
#   APPLICATION SETTINGS
# =================================
APP_QUEUE = os.environ.get('APP_QUEUE', "mediator_queue")

SARO_SKILL = """saro:{meta_value} a saro:{Kind} ;
	 saro:icCoreTo saro:ICT ;
	 rdfs:label "{String}" .
	 
	 """

SARO_PREFIXES = """
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix saro: <http://w3id.org/saro#> .
@prefix esco: <http://data.europa.eu/esco/model#> .

"""


# =================================
#   CELERY SETTINGS
# =================================
CELERY_BROKER_URL = 'pyamqp://{}:{}@{}:{}/{}'.format(
    RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST)

CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_ACKS_LATE = True
