import sys
from types import ModuleType
from datetime import date
from trading.data.providers.akshare_provider import AkshareProvider


class FakeDF:
    def __init__(self, rows):
        self._rows = rows

    def iterrows(self):
        for i, r in enumerate(self._rows):
            yield i, r


def install_fake_ak():
    m = ModuleType("akshare")

    class Row(dict):
        pass

    def stock_info_sz_name_code():
        return FakeDF([Row({"code": "000001", "name": "平安银行"})])

    def stock_info_sh_name_code():
        return FakeDF([Row({"code": "600000", "name": "浦发银行"})])

    def stock_zh_a_daily(symbol, adjust=""):
        return FakeDF(
            [
                Row(
                    {
                        "date": "2024-01-02",
                        "open": 10.0,
                        "high": 10.5,
                        "low": 9.8,
                        "close": 10.2,
                        "volume": 1000000,
                    }
                ),
                Row(
                    {
                        "date": "2024-01-03",
                        "open": 10.2,
                        "high": 10.7,
                        "low": 10.0,
                        "close": 10.6,
                        "volume": 1200000,
                    }
                ),
            ]
        )

    m.stock_info_sz_name_code = stock_info_sz_name_code
    m.stock_info_sh_name_code = stock_info_sh_name_code
    m.stock_zh_a_daily = stock_zh_a_daily
    sys.modules["akshare"] = m


def test_list_securities_akshare_monkeypatch():
    install_fake_ak()
    p = AkshareProvider()
    items = p.list_securities()
    codes = {s.symbol for s in items}
    assert "000001.SZ" in codes
    assert "600000.SH" in codes


def test_daily_bars_akshare_monkeypatch():
    install_fake_ak()
    p = AkshareProvider()
    bars = p.daily_bars("000001.SZ", date(2024, 1, 2), date(2024, 1, 3))
    assert len(bars) == 2
    assert bars[0].close == 10.2
    assert bars[1].close == 10.6
