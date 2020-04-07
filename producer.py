from clients.rabbitmq_client import RabbitMQClient
import json

from settings import APP_QUEUE

if __name__ == "__main__":
    rabbit_mq = RabbitMQClient()

    # payload = {
    #     "component": "QE",
    #     "message": {
    #         "tasks": [
    #             {
    #                 "label": "95671c903a5b97a9",
    #                 "jobDescription": "Moving Mobility Forward Aptiv is making mobility real. We are at the forefront of solving mobility toughest challenges. We have the people, experience, know-how and confidence to turn ideas into solutions. Solutions that move our world from what now to what next, while connecting us like never before. To us, nothing is impossible when you have the people with the passion to make anything possible. Mobility has the power to change the world, and we have the power to change mobility. Join our Innovative Team. Want to do more than just imagine the ways our world will move tomorrow? Here your opportunity. Join the technology company that is transforming the future of mobility today. About Aptiv Aptiv is a global technology company that develops safer, greener and more connected solutions, which enable the future of mobility."
    #             }
    #         ]
    #     }
    # }

    data = """
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix saro: <http://w3id.org/saro#> .
    @prefix esco: <http://data.europa.eu/esco/model#> .

    saro:netty a saro:Product ;
    	 saro:icCoreTo saro:ICT ;
    	 rdfs:label "netty" .

    saro:rdbms a saro:Topic ;
    	 saro:icCoreTo saro:ICT ;
    	 rdfs:label "rdbms" .

    saro:rubyOnRails a saro:Tool ;
    	 saro:icCoreTo saro:ICT ;
    	 rdfs:label "ruby on rails" ."""

    payload = {
        "component": "QE",
        "message": {
            "query": data
        }
    }
    rabbit_mq.producer(queue=APP_QUEUE, message=json.dumps(payload))
