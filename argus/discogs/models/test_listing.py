import os

import pytest

from argus.discogs.models.listing import Listing, ListingsPage, Condition


def test_sort_should_sort_correctly():
    first = Listing(
        listing_id=1,
        title="First listing",
        url="www.listing.com",
        media_condition=Condition.GENERIC,
        sleeve_condition=Condition.GENERIC,
        ships_from="somewhere",
        price=1.0,
        currency="EUR",
        seller="someone",
    )
    second = Listing(
        listing_id=2,
        title="Second listing",
        url="www.listing.com",
        media_condition=Condition.GENERIC,
        sleeve_condition=Condition.GENERIC,
        ships_from="somewhere",
        price=1.0,
        currency="EUR",
        seller="someone",
    )
    assert sorted([second, first]) == [first, second]


def test_price_as_string_should_return_expected_value():
    assert (
        Listing(
            id=1,
            title="First listing",
            url="www.listing.com",
            media_condition=Condition.GENERIC,
            sleeve_condition=Condition.GENERIC,
            ships_from="somewhere",
            price=1.0,
            currency="EUR",
            seller="someone",
        ).price_string
        == "€1.0"
    )


def test_price_as_string_should_raise_exception_for_invalid_currency():
    with pytest.raises(ValueError):
        Listing(
            id="1",
            title="First listing",
            url="www.listing.com",
            media_condition=Condition.GENERIC,
            sleeve_condition=Condition.GENERIC,
            ships_from="somewhere",
            price=1.0,
            currency="O@#",
            seller="someone",
        ).price_string


def test_should_parse_release_listings_page():
    with open(f"{os.path.dirname(__file__)}/fixtures/release_listings.html") as fh:
        assert sorted(ListingsPage.from_html(fh.read()).listings) == sorted(
            [
                Listing(
                    listing_id=2142025490,
                    title="Jode (3) - Jode (LP, Album)",
                    url="https://discogs.com/sell/item/2142025490",
                    media_condition=Condition.VERY_GOOD,
                    sleeve_condition=Condition.VERY_GOOD_PLUS,
                    ships_from="Brazil",
                    price=160.0,
                    currency="BRL",
                    seller="ErlonSilva",
                ),
                Listing(
                    title="Jode (3) - Jode (LP, Album)",
                    url="https://discogs.com/sell/item/1506778963",
                    listing_id=1506778963,
                    media_condition=Condition.VERY_GOOD_PLUS,
                    sleeve_condition=Condition.VERY_GOOD_PLUS,
                    ships_from="Brazil",
                    price=168.0,
                    currency="BRL",
                    seller="ChicoeZicoSP",
                ),
            ]
        )


def test_should_parse_master_listings_page():
    with open(f"{os.path.dirname(__file__)}/fixtures/master_listings.html") as fh:
        assert sorted(ListingsPage.from_html(fh.read()).listings) == sorted(
            [
                Listing(
                    listing_id=2703709795,
                    title="Esa (6) - Esa (LP, Album)",
                    url="https://discogs.com/sell/item/2703709795",
                    media_condition=Condition.VERY_GOOD,
                    sleeve_condition=Condition.GOOD_PLUS,
                    ships_from="France",
                    price=75.00,
                    currency="EUR",
                    seller="badou0032",
                ),
                Listing(
                    listing_id=2643428466,
                    title="Esa (6) - Esa (LP, Album)",
                    url="https://discogs.com/sell/item/2643428466",
                    media_condition=Condition.VERY_GOOD_PLUS,
                    sleeve_condition=Condition.VERY_GOOD_PLUS,
                    ships_from="United States",
                    price=119.99,
                    currency="USD",
                    seller="academyrecords",
                ),
            ]
        )
