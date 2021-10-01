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
        return DBClient(
            host=config["host"],
            db=config["db"],
            user=config["user"],
            pwd=config["pwd"],
            port=config["port"],
        )

    def connect(self) -> None:
        self.logger.info(f"Connecting to {self.host}")
        if not self.conn:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.db,
                user=self.user,
                password=self.pwd,
                port=self.port,
            )
            self.conn.autocommit = True

    def close(self) -> None:
        self.logger.info(f"Closing connection")
        self.conn.close()

    def execute(self, query: str) -> List[dict]:
        if not self.conn:
            self.connect()
        self.logger.info(f"Executing query: {query}")
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        try:
            results = [dict(r) for r in cursor.fetchall()]
            self.logger.info(f"Got {len(results)} results")
        except psycopg2.ProgrammingError:
            results = None
            self.logger.info(f"No results")
        return results

    def initialize_argus(
            self, init_sql_path: str = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "sql",
                "init.sql"
            )
    ) -> None:
        self.logger.info("Initializing the DB")
        with open(init_sql_path, "r") as fh:
            sql = fh.read()
        self.execute(sql)
