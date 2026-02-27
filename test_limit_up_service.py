"""
测试打板服务
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from datetime import date
from trading.services.limit_up_service import LimitUpService
from trading.data.database import get_db, TestingSessionLocal

def test_limit_up_service():
    print("🧪 测试打板服务...")
    
    # 创建测试数据库会话
    db = TestingSessionLocal()
    
    try:
        service = LimitUpService(db)
        
        # 测试获取股票数据
        print("\n1. 测试获取股票数据...")
        symbol = "000001.SZ"
        target_date = date(2024, 1, 15)
        
        try:
            # 直接测试数据获取
            stock_data = await service._fetch_stock_data(symbol, target_date)
            print(f"   获取成功: {stock_data}")
        except Exception as e:
            print(f"   ❌ 获取失败: {e}")
            import traceback
            traceback.print_exc()
            
    finally:
        db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_limit_up_service())
