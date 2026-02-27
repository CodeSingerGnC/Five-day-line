"use client";

import { useMemo, useState } from "react";
import useSWR from "swr";
import { CandlestickChart } from "@/components/chart/CandlestickChart";
import { IntradayChart } from "@/components/chart/IntradayChart";
import { TrendingUp } from "lucide-react";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

// Bar数据类型定义
interface Bar {
  symbol: string;
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

// 打板快照数据类型
interface LimitUpSnapshot {
  id: number;
  symbol: string;
  name: string;
  snapshot_date: string;
  limit_price: number;
  open_price: number;
  close_price: number;
  high_price: number;
  low_price: number;
  total_market_value: number;
  circulating_market_value: number;
  max_sealed_amount: number;
  volume: number;
  turnover: number;
  turnover_rate: number;
  change_percent: number;
  volume_ratio: number;
  created_at: string;
  updated_at: string;
  notes?: string;
  is_limit_up: boolean;
  sealed_amount_ratio: number;
}

export default function StockCard({ symbol }: { symbol: string }) {
  const today = new Date().toISOString().split("T")[0];
  const last90 = new Date(Date.now() - 90 * 24 * 3600 * 1000)
    .toISOString()
    .split("T")[0];
  
  // 获取普通K线数据
  const { data: bars }: { data?: Bar[] } = useSWR(
    `http://localhost:8000/api/v1/market/bars/${symbol}?start=${last90}&end=${today}`,
    fetcher
  );
  
  // 获取打板快照数据
  const { data: snapshots } = useSWR(
    `http://localhost:8000/api/v1/limit-up/snapshots?symbol=${symbol}&limit=10`,
    fetcher
  );
  
  const [mode, setMode] = useState<"minute" | "daily">("daily");

  // 获取当前显示的快照数据
  const currentSnapshot = useMemo(() => {
    if (!snapshots || snapshots.items.length === 0) return null;
    return snapshots.items[0]; // 最新的一条
  }, [snapshots]);
  
  // 根据快照数据调整图表显示范围
  const chartData = useMemo(() => {
    if (!bars) return [];
    
    if (currentSnapshot) {
      // 如果有打板快照，显示前后45个交易日
      const snapshotDate = new Date(currentSnapshot.snapshot_date);
      const snapshotIndex = bars.findIndex((bar: Bar) => 
        new Date(bar.timestamp).toDateString() === snapshotDate.toDateString()
      );
      
      if (snapshotIndex !== -1) {
        const startIndex = Math.max(0, snapshotIndex - 15);
        const endIndex = Math.min(bars.length, snapshotIndex + 31);
        return bars.slice(startIndex, endIndex);
      }
    }
    
    return bars;
  }, [bars, currentSnapshot]);
  
  const metrics = useMemo(() => {
    if (!bars || bars.length < 2)
      return { price: "-", pct: "-", high: "-", low: "-", vol: "-" };
    
    // 优先使用打板快照数据
    if (currentSnapshot) {
      return {
        price: currentSnapshot.close_price.toFixed(2),
        pct: `${currentSnapshot.change_percent >= 0 ? "+" : ""}${currentSnapshot.change_percent.toFixed(2)}%`,
        high: currentSnapshot.high_price.toFixed(2),
        low: currentSnapshot.low_price.toFixed(2),
        vol: Math.round(currentSnapshot.volume).toLocaleString(),
        limitPrice: currentSnapshot.limit_price.toFixed(2),
        isLimitUp: currentSnapshot.is_limit_up,
        sealedAmount: currentSnapshot.max_sealed_amount.toFixed(0),
        marketValue: (currentSnapshot.total_market_value / 10000).toFixed(1), // 转换为万亿元
        turnoverRate: `${currentSnapshot.turnover_rate.toFixed(2)}%`
      };
    }
    
    // 使用普通数据
    const last = bars[bars.length - 1];
    const prev = bars[bars.length - 2];
    const pct = ((Number(last.close) - Number(prev.close)) / Number(prev.close)) * 100;
    const hi = Math.max(...bars.map((x: any) => Number(x.high)));
    const lo = Math.min(...bars.map((x: any) => Number(x.low)));
    const v = Math.round(
      bars.slice(-20).reduce((s: number, x: any) => s + Number(x.volume), 0) / 20
    );
    return {
      price: Number(last.close).toFixed(2),
      pct: `${pct >= 0 ? "+" : ""}${pct.toFixed(2)}%`,
      high: hi.toFixed(2),
      low: lo.toFixed(2),
      vol: v.toLocaleString(),
      limitPrice: "-",
      isLimitUp: false,
      sealedAmount: "-",
      marketValue: "-",
      turnoverRate: "-"
    };
  }, [bars, currentSnapshot]);

  // 提交打板快照
  const handleSubmit = async () => {
    // 移除提交逻辑，由主页面处理
  };

  return (
    <article
      className={`flex h-[320px] flex-col overflow-hidden rounded-2xl border ${
        currentSnapshot?.is_limit_up ? 'border-rose-500 bg-rose-950/20' : 'border-zinc-800 bg-zinc-900'
      }`}
      role="group"
      aria-label={symbol}
    >
      <div className="grid grid-cols-3 border-b border-zinc-800 p-3">
        <div className="col-span-1">
          <div className="flex items-center gap-1">
            <span className="text-xs text-zinc-400">{symbol}</span>
            {currentSnapshot?.is_limit_up && (
              <TrendingUp className="h-3 w-3 text-rose-400" />
            )}
          </div>
          <div className="pt-1 text-2xl font-semibold">{metrics.price}</div>
          <div
            className={[
              "text-xs",
              (metrics.pct as string).includes("-") ? "text-emerald-400" : "text-rose-400",
            ].join(" ")}
          >
            {metrics.pct}
          </div>
          {currentSnapshot && (
            <div className="mt-1 text-xs text-zinc-400">
              涨停价: {metrics.limitPrice}
            </div>
          )}
        </div>
        <div className="col-span-1 space-y-1">
          <div className="flex items-center justify-between text-xs text-zinc-400">
            <span>高</span>
            <span className="text-zinc-200">{metrics.high}</span>
          </div>
          <div className="flex items-center justify-between text-xs text-zinc-400">
            <span>低</span>
            <span className="text-zinc-200">{metrics.low}</span>
          </div>
          <div className="flex items-center justify-between text-xs text-zinc-400">
            <span>成交量</span>
            <span className="text-zinc-200">{metrics.vol}</span>
          </div>
          {currentSnapshot && (
            <>
              <div className="flex items-center justify-between text-xs text-zinc-400">
                <span>封板金额</span>
                <span className="text-zinc-200">{metrics.sealedAmount}万</span>
              </div>
              <div className="flex items-center justify-between text-xs text-zinc-400">
                <span>市值</span>
                <span className="text-zinc-200">{metrics.marketValue}万亿</span>
              </div>
            </>
          )}
        </div>
        <div className="col-span-1 flex items-start justify-end">
          <div className="inline-flex rounded-full border border-zinc-700 p-1">
            <button
              className={[
                "rounded-full px-3 py-1 text-xs",
                mode === "minute"
                  ? "bg-zinc-100 text-zinc-900"
                  : "text-zinc-300 hover:text-white",
              ].join(" ")}
              onClick={() => setMode("minute")}
            >
              分时
            </button>
            <button
              className={[
                "rounded-full px-3 py-1 text-xs",
                mode === "daily"
                  ? "bg-zinc-100 text-zinc-900"
                  : "text-zinc-300 hover:text-white",
              ].join(" ")}
              onClick={() => setMode("daily")}
            >
              日线
            </button>
          </div>
        </div>
      </div>
      
      <div className="flex-1 p-2">
        {!bars ? (
          <div className="h-full rounded-lg border border-zinc-800 bg-zinc-950" />
        ) : mode === "daily" ? (
          <div className="h-full rounded-lg border border-zinc-800 bg-zinc-950 p-2">
            <CandlestickChart data={chartData} />
          </div>
        ) : (
          <div className="h-full rounded-lg border border-zinc-800 bg-zinc-950 p-2">
            <IntradayChart data={bars} />
          </div>
        )}
      </div>
    </article>
  );
}

