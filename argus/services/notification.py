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


async def _notify(message, user: User, telegram: TelegramClient) -> None:
    await telegram.send(message, user.telegram_chat_id)


async def notify_new_listing(user: User, listing: Listing, telegram: TelegramClient):
    logger.debug(
        "Notifying user about new listing",
        extra={
            "user": user.name,
            "listing_id": listing.listing_id,
        },
    )
    message = NewListingMessage(listing).prepare()
    await _notify(message=message, user=user, telegram=telegram)


async def notify_users_for_new_listing(
    listing: Listing, engine: Engine, telegram: TelegramClient
):
    with Session(engine) as session:
        logger.debug(
            "Finding users to notify about new listing",
            extra={
                "listing": listing.listing_id,
            },
        )
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
            await notify_new_listing(user, listing, telegram)


async def notify_new_error(user: User, error: Error, telegram: TelegramClient):
    logger.debug(
        "Notifying user about error",
        extra={
            "user": user.name,
            "error": error.text,
        },
    )
    message = ErrorMessage(error).prepare()
    await _notify(message=message, user=user, telegram=telegram)


async def notify_users_for_error(
    error: Error, engine: Engine, telegram: TelegramClient
):
    with Session(engine) as session:
        users = session.exec(select(User).where(User.warn_on_error)).all()
        for user in users:
            await notify_new_error(user, error, telegram)


async def notify_users(
    notification: NotificationTypes, engine: Engine, telegram: TelegramClient
):
    if isinstance(notification, Listing):
        await notify_users_for_new_listing(notification, engine, telegram)
    elif isinstance(notification, Error):
        await notify_users_for_error(notification, engine, telegram)
    else:
        message = f"Unexpected notification type: {type(notification)}"
        logger.exception(message)
        raise ValueError(message)
