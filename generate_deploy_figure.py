# -*- coding: utf-8 -*-
"""
Generate a deployment system schematic for the slide titled
"部署在树莓派" (Deploy on Raspberry Pi).

Layout (left -> right):
  [ 水声信号 ] -> [ ADC ]   ┐
                            │
   PC 端训练 -> ONNX 导出  -> [  树 莓 派 端  ]
                            │  · 预处理
                            │  · ONNX Runtime 推理
                            │  · Tk UI 显示
                            └-> [ 识别结果 / 类别 + 置信度 ]
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle
from matplotlib.patches import Rectangle, Polygon
import os


matplotlib.rcParams["font.sans-serif"] = [
    "WenQuanYi Micro Hei", "Noto Sans CJK SC",
    "Microsoft YaHei", "SimHei", "DejaVu Sans",
]
matplotlib.rcParams["axes.unicode_minus"] = False


# -- theme --
NAVY    = "#0B2A5B"
OCEAN   = "#0E4D92"
AZURE   = "#1D7AC4"
CYAN    = "#2EA8E0"
TEAL    = "#12B0B9"
LIGHT   = "#F4F8FC"
PANEL   = "#E9F1F9"
GREY    = "#647488"
DARK    = "#141E33"
ACCENT  = "#FFB703"
RED     = "#EF556B"
GREEN   = "#2AB77E"


def rounded(ax, x, y, w, h, fill=OCEAN, edge=None, lw=0.0,
            radius=0.12, alpha=1.0, zorder=2):
    ec = edge if edge is not None else fill
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=f"round,pad=0.02,rounding_size={radius}",
                         facecolor=fill, edgecolor=ec, linewidth=lw,
                         alpha=alpha, zorder=zorder)
    ax.add_patch(box)
    return box


def text(ax, x, y, s, size=11, color=DARK, bold=False, ha="center",
         va="center", italic=False, family="sans-serif", zorder=5):
    weight = "bold" if bold else "normal"
    style = "italic" if italic else "normal"
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va,
            fontweight=weight, fontstyle=style, family=family,
            zorder=zorder)


def arrow(ax, p1, p2, color=NAVY, lw=1.8, style="-|>", mut=18,
          rad=0.0, zorder=4, ls="-"):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=mut,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}", zorder=zorder)
    ax.add_patch(a)


# ---- simple icon drawers ----
def draw_pc(ax, cx, cy, w=1.6, h=1.05, color=AZURE):
    # monitor
    rounded(ax, cx - w/2, cy - h/2, w, h, fill="white",
            edge=color, lw=1.6, radius=0.05)
    # screen content (bars)
    inner_x = cx - w/2 + 0.12
    inner_y = cy - h/2 + 0.18
    inner_w = w - 0.24
    inner_h = h - 0.32
    rounded(ax, inner_x, inner_y, inner_w, inner_h, fill=color,
            radius=0.04, lw=0)
    # title bar
    rounded(ax, inner_x, inner_y + inner_h - 0.12, inner_w, 0.12,
            fill="white", radius=0.02, lw=0, alpha=0.4)
    # mock content lines
    for i, frac in enumerate([0.7, 0.45, 0.6, 0.5]):
        ly = inner_y + 0.1 + 0.13 * i
        rounded(ax, inner_x + 0.05, ly, (inner_w - 0.1) * frac, 0.06,
                fill="white", alpha=0.45, radius=0.02, lw=0)
    # base
    base_w = 0.4; base_h = 0.08
    rounded(ax, cx - base_w/2, cy - h/2 - 0.05, base_w, base_h,
            fill=color, radius=0.03, lw=0)
    rounded(ax, cx - 0.4, cy - h/2 - 0.18, 0.8, 0.08,
            fill=color, radius=0.03, lw=0)


def draw_onnx_file(ax, cx, cy, w=1.1, h=1.3, color="#74A4D9"):
    # folded corner card
    fold = 0.22
    path_pts = [
        (cx - w/2, cy + h/2),
        (cx + w/2 - fold, cy + h/2),
        (cx + w/2, cy + h/2 - fold),
        (cx + w/2, cy - h/2),
        (cx - w/2, cy - h/2),
    ]
    poly = Polygon(path_pts, closed=True, facecolor="white",
                   edgecolor=color, linewidth=2, zorder=3)
    ax.add_patch(poly)
    # corner triangle
    corner = Polygon([
        (cx + w/2 - fold, cy + h/2),
        (cx + w/2 - fold, cy + h/2 - fold),
        (cx + w/2, cy + h/2 - fold),
    ], facecolor=color, edgecolor=color, linewidth=1, zorder=4, alpha=0.4)
    ax.add_patch(corner)
    # ONNX text
    text(ax, cx, cy + 0.18, "ONNX", size=14, color=color, bold=True)
    text(ax, cx, cy - 0.04, "model", size=8.5, color=color)
    text(ax, cx, cy - 0.22, "*.onnx", size=8.5, color=GREY,
         italic=True, family="monospace")
    # dotted band
    for i, ly in enumerate([cy - 0.4, cy - 0.5]):
        ax.plot([cx - w/2 + 0.12, cx + w/2 - 0.12], [ly, ly],
                color=color, linewidth=1, linestyle=(0, (1.5, 1.5)),
                zorder=4)


def draw_raspberry_pi(ax, cx, cy, w=3.2, h=2.4):
    # board (green PCB)
    board_color = "#1F8A4E"
    rounded(ax, cx - w/2, cy - h/2, w, h, fill=board_color, radius=0.08,
            lw=0)
    # silkscreen highlights inside (a few rectangles for visual interest)
    # SoC chip
    chip_w, chip_h = 0.7, 0.7
    rounded(ax, cx - chip_w/2, cy + 0.2, chip_w, chip_h, fill="#1c1c1e",
            radius=0.04, lw=0)
    text(ax, cx, cy + 0.55, "Broadcom", size=7, color="white", bold=True)
    text(ax, cx, cy + 0.4, "BCM2711", size=6.5, color="white")
    # RAM chip
    ram_w, ram_h = 0.5, 0.32
    rounded(ax, cx + chip_w/2 + 0.1, cy + 0.4, ram_w, ram_h,
            fill="#2d2d30", radius=0.03, lw=0)
    # GPIO header (yellow strip)
    gp_w = w - 0.6; gp_h = 0.15
    rounded(ax, cx - gp_w/2, cy + h/2 - gp_h - 0.08, gp_w, gp_h,
            fill="#E4A012", radius=0.02, lw=0)
    for i in range(20):
        px = cx - gp_w/2 + 0.06 + i * (gp_w - 0.12) / 19
        rounded(ax, px - 0.025, cy + h/2 - gp_h - 0.07,
                0.05, gp_h - 0.02, fill="#7a4d00", radius=0.005, lw=0)
    # USB ports (4) on the right
    usb_w, usb_h = 0.32, 0.36
    for i in range(2):
        rounded(ax, cx + w/2 - usb_w - 0.05,
                cy - 0.6 + i * (usb_h + 0.08),
                usb_w, usb_h, fill="#8a8a8a", radius=0.02, lw=0)
    # ethernet port
    rounded(ax, cx + w/2 - usb_w - 0.05, cy - 1.1,
            usb_w, usb_h, fill="#cfcfcf", radius=0.02, lw=0)
    # micro hdmi / power on left
    for i in range(2):
        rounded(ax, cx - w/2 + 0.05, cy - 0.7 + i * 0.32,
                0.22, 0.18, fill="#cfcfcf", radius=0.02, lw=0)
    # micro-sd
    rounded(ax, cx - w/2 - 0.12, cy - 0.2, 0.18, 0.4,
            fill="#cfcfcf", radius=0.02, lw=0)
    # tiny mounting holes
    for hx, hy in [(cx - w/2 + 0.18, cy + h/2 - 0.18),
                   (cx + w/2 - 0.18, cy - h/2 + 0.18),
                   (cx - w/2 + 0.18, cy - h/2 + 0.18),
                   (cx + w/2 - 0.18, cy + h/2 - 0.18)]:
        ax.add_patch(Circle((hx, hy), 0.06, facecolor="white",
                            edgecolor="#444", lw=0.6, zorder=5))
    # board label
    text(ax, cx, cy - h/2 + 0.18, "Raspberry  Pi", size=9,
         color="white", bold=True)


def draw_screen(ax, cx, cy, w=2.4, h=1.55):
    # monitor frame
    rounded(ax, cx - w/2, cy - h/2, w, h, fill="#1f2733", radius=0.06, lw=0)
    inner_x = cx - w/2 + 0.1
    inner_y = cy - h/2 + 0.12
    iw = w - 0.2; ih = h - 0.24
    rounded(ax, inner_x, inner_y, iw, ih, fill="#0b2545", radius=0.04, lw=0)

    # title bar
    rounded(ax, inner_x, inner_y + ih - 0.18, iw, 0.18, fill=NAVY,
            radius=0.03, lw=0)
    text(ax, cx, inner_y + ih - 0.09, "UAM-Recognizer · 实时识别",
         size=8.5, color="white", bold=True)

    # waveform mini
    import math
    n = 50
    wx0 = inner_x + 0.08; wy0 = inner_y + ih * 0.55
    ww = iw - 0.16
    px, py = wx0, wy0
    for i in range(1, n + 1):
        x = wx0 + ww * (i / n)
        v = math.sin(i * 0.55) * 0.12 + math.sin(i * 0.22) * 0.05
        y = wy0 + v
        ax.plot([px, x], [py, y], color=CYAN, lw=1.2, zorder=6)
        px, py = x, y

    # result
    text(ax, cx - iw/2 + 0.18, inner_y + 0.32, "类别 :", size=8,
         color="#8DC8FF", ha="left")
    text(ax, cx - iw/2 + 0.62, inner_y + 0.32, "4PSK", size=11,
         color="white", bold=True, ha="left")
    text(ax, cx + iw/2 - 0.95, inner_y + 0.32, "Conf : 93.8 %",
         size=8.5, color=ACCENT, bold=True, ha="left")

    # buttons row
    for i, (txt, col) in enumerate([("Load", OCEAN), ("Run", AZURE),
                                    ("Stop", RED)]):
        bx = cx - iw/2 + 0.18 + i * 0.45
        by = inner_y + 0.05
        rounded(ax, bx, by, 0.38, 0.18, fill=col, radius=0.05, lw=0)
        text(ax, bx + 0.19, by + 0.09, txt, size=7,
             color="white", bold=True)

    # base / stand
    rounded(ax, cx - 0.25, cy - h/2 - 0.04, 0.5, 0.08, fill="#0f1822",
            radius=0.02, lw=0)
    rounded(ax, cx - 0.6, cy - h/2 - 0.16, 1.2, 0.08, fill="#0f1822",
            radius=0.03, lw=0)


def draw_waveform_icon(ax, cx, cy, w=1.3, h=0.85, color=OCEAN):
    rounded(ax, cx - w/2, cy - h/2, w, h, fill="white",
            edge=color, lw=1.4, radius=0.08)
    import math
    n = 40
    wx0 = cx - w/2 + 0.1; wy0 = cy
    ww = w - 0.2
    px, py = wx0, wy0
    for i in range(1, n + 1):
        x = wx0 + ww * (i / n)
        v = math.sin(i * 0.55) * (h*0.28) + math.sin(i * 0.22) * (h*0.1)
        y = wy0 + v
        ax.plot([px, x], [py, y], color=color, lw=1.3, zorder=4)
        px, py = x, y


def draw_hydrophone(ax, cx, cy, color=AZURE):
    # cylindrical body
    body_w, body_h = 0.5, 0.65
    rounded(ax, cx - body_w/2, cy - body_h/2, body_w, body_h,
            fill=color, radius=0.05, lw=0)
    # top transducer (lighter)
    rounded(ax, cx - body_w/2, cy + body_h/2 - 0.08, body_w, 0.16,
            fill="#9fd0ed", radius=0.03, lw=0)
    # bottom cable
    ax.plot([cx, cx], [cy - body_h/2, cy - body_h/2 - 0.35],
            color="#444", lw=1.6, zorder=4)
    # wave rings emanating from top
    for r in [0.18, 0.32, 0.46]:
        circ = patches.Arc((cx, cy + body_h/2 + 0.1), r*2, r*1.2,
                           angle=0, theta1=10, theta2=170,
                           color=color, linewidth=1.2, zorder=3)
        ax.add_patch(circ)


# ---- build figure ----
def build(out_path="figs/deployment_system.png"):
    fig = plt.figure(figsize=(15.5, 6.0), dpi=240)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 6.6)
    ax.set_aspect("equal")
    ax.axis("off")

    # bg
    ax.add_patch(Rectangle((0, 0), 16, 6.6, facecolor="#FBFCFE",
                           edgecolor="none", zorder=0))

    # Title intentionally omitted -- the PPT slide already provides one.

    # ===== Stage 1 : PC training =====
    panel1_x, panel1_y, panel1_w, panel1_h = 0.5, 2.45, 3.0, 3.4
    rounded(ax, panel1_x, panel1_y, panel1_w, panel1_h,
            fill=PANEL, radius=0.15, lw=0)
    text(ax, panel1_x + panel1_w/2, panel1_y + panel1_h - 0.3,
         "①  PC 端训练", size=12, color=OCEAN, bold=True)
    text(ax, panel1_x + panel1_w/2, panel1_y + panel1_h - 0.6,
         "PC  TRAINING", size=8.5, color=GREY, bold=True)
    draw_pc(ax, panel1_x + panel1_w/2, panel1_y + panel1_h/2 - 0.3,
            w=1.9, h=1.3, color=AZURE)
    text(ax, panel1_x + panel1_w/2, panel1_y + 0.45,
         "PyTorch  ·  Bi-LSTM × ResNet", size=9, color=NAVY, bold=True)
    text(ax, panel1_x + panel1_w/2, panel1_y + 0.2,
         "训练 + 验证 → 最优权重", size=9, color=DARK)

    # ===== Stage 2 : ONNX export =====
    panel2_x, panel2_y, panel2_w, panel2_h = 4.0, 2.45, 2.4, 3.4
    rounded(ax, panel2_x, panel2_y, panel2_w, panel2_h,
            fill=PANEL, radius=0.15, lw=0)
    text(ax, panel2_x + panel2_w/2, panel2_y + panel2_h - 0.3,
         "②  ONNX 导出", size=12, color=AZURE, bold=True)
    text(ax, panel2_x + panel2_w/2, panel2_y + panel2_h - 0.6,
         "EXPORT", size=8.5, color=GREY, bold=True)
    draw_onnx_file(ax, panel2_x + panel2_w/2,
                   panel2_y + panel2_h/2 - 0.3, w=1.3, h=1.55,
                   color="#5589C9")
    text(ax, panel2_x + panel2_w/2, panel2_y + 0.45,
         "跨平台模型格式", size=9, color=NAVY, bold=True)
    text(ax, panel2_x + panel2_w/2, panel2_y + 0.2,
         "训练框架 → 推理引擎解耦", size=9, color=DARK)

    # ===== Stage 3 : Raspberry Pi =====
    panel3_x, panel3_y, panel3_w, panel3_h = 6.9, 1.05, 4.7, 4.8
    rounded(ax, panel3_x, panel3_y, panel3_w, panel3_h,
            fill="#E6F3D9", radius=0.15, lw=0)
    text(ax, panel3_x + panel3_w/2, panel3_y + panel3_h - 0.3,
         "③  树莓派端推理", size=13, color="#1F6E36", bold=True)
    text(ax, panel3_x + panel3_w/2, panel3_y + panel3_h - 0.6,
         "ON-DEVICE  INFERENCE", size=9, color=GREY, bold=True)
    draw_raspberry_pi(ax, panel3_x + panel3_w/2,
                      panel3_y + panel3_h/2 + 0.5, w=3.2, h=2.0)
    # internal modules row (3 small chips)
    sub_y = panel3_y + 0.65
    sub_w = 1.35; sub_h = 0.65; sub_gap = 0.15
    total_w = 3*sub_w + 2*sub_gap
    sub_x0 = panel3_x + (panel3_w - total_w)/2
    mods = [
        ("预处理", "归一化 + STFT", OCEAN),
        ("ONNX Runtime", "ARM 推理引擎", AZURE),
        ("Tk UI", "波形 + 结果", TEAL),
    ]
    for i, (h, sub, col) in enumerate(mods):
        x = sub_x0 + i * (sub_w + sub_gap)
        rounded(ax, x, sub_y, sub_w, sub_h, fill=col, radius=0.08, lw=0)
        text(ax, x + sub_w/2, sub_y + sub_h - 0.18, h, size=10,
             color="white", bold=True)
        text(ax, x + sub_w/2, sub_y + 0.18, sub, size=8,
             color="white")

    # ===== Stage 4 : Output / Display =====
    panel4_x, panel4_y, panel4_w, panel4_h = 12.0, 2.45, 3.6, 3.4
    rounded(ax, panel4_x, panel4_y, panel4_w, panel4_h,
            fill=PANEL, radius=0.15, lw=0)
    text(ax, panel4_x + panel4_w/2, panel4_y + panel4_h - 0.3,
         "④  识别结果显示", size=12, color="#7a1f1f", bold=True)
    text(ax, panel4_x + panel4_w/2, panel4_y + panel4_h - 0.6,
         "RESULT  DISPLAY", size=8.5, color=GREY, bold=True)
    draw_screen(ax, panel4_x + panel4_w/2, panel4_y + panel4_h/2 - 0.25,
                w=2.8, h=1.65)
    text(ax, panel4_x + panel4_w/2, panel4_y + 0.45,
         "实时波形 + 类别 + 置信度", size=9, color=NAVY, bold=True)
    text(ax, panel4_x + panel4_w/2, panel4_y + 0.2,
         "Top-K 辅助参考输出", size=9, color=DARK)

    # ====== Bottom input chain: hydrophone -> ADC -> RPi  ======
    text(ax, 0.4, 1.95, "信  号  输  入  通  路", size=10.5,
         color=NAVY, bold=True, ha="left")
    # baseline y for the icon row
    y_row = 1.05
    draw_hydrophone(ax, 1.05, y_row, color=AZURE)
    text(ax, 1.05, 0.25, "水听器 / 信号源", size=9, color=NAVY,
         bold=True)

    draw_waveform_icon(ax, 2.7, y_row, w=1.4, h=0.65, color=OCEAN)
    text(ax, 2.7, 0.25, "模拟水声信号", size=9, color=NAVY, bold=True)

    rounded(ax, 4.45, y_row - 0.35, 1.0, 0.7, fill=ACCENT,
            radius=0.1, lw=0)
    text(ax, 4.95, y_row, "ADC", size=12, color="white", bold=True)
    text(ax, 4.95, 0.25, "模数转换", size=9, color=NAVY, bold=True)

    arrow(ax, (1.45, y_row), (2.05, y_row), color="#444", lw=1.6)
    arrow(ax, (3.35, y_row), (4.4, y_row), color="#444", lw=1.6)
    arrow(ax, (5.45, y_row), (panel3_x + 0.4, panel3_y + 0.35),
          color="#444", lw=1.6, rad=-0.15)

    # ====== Inter-stage horizontal arrows ======
    # PC -> ONNX
    y_mid = panel1_y + panel1_h/2 - 0.3
    arrow(ax, (panel1_x + panel1_w - 0.05, y_mid),
              (panel2_x + 0.05, y_mid),
          color=NAVY, lw=2.0)
    text(ax, (panel1_x + panel1_w + panel2_x)/2, y_mid + 0.25,
         "导出  export", size=9, color=NAVY, bold=True)

    # ONNX -> RPi
    arrow(ax, (panel2_x + panel2_w - 0.05, y_mid),
              (panel3_x + 0.05, panel3_y + panel3_h - 1.0),
          color=NAVY, lw=2.0, rad=-0.08)
    text(ax, (panel2_x + panel2_w + panel3_x)/2 - 0.05, y_mid + 0.35,
         "加载  load", size=9, color=NAVY, bold=True)

    # RPi -> Screen
    arrow(ax, (panel3_x + panel3_w - 0.05, panel3_y + panel3_h - 1.0),
              (panel4_x + 0.05, y_mid),
          color=NAVY, lw=2.0, rad=0.08)
    text(ax, (panel3_x + panel3_w + panel4_x)/2 + 0.1, y_mid + 0.35,
         "推理  inference", size=9, color=NAVY, bold=True)

    # save
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=240, bbox_inches="tight",
                facecolor="#FBFCFE")
    plt.close(fig)
    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    build()
