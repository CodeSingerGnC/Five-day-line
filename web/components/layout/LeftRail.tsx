"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Compass, PlusCircle, Bell, User, Menu } from "lucide-react";

const items = [
  { href: "/", label: "发现", icon: Compass },
  { href: "/publish", label: "发布", icon: PlusCircle },
  { href: "/notifications", label: "通知", icon: Bell },
  { href: "/me", label: "我", icon: User },
];

export default function LeftRail() {
  const pathname = usePathname();
  return (
    <aside
      className="fixed inset-y-0 left-0 z-30 hidden w-60 md:block"
      aria-label="left-rail"
    >
      <div className="flex h-full flex-col justify-between border-r border-[var(--border)] bg-[var(--panel)] px-3 pt-16 pb-4">
        <nav className="space-y-2">
          {items.map((it) => {
            const active = pathname === it.href;
            const Icon = it.icon;
            return (
              <Link
                key={it.href}
                href={it.href}
                className={[
                  "group flex items-center gap-3 rounded-xl px-3 py-2 text-sm",
                  active
                    ? "bg-[#1D1F22] text-zinc-100"
                    : "text-zinc-300 hover:bg-[#16181B] hover:text-white",
                ].join(" ")}
              >
                <div className="h-2 w-2 rounded-full bg-zinc-500" />
                <span className="tracking-wide">{it.label}</span>
              </Link>
            );
          })}
        </nav>
        <button
          type="button"
          className="flex items-center gap-3 rounded-xl px-3 py-2 text-left text-sm text-zinc-400 hover:bg-[#16181B] hover:text-zinc-100"
        >
          <Menu className="h-5 w-5 opacity-70" />
          <span className="tracking-wide">更多</span>
        </button>
      </div>
    </aside>
  );
}
