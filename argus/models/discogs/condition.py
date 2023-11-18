from dataclasses import dataclass
from enum import Enum


@dataclass
class _Condition:
	long: str
	short: str


class Condition(Enum):
	MINT = _Condition("Mint", "M")
	NEAR_MINT = _Condition("Near Mint", "NM or M-")
	VERY_GOOD_PLUS = _Condition("Very Good Plus", "VG+")
	VERY_GOOD = _Condition("Very Good", "VG")
	GOOD = _Condition("Good", "G")
	GOOD_PLUS = _Condition("Good Plus", "G+")
	POOR = _Condition("Poor", "P")
	FAIR = _Condition("Fair", "F")
	GENERIC = _Condition("Generic", "Gen")
