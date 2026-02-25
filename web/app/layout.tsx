import "./globals.css";
import type { Metadata } from "next";
import Topbar from "@/components/layout/Topbar";
import LeftRail from "@/components/layout/LeftRail";

export const metadata: Metadata = {
  title: "Five-Day-Line Trading System",
  description: "A professional trading system visualization platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="antialiased bg-zinc-950 text-zinc-100">
        <Topbar />
        <LeftRail />
        <div className="pt-14 md:ml-60">
          <main className="min-h-[calc(100dvh-3.5rem)] p-4">{children}</main>
        </div>
      </body>
    </html>
  );
}
