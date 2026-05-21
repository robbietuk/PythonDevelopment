from dataclasses import dataclass
from itertools import groupby
from operator import attrgetter

@dataclass(frozen=True, slots=True)
class Record:
    sector: str
    ticker: str

records: list[Record] = [
    Record(sector="Tech", ticker="AAPL"),
    Record(sector="Tech", ticker="MSFT"),
    Record(sector="Finance", ticker="JPM"),
    Record(sector="Finance", ticker="MS"),
]

records.sort(key=attrgetter("sector"))

print(records)
grouped: dict[str, list[str]] = {
    sector: [item.ticker for item in items]
    for sector, items in groupby(records, key=attrgetter("sector"))
}

print(grouped)