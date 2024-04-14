from sqlalchemy import Engine
from sqlmodel import Session

from argus.user import User


def main(
        name: str,
        discogs_token: str,
        telegram_chat_id: str,
        warn_on_error: bool,
        engine: Engine,
):
    with Session(engine) as session:
        session.add(User(
            name=name,
            discogs_token=discogs_token,
            telegram_chat_id=telegram_chat_id,
            warn_on_error=warn_on_error,
        ))
        session.commit()
