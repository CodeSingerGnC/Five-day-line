from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def draw_mock(width: int, height: int, out: Path) -> None:
    img = Image.new("RGB", (width, height), "#F8FAFC")
    d = ImageDraw.Draw(img)

    top_h = 56
    side_w = 256 if width >= 768 else 0

    d.rectangle([0, 0, width, top_h], fill="#FFFFFF")
    d.line([0, top_h, width, top_h], fill="#E5E7EB", width=1)

    if side_w:
        d.rectangle([0, top_h, side_w, height], fill="#FFFFFF")
        d.line([side_w, top_h, side_w, height], fill="#E5E7EB", width=1)

    content_x = side_w
    content_y = top_h
    d.rectangle([content_x, content_y, width, height], fill="#F1F5F9")

    title_y = content_y + 24
    title_x = content_x + 24
    d.rounded_rectangle(
        [title_x, title_y, title_x + 320, title_y + 36], 6, fill="#E2E8F0"
    )

    card_w = (width - content_x - 24 * 4) // 3
    card_h = 160
    base_y = title_y + 60
    for i in range(3):
        x0 = content_x + 24 + i * (card_w + 24)
        y0 = base_y
        d.rounded_rectangle([x0, y0, x0 + card_w, y0 + card_h], 10, fill="#FFFFFF")
        d.rectangle([x0, y0, x0 + card_w, y0 + 40], fill="#EFF6FF")
        d.rectangle([x0 + 16, y0 + 56, x0 + card_w - 16, y0 + 120], fill="#F8FAFC")

    chart_y = base_y + card_h + 24
    d.rounded_rectangle(
        [content_x + 24, chart_y, width - 24, height - 24], 12, fill="#FFFFFF"
    )
    d.rectangle(
        [content_x + 40, chart_y + 48, width - 40, height - 60], fill="#0EA5E9"
    )

    try:
        font = ImageFont.load_default()
        d.text((16, 18), "Topbar", font=font, fill="#64748B")
        if side_w:
            d.text((16, top_h + 12), "Sidebar", font=font, fill="#64748B")
        d.text((title_x + 12, title_y + 10), "Dashboard / Skeleton", font=font, fill="#334155")
    except Exception:
        pass

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")


def draw_xhs_dark(width: int, height: int, out: Path) -> None:
    bg = "#0B0B0C"
    panel = "#0F1113"
    border = "#23262B"
    pill_on = "#E6E8EB"
    pill_off = "#17191C"
    text_muted = "#8B8F96"

    img = Image.new("RGB", (width, height), bg)
    d = ImageDraw.Draw(img)

    top_h = 56
    left_w = 240 if width >= 1024 else 0

    # Top bar
    d.rectangle([0, 0, width, top_h], fill=panel)
    d.line([0, top_h, width, top_h], fill=border, width=1)
    # Search pill
    sx = width // 2 - 280
    sy = 12
    d.rounded_rectangle([sx, sy, sx + 560, sy + 32], 16, fill=bg, outline=border)
    d.ellipse([sx + 16, sy + 12, sx + 20, sy + 16], fill="#10B981")
    # Slogan
    try:
        font = ImageFont.load_default()
        d.text((width - 220, 20), "流畅 · 极简 · 专注", font=font, fill=text_muted)
    except Exception:
        pass

    # Left rail
    if left_w:
        d.rectangle([0, top_h, left_w, height], fill=panel)
        d.line([left_w, top_h, left_w, height], fill=border)
        y = top_h + 16
        btn_h = 40
        for i, label in enumerate(["发现", "发布", "通知", "我"]):
            fill = "#1D1F22" if i == 0 else pill_off
            d.rounded_rectangle([16, y, left_w - 16, y + btn_h], 12, fill=fill, outline=border)
            d.ellipse([28, y + 12, 40, y + 24], fill="#C1C5CC")
            try:
                d.text((52, y + 12), label, font=font, fill="#EAECEF")
            except Exception:
                pass
            y += btn_h + 8
        # 更多
        d.rounded_rectangle([16, height - 56, left_w - 16, height - 16], 12, fill=pill_off, outline=border)

    # Tabs
    content_x = left_w
    d.line([content_x, top_h + 56, width, top_h + 56], fill=border)
    tx = content_x + 16
    ty = top_h + 14
    pills = ["推荐", "穿搭", "美食", "彩妆", "影视", "家居", "职场", "旅行", "健身"]
    for i, p in enumerate(pills):
        w = 64 + len(p) * 8
        fill = pill_on if i == 0 else pill_off
        text_col = "#0C0D0F" if i == 0 else "#D1D5DB"
        d.rounded_rectangle([tx, ty, tx + w, ty + 28], 14, fill=fill, outline=border)
        try:
            d.text((tx + 14, ty + 8), p, font=font, fill=text_col)
        except Exception:
            pass
        tx += w + 8

    # Feed grid (uniform cards)
    gx = content_x + 16
    gy = top_h + 72
    gw = width - gx - 16
    cols = 4 if width >= 1440 else 3 if width >= 1024 else 2
    gutter = 12
    col_w = (gw - (cols - 1) * gutter) // cols
    img_h = 160
    card_h = img_h + 56
    total = 20
    rows = (total + cols - 1) // cols

    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= total:
                break
            x0 = gx + c * (col_w + gutter)
            y0 = gy + r * (card_h + gutter)
            d.rounded_rectangle([x0, y0, x0 + col_w, y0 + card_h], 16, fill=panel, outline=border)
            d.rectangle([x0 + 8, y0 + 8, x0 + col_w - 8, y0 + img_h], fill="#1B1D20")
            d.rectangle([x0 + 12, y0 + img_h + 14, x0 + col_w - 40, y0 + img_h + 22], fill="#2A2E33")
            d.rectangle([x0 + 12, y0 + img_h + 28, x0 + col_w - 80, y0 + img_h + 36], fill="#23272C")
            idx += 1

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    out_dir = root / "designs"
    draw_mock(1440, 900, out_dir / "ui-desktop.png")
    draw_mock(390, 844, out_dir / "ui-mobile.png")
    draw_xhs_dark(1440, 900, out_dir / "ui-xhs-desktop.png")
    draw_xhs_dark(430, 932, out_dir / "ui-xhs-mobile.png")


if __name__ == "__main__":
    main()
