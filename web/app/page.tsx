"use client";

import { useState } from "react";
import StockCard from "@/components/card/StockCard";
import { Plus, Calendar, TrendingUp } from "lucide-react";

export default function Home() {
  const tabs = ["推荐", "行业", "主题", "热门", "关注"];
  const symbols = [
    "000001.SZ",
    "600000.SH",
    "600519.SH",
    "000333.SZ",
    "300750.SZ",
    "601318.SH",
    "601012.SH",
    "000858.SZ",
    "000002.SZ",
  ];
  
  const [showAddForm, setShowAddForm] = useState(false);
  const [selectedSymbol, setSelectedSymbol] = useState(symbols[0]);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split("T")[0]);
  const [notes, setNotes] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // 提交打板快照
  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/limit-up/snapshots', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol: selectedSymbol,
          date: selectedDate,
          notes: notes || undefined
        })
      });
      
      if (response.ok) {
        setShowAddForm(false);
        setNotes('');
        setSelectedDate(new Date().toISOString().split("T")[0]);
        alert('打板快照录入成功！'); // 刷新页面数据
        window.location.reload();
      } else {
        const error = await response.json();
        alert(`录入失败: ${error.detail}`);
      }
    } catch (error) {
      alert(`录入失败: ${error}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="no-scrollbar sticky top-14 z-10 -mx-2 overflow-x-auto border-b border-zinc-800 bg-zinc-950/70 px-2 py-3 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            {tabs.map((t, i) => (
              <button
                key={t}
                className={[
                  "whitespace-nowrap rounded-full px-5 py-1.5 text-sm transition",
                  i === 0
                    ? "bg-zinc-100 text-zinc-900 shadow"
                    : "bg-[#17191C] text-zinc-300 hover:bg-[#1D1F22]",
                ].join(" ")}
              >
                {t}
              </button>
            ))}
          </div>
          
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="flex items-center gap-2 rounded-full bg-rose-600 px-4 py-2 text-sm text-white hover:bg-rose-700"
          >
            <Plus className="h-4 w-4" />
            录入打板快照
          </button>
        </div>
      </div>
      
      {/* 打板快照录入表单 */}
      {showAddForm && (
        <div className="mx-auto max-w-6xl rounded-2xl border border-rose-500 bg-rose-950/20 p-4">
          <div className="flex items-center gap-4">
            <TrendingUp className="h-5 w-5 text-rose-400" />
            <span className="text-sm font-medium text-rose-400">录入打板快照</span>
          </div>
          
          <div className="mt-4 flex items-center gap-4">
            <div className="flex items-center gap-2">
              <label className="text-xs text-zinc-400">股票:</label>
              <select
                value={selectedSymbol}
                onChange={(e) => setSelectedSymbol(e.target.value)}
                className="rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-zinc-200"
              >
                {symbols.map(symbol => (
                  <option key={symbol} value={symbol}>{symbol}</option>
                ))}
              </select>
            </div>
            
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-zinc-400" />
              <label className="text-xs text-zinc-400">日期:</label>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-zinc-200"
                max={new Date().toISOString().split("T")[0]}
              />
            </div>
            
            <div className="flex-1">
              <input
                type="text"
                placeholder="备注（可选）"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="w-full rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-zinc-200"
              />
            </div>
            
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="rounded bg-rose-600 px-4 py-2 text-sm text-white hover:bg-rose-700 disabled:opacity-50"
            >
              {isSubmitting ? '录入中...' : '录入'}
            </button>
            
            <button
              onClick={() => {
                setShowAddForm(false);
                setNotes('');
                setSelectedDate(new Date().toISOString().split("T")[0]);
              }}
              className="rounded border border-zinc-700 px-4 py-2 text-sm text-zinc-300 hover:bg-zinc-800"
            >
              取消
            </button>
          </div>
        </div>
      )}
      
      <div className="mx-auto max-w-6xl rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-4">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {symbols.map((s) => (
          <StockCard key={s} symbol={s} />
        ))}
        </div>
      </div>
    </div>
  );
}
