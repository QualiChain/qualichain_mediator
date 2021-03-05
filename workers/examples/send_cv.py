import json

import pika

cv = {
    "label": "Test CV 5",
    "comment": "Comment 5",
    "title": "CV Title 5",
    "personURI": "qc:1",
    "description": "Description 5",
    "targetSector": "Sector 2",
    "otherInfo": None,
    "currentJob": None,
    "userID": 2,
    "workHistory": [],
    "courses": [],
    "skills": [
        {
            "label": "Angularjs",
            "comment": "Skill comment 13",
            "proficiencyLevel": "basic",
            "priorityLevel": "high",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [
                "<http://rdfs.org/resume-rdf/cv.rdfs#Skill_4>",
                "<http://rdfs.org/resume-rdf/cv.rdfs#Skill_7>"
            ],
            "subClasses": [],
            "uri": "cv:Skill_13",
            "id": "Skill_13"
        },
        {
            "label": "Machine Learning",
            "comment": "Skill comment 14",
            "proficiencyLevel": "basic",
            "priorityLevel": "high",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [],
            "subClasses": [],
            "uri": "cv:Skill_14",
            "id": "Skill_14"
        },
        {
            "label": "Neural Network",
            "comment": "Skill comment 15",
            "proficiencyLevel": "advanced",
            "priorityLevel": "high",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [],
            "subClasses": [],
            "uri": "cv:Skill_15",
            "id": "Skill_15"
        }
    ],
    "skillURIs": [
        "cv:Skill_13",
        "cv:Skill_14",
        "cv:Skill_15"
    ],
    "applications": [
        {
            "label": None,
            "comment": None,
            "personURI": "qc:5",
            "jobURI": "saro:Job5",
            "expectedSalary": "1200",
            "salaryCurrency": "Euro",
            "availability": "01/01/21",
            "uri": "qc:app5",
            "id": "app5"
        }
    ],
    "info": "URI: cv:id5\nLabel: Test CV 5\nPerson: qc:5",
    "uri": "cv:id5",
    "id": "id5"
}
cv_payload = {'cv': cv}
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
