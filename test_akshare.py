"""
测试Akshare数据获取
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading.data.providers.akshare_provider import AkshareProvider

def test_akshare():
    print("🧪 测试Akshare数据获取...")
    
    provider = AkshareProvider()
    
    # 测试获取证券列表
    print("\n1. 测试获取证券列表...")
    try:
        securities = provider.list_securities()
        print(f"   获取到 {len(securities)} 只股票")
        
        # 查找测试股票
        test_symbol = "000001.SZ"
        stock_info = next((s for s in securities if s.symbol == test_symbol), None)
        if stock_info:
            print(f"   找到股票: {stock_info.symbol} - {stock_info.name}")
        else:
            print(f"   ❌ 未找到股票 {test_symbol}")
            return
            
    except Exception as e:
        print(f"   ❌ 获取证券列表失败: {e}")
        return
    
    # 测试获取K线数据
    print("\n2. 测试获取K线数据...")
    try:
        from datetime import date, timedelta
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        bars = provider.daily_bars(test_symbol, start_date, end_date)
        print(f"   获取到 {len(bars)} 条K线数据")
        
        if bars:
            latest = bars[-1]
            print(f"   最新数据: {latest.timestamp} - 收盘价 {latest.close}")
        else:
            print("   ❌ 未获取到K线数据")
            
    except Exception as e:
        print(f"   ❌ 获取K线数据失败: {e}")
        return
    
    print("\n✅ Akshare测试完成!")

if __name__ == "__main__":
    test_akshare()
