help:  ## Show this message
	# From https://gist.github.com/prwhite/8168133#gistcomment-3785627
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

build-latest:  ## Build with `latest` tag
	docker build . -t argus:latest

push-latest:  ## Push image with `latest` tag to ECR
	aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 595687261518.dkr.ecr.eu-west-1.amazonaws.com
	docker tag argus:latest 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest
	docker push 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest

build-push: build-latest push-latest  ## Build and push with `latest` tag

ssh-connect:  ## Connect to the instance
	ssh -i "~/.ssh/argus.pem" ec2-user@ec2-52-211-134-220.eu-west-1.compute.amazonaws.com

ssh-update-and-start:  ## Update and restart Argus remotely
	ssh -i "~/.ssh/argus.pem" ec2-user@ec2-52-211-134-220.eu-west-1.compute.amazonaws.com "sudo su -c 'source /usr/local/argus/update_argus.sh'"

deploy: build-push ssh-update-and-start  ## Build, push, update and restart Argus remotely

build-dev:  ## Build with `dev` tag
	docker build . -t argus:dev

run-dev:  ## Enter the container with `dev` tag
	docker run -v "$$(pwd)"/src:/usr/local/argus/src -v argus-data:/usr/local/argus/data -it argus:dev /bin/bash
