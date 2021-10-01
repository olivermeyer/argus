# argus

## Development
Build the image locally:

    docker build . -t argus:dev

Enter the image and attach all files in `src/`:

    docker run -v "$(pwd)"/src:/usr/local/argus/src -it argus:dev /bin/bash

## Access the instance
The following command only works from whitelisted IPs. If the command does not
run, check that ingress from your IP is allowed by a security group rule.

    make ssh-connect

## Deployment
### Build and Push to ECR
Build and push the image:

    make build-push

Update and restart on EC2:

    # connect to instance
    sudo su root
    source /usr/local/argus/update_and_start.sh

## Troubleshooting
### On EC2

    # connect to instance
    # find the relevant container:
    docker ps -a
    # check logs for the container:
    docker logs <name>
