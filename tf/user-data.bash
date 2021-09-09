#!/bin/bash

sudo su root
yum install -y docker
service docker start

aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 595687261518.dkr.ecr.eu-west-1.amazonaws.com
docker pull 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest
docker tag 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest argus:latest
docker run --restart=on-failure -d -t argus:latest python main.py
