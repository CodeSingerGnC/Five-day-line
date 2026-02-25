"use client";

export default function SpecCard() {
  return (
    <article className="overflow-hidden rounded-2xl border border-[var(--border)] bg-[var(--panel)]">
      <div className="h-40 w-full bg-[#1B1D20]" />
      <div className="space-y-2 p-3">
        <div className="h-3 w-3/4 rounded bg-[#2A2E33]" />
        <div className="h-3 w-1/2 rounded bg-[#23272C]" />
      </div>
    </article>
  );
}

