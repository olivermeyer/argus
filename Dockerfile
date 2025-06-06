FROM python:3.11-slim-buster

ENV ARGUS_DIRECTORY=/usr/local/argus
ENV DATA_DIRECTORY=${ARGUS_DIRECTORY}/data
RUN mkdir -p ${DATA_DIRECTORY}

ENV LOG_LEVEL=INFO
ENV LOG_DIRECTORY=/var/log/argus
RUN mkdir -p ${LOG_DIRECTORY}

WORKDIR ${ARGUS_DIRECTORY}

COPY pyproject.toml poetry.lock ${ARGUS_DIRECTORY}/

RUN pip install poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-root

COPY argus ${ARGUS_DIRECTORY}/argus

RUN poetry install
