from unittest.mock import MagicMock

from argus.clients.telegram.client import TelegramClient
from argus.models.discogs import Listing, Condition


def test_send_new_listing_message_should_send_expected_message():
	client = TelegramClient(
		token="abc",
		chat_id=123,
		bot=MagicMock()
	)
	listing = Listing(
		id="1",
		title="First listing",
		url="www.listing.com",
		media_condition=Condition.VERY_GOOD,
		sleeve_condition=Condition.GENERIC,
		ships_from="somewhere",
		price="1€",
		seller="someone",
	)
	client.send_new_listing_message(listing=listing)
	client.bot.send_message.assert_called_once_with(
		123,
		'*First listing*\nVG / Gen \\| 1€ \\| somewhere\nView on [Discogs](www.listing.com)',
		parse_mode='MarkdownV2',
	)
