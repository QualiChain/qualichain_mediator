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
#   POSTGRES SETTINGS
# =================================

POSTGRES_USER = os.environ.get('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'admin')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'qualichain.epu.ntua.gr')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'api_db')


ENGINE_STRING = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB
)

JOB_POSTS_TABLE = 'job_posts'

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

STOP_WORDS = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

# =================================
#   CELERY SETTINGS
# =================================
CELERY_BROKER_URL = 'pyamqp://{}:{}@{}:{}/{}'.format(
    RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST)

CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_ACKS_LATE = True
