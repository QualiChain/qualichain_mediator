import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from clients.rabbitmq_client import RabbitMQClient

from settings import APP_QUEUE

if __name__ == "__main__":
    rabbit_mq = RabbitMQClient()

    cv_payload = {
        "label": "Test CV 5",
        "comment": "Comment 5",
        "title": "CV Title 5",
        "personURI": "qc:3",
        "description": "Description 5",
        "targetSector": "Sector 2",
        "otherInfo": None,
        "currentJob": None,
        "workHistory": [],
        "education": [],
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
        "uri": "saro:Job2",
        "id": "Job2"
    }

    job_application = {
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

    payload = {'job': job}

    rabbit_mq.producer(queue=APP_QUEUE, message=json.dumps(payload))
