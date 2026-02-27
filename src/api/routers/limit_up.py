"""
打板股票快照 API 路由
"""
from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from trading.data.database import get_db
from trading.services.limit_up_service import LimitUpService


# Pydantic 模型用于请求/响应
class LimitUpSnapshotCreate(BaseModel):
    """创建打板快照请求模型"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    symbol: str = Field(..., description="股票编码")
    date: Optional[date] = Field(None, description="快照日期 (YYYY-MM-DD)，默认为当天")
    notes: Optional[str] = Field(None, description="备注信息")


class LimitUpSnapshotResponse(BaseModel):
    """打板快照响应模型"""
    id: int
    symbol: str
    name: str
    snapshot_date: str
    limit_price: float
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    total_market_value: float
    circulating_market_value: float
    max_sealed_amount: float
    volume: float
    turnover: float
    turnover_rate: float
    change_percent: float
    volume_ratio: float
    created_at: str
    updated_at: str
    notes: Optional[str]
    is_limit_up: bool
    sealed_amount_ratio: float


class LimitUpSnapshotList(BaseModel):
    """打板快照列表响应模型"""
    items: List[LimitUpSnapshotResponse]
    total: int
    page: int
    limit: int
    pages: int


router = APIRouter(prefix="/limit-up", tags=["Limit Up Snapshots"])


@router.post("/snapshots", response_model=LimitUpSnapshotResponse, status_code=201)
async def create_snapshot(
    request: LimitUpSnapshotCreate,
    db: Session = Depends(get_db)
):
    """
    创建打板股票快照
    
    - **symbol**: 股票编码（必需）
    - **date**: 快照日期（可选，默认当天北京时间）
    - **notes**: 备注信息（可选）
    """
    service = LimitUpService(db)
    
    try:
        snapshot = await service.create_snapshot(
            symbol=request.symbol,
            target_date=request.date,
            notes=request.notes
        )
        return LimitUpSnapshotResponse(**snapshot.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建快照失败: {str(e)}")


@router.get("/snapshots", response_model=LimitUpSnapshotList)
async def list_snapshots(
    symbol: Optional[str] = Query(None, description="股票编码过滤"),
    start_date: Optional[date] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="结束日期 (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    查询打板快照列表
    
    支持以下过滤条件：
    - **symbol**: 按股票编码过滤
    - **start_date**: 按开始日期过滤
    - **end_date**: 按结束日期过滤
    - **page**: 分页页码
    - **limit**: 每页数量（最大100）
    """
    service = LimitUpService(db)
    
    try:
        snapshots, total = service.get_snapshots(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            page=page,
            limit=limit
        )
        
        pages = (total + limit - 1) // limit  # 计算总页数
        
        return LimitUpSnapshotList(
            items=[LimitUpSnapshotResponse(**s.to_dict()) for s in snapshots],
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/snapshots/statistics")
async def get_statistics(
    db: Session = Depends(get_db)
):
    """
    获取打板快照统计信息
    
    返回：
    - 总快照数量
    - 今日新增数量
    - 最活跃股票（打板次数最多）
    - 最近打板日期
    """
    service = LimitUpService(db)
    
    try:
        # 这里可以添加更多统计逻辑
        snapshots, total = service.get_snapshots(limit=1000)
        
        # 统计最活跃股票
        stock_counts = {}
        for snapshot in snapshots:
            stock_counts[snapshot.symbol] = stock_counts.get(snapshot.symbol, 0) + 1
        
        most_active = sorted(stock_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # 统计今日新增
        today = date.today()
        today_snapshots, today_count = service.get_snapshots(
            start_date=today,
            end_date=today
        )
        
        return {
            "total_snapshots": total,
            "today_new": today_count,
            "most_active_stocks": [
                {"symbol": symbol, "count": count} 
                for symbol, count in most_active
            ],
            "latest_date": snapshots[0].snapshot_date.isoformat() if snapshots else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计失败: {str(e)}")


@router.get("/snapshots/{snapshot_id}", response_model=LimitUpSnapshotResponse)
async def get_snapshot(
    snapshot_id: int,
    db: Session = Depends(get_db)
):
    """
    获取单个打板快照详情
    
    - **snapshot_id**: 快照ID
    """
    service = LimitUpService(db)
    
    try:
        snapshot = service.get_snapshot_by_id(snapshot_id)
        if not snapshot:
            raise HTTPException(status_code=404, detail="快照不存在")
        
        return LimitUpSnapshotResponse(**snapshot.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.delete("/snapshots/{snapshot_id}", status_code=204)
async def delete_snapshot(
    snapshot_id: int,
    db: Session = Depends(get_db)
):
    """
    删除打板快照
    
    - **snapshot_id**: 快照ID
    """
    service = LimitUpService(db)
    
    try:
        success = service.delete_snapshot(snapshot_id)
        if not success:
            raise HTTPException(status_code=404, detail="快照不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")
