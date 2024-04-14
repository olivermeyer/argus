import pytest
from sqlmodel import Session, select

from argus.discogs.models.condition import Condition
from argus.discogs.models.listing import Listing
from argus.discogs.models.wantlist import WantlistItem
from argus.tasks.find_new_listings import find_new_listings
from argus.user import User


@pytest.mark.asyncio
def test_find_new_listings_for_new_release(
    mock_get_release_listings_page,
    mock_get_wantlist_item_ids,
    engine,
    telegram,
):
    # Given
    with Session(engine) as session:
        session.add(
            User(name="test", discogs_token="with_wantlist", telegram_chat_id=1)
        )
        session.commit()
    # When
    find_new_listings(
        engine=engine,
        telegram=telegram,
    )
    # Then
    with Session(engine) as session:
        assert len(session.exec(select(WantlistItem)).all()) == 1
        assert len(session.exec(select(Listing)).all()) == 2
    assert telegram.send.call_count == 0


@pytest.mark.asyncio
def test_find_new_listings_for_existing_release(
    mock_get_release_listings_page,
    mock_get_wantlist_item_ids,
    engine,
    telegram,
):
    # Given
    with Session(engine) as session:
        session.add(
            User(name="test", discogs_token="with_wantlist", telegram_chat_id=1)
        )
        session.add(
            User(name="test2", discogs_token="without_wantlist", telegram_chat_id=2)
        )
        session.add(
            Listing(
                release_id=10105811,
                listing_id=1506778963,
                title="test title",
                url="http://test.url",
                media_condition=Condition.MINT,
                sleeve_condition=Condition.MINT,
                ships_from="Poland",
                price=100.0,
                currency="USD",
                seller="test seller",
            )
        )
        session.commit()
    # When
    find_new_listings(
        engine=engine,
        telegram=telegram,
    )
    # Then
    with Session(engine) as session:
        assert len(session.exec(select(WantlistItem)).all()) == 1
        assert len(session.exec(select(Listing)).all()) == 2
    assert telegram.send.call_count == 1
