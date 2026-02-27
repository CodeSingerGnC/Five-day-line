"""
打板股票快照业务逻辑服务
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc

from trading.data.models.limit_up_table import LimitUpSnapshotTable
from trading.data.models.limit_up import LimitUpSnapshot
from trading.data.providers.akshare_provider import AkshareProvider


class LimitUpService:
    """打板股票快照服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.akshare_provider = AkshareProvider()
    
    async def create_snapshot(
        self, 
        symbol: str, 
        target_date: Optional[date] = None,
        notes: Optional[str] = None
    ) -> LimitUpSnapshot:
        """
        创建打板股票快照
        
        Args:
            symbol: 股票编码
            target_date: 目标日期，默认为当天
            notes: 备注信息
            
        Returns:
            LimitUpSnapshot: 创建的快照对象
            
        Raises:
            ValueError: 股票编码无效或数据获取失败
            Exception: 数据库操作异常
        """
        # 使用北京时间
        beijing_tz = datetime.now().astimezone()
        snapshot_date = target_date or beijing_tz.date()
        
        # 检查是否已存在
        existing = self.db.query(LimitUpSnapshotTable).filter(
            and_(
                LimitUpSnapshotTable.symbol == symbol,
                LimitUpSnapshotTable.snapshot_date == snapshot_date
            )
        ).first()
        
        if existing:
            raise ValueError(f"股票 {symbol} 在 {snapshot_date} 的快照已存在")
        
        # 获取股票数据
        try:
            stock_data = await self._fetch_stock_data(symbol, snapshot_date)
        except Exception as e:
            raise ValueError(f"获取股票 {symbol} 数据失败: {str(e)}")
        
        # 创建快照记录
        snapshot_table = LimitUpSnapshotTable(
            symbol=symbol,
            name=stock_data['name'],
            snapshot_date=snapshot_date,
            limit_price=Decimal(str(stock_data['limit_price'])),
            open_price=Decimal(str(stock_data['open_price'])),
            close_price=Decimal(str(stock_data['close_price'])),
            high_price=Decimal(str(stock_data['high_price'])),
            low_price=Decimal(str(stock_data['low_price'])),
            total_market_value=Decimal(str(stock_data.get('total_market_value', 0))),
            circulating_market_value=Decimal(str(stock_data.get('circulating_market_value', 0))),
            max_sealed_amount=Decimal(str(stock_data.get('max_sealed_amount', 0))),
            volume=Decimal(str(stock_data.get('volume', 0))),
            turnover=Decimal(str(stock_data.get('turnover', 0))),
            turnover_rate=Decimal(str(stock_data.get('turnover_rate', 0))),
            change_percent=Decimal(str(stock_data.get('change_percent', 0))),
            volume_ratio=Decimal(str(stock_data.get('volume_ratio', 0))),
            notes=notes
        )
        
        # 保存到数据库
        self.db.add(snapshot_table)
        self.db.commit()
        self.db.refresh(snapshot_table)
        
        # 转换为业务对象
        return self._table_to_model(snapshot_table)
    
    async def _fetch_stock_data(self, symbol: str, target_date: date) -> dict:
        """
        从 Akshare 获取股票数据
        
        Args:
            symbol: 股票编码
            target_date: 目标日期
            
        Returns:
            dict: 股票数据字典
        """
        # 获取基本信息
        securities = self.akshare_provider.list_securities()
        stock_info = next((s for s in securities if s.symbol == symbol), None)
        if not stock_info:
            raise ValueError(f"未找到股票 {symbol}")
        
        # 获取 K 线数据
        bars = self.akshare_provider.daily_bars(symbol, target_date, target_date)
        if not bars:
            raise ValueError(f"未找到股票 {symbol} 在 {target_date} 的交易数据")
        
        bar = bars[0]  # 获取当天的数据
        
        # 简化计算，使用固定值
        return {
            'name': stock_info.name,
            'limit_price': bar.close * 1.1,  # 简化涨停价计算
            'open_price': bar.open,
            'close_price': bar.close,
            'high_price': bar.high,
            'low_price': bar.low,
            'total_market_value': 1000.0,  # 临时固定值
            'circulating_market_value': 800.0,  # 临时固定值
            'max_sealed_amount': 5000.0,  # 临时固定值
            'volume': bar.volume,
            'turnover': bar.volume * bar.close / 10000,
            'turnover_rate': 5.0,  # 临时固定值
            'change_percent': 10.0,  # 临时固定值
            'volume_ratio': 1.2  # 临时固定值
        }
    
    def _get_previous_close(self, symbol: str, target_date: date) -> Decimal:
        """获取前一交易日收盘价"""
        # 简化实现，实际应该获取前一交易日
        from datetime import timedelta
        prev_date = target_date - timedelta(days=1)
        
        try:
            bars = self.akshare_provider.daily_bars(symbol, prev_date, prev_date)
            if bars:
                return Decimal(str(bars[0].close))
        except Exception:
            pass
        
        # 如果获取不到，返回一个默认值
        return Decimal('10.0')  # 默认价格
    
    def _is_st_stock(self, symbol: str) -> bool:
        """判断是否为 ST 股票（ST 股涨跌幅限制为 5%）"""
        # 简化实现，实际应该查询股票名称
        return False
    
    async def _fetch_market_data(self, symbol: str, target_date: date) -> dict:
        """
        获取市场数据（市值、封板金额等）
        
        这里需要扩展 AkshareProvider 或使用其他数据源
        """
        # 临时返回默认值，后续需要实现真实数据获取
        return {
            'total_market_value': 0,
            'circulating_market_value': 0,
            'max_sealed_amount': 0,
            'turnover_rate': 0,
            'volume_ratio': 0
        }
    
    def get_snapshots(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[List[LimitUpSnapshot], int]:
        """
        查询打板快照列表
        
        Args:
            symbol: 股票编码过滤
            start_date: 开始日期
            end_date: 结束日期
            page: 页码
            limit: 每页数量
            
        Returns:
            Tuple[List[LimitUpSnapshot], int]: 快照列表和总数
        """
        query = self.db.query(LimitUpSnapshotTable)
        
        # 应用过滤条件
        if symbol:
            query = query.filter(LimitUpSnapshotTable.symbol == symbol)
        
        if start_date:
            query = query.filter(LimitUpSnapshotTable.snapshot_date >= start_date)
        
        if end_date:
            query = query.filter(LimitUpSnapshotTable.snapshot_date <= end_date)
        
        # 获取总数
        total = query.count()
        
        # 分页查询
        offset = (page - 1) * limit
        snapshots = query.order_by(desc(LimitUpSnapshotTable.snapshot_date)).offset(offset).limit(limit).all()
        
        # 转换为业务对象
        return [self._table_to_model(s) for s in snapshots], total
    
    def get_snapshot_by_id(self, snapshot_id: int) -> Optional[LimitUpSnapshot]:
        """根据ID获取快照"""
        snapshot = self.db.query(LimitUpSnapshotTable).filter(
            LimitUpSnapshotTable.id == snapshot_id
        ).first()
        
        return self._table_to_model(snapshot) if snapshot else None
    
    def delete_snapshot(self, snapshot_id: int) -> bool:
        """删除快照"""
        snapshot = self.db.query(LimitUpSnapshotTable).filter(
            LimitUpSnapshotTable.id == snapshot_id
        ).first()
        
        if snapshot:
            self.db.delete(snapshot)
            self.db.commit()
            return True
        
        return False
    
    def _table_to_model(self, table: LimitUpSnapshotTable) -> LimitUpSnapshot:
        """数据库表对象转换为业务模型对象"""
        return LimitUpSnapshot(
            id=table.id,
            symbol=table.symbol,
            name=table.name,
            snapshot_date=table.snapshot_date,
            limit_price=table.limit_price,
            open_price=table.open_price,
            close_price=table.close_price,
            high_price=table.high_price,
            low_price=table.low_price,
            total_market_value=table.total_market_value,
            circulating_market_value=table.circulating_market_value,
            max_sealed_amount=table.max_sealed_amount,
            volume=table.volume,
            turnover=table.turnover,
            turnover_rate=table.turnover_rate,
            change_percent=table.change_percent,
            volume_ratio=table.volume_ratio,
            created_at=table.created_at,
            updated_at=table.updated_at,
            notes=table.notes
        )
