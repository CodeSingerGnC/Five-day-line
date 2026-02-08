from datetime import date, datetime
from typing import Any, List
from trading.data.models.security import Security
from trading.data.provider import DataProvider
from trading.data.models.bar import Bar


def _to_ak_symbol(symbol: str) -> str:
    code, exch = symbol.split(".")
    p = "sz" if exch == "SZ" else "sh"
    return f"{p}{code}"


def _ak() -> Any:
    return __import__("akshare")


class AkshareProvider(DataProvider):
    def list_securities(self) -> List[Security]:
        ak = _ak()
        sz = ak.stock_info_sz_name_code()
        sh = ak.stock_info_sh_name_code()
        out: List[Security] = []
        for _, row in sz.iterrows():
            out.append(
                Security(
                    symbol=f"{row['code']}.SZ",
                    name=row["name"],
                    exchange="SZSE",
                    list_date=None,
                )
            )
        for _, row in sh.iterrows():
            out.append(
                Security(
                    symbol=f"{row['code']}.SH",
                    name=row["name"],
                    exchange="SSE",
                    list_date=None,
                )
            )
        return out

    def daily_bars(self, symbol: str, start: date, end: date) -> List[Bar]:
        ak = _ak()
        s = _to_ak_symbol(symbol)
        df = ak.stock_zh_a_daily(symbol=s, adjust="")
        out: List[Bar] = []
        for _, row in df.iterrows():
            d = datetime.strptime(str(row["date"]), "%Y-%m-%d").date()
            if d < start or d > end:
                continue
            ts = datetime(d.year, d.month, d.day)
            out.append(
                Bar(
                    symbol=symbol,
                    timestamp=ts,
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row.get("volume", row.get("vol", 0))),
                )
            )
        return out
