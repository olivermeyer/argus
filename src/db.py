import os
from logging import Logger
from typing import List

import psycopg2
from psycopg2.extras import RealDictCursor

from src.logger import logger


class DBClient:
    def __init__(
            self,
            host: str,
            db: str,
            user: str,
            pwd: str,
            port: int = 5432,
            logger: Logger = logger,
    ) -> None:
        self.host = host
        self.db = db
        self.user = user
        self.pwd = pwd
        self.port = port
        self.conn = None
        self.logger = logger

    @staticmethod
    def from_config(config: dict) -> 'DBClient':
        """
        Initializes and returns a DBClient object.
        """
        return DBClient(
            host=config["host"],
            db=config["db"],
            user=config["user"],
            pwd=config["pwd"],
            port=config["port"],
        )

    def connect(self) -> None:
        """
        Connects to the database.
        """
        self.logger.info(f"Connecting to {self.host}")
        if not self.conn:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.db,
                user=self.user,
                password=self.pwd,
                port=self.port,
            )

    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        self.logger.info(f"Closing connection")
        self.conn.close()

    def execute(self, query: str) -> List[dict]:
        """
        Executes a query.
        """
        if not self.conn:
            self.connect()
        self.logger.debug(f"Executing query: {query}")
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        self.conn.commit()
        try:
            results = [dict(r) for r in cursor.fetchall()]
            self.logger.debug(f"Got {len(results)} results")
        except psycopg2.ProgrammingError:
            results = None
            self.logger.debug(f"No results")
        return results

    def initialize_argus(
            self,
            init_sql_path: str = ""
    ) -> None:
        """
        Initializes the database for Argus.
        """
        self.logger.info("Initializing the DB")
        if not init_sql_path:
            init_sql_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "sql",
                "init.sql"
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
        logger.info(f"Updating wantlist for user {user}")
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

    def update_listings(self, release_id, listing_ids) -> None:
        """
        Updates the listings for a release.
        """
        self.logger.info(f"Updating listings for release {release_id}")
        values = [
            f"('{release_id}', '{listing_id}')" for listing_id in listing_ids
        ]
        query = f"""
DELETE FROM listings WHERE release_id='{release_id}';
INSERT INTO listings VALUES {', '.join(values)};
"""
        self.execute(query)
