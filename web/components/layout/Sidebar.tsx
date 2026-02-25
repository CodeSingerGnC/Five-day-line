"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, LineChart, Settings } from "lucide-react";

const nav = [
  { href: "/", label: "仪表盘", icon: LayoutDashboard },
  { href: "/feature-extraction", label: "特征提取", icon: LineChart },
  { href: "/settings", label: "设置", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-56 border-r bg-white pt-14 md:block">
      <nav className="space-y-2 p-3" role="tablist" aria-label="primary">
        {nav.map((n) => {
          const active = pathname === n.href;
          const Icon = n.icon;
          return (
            <Link
              key={n.href}
              href={n.href}
              className={[
                "group flex items-center gap-3 rounded-lg border px-3 py-2 text-sm transition",
                active ? "border-zinc-900 bg-zinc-900 text-white" : "border-slate-200 hover:border-slate-300",
              ].join(" ")}
              role="tab"
              aria-selected={active}
            >
              <Icon className={["h-4 w-4", active ? "opacity-90" : "text-slate-500"].join(" ")} />
              <span className="truncate">{n.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
