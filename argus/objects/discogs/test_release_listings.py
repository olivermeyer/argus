import os

from argus.models.discogs.condition import Condition
from argus.models.discogs.listing import Listing
from argus.objects.discogs.release_listings import ReleaseListingsPageParser


def test_parse_listings():
    with open(f"{os.path.dirname(__file__)}/test_release_listings.html") as fh:
        assert sorted(ReleaseListingsPageParser().parse_listings(fh.read())) == sorted([
            Listing(
                id="2142025490",
                title="Jode (3) - Jode (LP, Album)",
                url="https://discogs.com/sell/item/2142025490",
                media_condition=Condition.VERY_GOOD,
                sleeve_condition=Condition.VERY_GOOD_PLUS,
                ships_from="Brazil",
                price="R$160.00",
                seller="ErlonSilva",
            ),
            Listing(
                title="Jode (3) - Jode (LP, Album)",
                url="https://discogs.com/sell/item/1506778963",
                id="1506778963",
                media_condition=Condition.VERY_GOOD_PLUS,
                sleeve_condition=Condition.VERY_GOOD_PLUS,
                ships_from="Brazil",
                price="R$168.00",
                seller="ChicoeZicoSP",
            ),
        ])
