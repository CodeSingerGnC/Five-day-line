from datetime import date
from typing import List
from fastapi import APIRouter, HTTPException, Query
from trading.data.models.bar import Bar
from trading.data.models.security import Security
from trading.data.providers.akshare_provider import AkshareProvider

router = APIRouter(prefix="/market", tags=["Market Data"])
provider = AkshareProvider()


@router.get("/securities", response_model=List[Security])
def list_securities():
    """
    获取全市场证券列表
    """
    try:
        return provider.list_securities()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取证券列表失败: {str(e)}")


@router.get("/bars/{symbol}", response_model=List[Bar])
def get_bars(
    symbol: str,
    start: date = Query(..., description="开始日期 (YYYY-MM-DD)"),
    end: date = Query(..., description="结束日期 (YYYY-MM-DD)"),
):
    """
    获取指定证券的日线行情数据
    """
    try:
        bars = provider.daily_bars(symbol, start, end)
        return bars
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行情数据失败: {str(e)}")
