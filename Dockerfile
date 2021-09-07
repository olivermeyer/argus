from python:slim-buster

RUN useradd -ms /bin/bash argus

ENV ARGUS_DIRECTORY=/usr/local/argus

COPY . ${ARGUS_DIRECTORY}

USER argus

WORKDIR ${ARGUS_DIRECTORY}

RUN pip install -r ${ARGUS_DIRECTORY}/requirements.txt

