from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, select, Field

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
            logger.info(f"Updating wantlist for user {user.name}")
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
        except Exception as e:
            logger.error(f"Failed to update wantlist for user {user.name}: {e}")
            raise

    @staticmethod
    def fetch_all_release_ids(engine: Engine) -> set[int]:
        """Fetches all release IDs in the wantlist."""
        try:
            logger.info("Fetching all release IDs in the WantlistItem table")
            with Session(engine) as session:
                return set(session.exec(select(WantlistItem.release_id)).all())
        except Exception as e:
            logger.error(
                f"Failed to fetch all release IDs in the WantlistItem table: {e}"
            )
            raise
