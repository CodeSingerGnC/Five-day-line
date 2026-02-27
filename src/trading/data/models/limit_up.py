from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from decimal import Decimal


@dataclass
class LimitUpSnapshot:
    """
    打板股票快照数据模型
    
    记录涨停板股票在特定日期的完整交易数据快照
    """
    id: Optional[int] = None
    symbol: str = ""                    # 股票编码，如 "000001.SZ"
    name: str = ""                      # 股票名称
    snapshot_date: date = date.today()   # 快照日期（打板日期）
    
    # 价格数据
    limit_price: Decimal = Decimal('0')     # 涨停价
    open_price: Decimal = Decimal('0')      # 开盘价
    close_price: Decimal = Decimal('0')     # 收盘价
    high_price: Decimal = Decimal('0')      # 最高价
    low_price: Decimal = Decimal('0')       # 最低价
    
    # 市值数据（单位：亿元）
    total_market_value: Decimal = Decimal('0')        # 总市值
    circulating_market_value: Decimal = Decimal('0')   # 流通市值
    
    # 交易数据
    max_sealed_amount: Decimal = Decimal('0')    # 最大封板金额（万元）
    volume: Decimal = Decimal('0')               # 成交量（手）
    turnover: Decimal = Decimal('0')             # 成交额（万元）
    turnover_rate: Decimal = Decimal('0')       # 换手率（%）
    
    # 技术指标
    change_percent: Decimal = Decimal('0')      # 涨跌幅（%）
    volume_ratio: Decimal = Decimal('0')         # 量比
    
    # 元数据
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    notes: Optional[str] = None                  # 备注信息
    
    def __post_init__(self):
        """数据验证"""
        if not self.symbol:
            raise ValueError("股票编码不能为空")
        if not self.name:
            raise ValueError("股票名称不能为空")
        if self.limit_price <= 0:
            raise ValueError("涨停价必须大于0")
    
    @property
    def is_limit_up(self) -> bool:
        """判断是否真实涨停（收盘价等于涨停价）"""
        return self.close_price == self.limit_price
    
    @property
    def sealed_amount_ratio(self) -> Decimal:
        """封板金额占比（封板金额/成交额）"""
        if self.turnover == 0:
            return Decimal('0')
        return (self.max_sealed_amount / self.turnover) * 100
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'snapshot_date': self.snapshot_date.isoformat(),
            'limit_price': float(self.limit_price),
            'open_price': float(self.open_price),
            'close_price': float(self.close_price),
            'high_price': float(self.high_price),
            'low_price': float(self.low_price),
            'total_market_value': float(self.total_market_value),
            'circulating_market_value': float(self.circulating_market_value),
            'max_sealed_amount': float(self.max_sealed_amount),
            'volume': float(self.volume),
            'turnover': float(self.turnover),
            'turnover_rate': float(self.turnover_rate),
            'change_percent': float(self.change_percent),
            'volume_ratio': float(self.volume_ratio),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'notes': self.notes,
            'is_limit_up': self.is_limit_up,
            'sealed_amount_ratio': float(self.sealed_amount_ratio)
        }
