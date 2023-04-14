import os
import sqlite3
from typing import List

from argus.resources.db.generic import GenericDbClient


DEFAULT_SQLITE_DB_LOCATION = os.path.join(os.environ["DATA_DIRECTORY"], "argus.db")


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
