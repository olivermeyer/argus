import os
import sqlite3
from abc import ABC, abstractmethod
from logging import Logger
from typing import List

from src.resources.logger import logger


DEFAULT_SQLITE_DB_LOCATION = os.path.join(os.environ["DATA_DIRECTORY"], "argus.db")


class GenericDbClient(ABC):
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
                os.path.dirname(os.path.abspath(__file__)), "..", "sql", "init.sql"
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

    def update_listings(self, release_id, listings: List[dict]) -> None:
        """
        Updates the listings for a release.
        """
        self.logger.debug(f"Updating listings for release {release_id}")
        if listings:
            values = []
            for listing in listings:
                listing_id = listing["id"]
                listing_title = listing["title"].replace("'", "")
                listing_url = listing["url"]
                listing_media_condition = listing["media_condition"]
                listing_sleeve_condition = listing["sleeve_condition"]
                listing_ships_from = listing["ships_from"]
                listing_price = listing["price"]
                values.append(
                    f"('{release_id}', '{listing_id}', '{listing_title}', '{listing_url}', '{listing_media_condition}', '{listing_sleeve_condition}', '{listing_ships_from}', '{listing_price}')"
                )
        else:
            values = [
                f"('{release_id}', 'none', 'none', 'none', 'none', 'none', 'none', 'none')"
            ]
        query = f"""
DELETE FROM listings WHERE release_id='{release_id}';
INSERT INTO listings VALUES {', '.join(values)};
"""
        self.execute(query)


class SqliteDbClient(GenericDbClient):
    def __init__(self, db_location: str = DEFAULT_SQLITE_DB_LOCATION, **kwargs) -> None:
        super().__init__(**kwargs)
        self.db_location = db_location

    def connect(self) -> None:
        self.logger.info(f"Connecting to SQLite DB in {self.db_location}")
        if not self.conn:
            self.conn = sqlite3.connect(self.db_location)
            # Set row_factory to enable name-based access to columns; see
            # https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
            self.conn.row_factory = sqlite3.Row

    def close(self) -> None:
        self.logger.info(f"Closing SQLite connection")
        self.conn.close()

    def execute(self, query: str) -> List[dict]:
        if not self.conn:
            self.connect()
        self.logger.debug(f"Executing query: {query}")
        cursor = self.conn.cursor()
        for statement in query.split(";"):
            cursor.execute(statement)
            self.conn.commit()
        results = [dict(r) for r in cursor.fetchall()]
        self.logger.debug(f"Got {len(results)} results")
        return results
