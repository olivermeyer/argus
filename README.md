# argus

## Deployment
### Build and Push to ECR
Build and push the image:

    make build-push

Pull to EC2:

    # connect to instance
    sudo su root
    update_argus

## Troubleshooting
### On EC2

    # connect to instance
    # find the relevant container:
    docker ps -a
    # check logs for the container:
    docker logs <name>
