from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Bar:
    """
    K 线数据模型 (Bar / Candlestick)。
    代表某个时间窗口 (如日、分钟) 内的单一市场行情数据点。

    属性:
        symbol (str): 标的代码，例如 "000001.SZ"。
        timestamp (datetime): 该 Bar 的开始时间或结束时间 (取决于数据源定义)。
        open (float): 开盘价。
        high (float): 最高价。
        low (float): 最低价。
        close (float): 收盘价。
        volume (float): 成交量 (通常为股数或手数)。

    注意:
        frozen=True 表示该对象一旦创建不可修改 (Immutable)，
        这有助于在多线程或缓存场景下的安全性。
    """

    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
