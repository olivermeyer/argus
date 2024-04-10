IPV4_DNS=ec2-34-242-43-219.eu-west-1.compute.amazonaws.com

help:  ## Show this message
	# From https://gist.github.com/prwhite/8168133#gistcomment-3785627
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

start:  ## Starts all containers
	docker compose up --build -d

stop:  ## Stops all containers
	docker compose down
