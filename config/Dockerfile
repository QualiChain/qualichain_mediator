FROM python:3.7-slim

RUN apt-get update && apt-get install -y netcat && apt-get install dos2unix

WORKDIR /opt/qualichain_mediator

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN dos2unix config/run.sh
CMD bash config/run.sh