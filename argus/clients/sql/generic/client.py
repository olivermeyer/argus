import os
from abc import ABC, abstractmethod
from logging import Logger
from typing import List

from argus.models.discogs.listing import Listing
from argus.objects.logger import logger


class GenericSqlClient(ABC):
    """
    Generic Argus database client.
    """

    def __init__(self, logger: Logger = logger):
        self.logger = logger
        self.conn = None

    @abstractmethod
    def connect(self):
        """
        Connects to the database and sets self.conn.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Closes the connections to the database.
        """
        pass

    @abstractmethod
    def execute(self, query: str) -> List[dict]:
        """
        Takes a query and returns the results as a list of dictionaries.
        """
        pass

    def initialize_argus(self, init_sql_path: str = "") -> None:
        """
        Initializes the database for Argus.
        """
        self.logger.info("Initializing the DB")
        if not init_sql_path:
            init_sql_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "../init.sql"
            )
        with open(init_sql_path, "r") as fh:
            sql = fh.read()
        self.execute(sql)

    def update_wantlist(
        self,
        user: str,
        release_ids: List[str],
    ) -> None:
        """
        Updates the wantlists table for the user.
        """
        self.logger.info(f"Updating wantlist for user {user}")
        values = [f"('{user}', '{release_id}')" for release_id in release_ids]
        query = f"""
DELETE FROM wantlists WHERE username='{user}';
INSERT INTO wantlists VALUES {', '.join(values)};"""
        self.execute(query)

    def get_listing_ids(self, release_id: str) -> list:
        """
        Gets the listing IDs for a release.
        """
        query = f"""
SELECT listing_id FROM listings WHERE release_id='{release_id}'"""
        results = self.execute(query)
        return [listing["listing_id"] for listing in results]

    def update_listings(self, release_id, listings: list[Listing]) -> None:
        """
        Updates the listings for a release.
        """
        self.logger.debug(f"Updating listings for release {release_id}")
        if listings:
            values = []
            for listing in listings:
                values.append(
                    f"""(
'{release_id}',
'{listing.id}',
'{listing.title.replace("'", "")}',
'{listing.url}',
'{listing.media_condition}',
'{listing.sleeve_condition}',
'{listing.ships_from}',
'{listing.price}',
'{listing.seller}'
)"""
                )
        else:
            values = [
                f"""(
'{release_id}',
'none',
'none',
'none',
'none',
'none',
'none',
'none',
'none'
)"""
            ]
        query = f"""
DELETE FROM listings WHERE release_id='{release_id}';
INSERT INTO listings VALUES {', '.join(values)};
"""
        self.execute(query)
