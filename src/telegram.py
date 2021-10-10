from logging import Logger

import telegram

from src.logger import logger


class TelegramBot(telegram.Bot):
    def __init__(self, token: str, logger: Logger = logger, **kwargs):
        self.logger = logger
        super(TelegramBot, self).__init__(token, **kwargs)

    def send_new_listing_message(self, chat_id: int, listing: dict) -> None:
        """
        Prepares and sends a message for a new listing.
        """
        text = self.prepare_new_listing_message(listing)
        try:
            self.send_message(chat_id, text, parse_mode='MarkdownV2')
        except telegram.error.BadRequest:
            raise RuntimeError(
                f"Failed to send listing {listing['id']} to chat {chat_id}"
            )

    def prepare_new_listing_message(self, listing: dict) -> str:
        """
        Builds the text for a new listing message.

        * The first line contains the title in bold
        * The second line contains the condition, price and location
        * The third line contains a link to the listing
        """
        first_line = f"{listing['title']}"
        second_line = "{mc} / {sc} | {p} | {sf}".format(
            mc=self.short_condition(listing["media_condition"]),
            sc=self.short_condition(listing["sleeve_condition"]),
            p=listing["price"],
            sf=listing["ships_from"]
        )
        third_line = f"View on [Discogs]({listing['url']})"
        return f"*{self.clean_string(first_line)}*\n" \
               f"{self.clean_string(second_line)}\n" \
               f"{third_line}"

    @staticmethod
    def short_condition(condition: str) -> str:
        """
        Returns the abbreviated condition.

        E.g. 'Very Good+ (VG+)' becomes 'VG+'. 'Generic' becomes 'Gen'.
        """
        if "Generic" in condition:
            short_condition = "Gen"
        else:
            short_condition = condition[
                              condition.find("(") + 1:condition.find(")")
                              ]
        return short_condition

    @staticmethod
    def clean_string(string: str) -> str:
        return string.replace(
            "-", "\-"
        ).replace(
            "(", "\("
        ).replace(
            ")", "\)"
        ).replace(
            ".", "\."
        ).replace(
            "+", "\+"
        ).replace(
            "*", ""
        ).replace(
            "=", "\="
        ).replace(
            ":", "\:"
        ).replace(
            "|", "\|"
        ).replace(
            "!", "\!"
        )
