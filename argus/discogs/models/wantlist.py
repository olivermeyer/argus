import traceback

from sqlalchemy import Engine
from sqlmodel import Field, Session, SQLModel, select

from argus.discogs.clients.api import DiscogsApiClient
from argus.logger import logger
from argus.user import User


class WantlistItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    release_id: int

    @staticmethod
    def update(user: User, client: DiscogsApiClient, engine: Engine) -> None:
        """Updates the wantlist."""
        try:
            logger.info(
                "Updating wantlist for user in database",
                extra={
                    "user": user.name,
                },
            )
            with Session(engine) as session:
                for result in session.exec(
                    select(WantlistItem).where(WantlistItem.user_id == user.id)
                ).all():
                    session.delete(result)
                for release_id in client.get_wantlist_item_ids(
                    token=user.discogs_token
                ):
                    session.add(WantlistItem(user_id=user.id, release_id=release_id))
                session.commit()
        except Exception:
            logger.exception(
                "Failed to update wantlist",
                extra={
                    "user": user.name,
                    "traceback": traceback.format_exc(),
                },
            )
            raise

    @staticmethod
    def fetch_all_release_ids(engine: Engine) -> set[int]:
        """Fetches all release IDs in the wantlist."""
        try:
            logger.info("Fetching all release IDs in wantlists in database")
            with Session(engine) as session:
                return set(session.exec(select(WantlistItem.release_id)).all())
        except Exception:
            logger.exception(
                "Failed to fetch all release IDs in the WantlistItem table",
                extra={
                    "traceback": traceback.format_exc(),
                },
            )
            raise
