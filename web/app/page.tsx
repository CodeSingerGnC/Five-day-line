"use client";

import { useState } from "react";
import useSWR from "swr";
import { CandlestickChart } from "@/components/chart/CandlestickChart";
import { Card, Title, Text } from "@tremor/react";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function Home() {
  // 默认使用平安银行作为演示
  const [symbol, setSymbol] = useState("000001.SZ");
  const today = new Date().toISOString().split("T")[0];
  const lastYear = new Date(new Date().setFullYear(new Date().getFullYear() - 1))
    .toISOString()
    .split("T")[0];

  const { data: bars, error } = useSWR(
    `http://localhost:8000/api/v1/market/bars/${symbol}?start=${lastYear}&end=${today}`,
    fetcher
  );

  if (error) return <div>Failed to load data</div>;
  if (!bars) return <div>Loading...</div>;

  return (
    <main className="p-12">
      <Title>A股行情可视化</Title>
      <Text>展示最近一年的日线数据</Text>

      <Card className="mt-6">
        <CandlestickChart data={bars} />
      </Card>
    </main>
  );
}
