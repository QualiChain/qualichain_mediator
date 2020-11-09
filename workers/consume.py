
from schema_validator import CValidator

json_example = {
    'label': 'some label',
    'title': 'some comment',
    'personURI': 'some personURI',
    'skills': [
        {"label": "label", "proficiencyLevel": "basic", "priorityLevel": "high"}

    ]
}

validator = CValidator()
validator.evaluate(json_example)

# if __name__ == "__main__":
#     rabbit_mq = RabbitMQClient()
#     rabbit_mq.consumer(queue=APP_QUEUE)
