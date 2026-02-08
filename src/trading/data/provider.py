from datetime import date
from typing import List
from trading.data.models.bar import Bar
from trading.data.models.security import Security


class DataProvider:
    def list_securities(self) -> List[Security]:
        raise NotImplementedError

    def daily_bars(self, symbol: str, start: date, end: date) -> List[Bar]:
        raise NotImplementedError
