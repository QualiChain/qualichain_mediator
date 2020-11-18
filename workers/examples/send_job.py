import json

import pika

job = {
    "label": "Data Scientist",
    "comment": "JobPosting Comment 5",
    "creator_id": "5",
    "jobDescription": "Job Description 5",
    "contractType": "full_time",
    "sector": "Backend Developer",
    "occupation": "Blockchain Engineer",
    "country": "Greece",
    "state": "Attica",
    "city": "Athens",
    "startDate": "2020-01-01",
    "endDate": "2022-01-01",
    "seniorityLevel": "intermediate",
    "expectedSalary": None,
    "salaryCurrency": None,
    "skillReqURIs": [
        "cv:Skill_10",
        "cv:Skill_6",
        "cv:Skill_8"
    ],
    "skillReq": [
        {
            "label": "C#",
            "comment": "Skill comment 10",
            "proficiencyLevel": "basic",
            "priorityLevel": "high",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [
                "<http://rdfs.org/resume-rdf/cv.rdfs#Skill_4>"
            ],
            "subClasses": [],
            "uri": "cv:Skill_10",
            "id": "Skill_10"
        },
        {
            "label": "Angular",
            "comment": "Skill comment 6",
            "proficiencyLevel": "basic",
            "priorityLevel": "high",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [
                "<http://rdfs.org/resume-rdf/cv.rdfs#Skill_4>"
            ],
            "subClasses": [],
            "uri": "cv:Skill_6",
            "id": "Skill_6"
        },
        {
            "label": "Blockchain",
            "comment": "Skill comment 8",
            "proficiencyLevel": "basic",
            "priorityLevel": "high",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [],
            "subClasses": [],
            "uri": "cv:Skill_8",
            "id": "Skill_8"
        }
    ],
    "workExperienceReq": [],
    "educationReq": [],
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
    "hiringOrg": "Hiring Organization 2",
    "listingOrg": "Listing Organization 2",
    "capabilityReq": [],
    "jobSkillReqLabels": [
        "C#",
        "Angular",
        "Blockchain"
    ],
    "uri": "saro:Job1",
    "id": "Job1"
}
job_payload = {'job': job}
job_json_obj = json.dumps(job_payload)

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
channel.basic_publish(exchange='', routing_key=QUEUE, body=job_json_obj)

connection.close()

