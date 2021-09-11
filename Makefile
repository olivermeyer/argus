build-push:
	export AWS_PROFILE=perso
	docker build . -t argus:latest
	aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 595687261518.dkr.ecr.eu-west-1.amazonaws.com
	docker tag argus:latest 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest
	docker push 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest
