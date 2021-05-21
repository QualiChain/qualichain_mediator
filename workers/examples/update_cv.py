import json

import pika

cv_payload = {"cv":
    {
        "label": "CVTest",
        "uri": ":CV5235",
        "id": "CV5235",
        "comment": "Update CV test 3",
        "title": "Updated CV through API",
        "personURI": ":19",
        "userID": "19",
        "targetSector": "SectorOfChoice",
        "description": "It is an update test CV",
        "realocationInfo": "Not available for realocation",
        "skills": [
            {
                "label": "Java",
                "comment": "Skill comment 1",
                "proficiencyLevel": "basic",
                "coreTo": None,
                "isFrom": None,
                "skillType": None,
                "uri": "saro:Skill_1",
                "id": "Skill_1"
            }
        ],
        "workHistory": [
            {
                "label": "workHistoryCVInsertTest1",
                "comment": "Extra comment if necessary",
                "position": "Position at the company",
                "employer": "Name of the organisation worked at",
                "description": "Description of the work done at the company",
                "jobReference": ":JobURI",
                "jobType": "Maybe used for Sector description of Sector URI later on",
                "from": "11/12/10",
                "to": "01/01/15",
                "duration": "Aproximately 4 years",
                "uri": "cv:whworkHistoryCVInsertTest1",
                "id": "whworkHistoryCVInsertTest1"
            }
        ]
    },
    "status": "update"
}

cv_payload_json = json.dumps(cv_payload)

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
channel.basic_publish(exchange='', routing_key=QUEUE, body=cv_payload_json)

connection.close()
