from clients.rabbitmq_client import RabbitMQClient
import json

from settings import APP_QUEUE

if __name__ == "__main__":
    rabbit_mq = RabbitMQClient()

    payload = {
        "component": "DOBIE",
        "message": {
            "tasks": [
                {
                    "label": "95671c903a5b97a9",
                    "jobDescription": "memcached, win32, pig,  rdf, linear programming"
                }
            ]
        }
    }

#     data = """SELECT ?subject ?predicate ?object
# WHERE {
#   ?subject ?predicate ?object
# }
# LIMIT 100000"""

    # payload = {
    #     "component": "QE",
    #     "message": {
    #         "query": payload
    #     }
    # }
    rabbit_mq.producer(queue=APP_QUEUE, message=json.dumps(payload))
