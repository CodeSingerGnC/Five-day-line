from datetime import date, datetime
from typing import Any, List
from trading.data.models.security import Security
from trading.data.provider import DataProvider
from trading.data.models.bar import Bar


def _to_ak_symbol(symbol: str) -> str:
    """
    将标准 symbol (如 000001.SZ) 转换为 akshare 格式 (如 sz000001)。

    :param symbol: 标准格式的股票代码，如 "000001.SZ" 或 "600000.SH"
    :return: akshare 格式的股票代码，如 "sz000001"
    """
    code, exch = symbol.split(".")
    p = "sz" if exch == "SZ" else "sh"
    return f"{p}{code}"


def _ak() -> Any:
    """
    延迟导入 akshare 模块。
    akshare 及其依赖较大，延迟导入可加快启动速度，
    并避免在仅做静态检查时强制要求安装该库。
    """
    return __import__("akshare")


class AkshareProvider(DataProvider):
    """
    基于 Akshare 的数据提供者实现。

    提供 A 股市场的证券列表获取与日线行情数据获取功能。
    Akshare 是一个开源财经数据接口库，封装了众多公开数据源。
    """

    def list_securities(self) -> List[Security]:
        """
        获取当前 A 股市场所有上市股票列表。

        分别获取深交所 (SZSE) 和上交所 (SSE) 的股票信息，
        并统一转换为 Security 对象列表。

        :return: 包含所有 A 股股票信息的列表
        """
        ak = _ak()
        # 获取深交所股票列表¥
        sz = ak.stock_info_sz_name_code()
        # 获取上交所股票列表
        sh = ak.stock_info_sh_name_code()

        out: List[Security] = []

        # 处理深交所数据
        for _, row in sz.iterrows():
            out.append(
                Security(
                    symbol=f"{row['code']}.SZ",
                    name=row["name"],
                    exchange="SZSE",
                    list_date=None,  # akshare 此接口暂未提供上市日期
                )
            )

        # 处理上交所数据
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
        """
        获取指定股票在指定日期范围内的日线行情数据。

        :param symbol: 股票代码，格式如 "000001.SZ"
        :param start: 开始日期 (包含)
        :param end: 结束日期 (包含)
        :return: Bar 对象列表，按时间升序排列
        """
        ak = _ak()
        # 转换为 akshare 所需的 symbol 格式
        s = _to_ak_symbol(symbol)

        # 调用 akshare 获取日线数据，adjust="" 表示不复权
        # 注意：akshare 返回的是全量历史数据，需要在内存中过滤日期
        df = ak.stock_zh_a_daily(symbol=s, adjust="")

        out: List[Bar] = []
        for _, row in df.iterrows():
            # 解析日期字符串 "YYYY-MM-DD"
            d = datetime.strptime(str(row["date"]), "%Y-%m-%d").date()

            # 过滤不在请求范围内的数据
            if d < start or d > end:
                continue

            # 构造带时间戳的 datetime 对象 (日线通常设为当日 0 点)
            ts = datetime(d.year, d.month, d.day)

            # 构造 Bar 对象
            out.append(
                Bar(
                    symbol=symbol,
                    timestamp=ts,
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    # 处理不同接口返回 volume 字段名可能不一致的情况
                    volume=float(row.get("volume", row.get("vol", 0))),
                )
            )
        return out
