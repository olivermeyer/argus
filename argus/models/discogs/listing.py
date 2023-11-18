from enum import Enum

from pydantic import BaseModel


class Condition(Enum):
    MINT = "Mint (M)"
    NEAR_MINT = "Near Mint (NM or M-)"
    VERY_GOOD_PLUS = "Very Good Plus (VG+)"
    VERY_GOOD = "Very Good (VG)"
    GOOD = "Good (G)"
    GOOD_PLUS = "Good Plus (G+)"
    POOR = "Poor (P)"
    FAIR = "Fair (F)"
    GENERIC = "Generic"


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
