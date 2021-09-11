#!/bin/bash

start_argus () {
	USER=$1
    if [ "$(docker ps -aq -f name=$USER)" ]; then
    	echo "Removing existing container for ${USER}"
        docker rm -f $USER
    fi
    docker run --name $USER -v $USER:/usr/local/argus/state --restart=on-failure -d -t argus:latest python main.py --user ${USER}
}

update_argus() {
	aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 595687261518.dkr.ecr.eu-west-1.amazonaws.com
	docker pull 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest
	docker tag 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest argus:latest
	start_argus oli
	start_argus pa
}

sudo su root
yum install -y docker
service docker start
update_argus
