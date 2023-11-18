from argus.models.discogs.condition import Condition
from argus.models.discogs.listing import Listing


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
