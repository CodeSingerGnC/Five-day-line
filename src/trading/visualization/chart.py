import pandas as pd
import mplfinance as mpf  # type: ignore
from typing import List
from trading.data.models.bar import Bar


def plot_candle(
    bars: List[Bar], title: str = "Candlestick Chart", save_path: str = "chart.png"
) -> None:
    """
    将行情数据 (Bar 列表) 绘制成专业的蜡烛图 (K线图) 并保存为图片文件。

    该函数使用 mplfinance 库，默认采用 'charles' 样式 (红涨绿跌)，
    并自动叠加 5、10、20 日移动平均线 (MA) 以及成交量副图。

    :param bars: Bar 对象列表，需包含时间戳、开高低收价格及成交量信息
    :param title: 图表标题，默认为 "Candlestick Chart"
    :param save_path: 图片保存路径，默认为当前目录下的 "chart.png"
    """
    if not bars:
        print("警告: 传入的数据列表为空，无法绘制图表")
        return

    # 1. 数据转换: Bar List -> DataFrame
    # mplfinance 要求索引为 DatetimeIndex，且列名为 Open, High, Low, Close, Volume
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
    # 将 Date 列设为索引，inplace=True 表示直接修改原 DataFrame
    df.set_index("Date", inplace=True)

    # 2. 设置绘图样式
    # base_mpf_style='charles': 使用经典的红绿配色 (涨红跌绿)
    # rc={'font.family': 'sans-serif'}: 设置字体为无衬线字体，避免中文乱码或字体缺失问题
    style = mpf.make_mpf_style(
        base_mpf_style="charles", rc={"font.family": "sans-serif"}
    )

    # 3. 执行绘图并保存
    # type='candle': 绘制蜡烛图
    # volume=True: 显示成交量副图
    # mav=(5, 10, 20): 计算并绘制 5日、10日、20日 简单移动平均线
    # tight_layout=True: 自动调整布局以去除多余白边
    mpf.plot(
        df,
        type="candle",
        title=title,
        ylabel="Price",
        ylabel_lower="Volume",
        volume=True,
        mav=(5, 10, 20),
        style=style,
        savefig=save_path,
        figratio=(12, 8),
        tight_layout=True,
    )
    print(f"成功: 图表已保存至 {save_path}")
