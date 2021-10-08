# argus

## Onboarding a new user
1. Get their Discogs API token and add it to `secrets.yaml`
1. Get their chat ID
    1. Have the new user start a conversation with `@ArcogsBot` on Telegram
    1. Monitor the bot's [updates](https://api.telegram.org/bot1997819840:AAFlb7dYUy6m6hl0VIEiQHPWNx3laid2zKI/getUpdates)
       and get the chat ID for the conversation
    1. Add the chat ID to `secrets.yaml`
1. Add the user to `update_and_start.sh` in `user-data.bash`
1. Deploy Argus

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

    export AWS_PROFILE=perso
    make build-push

Update and restart on EC2:

    make ssh-update-and-start

## Troubleshooting
### On EC2

    # connect to instance
    # find the relevant container:
    docker ps -a
    # check logs for the container:
    docker logs <name>
