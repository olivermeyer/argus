from unittest.mock import MagicMock

from argus.clients.telegram.client import TelegramClient
from argus.models.discogs.listing import Listing


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
		media_condition="Generic",
		sleeve_condition="Generic",
		ships_from="somewhere",
		price="1€",
		seller="someone",
	)
	client.send_new_listing_message(listing=listing)
	client.bot.send_message.assert_called_once_with(
		123,
		'*First listing*\nGen / Gen \\| 1€ \\| somewhere\nView on [Discogs](www.listing.com)',
		parse_mode='MarkdownV2',
	)
