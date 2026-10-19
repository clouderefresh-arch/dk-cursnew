#!/usr/bin/env python3
"""Чертеж участка, схема информационного потока и диаграмма стоимости."""

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Circle, Rectangle
from matplotlib.lines import Line2D

OUT = Path("/workspace/figures")
FONT = "Liberation Serif"

PTS = [
    ("н1", 420840.25, 2217780.05),
    ("н2", 420842.04, 2217801.55),
    ("н3", 420842.35, 2217807.29),
    ("н4", 420804.79, 2217809.86),
    ("н5", 420804.20, 2217782.78),
]


def dist(a, b):
    return math.hypot(b[1] - a[1], b[2] - a[2])


def azimuth(a, b):
    return math.degrees(math.atan2(b[2] - a[2], b[1] - a[1])) % 360


def side_label(a, b):
    return f"{dist(a, b):.2f} м".replace(".", ",")


def draw_north(ax, x, y, scale=1.0):
    ax.annotate(
        "",
        xy=(x, y + 4.2 * scale),
        xytext=(x, y),
        arrowprops=dict(arrowstyle="-|>", color="black", lw=1.1),
    )
    ax.plot([x, x], [y, y + 4.2 * scale], color="black", lw=1.1)
    ax.text(x, y + 4.6 * scale, "С", ha="center", va="bottom", fontsize=11, fontname=FONT)
    ax.text(x + 0.15 * scale, y + 1.6 * scale, "Ю", ha="left", va="center", fontsize=8, fontname=FONT, color="#333333")


def plot_boundary(path, title_inside=False):
    fig, ax = plt.subplots(figsize=(11.2, 13.4), dpi=160)
    ax.set_aspect("equal")
    xs = [p[2] for p in PTS]  # восток
    ys = [p[1] for p in PTS]  # север
    poly = list(zip(xs, ys))
    ax.add_patch(
        Polygon(poly, closed=True, facecolor="#f4efe6", edgecolor="#9a2b2b", linewidth=2.0, zorder=2)
    )
    # заливка штриховкой, читаемой в черно-белой печати
    ax.add_patch(
        Polygon(poly, closed=True, facecolor="none", edgecolor="#9a2b2b", linewidth=2.0, hatch="....", zorder=3)
    )

    # смежные подписи — снаружи сторон
    neighbors = [
        "смежный\n50:28:0090134:4\nСНТ «Ветеран-5»",
        "смежный\n50:28:0090134:4\nСНТ «Ветеран-5»",
        "смежный\n50:28:0090134:104",
        "смежный\n50:28:0090134:4\nСНТ «Ветеран-5»",
        "смежный\n50:28:0090134:10\nправообладатель\nне установлен",
    ]
    # подписи сторон: вынос наружу по нормали
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    for i, p in enumerate(PTS):
        q = PTS[(i + 1) % len(PTS)]
        mx = (p[2] + q[2]) / 2
        my = (p[1] + q[1]) / 2
        vx, vy = mx - cx, my - cy
        norm = math.hypot(vx, vy) or 1
        ox, oy = vx / norm * 7.2, vy / norm * 7.2
        ax.text(
            mx + ox,
            my + oy,
            side_label(p, q),
            ha="center",
            va="center",
            fontsize=9,
            fontname=FONT,
            color="#7a1f1f",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9),
            zorder=5,
        )
        ax.text(
            mx + ox * 1.85,
            my + oy * 1.85,
            neighbors[i],
            ha="center",
            va="center",
            fontsize=7.2,
            fontname=FONT,
            color="#333333",
            zorder=5,
        )

    for name, x, y in PTS:
        ax.plot(y, x, "o", color="black", markersize=5.5, zorder=6)
        # подпись точки внутрь участка
        dx, dy = cx - y, cy - x
        n = math.hypot(dx, dy) or 1
        ax.text(
            y + dx / n * 1.6,
            x + dy / n * 1.6,
            name,
            ha="center",
            va="center",
            fontsize=10,
            fontname=FONT,
            fontweight="bold",
            zorder=7,
        )

    ax.text(
        cx,
        cy + 1.2,
        "50:28:0000000:51403",
        ha="center",
        va="center",
        fontsize=9,
        fontname=FONT,
        fontweight="bold",
        zorder=6,
    )
    ax.text(
        cx,
        cy - 2.4,
        "P = 1 005 кв. м",
        ha="center",
        va="center",
        fontsize=8.5,
        fontname=FONT,
        zorder=6,
    )

    # линейный масштаб 10 м
    sx, sy = min(xs) - 2, min(ys) - 16
    ax.plot([sx, sx + 10], [sy, sy], color="black", lw=2.0, solid_capstyle="butt")
    ax.plot([sx, sx], [sy - 0.6, sy + 0.6], color="black", lw=1.2)
    ax.plot([sx + 10, sx + 10], [sy - 0.6, sy + 0.6], color="black", lw=1.2)
    ax.text(sx + 5, sy + 1.3, "10 м", ha="center", va="bottom", fontsize=8, fontname=FONT)
    ax.text(sx + 5, sy - 1.5, "Линейный масштаб", ha="center", va="top", fontsize=7.5, fontname=FONT)

    draw_north(ax, max(xs) + 8, max(ys) - 6, scale=1.15)

    pad_x, pad_y = 22, 24
    ax.set_xlim(min(xs) - pad_x, max(xs) + pad_x)
    ax.set_ylim(min(ys) - pad_y, max(ys) + 8)
    ax.axis("off")

    # рамка
    fig.subplots_adjust(left=0.06, right=0.94, top=0.93, bottom=0.08)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.0)

    fig.text(
        0.5,
        0.965,
        "Чертеж земельного участка 50:28:0000000:51403",
        ha="center",
        va="top",
        fontsize=13,
        fontname=FONT,
    )
    fig.text(
        0.5,
        0.028,
        "Система координат МСК-50.    Красная линия — граница, сведения о которой достаточны для определения ее местоположения.\n"
        "Характерные точки н1–н5 подлежат выносу на местность по каталогу координат (разбивка).",
        ha="center",
        va="bottom",
        fontsize=8,
        fontname=FONT,
    )
    fig.savefig(path, dpi=160)
    plt.close()


def plot_flow(path):
    fig, ax = plt.subplots(figsize=(11.0, 3.6), dpi=160)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 30)
    ax.axis("off")
    boxes = [
        (2, 8, 18, 14, "Межевой план\nкоординаты, площадь,\nсмежные границы"),
        (28, 8, 18, 14, "Кадастровый\nучет\nвнесение сведений"),
        (54, 8, 18, 14, "ЕГРН\nграницы, права,\nкадастровая стоимость"),
        (80, 8, 18, 14, "Решение\nна рынке\nсделка, налог, залог"),
    ]
    for x, y, w, h, text in boxes:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.3,rounding_size=0.6",
                linewidth=1.1,
                edgecolor="black",
                facecolor="#f7f4ef",
            )
        )
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9, fontname=FONT)
    for x1, x2 in ((20, 28), (46, 54), (72, 80)):
        ax.annotate(
            "",
            xy=(x2, 15),
            xytext=(x1, 15),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.1),
        )
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def plot_values(path):
    fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=160)
    labels = [
        "Удельный показатель\nкадастровой стоимости",
        "Удельный показатель\nрыночной стоимости",
    ]
    values = [3063.55, 1421.89]
    colors = ["#5c5c5c", "#9a2b2b"]
    bars = ax.bar(labels, values, color=colors, width=0.55, zorder=3)
    ax.set_ylabel("руб. за 1 кв. м", fontname=FONT, fontsize=11)
    ax.set_ylim(0, 3800)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.6, color="#bbbbbb", zorder=0)
    ax.set_axisbelow(True)
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + 80,
            f"{val:,.2f}".replace(",", " ").replace(".", ","),
            ha="center",
            va="bottom",
            fontsize=11,
            fontname=FONT,
        )
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontname(FONT)
        label.set_fontsize(10)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


if __name__ == "__main__":
    plot_boundary(OUT / "chertezh.png")
    plot_flow(OUT / "flow.png")
    plot_values(OUT / "values.png")
    print("ok", list(OUT.glob("*.png")))
