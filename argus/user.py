from typing import Sequence

from sqlalchemy import Engine
from sqlmodel import Field, Session, SQLModel, select

from argus.logger import logger


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    discogs_token: str
    telegram_chat_id: int
    warn_on_error: bool = False

    @staticmethod
    def fetch_all(engine: Engine) -> Sequence["User"]:
        logger.info("Fetching all users in database")
        try:
            with Session(engine) as session:
                return session.exec(select(User)).all()
        except Exception:
            logger.exception("Error fetching all users")
            raise
