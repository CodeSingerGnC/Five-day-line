"use client";

import { createChart, ColorType, IChartApi } from "lightweight-charts";
import React, { useEffect, useRef } from "react";

export function IntradayChart({ data }: { data: any[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      layout: {
        background: { type: ColorType.Solid, color: "#0F1113" },
        textColor: "#D1D5DB",
      },
      grid: {
        vertLines: { color: "#16191D" },
        horzLines: { color: "#16191D" },
      },
      width: ref.current.clientWidth,
      height: 180,
    });
    chartRef.current = chart;
    const series = chart.addAreaSeries({
      lineColor: "#60A5FA",
      topColor: "rgba(96,165,250,0.35)",
      bottomColor: "rgba(96,165,250,0.02)",
    });
    const formatted = data.map((d) => ({
      time: String(d.timestamp).split("T")[0],
      value: Number(d.close),
    }));
    series.setData(formatted);
    chart.timeScale().fitContent();
    const onResize = () => {
      if (ref.current) {
        chart.applyOptions({ width: ref.current.clientWidth });
      }
    };
    window.addEventListener("resize", onResize);
    return () => {
      window.removeEventListener("resize", onResize);
      chart.remove();
    };
  }, [data]);
  return <div ref={ref} className="w-full" />;
}

