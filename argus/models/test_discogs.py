import os

from argus.models.discogs import Listing, ListingsPage, Condition


def test_sort_should_sort_correctly():
	first = Listing(
		id="1",
		title="First listing",
		url="www.listing.com",
		media_condition=Condition.GENERIC,
		sleeve_condition=Condition.GENERIC,
		ships_from="somewhere",
		price="1€",
		seller="someone",
	)
	second = Listing(
		id="2",
		title="Second listing",
		url="www.listing.com",
		media_condition=Condition.GENERIC,
		sleeve_condition=Condition.GENERIC,
		ships_from="somewhere",
		price="1€",
		seller="someone",
	)
	assert sorted([second, first]) == [first, second]


def test_should_parse_release_listings_page():
	with open(f"{os.path.dirname(__file__)}/fixtures/release_listings.html") as fh:
		assert sorted(ListingsPage(fh.read()).listings) == sorted([
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


def test_should_parse_master_listings_page():
	with open(f"{os.path.dirname(__file__)}/fixtures/master_listings.html") as fh:
		assert sorted(ListingsPage(fh.read()).listings) == sorted([
			Listing(
				id="2703709795",
				title="Esa (6) - Esa (LP, Album)",
				url="https://discogs.com/sell/item/2703709795",
				media_condition=Condition.VERY_GOOD,
				sleeve_condition=Condition.GOOD_PLUS,
				ships_from="France",
				price="€75.00",
				seller="badou0032",
			),
			Listing(
				id="2643428466",
				title="Esa (6) - Esa (LP, Album)",
				url="https://discogs.com/sell/item/2643428466",
				media_condition=Condition.VERY_GOOD_PLUS,
				sleeve_condition=Condition.VERY_GOOD_PLUS,
				ships_from="United States",
				price="$119.99",
				seller="academyrecords",
			),
		])
