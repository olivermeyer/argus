from python:slim-buster

ENV ARGUS_DIRECTORY=/usr/local/argus
ENV STATE_DIRECTORY=/var/argus/state

RUN mkdir -p ${STATE_DIRECTORY}

COPY . ${ARGUS_DIRECTORY}

RUN pip install -r ${ARGUS_DIRECTORY}/requirements.txt

WORKDIR ${ARGUS_DIRECTORY}
