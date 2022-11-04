FROM python:3.7.12-slim-buster

ENV ARGUS_DIRECTORY=/usr/local/argus
ENV DATA_DIRECTORY=${ARGUS_DIRECTORY}/data
RUN mkdir -p ${DATA_DIRECTORY}

ENV LOG_LEVEL=INFO
ENV LOG_DIRECTORY=/var/log/argus
RUN mkdir -p ${LOG_DIRECTORY}

COPY ./requirements.txt ${ARGUS_DIRECTORY}/requirements.txt
RUN pip install --no-cache -r ${ARGUS_DIRECTORY}/requirements.txt

COPY ./src ${ARGUS_DIRECTORY}/src
COPY ./Dockerfile ${ARGUS_DIRECTORY}/Dockerfile
COPY ./main.py ${ARGUS_DIRECTORY}/main.py

WORKDIR ${ARGUS_DIRECTORY}
