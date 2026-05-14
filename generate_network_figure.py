# -*- coding: utf-8 -*-
"""
Generate a 3D-block style neural network architecture figure
(similar to Ahmed et al. CVPR'15 style) for the thesis:
《基于树莓派的水声信号制式识别》

Architecture:
  - Top branch (time-domain):  1D waveform (4096x1)
        -> Bi-LSTM (forward + backward) -> Mean Pooling -> f_t
  - Bottom branch (spectrogram):  STFT 2xHxW
        -> ResNet-18* (first conv: 2-ch input) -> GAP -> f_s
  - Concat [f_t; f_s] -> FC -> Softmax -> 9 modulation classes
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Polygon
from matplotlib.font_manager import FontProperties
import numpy as np
import os


# -------- font setup (try Chinese fonts that are installed) --------
CN_FONT_CANDIDATES = [
    "WenQuanYi Micro Hei",
    "Noto Sans CJK SC",
    "Microsoft YaHei",
    "SimHei",
    "DejaVu Sans",
]
matplotlib.rcParams["font.sans-serif"] = CN_FONT_CANDIDATES
matplotlib.rcParams["axes.unicode_minus"] = False


# -------- helpers ---------
def cuboid(ax, x, y, w, h, depth, color,
           edge="#222", lw=0.8, alpha=1.0, label_top=None,
           label_top_color="#333", label_top_size=9,
           label_bottom=None, label_bottom_color="#333",
           label_bottom_size=9, side_text=None,
           label_top_dy=0.18, label_bottom_dy=0.22):
    """Draw an axonometric cuboid.

    (x, y) = bottom-left of the FRONT face
    w, h    = width / height of the front face
    depth   = depth offset (drawn as dx=depth*0.5, dy=depth*0.55)
    """
    dx = depth * 0.45
    dy = depth * 0.55
    # darker / lighter shades for top and right
    def shade(hex_color, factor):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        r = max(0, min(1, r * factor))
        g = max(0, min(1, g * factor))
        b = max(0, min(1, b * factor))
        return (r, g, b)

    front_color = color
    top_color = shade(color, 1.18)
    side_color = shade(color, 0.78)

    front = patches.Rectangle((x, y), w, h, facecolor=front_color,
                              edgecolor=edge, linewidth=lw, alpha=alpha,
                              zorder=2)
    ax.add_patch(front)

    top = Polygon([(x, y + h),
                   (x + dx, y + h + dy),
                   (x + w + dx, y + h + dy),
                   (x + w, y + h)],
                  facecolor=top_color, edgecolor=edge, linewidth=lw,
                  alpha=alpha, zorder=2)
    ax.add_patch(top)

    side = Polygon([(x + w, y),
                    (x + w + dx, y + dy),
                    (x + w + dx, y + h + dy),
                    (x + w, y + h)],
                   facecolor=side_color, edgecolor=edge, linewidth=lw,
                   alpha=alpha, zorder=2)
    ax.add_patch(side)

    cx = x + w / 2 + dx / 2
    if label_top:
        ax.text(cx, y + h + dy + label_top_dy, label_top,
                ha="center", va="bottom",
                fontsize=label_top_size, color=label_top_color,
                fontweight="bold", zorder=5)
    if label_bottom:
        ax.text(cx, y - label_bottom_dy, label_bottom,
                ha="center", va="top",
                fontsize=label_bottom_size, color=label_bottom_color,
                fontweight="bold", zorder=5)
    if side_text:
        ax.text(x + w + dx + 0.05, y + h / 2 + dy / 2, side_text,
                ha="left", va="center", fontsize=8, color="#555",
                rotation=0, zorder=5)

    # return useful coords
    return {
        "front_left":   (x, y + h / 2),
        "front_right":  (x + w, y + h / 2),
        "top_center":   (cx, y + h + dy),
        "bottom_center": (cx, y),
        "right_center": (x + w + dx, y + h / 2 + dy / 2),
        "back_right":   (x + w + dx, y + h / 2 + dy / 2),
        "center":       (cx, y + h / 2 + dy / 2),
    }


def arrow(ax, p1, p2, color="#333", lw=1.6, style="-|>", mutation=14,
          zorder=4, rad=0.0):
    a = FancyArrowPatch(p1, p2,
                        arrowstyle=style,
                        mutation_scale=mutation,
                        linewidth=lw,
                        color=color,
                        connectionstyle=f"arc3,rad={rad}",
                        zorder=zorder)
    ax.add_patch(a)


def labelled_arrow(ax, p1, p2, text, color="#1d4ed8", lw=1.4,
                   text_color="#1d4ed8", text_size=8.5, text_dy=0.12):
    arrow(ax, p1, p2, color=color, lw=lw)
    mx = (p1[0] + p2[0]) / 2
    my = (p1[1] + p2[1]) / 2 + text_dy
    ax.text(mx, my, text, ha="center", va="bottom",
            fontsize=text_size, color=text_color, fontweight="bold")


# --------- the network drawing ---------

def build_figure(out_path="figs/network_architecture.png"):
    fig = plt.figure(figsize=(15.5, 8.0), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")

    # subtle background
    bg = patches.Rectangle((0, 0), 21, 10, facecolor="#FBFCFE",
                           edgecolor="none", zorder=0)
    ax.add_patch(bg)

    # title bar (optional)
    # ax.text(10.5, 9.55, "Bi-LSTM × ResNet-18 双分支融合网络",
    #         ha="center", va="center", fontsize=15, fontweight="bold",
    #         color="#0B2A5B")

    # ---------- TOP BRANCH (time-domain) ----------
    top_y_base = 6.2
    bot_y_base = 1.7

    # Branch badges (small, top-left of each row, no overlap with blocks)
    badge_top = patches.FancyBboxPatch(
        (0.3, top_y_base + 2.4), 2.6, 0.42,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        facecolor="#0E4D92", edgecolor="none", zorder=3)
    ax.add_patch(badge_top)
    ax.text(0.45, top_y_base + 2.61, "◆  时域分支  Time-domain",
            fontsize=10, color="white", fontweight="bold", va="center")

    badge_bot = patches.FancyBboxPatch(
        (0.3, bot_y_base + 2.4), 2.6, 0.42,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        facecolor="#1D7AC4", edgecolor="none", zorder=3)
    ax.add_patch(badge_bot)
    ax.text(0.45, bot_y_base + 2.61, "◆  谱图分支  Spectrogram",
            fontsize=10, color="white", fontweight="bold", va="center")

    # ----- input waveform: 1D long thin block (rotated horizontally) -----
    wave_x = 0.7; wave_y = top_y_base + 0.4
    wave_w = 0.6; wave_h = 1.4
    cuboid(ax, wave_x, wave_y, wave_w, wave_h, depth=0.45,
           color="#EEF6CB",
           label_top="4096", label_top_color="#5d6b00",
           label_top_size=9,
           label_bottom="1D 时域波形\nWaveform",
           label_bottom_color="#0E4D92", label_bottom_size=10,
           label_bottom_dy=0.55)
    ax.text(wave_x - 0.05, wave_y + wave_h / 2, "1",
            ha="right", va="center", fontsize=8.5, color="#5d6b00")

    # ----- Bi-LSTM block ----- two stacked cuboids representing forward/backward
    bls_x = 2.3
    bls_y = top_y_base + 0.6
    bls = cuboid(ax, bls_x, bls_y, 1.2, 1.1, depth=0.6,
                 color="#C9DAF8",
                 label_top="hidden", label_top_color="#1d4ed8",
                 label_top_size=8.5,
                 label_bottom="Bi-LSTM\nforward + backward",
                 label_bottom_color="#0E4D92",
                 label_bottom_dy=0.55)
    # mini forward/backward arrows inside (decorative)
    ax.annotate("", xy=(bls_x + 1.05, bls_y + 0.78),
                xytext=(bls_x + 0.15, bls_y + 0.78),
                arrowprops=dict(arrowstyle="->", color="#1d4ed8", lw=1.0),
                zorder=4)
    ax.annotate("", xy=(bls_x + 0.15, bls_y + 0.32),
                xytext=(bls_x + 1.05, bls_y + 0.32),
                arrowprops=dict(arrowstyle="->", color="#1d4ed8", lw=1.0),
                zorder=4)

    # arrow from waveform to BiLSTM
    arrow(ax, (wave_x + wave_w + 0.5, wave_y + wave_h/2 + 0.2),
              (bls_x - 0.05, bls_y + 1.1/2),
          color="#444", lw=1.5)

    # ----- Mean Pooling (top branch) -----
    mp_x = 4.7; mp_y = top_y_base + 0.65
    mp = cuboid(ax, mp_x, mp_y, 0.9, 1.0, depth=0.5,
                color="#FFE5A8",
                label_top="T-pool", label_top_color="#996300",
                label_top_size=8.5,
                label_bottom="时间均值池化\nMean Pool",
                label_bottom_color="#996300", label_bottom_dy=0.55)
    arrow(ax, (bls_x + 1.2 + 0.55, bls_y + 1.1/2 + 0.25),
              (mp_x - 0.05, mp_y + 1.0/2),
          color="#444", lw=1.5)

    # ----- f_t feature vector (tall thin) -----
    ft_x = 6.8; ft_y = top_y_base + 0.35
    ft = cuboid(ax, ft_x, ft_y, 0.45, 1.55, depth=0.4,
                color="#B8E0D2",
                label_top="d_t", label_top_color="#0d5e4c",
                label_top_size=8.5,
                label_bottom="时域特征\nf_t", label_bottom_color="#0d5e4c",
                label_bottom_dy=0.5)
    arrow(ax, (mp_x + 0.9 + 0.5, mp_y + 1.0/2 + 0.2),
              (ft_x - 0.05, ft_y + 1.55/2),
          color="#444", lw=1.5)

    # ---------- BOTTOM BRANCH (spectrogram / ResNet) ----------
    stft_x = 0.7; stft_y = bot_y_base + 0.1
    cuboid(ax, stft_x + 0.18, stft_y + 0.15, 1.1, 1.55, depth=0.4,
           color="#F6CACA",
           label_top=None, label_bottom=None)
    cuboid(ax, stft_x, stft_y, 1.1, 1.55, depth=0.4,
           color="#F4A6A6",
           label_top="2", label_top_color="#7a1f1f",
           label_top_size=8.5,
           label_bottom="STFT 双通道谱图\n|X| & arg(X)",
           label_bottom_color="#7a1f1f", label_bottom_dy=0.45)

    # ----- ResNet stages: 4 conv blocks of increasing depth -----
    resnet_colors = ["#D7E7FD", "#B7D0F9", "#8FB1ED", "#6A8FE0"]
    rn_x = 2.6
    rn_specs = [
        (1.45, 0.45, "64",  "conv1\n+pool"),
        (1.25, 0.5,  "128", "stage 2"),
        (1.05, 0.55, "256", "stage 3"),
        (0.85, 0.6,  "512", "stage 4"),
    ]
    rn_top_y = bot_y_base + 0.55
    rn_centers = []
    cur_x = rn_x
    rn_block_bottom = None
    for i, (h_, d_, ch, name) in enumerate(rn_specs):
        bx = cur_x
        by = rn_top_y - h_/2 - 0.3
        if rn_block_bottom is None or by < rn_block_bottom:
            rn_block_bottom = by
        b = cuboid(ax, bx, by, 0.65, h_, depth=d_,
                   color=resnet_colors[i],
                   label_top=ch, label_top_color="#0E4D92",
                   label_top_size=8.5,
                   label_bottom=name, label_bottom_color="#0E4D92",
                   label_bottom_size=8.0, label_bottom_dy=0.15)
        rn_centers.append(b)
        cur_x += 0.65 + 0.55

    # arrow from STFT input to ResNet first block
    arrow(ax, (stft_x + 1.1 + 0.5, stft_y + 1.55/2 + 0.2),
              (rn_x - 0.05, rn_top_y + 0.05),
          color="#444", lw=1.5)
    # arrows between ResNet blocks
    cur_x = rn_x
    for i, (h_, d_, ch, name) in enumerate(rn_specs[:-1]):
        right_x = cur_x + 0.65 + d_ * 0.45
        right_y = (rn_top_y - h_/2 - 0.3) + h_/2 + d_*0.55/2
        next_x = cur_x + 0.65 + 0.55
        next_h = rn_specs[i+1][0]
        next_y = (rn_top_y - next_h/2 - 0.3) + next_h/2
        arrow(ax, (right_x + 0.02, right_y),
              (next_x - 0.05, next_y),
              color="#666", lw=1.2)
        cur_x += 0.65 + 0.55

    # Brace below ResNet to label it
    last_right = rn_x + 4 * 0.65 + 3 * 0.55
    rn_label_x = (rn_x + last_right) / 2
    brace_y = rn_block_bottom - 0.85
    ax.annotate("", xy=(last_right - 0.1, brace_y),
                xytext=(rn_x + 0.1, brace_y),
                arrowprops=dict(arrowstyle="-", color="#0E4D92", lw=1.5),
                zorder=3)
    # short ticks
    ax.plot([rn_x + 0.1, rn_x + 0.1], [brace_y, brace_y + 0.08],
            color="#0E4D92", lw=1.5, zorder=3)
    ax.plot([last_right - 0.1, last_right - 0.1],
            [brace_y, brace_y + 0.08],
            color="#0E4D92", lw=1.5, zorder=3)
    ax.text(rn_label_x, brace_y - 0.18, "ResNet-18 *",
            ha="center", va="top", fontsize=11.5, fontweight="bold",
            color="#0E4D92")
    ax.text(rn_label_x, brace_y - 0.55,
            "(first conv: 2-channel input)",
            ha="center", va="top", fontsize=8.5, color="#0E4D92",
            style="italic")

    # ----- GAP (bottom branch) -----
    gap_x = last_right + 0.65; gap_y = bot_y_base + 0.55
    gap = cuboid(ax, gap_x, gap_y, 0.85, 0.85, depth=0.45,
                 color="#FFE5A8",
                 label_top="1×1", label_top_color="#996300",
                 label_top_size=8.5,
                 label_bottom="全局平均池化\nGAP",
                 label_bottom_color="#996300", label_bottom_dy=0.4)
    arrow(ax, (last_right + 0.05, bot_y_base + 0.55 + 0.85/2 - 0.05),
              (gap_x - 0.05, gap_y + 0.85/2),
          color="#444", lw=1.5)

    # ----- f_s feature vector -----
    fs_x = gap_x + 1.2; fs_y = bot_y_base + 0.25
    fs = cuboid(ax, fs_x, fs_y, 0.45, 1.55, depth=0.4,
                color="#B8E0D2",
                label_top="d_s", label_top_color="#0d5e4c",
                label_top_size=8.5,
                label_bottom="谱图特征\nf_s", label_bottom_color="#0d5e4c",
                label_bottom_dy=0.5)
    arrow(ax, (gap_x + 0.85 + 0.2, gap_y + 0.85/2 + 0.12),
              (fs_x - 0.05, fs_y + 1.55/2),
          color="#444", lw=1.5)

    # ---------- CONCAT (cross-feature) ----------
    cc_x = 10.4
    # bracket vertical from f_t (top) and f_s (bottom) into concat block
    cc_y_top = top_y_base + 0.35       # match f_t bottom
    cc_y_bot = bot_y_base + 0.25       # match f_s bottom
    cc_block_x = cc_x
    cc_block_y = (top_y_base + bot_y_base) / 2  # center
    cc_block_h = 2.3
    cc_block_y_bottom = cc_block_y - cc_block_h / 2 + 0.7
    concat = cuboid(ax, cc_block_x, cc_block_y_bottom,
                    1.0, cc_block_h, depth=0.5,
                    color="#F4A6A6",
                    label_top="d_t + d_s",
                    label_top_color="#7a1f1f", label_top_size=8.5,
                    label_bottom="Feature Concat\n[ f_t ; f_s ]",
                    label_bottom_color="#7a1f1f", label_bottom_dy=0.5)

    # arrows from f_t / f_s into concat
    p1 = (ft_x + 0.45 + 0.2, ft_y + 1.55/2 + 0.22)
    p2 = (cc_block_x - 0.05, cc_block_y_bottom + cc_block_h - 0.5)
    arrow(ax, p1, p2, color="#444", lw=1.5, rad=-0.18)
    p1b = (fs_x + 0.45 + 0.2, fs_y + 1.55/2 + 0.22)
    p2b = (cc_block_x - 0.05, cc_block_y_bottom + 0.5)
    arrow(ax, p1b, p2b, color="#444", lw=1.5, rad=0.18)

    # ---------- FC tall thin block ----------
    fc_x = 12.6
    fc_h = 4.2
    fc_y = 5 - fc_h/2 + 0.1
    fc = cuboid(ax, fc_x, fc_y, 0.55, fc_h, depth=0.5,
                color="#C7B6E6",
                label_top="500", label_top_color="#4a2c93",
                label_top_size=10,
                label_bottom="Fully\nConnected",
                label_bottom_color="#4a2c93", label_bottom_size=10,
                label_bottom_dy=0.5)
    # arrow concat -> fc
    arrow(ax,
          (cc_block_x + 1.0 + 0.5, cc_block_y_bottom + cc_block_h/2 + 0.25),
          (fc_x - 0.05, fc_y + fc_h/2),
          color="#444", lw=1.5)

    # ---------- Softmax (fan-out lines + nodes) ----------
    sx0 = fc_x + 0.55 + 0.5 + 0.6  # start of softmax fan
    sx1 = sx0 + 2.6
    classes = ["2FSK", "4FSK", "8FSK",
               "2PSK", "4PSK", "8PSK",
               "16QAM", "64QAM", "64OFDM"]
    n = len(classes)
    # vertical span
    sy_top = 8.0
    sy_bot = 2.0
    y_positions = np.linspace(sy_top, sy_bot, n)

    # SoftMax title near the fan
    ax.text(sx0 + 1.0, 9.3, "SoftMax",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color="#E07A1F")

    # fan lines from FC right side to each class node
    fc_right_x = fc_x + 0.55 + 0.5
    fc_right_y_top = fc_y + fc_h
    fc_right_y_bot = fc_y
    # connect each class to multiple sample points on FC for "fan" effect
    sample_ys = np.linspace(fc_right_y_top - 0.1, fc_right_y_bot + 0.1, 12)
    for ys in sample_ys:
        for yp in y_positions:
            ax.plot([fc_right_x + 0.02, sx1 - 0.18],
                    [ys, yp],
                    color="#C7B6E6", lw=0.35, alpha=0.55, zorder=1)

    # class circles
    node_colors = ["#F4A261", "#F4A261", "#F4A261",
                   "#2A9D8F", "#2A9D8F", "#2A9D8F",
                   "#1D7AC4", "#1D7AC4",
                   "#E76F51"]
    for yp, cls, c in zip(y_positions, classes, node_colors):
        ax.add_patch(patches.Circle((sx1, yp), 0.15, facecolor=c,
                                    edgecolor="#222", linewidth=0.8,
                                    zorder=5))
        ax.text(sx1 + 0.35, yp, cls,
                ha="left", va="center", fontsize=10.5,
                color="#222", fontweight="bold", zorder=5)

    # final-decision tag
    ax.text(sx1 + 2.55, 5.05, "调 制 制 式\n分     类",
            ha="left", va="center", fontsize=11.5, color="#0E4D92",
            fontweight="bold")

    # ---------- decoration / header ----------
    ax.text(0.3, 9.65, "Bi-LSTM × ResNet-18  Fusion Network",
            fontsize=15, color="#0B2A5B", fontweight="bold")
    ax.text(0.3, 9.25,
            "Underwater Acoustic Modulation Recognition  ·  9-class output",
            fontsize=10.5, color="#0E4D92", style="italic")
    ax.plot([0.3, 20.7], [9.05, 9.05], color="#cfd6e0", lw=0.6, zorder=0)

    # Save
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=240, bbox_inches="tight",
                facecolor="#FBFCFE")
    plt.close(fig)
    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    build_figure()
