"use client";

import { useMemo, useState } from "react";
import useSWR from "swr";
import { CandlestickChart } from "@/components/chart/CandlestickChart";
import { IntradayChart } from "@/components/chart/IntradayChart";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export default function StockCard({ symbol }: { symbol: string }) {
  const today = new Date().toISOString().split("T")[0];
  const last90 = new Date(Date.now() - 90 * 24 * 3600 * 1000)
    .toISOString()
    .split("T")[0];
  const { data: bars } = useSWR(
    `http://localhost:8000/api/v1/market/bars/${symbol}?start=${last90}&end=${today}`,
    fetcher
  );
  const [mode, setMode] = useState<"minute" | "daily">("daily");

  const metrics = useMemo(() => {
    if (!bars || bars.length < 2)
      return { price: "-", pct: "-", high: "-", low: "-", vol: "-" };
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
    };
  }, [bars]);

  return (
    <article
      className="flex h-[320px] flex-col overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900"
      role="group"
      aria-label={symbol}
    >
      <div className="grid grid-cols-3 border-b border-zinc-800 p-3">
        <div className="col-span-1">
          <div className="text-xs text-zinc-400">{symbol}</div>
          <div className="pt-1 text-2xl font-semibold">{metrics.price}</div>
          <div
            className={[
              "text-xs",
              (metrics.pct as string).includes("-") ? "text-emerald-400" : "text-rose-400",
            ].join(" ")}
          >
            {metrics.pct}
          </div>
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
            <span>20日均量</span>
            <span className="text-zinc-200">{metrics.vol}</span>
          </div>
        </div>
        <div className="col-span-1 flex items-start justify-end gap-2">
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
            <CandlestickChart data={bars} />
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

