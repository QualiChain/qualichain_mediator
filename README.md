# QualiChain-mediator

### Install Project Requirements

`pip install -r requirements.txt`

### Install RabbitMQ and Qualichain Mediator
1.  `cd /config`

2. `docker-compose up -d --build`

### Send messages to Qualichain Mediator

Send messages to Qualichain Mediator using this command: `python producer.py`

### Skills Extraction Pipeline

QualiChain Mediator also uses Dobie to extract skills from crawled job posts and save these skills to `extracted_skill` Table in Qualichain Table

In order to run this pipeline you should run:
 1. *Locally*: `python run_skill_extraction.py`
 2. *From Docker Command* `docker exec -it qmediator_consumer python run_skill_extraction.py`

### LICENSE
This project is licensed under [MIT](https://github.com/epu-ntua/QualiChain-mediator/blob/master/LICENSE)
