from pydantic import BaseModel

from argus.models.discogs.condition import Condition


class Listing(BaseModel):
    id: str  # TODO: Change this to int
    title: str
    url: str
    media_condition: Condition
    sleeve_condition: Condition
    ships_from: str
    price: str
    seller: str

    def __lt__(self, other: "Listing"):
        return int(self.id) < int(other.id)
