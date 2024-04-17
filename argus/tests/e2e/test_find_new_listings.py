from unittest.mock import patch

import pytest
from sqlmodel import Session, select

from argus.discogs.models.listing import Listing
from argus.discogs.models.wantlist import WantlistItem
from argus.tasks.find_new_listings import find_new_listings
from argus.telegram_.messages import ErrorMessage, NewListingMessage
from argus.tests.conftest import listing_factory
from argus.user import User


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "listings",
    [
        [
            listing_factory(release_id=100, listing_id=200),
            listing_factory(release_id=100, listing_id=201),
        ]
    ],
)
async def test_find_new_listings_for_new_release_with_listings(
    mock_listings_on_discogs,
    mock_get_wantlist_item_ids,
    engine,
    telegram,
):
    """
    Tests that when a new release appears in a wantlist, and that release has a listing,
    then that listing is inserted into the DB and no messages are sent to Telegram.
    """
    # Given
    with Session(engine) as session:
        session.add(
            User(name="test", discogs_token="with_wantlist", telegram_chat_id=1)
        )
        session.commit()
    # When
    await find_new_listings(
        engine=engine,
        telegram=telegram,
    )
    # Then
    with Session(engine) as session:
        assert len(session.exec(select(WantlistItem)).all()) == 1
        assert len(session.exec(select(Listing)).all()) == 2
    assert telegram.send.call_count == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "listings",
    [[]],
)
async def test_find_new_listings_for_new_release_with_no_listings(
    mock_listings_on_discogs,
    mock_get_wantlist_item_ids,
    engine,
    telegram,
):
    """
    Tests that when a new release appears in a wantlist, and that release has no listings,
    a dummy listing is inserted into the DB and no messages are sent to Telegram."""
    # Given
    with Session(engine) as session:
        session.add(
            User(name="test", discogs_token="with_wantlist", telegram_chat_id=1)
        )
        session.commit()
    # When
    await find_new_listings(
        engine=engine,
        telegram=telegram,
    )
    # Then
    with Session(engine) as session:
        assert len(session.exec(select(WantlistItem)).all()) == 1
        assert len(session.exec(select(Listing)).all()) == 1
    assert telegram.send.call_count == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "listings",
    [
        [
            listing_factory(release_id=100, listing_id=200),
            listing_factory(release_id=100, listing_id=201),
        ]
    ],
)
async def test_find_new_listings_for_existing_release(
    mock_listings_on_discogs,
    mock_get_wantlist_item_ids,
    engine,
    telegram,
):
    """
    Tests that when a new listing appears for a release which already has a listing in the DB,
    then that listing is added to the DB and a message is sent to Telegram.
    """
    # Given
    with Session(engine) as session:
        session.add(
            User(name="test", discogs_token="with_wantlist", telegram_chat_id=1)
        )
        session.add(
            User(name="test2", discogs_token="without_wantlist", telegram_chat_id=2)
        )
        session.add(listing_factory(release_id=100, listing_id=201))
        session.commit()
    # When
    await find_new_listings(
        engine=engine,
        telegram=telegram,
    )
    # Then
    with Session(engine) as session:
        assert len(session.exec(select(WantlistItem)).all()) == 1
        assert len(session.exec(select(Listing)).all()) == 2
    assert telegram.send.call_count == 1
    assert isinstance(telegram.send.call_args.args[0], NewListingMessage)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "listings",
    [[]],
)
@patch("argus.discogs.models.listing.Listings.in_db")
async def test_find_new_listings_should_send_error_to_telegram_for_exception_in_process_release(
    mock_listings_on_db,
    mock_listings_on_discogs,
    mock_get_wantlist_item_ids,
    engine,
    telegram,
):
    """"""

    # Given
    def raise_exception(*args, **kwargs):
        raise RuntimeError("Some error")

    mock_listings_on_db.side_effect = raise_exception
    with Session(engine) as session:
        session.add(
            User(
                name="test",
                discogs_token="with_wantlist",
                telegram_chat_id=1,
                warn_on_error=True,
            )
        )
        session.commit()
    # When
    await find_new_listings(
        engine=engine,
        telegram=telegram,
    )
    # Then
    with Session(engine) as session:
        assert len(session.exec(select(WantlistItem)).all()) == 1
        assert len(session.exec(select(Listing)).all()) == 0
    assert telegram.send.call_count == 1
    assert isinstance(telegram.send.call_args.args[0], ErrorMessage)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "listings",
    [[]],
)
@patch("argus.user.User.fetch_all")
async def test_find_new_listings_should_send_error_to_telegram_for_exception_in_find_new_listing(
    mock_user_fetch_all,
    mock_listings_on_discogs,
    mock_get_wantlist_item_ids,
    engine,
    telegram,
):
    """"""

    # Given
    def raise_exception(*args, **kwargs):
        raise RuntimeError("Some error")

    mock_user_fetch_all.side_effect = raise_exception
    with Session(engine) as session:
        session.add(
            User(
                name="test",
                discogs_token="with_wantlist",
                telegram_chat_id=1,
                warn_on_error=True,
            )
        )
        session.commit()
    # When
    await find_new_listings(
        engine=engine,
        telegram=telegram,
    )
    # Then
    with Session(engine) as session:
        assert len(session.exec(select(WantlistItem)).all()) == 0
        assert len(session.exec(select(Listing)).all()) == 0
    assert telegram.send.call_count == 1
    assert isinstance(telegram.send.call_args.args[0], ErrorMessage)
