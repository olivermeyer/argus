# Argus
## Who is Argus?
Argus is any Discogs user's best friend: he loves watching over his friends'
wantlists, pinging them whenever a release in their wantlist has a new listing.

## How does Argus work?
At a high level, Argus pulls a user's wantlist from the Discogs API and, for each
release in the wantlist, scrapes its listings from the Discogs website and looks
for new listings. Whenever a new listing is found, Argus sends a notification
to the user on Telegram.

Argus is happy to help as many people as possible, and can easily run in parallel
for several users. The only limitation will come from Discogs, who will eventually
figure out that Argus has been snooping around their website. So far, so good.

## Where does Argus run?
As of today, Argus runs on a small AWS EC2 instance. Argus can accomplish one task:
he can `crawl_wantlist`, which... crawls a Discogs user's wantlist.
He does this every so often, as defined by the EC2's root crontab.

### List scraper
Argus comes with a neat little utility which, given a list ID, will return the
sellers with the most listings for releases in that list. Usage example below:

      make bash-dev
      AWS_PROFILE=perso python entrypoint.py scrape-list --user om93-wants --list_id 574693

## DB
Argus uses SQLite and uses a .db file in `/usr/local/argus/data/`.
This directory is persisted in a Docker volume to
avoid having to re-create it at each run. This does however mean that, when
provisioning a new host, Argus always re-creates the DB from scratch on the
first run.

## Onboarding a new user
1. Get the users's Discogs API token and Telegram chat ID
   1. Have the new user start a conversation with `@ArcogsBot` on Telegram
   1. Monitor the bot's [updates](https://api.telegram.org/bot<token>/getUpdates)
      and get the chat ID for the conversation
1. Add both secrets to the `argus` secret in AWS
1. Add the user to the crontab (see other users for example)
1. Deploy Argus: `make deploy`

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

### Schema changes
If the schema of one of the tables changes, we need to wipe the data volumes on the EC2:

    make deploy
    make ssh-connect
    docker volume rm $(docker volume ls --filter name='_data' --format "{{.Name}}")

The tables will be recreated on the next run.

## Troubleshooting
To check the logs:

    make ssh-connect
    more /var/lib/docker/volumes/<user>_logs/_data/argus.log
