from datetime import date
from typing import List
from trading.data.models.bar import Bar
from trading.data.models.security import Security


class DataProvider:
    """
    数据提供者抽象基类 (Interface)。
    定义了所有数据源 (如 Akshare, Tushare, 本地 CSV) 必须实现的通用接口。
    """

    def list_securities(self) -> List[Security]:
        """
        列出所有可用证券信息。

        :return: Security 对象列表
        :raises NotImplementedError: 如果子类未实现此方法
        """
        raise NotImplementedError

    def daily_bars(self, symbol: str, start: date, end: date) -> List[Bar]:
        """
        获取指定证券的历史日线行情。

        :param symbol: 证券代码
        :param start: 开始日期
        :param end: 结束日期
        :return: Bar 对象列表 (按时间排序)
        :raises NotImplementedError: 如果子类未实现此方法
        """
        raise NotImplementedError
