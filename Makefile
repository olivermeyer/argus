IPV4_DNS=UPDATE_ME

help:  ## Show this message
	# From https://gist.github.com/prwhite/8168133#gistcomment-3785627
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

start-dev:  ## Starts all containers (dev)
	docker-compose -f docker-compose.dev.yaml up --build -d

start-prod:  ## Starts all containers (prod)
	docker-compose -f docker-compose.prod.yaml up --build -d

stop-dev:  ## Stops all containers
	docker-compose -f docker-compose.dev.yaml down

stop-prod:  ## Stops all containers
	docker-compose -f docker-compose.prod.yaml down

test:
	ENVIRONMENT=test poetry run pytest
