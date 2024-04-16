import asyncio
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel

from argus.discogs.models.condition import Condition
from argus.discogs.models.listing import Listing


def listing_factory(**kwargs: Any) -> Listing:
    default_args = {
        "title": "Title",
        "url": "http://discogs.com",
        "media_condition": Condition.NEAR_MINT,
        "sleeve_condition": Condition.NOT_GRADED,
        "ships_from": "Switzerland",
        "price": 100,
        "currency": "CHF",
        "seller": "dobshizzle",
    }
    return Listing(**{**default_args, **kwargs})


@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def mock_get_wantlist_item_ids():
    def return_value(token: str):
        if token == "with_wantlist":
            return {100}
        return set()

    with patch(
        "argus.discogs.clients.api.DiscogsApiClient.get_wantlist_item_ids"
    ) as mock:
        mock.side_effect = return_value
        yield


@pytest.fixture
def mock_listings_on_discogs(listings: list[Listing]):
    with patch("argus.discogs.models.listing.Listings.on_discogs") as mock:
        future = asyncio.Future()
        future.set_result(listings)
        mock.return_value = future.result()
        yield


@pytest.fixture
def telegram():
    yield AsyncMock()
