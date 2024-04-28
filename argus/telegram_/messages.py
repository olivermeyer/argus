from dataclasses import dataclass

from argus.discogs.models.listing import Listing
from argus.error import Error


def clean(string: str) -> str:
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


@dataclass
class NewListingMessage:
    listing: Listing
    text: str = ""

    def prepare(self):
        first_line = self.listing.title
        second_line = "{mc} / {sc} | {p} | {sf}".format(
            mc=self.listing.media_condition.value.short,
            sc=self.listing.sleeve_condition.value.short,
            p=self.listing.price_string,
            sf=self.listing.ships_from,
        )
        third_line = f"View on [Discogs]({self.listing.url})"
        self.text = f"*{clean(first_line)}*\n" f"{clean(second_line)}\n" f"{third_line}"
        return self


@dataclass
class ErrorMessage:
    error: Error
    text: str = ""

    def prepare(self):
        self.text = clean(self.error.text)
        return self
