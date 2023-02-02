import asyncio

from aiohttp import ClientSession, TCPConnector

from argus.resources.db import SqliteDbClient, GenericDbClient
from argus.resources.discogs import get_wantlist_ids, ListingsPage
from argus.resources.telegram import TelegramBot
from argus.tasks.abstract import AbstractTask


class CrawlWantlistTask(AbstractTask):
    def execute(self):
        db = SqliteDbClient()
        db.initialize_argus()
        telegram = TelegramBot(self.config["telegram_token"])
        try:
            wantlist_ids = get_wantlist_ids(self.config["discogs_token"])
            db.update_wantlist(user=self.config["user"], release_ids=wantlist_ids)
            self.logger.info(f"Scanning {len(wantlist_ids)} releases")
            asyncio.run(
                self._crawl_async(
                    wantlist_ids,
                    db,
                    telegram,
                    self.config,
                )
            )
        finally:
            db.close()

    async def _crawl_async(
        self,
        wantlist_ids: list,
        db: GenericDbClient,
        telegram: TelegramBot,
        config: dict,
    ):
        tasks = []
        connector = TCPConnector(limit=50)
        async with ClientSession(connector=connector) as session:
            for release_id in wantlist_ids:
                tasks.append(
                    self._process_release(
                        release_id, db, telegram, config, session
                    )
                )
            await asyncio.gather(*tasks)

    async def _process_release(
        self,
        release_id: str,
        db: GenericDbClient,
        telegram: TelegramBot,
        config: dict,
        session: ClientSession,
    ):
        """
        Asynchronously processes a single release.
        """
        self.logger.info(f"Processing release {release_id}")
        discogs_listings = await ListingsPage(release_id).fetch_async(session)
        db_listings = db.get_listing_ids(release_id)
        if db_listings:
            for listing in discogs_listings:
                if listing["id"] not in db_listings:
                    self.logger.info(f"Found new listing: {listing['id']}")
                    telegram.send_new_listing_message(
                        config["telegram_chat_id"], listing
                    )
        else:
            self.logger.debug(f"Release {release_id} not yet in state")
        db.update_listings(
            release_id=release_id,
            listings=discogs_listings,
        )
