FROM python:3.7.12-slim-buster

ENV ARGUS_DIRECTORY=/usr/local/argus
ENV DATA_DIRECTORY=${ARGUS_DIRECTORY}/data
ENV LOG_LEVEL=INFO

RUN mkdir -p ${DATA_DIRECTORY}

COPY ./src ${ARGUS_DIRECTORY}/src
COPY ./Dockerfile ${ARGUS_DIRECTORY}/Dockerfile
COPY ./main.py ${ARGUS_DIRECTORY}/main.py
COPY ./requirements.txt ${ARGUS_DIRECTORY}/requirements.txt
COPY ./secrets.yaml ${ARGUS_DIRECTORY}/secrets.yaml

RUN pip install --no-cache -r ${ARGUS_DIRECTORY}/requirements.txt

WORKDIR ${ARGUS_DIRECTORY}
