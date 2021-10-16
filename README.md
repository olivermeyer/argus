# argus

## DB
To avoid paying for an RDS instance, Argus uses SQLite and uses a .db file in
`/usr/local/argus/data/`. This directory is persisted in a Docker volume to
avoid having to re-create it at each run. This does however mean that, when
provisioning a new host, Argus always re-creates the DB from scratch on the
first run.

## Onboarding a new user
1. Add user to the `--user` argument choices in `main.py`
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

    make build-dev

Enter the image and attach all files in `src/`:

    make run-dev

## Access the instance
The following command only works from whitelisted IPs. If the command does not
run, check that ingress from your IP is allowed by a security group rule.

    make ssh-connect

## Deployment
A single Makefile target builds the image, pushes it to ECR, then pulls it to
the EC2 instance and restarts the processes:

    make deploy
