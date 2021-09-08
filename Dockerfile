from python:slim-buster

ENV ARGUS_DIRECTORY=/usr/local/argus
ENV STATE_DIRECTORY=${ARGUS_DIRECTORY}/state
ENV LOGS_DIRECTORY=${ARGUS_DIRECTORY}/logs

RUN mkdir -p ${STATE_DIRECTORY}
RUN mkdir -p ${LOGS_DIRECTORY}

COPY ./src ${ARGUS_DIRECTORY}/src
COPY ./Dockerfile ${ARGUS_DIRECTORY}/Dockerfile
COPY ./main.py ${ARGUS_DIRECTORY}/main.py
COPY ./requirements.txt ${ARGUS_DIRECTORY}/requirements.txt
COPY ./secrets.yaml ${ARGUS_DIRECTORY}/secrets.yaml

RUN pip install -r ${ARGUS_DIRECTORY}/requirements.txt

WORKDIR ${ARGUS_DIRECTORY}
