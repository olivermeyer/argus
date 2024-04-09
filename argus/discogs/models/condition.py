from dataclasses import dataclass
from enum import Enum


@dataclass
class _Condition:
    full: str
    long: str
    short: str


class Condition(Enum):
    MINT = _Condition("Mint (M)", "Mint", "M")
    NEAR_MINT = _Condition("Near Mint (NM or M-)", "Near Mint", "NM or M-")
    VERY_GOOD_PLUS = _Condition("Very Good Plus (VG+)", "Very Good Plus", "VG+")
    VERY_GOOD = _Condition("Very Good (VG)", "Very Good", "VG")
    GOOD = _Condition("Good (G)", "Good", "G")
    GOOD_PLUS = _Condition("Good Plus (G+)", "Good Plus", "G+")
    POOR = _Condition("Poor (P)", "Poor", "P")
    FAIR = _Condition("Fair (F)", "Fair", "F")
    GENERIC = _Condition("Generic", "Generic", "Gen")
    NOT_GRADED = _Condition("Not Graded", "Not Graded", "Not Graded")
    NO_COVER = _Condition("No Cover", "No Cover", "No Cover")
