# Argus

# UPDATE: Argus is retired
The wonderful folk at [discdogs](https://www.discdogs.app/) have put out a great replacement for Argus; I've therefore retired Argus and am making this repo public for anyone interested to use.

## Who is Argus?
Argus is any Discogs user's best friend: he loves watching over his friends' wantlists, pinging them whenever a
release in their wantlist has a new listing.

## How does Argus work?
The core of Argus is the `find_new_listings` task. This tasks does the following:
* Update the wantlist items for all users
* For every release in all wantlists, scrape the listings for that release and look for new listings
* If a new listing is found, notify any user with that release in their wantlist

Argus can theoretically support an unlimited number of users. Practical limitations will however surface:
* The more users, the more distinct items in all wantlists, the longer every run takes. Longer runs means notifications
for new listings are delayed.
* Eventually, Discogs will notice the high number of requests coming from a single IP and most likely block it.
So far, so good.

## Adding a user
1. Get the users's Discogs API token and Telegram chat ID
   1. Have the new user start a conversation with `@ArcogsBot` on Telegram
   2. Monitor the bot's [updates](https://api.telegram.org/bot<token>/getUpdates) and get the chat ID for the conversation
2. Add both secrets to the `argus` secret in AWS for persistence
3. SSH into the instance
4. Attach to the `argus-argus-1` container: `docker exec -it argus-argus-1 /bin/bash`
5. Add the user: `python argus/app.py add-user --name <name> --discogs_token <token> --telegram_chat_id <chat ID>`
   * Optionally, if the user should receive error notifications, add the `--warn_on_error` flag

## Deployment
Any change pushed to the `main` branch is automatically checked and deployed to the instance.

## Monitoring
Argus has built-in monitoring using Loki and Grafana, accessible at port 3000 of the instance on which it's running.
