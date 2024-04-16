from typing import Union

from sqlalchemy import Engine
from sqlmodel import Session, col, select

from argus.discogs.models.listing import Listing
from argus.discogs.models.wantlist import WantlistItem
from argus.error import Error
from argus.logger import logger
from argus.telegram_.client import TelegramClient
from argus.telegram_.messages import ErrorMessage, NewListingMessage
from argus.user import User

NotificationTypes = Union[Listing, Error]


def notify_new_listing(user: User, listing: Listing, telegram: TelegramClient):
    logger.debug(f"Notifying user {user.name} about new listing {listing.listing_id}")
    message = NewListingMessage(listing).prepare()
    telegram.send(message, user.telegram_chat_id)


def notify_users_for_new_listing(
    listing: Listing, engine: Engine, telegram: TelegramClient
):
    with Session(engine) as session:
        logger.debug(f"Finding users to notify about new listing {listing.listing_id}")
        users = session.exec(
            select(User).where(
                col(User.id).in_(
                    session.exec(
                        select(WantlistItem.user_id).where(
                            WantlistItem.release_id == listing.release_id
                        )
                    ).all()
                )
            )
        ).all()
        for user in users:
            notify_new_listing(user, listing, telegram)


def notify_new_error(user: User, error: Error, telegram: TelegramClient):
    logger.debug(f"Notifying user {user.name} about {error.text}")
    message = ErrorMessage(error).prepare()
    telegram.send(message, user.telegram_chat_id)


def notify_users_for_error(error: Error, engine: Engine, telegram: TelegramClient):
    with Session(engine) as session:
        users = session.exec(select(User).where(User.warn_on_error)).all()
        for user in users:
            notify_new_error(user, error, telegram)


def notify_users(
    notification: NotificationTypes, engine: Engine, telegram: TelegramClient
):
    if isinstance(notification, Listing):
        notify_users_for_new_listing(notification, engine, telegram)
    elif isinstance(notification, Error):
        notify_users_for_error(notification, engine, telegram)
    else:
        raise ValueError(f"Unexpected notification type: {type(notification)}")
