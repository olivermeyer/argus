from dataclasses import dataclass
from logging import Logger

import telegram

from argus.models.discogs import Listing
from argus.logger import logger


@dataclass
class TelegramClient:
    """
    Class representing a Telegram client.
    """
    token: str
    chat_id: int
    bot: telegram.Bot = None
    logger: Logger = logger

    def __post_init__(self):
        if not self.bot:
            self.bot = telegram.Bot(token=self.token)

    def send_new_listing_message(self, listing: Listing) -> None:
        """
        Prepares and sends a message for a new listing.
        """
        text = self.prepare_new_listing_message(listing)
        try:
            self.bot.send_message(self.chat_id, text, parse_mode="MarkdownV2")
        except telegram.error.BadRequest:
            raise RuntimeError(
                f"Failed to send listing {listing['id']} to chat {self.chat_id}"
            )

    def prepare_new_listing_message(self, listing: Listing) -> str:
        """
        Builds the text for a new listing message.

        * The first line contains the title in bold
        * The second line contains the condition, price and location
        * The third line contains a link to the listing
        """
        first_line = listing.title
        logger.error(listing)
        second_line = "{mc} / {sc} | {p} | {sf}".format(
            mc=listing.media_condition.value.short,
            sc=listing.sleeve_condition.value.short,
            p=listing.price,
            sf=listing.ships_from,
        )
        third_line = f"View on [Discogs]({listing.url})"
        return (
            f"*{self.clean_string(first_line)}*\n"
            f"{self.clean_string(second_line)}\n"
            f"{third_line}"
        )

    @staticmethod
    def clean_string(string: str) -> str:
        """
        Prefixes certain characters with a backslash.

        The list of characters is taken from
        https://core.telegram.org/bots/api#sendmessage.
        """
        reserved_chars = [
            "_",
            "*",
            "[",
            "]",
            "(",
            ")",
            "~",
            "`",
            ">",
            "#",
            "+",
            "-",
            "=",
            "|",
            "{",
            "}",
            ".",
            "!",
        ]
        for char in reserved_chars:
            string = string.replace(char, f"\\{char}")
        return string
