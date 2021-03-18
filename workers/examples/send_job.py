import json

import pika

job = {
    "label": "Test JobPosting New",
    "comment": None,
    "creator_id": "6",
    "jobDescription": "Job Description N",
    "contractType": "full_time",
    "sector": "Backend Developer",
    "occupation": "Blockchain Engineer",
    "listingOrganization": "Listing Organization 2",
    "hiringOrganization": "Hiring Organization 2",
    "jobLocation": "Location N",
    "country": "Greece",
    "state": "Attica",
    "city": "Athens",
    "startDate": "2021-03-05",
    "endDate": "2024-03-04",
    "seniorityLevel": "intermediate",
    "expectedSalary": None,
    "salaryCurrency": None,
    "uri": ":3995",
    "id": "5997",
    "skillReq": [
        {
            "label": "PHP",
            "comment": "Skill comment 9",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [
                ":Skill_4"
            ],
            "subClasses": [],
            "skillURI": ":Skill_9",
            "skillID": "Skill_9",
            "proficiencyLevel": "basic",
            "priorityLevel": "low",
            "uri": ":ida8aea504-5462-4e58-973d-3714306b1005",
            "id": "ida8aea504-5462-4e58-973d-3714306b1005"
        },
        {
            "label": "Javascript",
            "comment": "Skill comment 7",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [
                ":Skill_1",
                ":Skill_4"
            ],
            "subClasses": [
                ":Skill_13",
                ":Skill_5"
            ],
            "skillURI": ":Skill_7",
            "skillID": "Skill_7",
            "proficiencyLevel": "basic",
            "priorityLevel": "low",
            "uri": ":id274e442d-75cf-47fe-b22e-4a47e0056cb6",
            "id": "id274e442d-75cf-47fe-b22e-4a47e0056cb6"
        },
        {
            "label": "Python",
            "comment": "Skill comment 2",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [
                ":Skill_4"
            ],
            "subClasses": [],
            "skillURI": ":Skill_2",
            "skillID": "Skill_2",
            "proficiencyLevel": "basic",
            "priorityLevel": "low",
            "uri": ":idd03a7549-7812-465d-bac6-7a8bc52f3b56",
            "id": "idd03a7549-7812-465d-bac6-7a8bc52f3b56"
        },
        {
            "label": "C++",
            "comment": "Skill comment 3",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [
                ":Skill_4"
            ],
            "subClasses": [],
            "skillURI": ":Skill_3",
            "skillID": "Skill_3",
            "proficiencyLevel": "basic",
            "priorityLevel": "low",
            "uri": ":idd1cb6c5d-4ace-4914-bdc5-eec820f3d299",
            "id": "idd1cb6c5d-4ace-4914-bdc5-eec820f3d299"
        },
        {
            "label": "Blockchain",
            "comment": "Skill comment 8",
            "coreTo": None,
            "isFrom": None,
            "skillType": None,
            "reuseLevel": None,
            "synonyms": [],
            "superClasses": [],
            "subClasses": [],
            "skillURI": ":Skill_8",
            "skillID": "Skill_8",
            "proficiencyLevel": "basic",
            "priorityLevel": "low",
            "uri": ":id130ccddf-b87b-4fd8-99f0-317157901a76",
            "id": "id130ccddf-b87b-4fd8-99f0-317157901a76"
        }
    ],
    "workExperienceReq": [],
    "coursesReq": [],
    "educationReq": []
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
