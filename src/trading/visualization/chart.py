import pandas as pd
import mplfinance as mpf  # type: ignore
from typing import List
from trading.data.models.bar import Bar


def plot_candle(
    bars: List[Bar], title: str = "Candlestick Chart", save_path: str = "chart.png"
) -> None:
    """
    将 Bar 列表绘制成蜡烛图并保存为图片
    """
    if not bars:
        print("没有数据可以绘制")
        return

    # 1. 转换为 DataFrame
    data = []
    for b in bars:
        data.append(
            {
                "Date": b.timestamp,
                "Open": b.open,
                "High": b.high,
                "Low": b.low,
                "Close": b.close,
                "Volume": b.volume,
            }
        )

    df = pd.DataFrame(data)
    df.set_index("Date", inplace=True)

    # 2. 设置绘图样式 (使用内置的 'charles' 样式，类似通达信/东方财富)
    style = mpf.make_mpf_style(
        base_mpf_style="charles", rc={"font.family": "sans-serif"}
    )

    # 3. 绘图并保存
    mpf.plot(
        df,
        type="candle",
        title=title,
        ylabel="Price",
        ylabel_lower="Volume",
        volume=True,
        mav=(5, 10, 20),  # 顺便画出 5, 10, 20 日均线
        style=style,
        savefig=save_path,
        figratio=(12, 8),
        tight_layout=True,
    )
    print(f"图表已保存至: {save_path}")
