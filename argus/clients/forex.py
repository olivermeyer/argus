from dataclasses import dataclass

from forex_python.converter import CurrencyRates


@dataclass
class ForexClient:
    client: CurrencyRates = None

    def __post_init__(self):
        if not self.client:
            self.client = CurrencyRates()

    def convert(self, amount: float, from_: str, to_: str) -> float:
        return self.client.convert(from_, to_, amount)
