import json

import pika

job_payload = {"job":
    {
        "label": "Test JobPosting New Creator ID test",
        "comment": None,
        "jobDescription": "Job Description N",
        "contractType": "Full-time",
        "specialization": "Something something created",
        "sector": "Backend Developer",
        "country": "Greece",
        "state": "Attica",
        "hiringOrg": "Hiring Organization 2",
        "city": "Athens", "creator_id": "6",
        "occupation": "Blockchain Engineer",
        "startDate": "2021-03-05",
        "endDate": "2024-03-04",
        "seniorityLevel": "intermediate",
        "expectedSalary": "1200",
        "salaryCurrency": "Euro",
        "uri": ":2007",
        "id": "2007",
        "skills": [
            {
                "label": "PHP",
                "comment": "Skill comment 9",
                "uri": "saro:Skill_9",
                "id": "Skill_9",
                "proficiencyLevel": "basic",
                "priorityLevel": "low",
                "coreTo": None,
                "isFrom": None,
                "skillType": None
            },
            {
                "label": "Javascript",
                "comment": "Skill comment 7",
                "uri": "saro:Skill_7",
                "id": "Skill_7",
                "proficiencyLevel": "basic",
                "priorityLevel": "low",
                "coreTo": None,
                "isFrom": None,
                "skillType": None
            },
            {
                "label": "C++",
                "comment": "Skill comment 3",
                "uri": "saro:Skill_3",
                "id": "Skill_3",
                "proficiencyLevel": "basic",
                "priorityLevel": "low",
                "coreTo": None,
                "isFrom": None,
                "skillType": None
            },
            {
                "label": "Blockchain",
                "comment": "Skill comment 8",
                "uri": "saro:Skill_8",
                "id": "Skill_8",
                "proficiencyLevel": "basic",
                "priorityLevel": "low",
                "coreTo": None,
                "isFrom": None,
                "skillType": None
            },
            {
                "label": "Python",
                "comment": "Skill comment 2",
                "uri": "saro:Skill_2",
                "id": "Skill_2",
                "proficiencyLevel": "basic",
                "priorityLevel": "low",
                "coreTo": None,
                "isFrom": None,
                "skillType": None
            },
            {
                "label": "Angular",
                "comment": "Skill comment 6",
                "uri": "saro:Skill_6",
                "id": "Skill_6",
                "proficiencyLevel": "advanced",
                "priorityLevel": "low",
                "coreTo": None,
                "isFrom": None,
                "skillType": None
            }
        ]
    },
    "status": "update"
}
cv_payload_json = json.dumps(job_payload)

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
