"""
打板股票快照数据库表模型（SQLAlchemy ORM）
"""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, Text, Index, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class LimitUpSnapshotTable(Base):
    """
    打板股票快照数据库表模型
    """
    __tablename__ = "limit_up_snapshots"
    
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    
    # 基础信息
    symbol = Column(String(20), nullable=False, comment="股票编码")
    name = Column(String(100), nullable=False, comment="股票名称")
    snapshot_date = Column(Date, nullable=False, comment="快照日期")
    
    # 价格数据（使用 Numeric 确保精度）
    limit_price = Column(Numeric(10, 3), nullable=False, comment="涨停价")
    open_price = Column(Numeric(10, 3), nullable=False, comment="开盘价")
    close_price = Column(Numeric(10, 3), nullable=False, comment="收盘价")
    high_price = Column(Numeric(10, 3), nullable=False, comment="最高价")
    low_price = Column(Numeric(10, 3), nullable=False, comment="最低价")
    
    # 市值数据（单位：亿元）
    total_market_value = Column(Numeric(20, 2), comment="总市值")
    circulating_market_value = Column(Numeric(20, 2), comment="流通市值")
    
    # 交易数据
    max_sealed_amount = Column(Numeric(20, 2), comment="最大封板金额（万元）")
    volume = Column(Numeric(20, 2), comment="成交量（手）")
    turnover = Column(Numeric(20, 2), comment="成交额（万元）")
    turnover_rate = Column(Numeric(8, 4), comment="换手率（%）")
    
    # 技术指标
    change_percent = Column(Numeric(8, 4), comment="涨跌幅（%）")
    volume_ratio = Column(Numeric(8, 4), comment="量比")
    
    # 元数据
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    notes = Column(Text, comment="备注信息")
    
    # 约束和索引
    __table_args__ = (
        UniqueConstraint('symbol', 'snapshot_date', name='uq_symbol_date'),
        Index('idx_symbol_date', 'symbol', 'snapshot_date'),
        Index('idx_snapshot_date', 'snapshot_date'),
        Index('idx_created_at', 'created_at'),
        {'comment': '打板股票快照表'}
    )
    
    def __repr__(self):
        return f"<LimitUpSnapshot(symbol={self.symbol}, date={self.snapshot_date}, name={self.name})>"
    
    @property
    def is_limit_up(self) -> bool:
        """判断是否真实涨停"""
        return self.close_price == self.limit_price
    
    @property
    def sealed_amount_ratio(self) -> Decimal:
        """封板金额占比"""
        if self.turnover == 0:
            return Decimal('0')
        return (self.max_sealed_amount / self.turnover) * 100
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'snapshot_date': self.snapshot_date.isoformat() if self.snapshot_date else None,
            'limit_price': float(self.limit_price) if self.limit_price else 0,
            'open_price': float(self.open_price) if self.open_price else 0,
            'close_price': float(self.close_price) if self.close_price else 0,
            'high_price': float(self.high_price) if self.high_price else 0,
            'low_price': float(self.low_price) if self.low_price else 0,
            'total_market_value': float(self.total_market_value) if self.total_market_value else 0,
            'circulating_market_value': float(self.circulating_market_value) if self.circulating_market_value else 0,
            'max_sealed_amount': float(self.max_sealed_amount) if self.max_sealed_amount else 0,
            'volume': float(self.volume) if self.volume else 0,
            'turnover': float(self.turnover) if self.turnover else 0,
            'turnover_rate': float(self.turnover_rate) if self.turnover_rate else 0,
            'change_percent': float(self.change_percent) if self.change_percent else 0,
            'volume_ratio': float(self.volume_ratio) if self.volume_ratio else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'notes': self.notes,
            'is_limit_up': self.is_limit_up,
            'sealed_amount_ratio': float(self.sealed_amount_ratio)
        }
