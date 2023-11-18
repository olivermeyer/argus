from dataclasses import dataclass, field
from logging import Logger

import telegram

from argus.models.discogs.listing import Listing, Condition
from argus.objects.logger import logger


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
        second_line = "{mc} / {sc} | {p} | {sf}".format(
            mc=self.short_condition(listing.media_condition),
            sc=self.short_condition(listing.sleeve_condition),
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
    def short_condition(condition: Condition) -> str:
        """
        Returns the abbreviated condition.

        E.g. 'Very Good+ (VG+)' becomes 'VG+'. 'Generic' becomes 'Gen'.
        """
        if "Generic" in condition.value:
            short_condition = "Gen"
        else:
            short_condition = condition.value[
                              condition.value.find("(") + 1 : condition.value.find(")")
                              ]
        return short_condition

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
