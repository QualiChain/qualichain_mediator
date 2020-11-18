import json

import pika

job_application = {
    "label": None,
    "comment": None,
    "personURI": "qc:1",
    "jobURI": "saro:Job1",
    "expectedSalary": "1200",
    "salaryCurrency": "Euro",
    "availability": "01/01/21",
    "uri": "qc:app5",
    "id": "app5"
}

job_application_payload = {'job_application': job_application}
job_application_json_obj = json.dumps(job_application_payload)

RABBITMQ_USER = 'rabbitmq'
RABBITMQ_PASSWORD = 'rabbitmq'
RABBITMQ_VHOST = '/'
RABBITMQ_HOST = 'qualichain.epu.ntua.gr'
RABBITMQ_PORT = 5672
EXCHANGE = ''
QUEUE = 'analytics_consumer'

user_credentials = pika.PlainCredentials(
    username=RABBITMQ_USER,
    password=RABBITMQ_PASSWORD
)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    virtual_host=RABBITMQ_VHOST,
    credentials=user_credentials
))
channel = connection.channel()

channel.queue_declare(queue=QUEUE)
channel.basic_publish(exchange='', routing_key=QUEUE, body=job_application_json_obj)

connection.close()
