from src.resources.db import SqliteDbClient
from src.resources.discogs import get_wantlist_ids, ListingsPage
from src.resources.telegram import TelegramBot
from src.tasks.abstract import AbstractTask


class CrawlTask(AbstractTask):
    def execute(self):
        user_secrets = self.secrets[self.user]
        db = SqliteDbClient()
        db.initialize_argus()
        telegram = TelegramBot(self.secrets["telegram_token"])
        try:
            wantlist_ids = get_wantlist_ids(user_secrets['discogs_token'])
            db.update_wantlist(user=self.user, release_ids=wantlist_ids)
            self.logger.info(f"Scanning {len(wantlist_ids)} releases")
            for release_id in wantlist_ids:
                self.logger.info(f"Processing release {release_id}")
                discogs_listings = ListingsPage(release_id).fetch()
                db_listings = db.get_listing_ids(release_id)
                if db_listings:
                    for listing in discogs_listings:
                        if listing["id"] not in db_listings:
                            self.logger.info(f"Found new listing: {listing['id']}")
                            telegram.send_new_listing_message(
                                user_secrets['telegram_chat_id'],
                                listing
                            )
                else:
                    self.logger.debug(f"Release {release_id} not yet in state")
                db.update_listings(
                    release_id=release_id,
                    listings=discogs_listings,
                )
        finally:
            db.close()
