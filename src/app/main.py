from datetime import date
from trading.data.providers.akshare_provider import AkshareProvider
from trading.visualization.chart import plot_candle


def main() -> None:
    # 1. 初始化数据提供者 (Akshare)
    provider = AkshareProvider()
    symbol = "000001.SZ"
    start_date = date(2024, 1, 1)
    end_date = date(2024, 3, 31)  # 获取一个季度的数据

    print(f"正在获取 {symbol} 从 {start_date} 到 {end_date} 的日线数据...")

    try:
        # 2. 获取行情数据
        bars = provider.daily_bars(symbol, start_date, end_date)
        print(f"获取到 {len(bars)} 条行情数据")

        if bars:
            # 3. 绘制并保存蜡烛图
            chart_filename = f"{symbol}_candle.png"
            plot_candle(
                bars, title=f"{symbol} Candlestick (2024-Q1)", save_path=chart_filename
            )

    except Exception as e:
        print(f"执行失败: {e}")


if __name__ == "__main__":
    main()
