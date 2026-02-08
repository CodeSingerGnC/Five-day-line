from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class Security:
    symbol: str
    name: str
    exchange: str
    list_date: Optional[date]
