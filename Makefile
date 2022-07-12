IPV4_DNS=ec2-34-243-229-82.eu-west-1.compute.amazonaws.com

help:  ## Show this message
	# From https://gist.github.com/prwhite/8168133#gistcomment-3785627
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

build-latest:  ## Build with `latest` tag
	docker build . -t argus:latest

push-latest:  ## Push image with `latest` tag to ECR
	AWS_PROFILE=perso aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 595687261518.dkr.ecr.eu-west-1.amazonaws.com
	docker tag argus:latest 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest
	docker push 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest

build-push: build-latest push-latest  ## Build and push with `latest` tag

ssh-connect:  ## Connect to the instance
	ssh -i "~/.ssh/argus.pem" ec2-user@$(IPV4_DNS)

ssh-update-argus:  ## Update Argus remotely
	ssh -i "~/.ssh/argus.pem" ec2-user@$(IPV4_DNS) "sudo su -c 'source /usr/local/argus/update_argus.sh'"

ssh-update-crontab: ## Update the crontab remotely
	cat crontab | ssh -i "~/.ssh/argus.pem" ec2-user@$(IPV4_DNS) "sudo su -c 'crontab -'"

deploy: build-push ssh-update-argus ssh-update-crontab ## Build, push and update Argus remotely

build-dev:  ## Build with `dev` tag
	docker build . -t argus:dev

run-dev:  ## Enter the container with `dev` tag
	docker run -v "$$(pwd)"/src:/usr/local/argus/src -v argus-data:/usr/local/argus/data -it argus:dev /bin/bash
