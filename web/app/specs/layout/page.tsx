import SpecCard from "@/components/spec/SpecCard";

export default function SpecLayout() {
  return (
    <div className="space-y-4">
      <div className="-mx-2 border-b border-[var(--border)] bg-[var(--bg)] px-2 py-3">
        <div className="mx-auto flex max-w-[1200px] items-center gap-2">
          {["推荐", "行业", "主题", "热门", "关注"].map((t, i) => (
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
      <div className="mx-auto max-w-[1200px] rounded-2xl border border-[var(--border)] bg-[var(--panel)] p-4">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3 lg:grid-cols-4">
          {Array.from({ length: 12 }).map((_, i) => (
            <SpecCard key={i} />
          ))}
        </div>
      </div>
    </div>
  );
}

