"use client";

import StockCard from "@/components/card/StockCard";

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

  return (
    <div className="space-y-4">
      <div className="no-scrollbar sticky top-14 z-10 -mx-2 overflow-x-auto border-b border-zinc-800 bg-zinc-950/70 px-2 py-3 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center gap-2">
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
      </div>
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
