from __future__ import annotations

from html import escape
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent

LABELS = [
    "R2FSK",
    "R4FSK",
    "R8FSK",
    "R2PSK",
    "R4PSK",
    "R8PSK",
    "R16QAM",
    "R64QAM",
    "R64OFDM",
]

MATRICES = [
    (
        "fig12_confusion_rnn1d.svg",
        "时域 RNN 混淆矩阵",
        [
            [97, 0, 0, 0, 0, 0, 0, 1, 2],
            [0, 97, 1, 0, 0, 0, 0, 0, 2],
            [0, 1, 99, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 78, 3, 9, 5, 5, 0],
            [0, 0, 0, 24, 59, 9, 2, 6, 0],
            [0, 0, 0, 31, 53, 5, 4, 7, 0],
            [0, 0, 0, 1, 9, 3, 56, 31, 0],
            [0, 0, 0, 6, 3, 4, 33, 54, 0],
            [1, 5, 0, 0, 0, 0, 0, 0, 94],
        ],
    ),
    (
        "fig13_confusion_stft_tinycnn.svg",
        "STFT + TinyCNN 混淆矩阵",
        [
            [100, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 97, 1, 0, 0, 0, 0, 0, 2],
            [0, 0, 100, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 93, 1, 0, 5, 1, 0],
            [0, 0, 0, 2, 88, 1, 8, 1, 0],
            [0, 0, 0, 3, 81, 4, 12, 0, 0],
            [0, 0, 0, 1, 0, 0, 41, 58, 0],
            [0, 0, 0, 0, 1, 0, 35, 64, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 99],
        ],
    ),
    (
        "fig14_confusion_stft_resnet.svg",
        "STFT + ResNet 混淆矩阵",
        [
            [100, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 100, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 100, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 94, 3, 0, 1, 2, 0],
            [0, 0, 0, 0, 39, 54, 5, 2, 0],
            [0, 0, 0, 0, 30, 60, 5, 5, 0],
            [0, 0, 0, 1, 3, 0, 66, 30, 0],
            [0, 0, 0, 0, 1, 1, 43, 55, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 100],
        ],
    ),
    (
        "fig15_confusion_stft_cnn_rnn.svg",
        "STFT + CNN + RNN 融合模型混淆矩阵",
        [
            [97, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 89, 11, 0, 0, 0, 0, 0, 0],
            [0, 1, 99, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 65, 4, 30, 1, 0, 0],
            [0, 0, 0, 14, 67, 19, 0, 0, 0],
            [0, 0, 0, 22, 35, 43, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 78, 22, 0],
            [0, 0, 0, 0, 0, 0, 10, 90, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 100],
        ],
    ),
    (
        "fig16_confusion_stft_resnet_rnn.svg",
        "STFT + ResNet + RNN 融合模型混淆矩阵",
        [
            [100, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 100, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 100, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 100, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 78, 21, 0, 0, 0],
            [0, 0, 0, 2, 27, 71, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 88, 12, 0],
            [0, 0, 0, 0, 0, 0, 14, 86, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 100],
        ],
    ),
]


def text(
    x: float,
    y: float,
    content: str,
    *,
    size: int = 22,
    weight: int | str = 400,
    anchor: str = "middle",
    color: str = "#1f1f1f",
    rotate: float | None = None,
) -> str:
    transform = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}"{transform}>{escape(content)}</text>'
    )


def heat_color(value: int) -> str:
    # White to thesis-blue heat scale.
    t = max(0.0, min(value / 100.0, 1.0))
    start = (246, 251, 255)
    end = (46, 104, 166)
    rgb = tuple(round(start[i] + (end[i] - start[i]) * t) for i in range(3))
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def make_svg(title: str, matrix: list[list[int]]) -> str:
    width, height = 1200, 1120
    left, top = 250, 220
    cell = 82
    grid = cell * len(LABELS)
    body: list[str] = []

    body.append(f'<rect width="{width}" height="{height}" fill="#ffffff"/>')
    body.append(text(width / 2, 64, title, size=34, weight=700, color="#123a5a"))
    body.append(text(left + grid / 2, 156, "预测类别", size=27, weight=700))
    body.append(text(60, top + grid / 2, "真实类别", size=27, weight=700, rotate=-90))

    for j, label in enumerate(LABELS):
        x = left + j * cell + cell / 2
        body.append(text(x, top - 22, label, size=18, rotate=-35))
    for i, label in enumerate(LABELS):
        y = top + i * cell + cell / 2 + 8
        body.append(text(left - 22, y, label, size=19, anchor="end"))

    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            x = left + j * cell
            y = top + i * cell
            fill = heat_color(value)
            body.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{fill}" '
                f'stroke="#ffffff" stroke-width="2"/>'
            )
            color = "#ffffff" if value >= 55 else "#1f1f1f"
            weight = 700 if value > 0 else 400
            body.append(text(x + cell / 2, y + cell / 2 + 8, str(value), size=22, weight=weight, color=color))

    body.append(
        f'<rect x="{left}" y="{top}" width="{grid}" height="{grid}" fill="none" '
        f'stroke="#333333" stroke-width="2.2"/>'
    )

    # Color legend.
    legend_x, legend_y, legend_w, legend_h = 1030, 315, 30, 360
    for k in range(60):
        value = round(100 * (1 - k / 59))
        y = legend_y + k * legend_h / 60
        body.append(
            f'<rect x="{legend_x}" y="{y:.1f}" width="{legend_w}" height="{legend_h / 60 + 0.5:.1f}" '
            f'fill="{heat_color(value)}" stroke="none"/>'
        )
    body.append(f'<rect x="{legend_x}" y="{legend_y}" width="{legend_w}" height="{legend_h}" fill="none" stroke="#555555" stroke-width="1.3"/>')
    body.append(text(legend_x + 48, legend_y + 8, "100", size=18, anchor="start"))
    body.append(text(legend_x + 48, legend_y + legend_h + 5, "0", size=18, anchor="start"))
    body.append(text(legend_x + 14, legend_y + legend_h + 46, "样本数", size=19))

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="150mm" height="140mm" viewBox="0 0 {width} {height}">
  <style>
    text {{ font-family: "SimSun", "Songti SC", "Noto Serif CJK SC", serif; dominant-baseline: alphabetic; }}
  </style>
  {"".join(body)}
</svg>
'''


def main() -> None:
    for filename, title, matrix in MATRICES:
        (OUT_DIR / filename).write_text(make_svg(title, matrix), encoding="utf-8")


if __name__ == "__main__":
    main()
