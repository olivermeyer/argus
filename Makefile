build-latest:
	docker build . -t argus:latest

push-latest:
	aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 595687261518.dkr.ecr.eu-west-1.amazonaws.com
	docker tag argus:latest 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest
	docker push 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest

build-push: build-latest push-latest

ssh-connect:
	ssh -i "~/.ssh/argus.pem" ec2-user@ec2-52-211-134-220.eu-west-1.compute.amazonaws.com

ssh-update-and-start:
	ssh -i "~/.ssh/argus.pem" ec2-user@ec2-52-211-134-220.eu-west-1.compute.amazonaws.com "sudo su -c 'source /usr/local/argus/update_and_start.sh'"

deploy: build-push ssh-update-and-start

build-dev:
	docker build . -t argus:dev

run-dev:
	docker run -v "$$(pwd)"/src:/usr/local/argus/src -it argus:dev /bin/bash
