export default function Topbar() {
  return (
    <header className="fixed inset-x-0 top-0 z-40 h-14 border-b border-[var(--border)] bg-[var(--panel)]/80 backdrop-blur">
      <div className="mx-auto grid h-full max-w-[1200px] grid-cols-3 items-center px-6">
        <div className="hidden md:block" />
        <div className="flex items-center justify-center">
          <div className="w-full max-w-[680px]">
            <div className="flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg)] px-5 py-2">
              <div className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
              <input
                aria-label="搜索"
                placeholder="搜索"
                className="w-full bg-transparent text-sm text-zinc-300 placeholder-zinc-600 outline-none"
              />
            </div>
          </div>
        </div>
        <div className="flex items-center justify-end">
          <div className="select-none text-xs tracking-[0.2em] text-zinc-400">
            流畅 · 极简 · 专注
          </div>
        </div>
      </div>
    </header>
  );
}
