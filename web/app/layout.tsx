import "./globals.css";
import type { Metadata } from "next";

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
    <html lang="en">
      <body className="antialiased bg-slate-50">{children}</body>
    </html>
  );
}
