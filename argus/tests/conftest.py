import asyncio
import os
from unittest.mock import patch, Mock, AsyncMock

import pytest
from sqlmodel import SQLModel

from sqlalchemy import create_engine


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
            return {10105811}
        return set()

    with patch("argus.discogs.clients.api.DiscogsApiClient.get_wantlist_item_ids") as mock:
        mock.side_effect = return_value
        yield


@pytest.fixture
def mock_get_release_listings_page():
    with patch("argus.discogs.clients.web.DiscogsWebClient.get_release_listings_page") as mock:
        future = asyncio.Future()
        path = os.path.join(os.path.dirname(__file__), "fixtures/release_listings.html")
        with open(path) as f:
            future.set_result(f.read())
        mock.return_value = future.result()
        yield


@pytest.fixture
def telegram():
    yield AsyncMock()
