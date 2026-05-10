from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable


OUT_DIR = Path(__file__).resolve().parent

WIDE_W = 1500
WIDE_H = 760
MEDIUM_H = 820

INK = "#1f1f1f"
MUTED = "#4c4c4c"
LINE = "#4a4a4a"
BLUE = "#2f5f8f"
BLUE_LIGHT = "#edf4fb"
GRAY = "#f6f6f6"
GREEN_LIGHT = "#eef7ef"
ORANGE_LIGHT = "#fff3e6"


def text(
    x: int,
    y: int,
    content: str,
    *,
    size: int = 26,
    weight: int | str = 400,
    anchor: str = "middle",
    color: str = INK,
) -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}">{escape(content)}</text>'
    )


def lines(
    x: int,
    y: int,
    content: Iterable[str],
    *,
    size: int = 22,
    gap: int = 32,
    anchor: str = "middle",
    color: str = MUTED,
) -> str:
    return "\n".join(
        text(x, y + i * gap, item, size=size, anchor=anchor, color=color)
        for i, item in enumerate(content)
    )


def box(
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
    body: Iterable[str] = (),
    *,
    fill: str = "#ffffff",
    stroke: str = LINE,
    title_size: int = 25,
    body_size: int = 21,
) -> str:
    body_items = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="2"/>',
        text(x + w // 2, y + 39, title, size=title_size, weight=700, color=INK),
    ]
    body_list = list(body)
    if body_list:
        body_items.append(lines(x + w // 2, y + 76, body_list, size=body_size, gap=30))
    return "\n".join(body_items)


def section_label(x: int, y: int, content: str) -> str:
    return (
        f'<rect x="{x - 74}" y="{y - 28}" width="148" height="38" rx="19" '
        f'fill="{BLUE_LIGHT}" stroke="{BLUE}" stroke-width="1.6"/>'
        + text(x, y - 2, content, size=20, weight=700, color=BLUE)
    )


def arrow(x1: int, y1: int, x2: int, y2: int, label: str = "") -> str:
    body = [
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LINE}" '
        f'stroke-width="2.4" marker-end="url(#arrow)"/>'
    ]
    if label:
        body.append(text((x1 + x2) // 2, (y1 + y2) // 2 - 10, label, size=18, color=MUTED))
    return "\n".join(body)


def svg(width: int, height: int, body: Iterable[str]) -> str:
    # Width/height use millimeters so Word inserts the image close to thesis text width.
    svg_width_mm = 150
    svg_height_mm = round(svg_width_mm * height / width, 1)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width_mm}mm" height="{svg_height_mm}mm" viewBox="0 0 {width} {height}">
  <defs>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M2,2 L11,6 L2,10 Z" fill="{LINE}"/>
    </marker>
    <style>
      text {{ font-family: "SimSun", "Songti SC", "Noto Serif CJK SC", serif; dominant-baseline: alphabetic; }}
      rect, path, line, polyline {{ vector-effect: non-scaling-stroke; }}
    </style>
  </defs>
  <rect width="{width}" height="{height}" fill="#ffffff"/>
  {"".join(body)}
</svg>
'''


def write(name: str, content: str) -> None:
    (OUT_DIR / name).write_text(content, encoding="utf-8")


def wave_path(x: int, y: int, w: int, amp: int, *, color: str = BLUE) -> str:
    step = w // 6
    return (
        f'<path d="M{x},{y} C{x + step // 2},{y - amp} {x + step},{y + amp} {x + step * 2},{y} '
        f'S{x + step * 3},{y - amp} {x + step * 4},{y} S{x + step * 5},{y + amp} {x + w},{y}" '
        f'fill="none" stroke="{color}" stroke-width="3"/>'
    )


def heatmap(x0: int, y0: int, *, phase: bool = False) -> str:
    palette = ["#f8fbff", "#dbe8f5", "#aac6df", "#6f96bd"] if not phase else ["#fffaf4", "#f7d8b7", "#e6aa70", "#b8793d"]
    cells = []
    for r in range(7):
        for c in range(8):
            idx = (r * 2 + c * 3 + (2 if phase else 0)) % len(palette)
            cells.append(
                f'<rect x="{x0 + c * 26}" y="{y0 + r * 22}" width="24" height="20" '
                f'fill="{palette[idx]}" stroke="#ffffff" stroke-width="1"/>'
            )
    return "\n".join(cells)


def figure_01() -> None:
    body = [
        section_label(750, 58, "总体技术路线"),
        box(70, 150, 235, 145, "数据获取", ["11k8m 数据集", ".mat 一维波形", "类别标签映射"], fill=GRAY),
        box(350, 150, 235, 145, "预处理", ["4096 点定长", "零均值归一化", "STFT 双通道"], fill=BLUE_LIGHT),
        box(630, 150, 235, 145, "模型训练", ["TinyCNN / ResNet18", "RNN1D", "FusionRNNResNet"], fill=GRAY),
        box(910, 150, 235, 145, "鲁棒评估", ["AWGN 加噪", "SNR 区间扫描", "准确率曲线"], fill=BLUE_LIGHT),
        box(1190, 150, 235, 145, "边缘部署", ["ONNX 导出", "树莓派推理", "UI 展示"], fill=GRAY),
        arrow(305, 222, 350, 222),
        arrow(585, 222, 630, 222),
        arrow(865, 222, 910, 222),
        arrow(1145, 222, 1190, 222),
        box(170, 440, 300, 145, "论文研究重点", ["时域动态与谱域纹理互补", "跨噪声条件泛化能力"], fill="#ffffff"),
        box(600, 440, 300, 145, "工程实现重点", ["统一数据接口", "可复现实验脚本", "轻量化推理链路"], fill="#ffffff"),
        box(1030, 440, 300, 145, "系统扩展方向", ["水听器采集前端", "实时显示与日志", "嵌入式样机联调"], fill="#ffffff"),
        arrow(470, 512, 600, 512),
        arrow(900, 512, 1030, 512),
    ]
    write("fig01_research_framework.svg", svg(WIDE_W, WIDE_H, body))


def figure_02() -> None:
    body = [
        section_label(750, 58, "数据预处理流程"),
        box(70, 145, 220, 130, "原始样本", ["11k8m/11k8m", "子文件夹为类别", ".mat 文件"], fill=GRAY),
        box(350, 145, 220, 130, "波形读取", ["loadmat", "展开为一维数组", "标签编码"], fill="#ffffff"),
        box(630, 145, 220, 130, "长度统一", ["截断过长样本", "短样本零填充", "4096 点"], fill=BLUE_LIGHT),
        box(910, 145, 220, 130, "幅值处理", ["零均值", "单位方差", "稳定优化"], fill="#ffffff"),
        box(1190, 145, 220, 130, "噪声增强", ["AWGN", "随机 SNR", "训练可选"], fill=GRAY),
        arrow(290, 210, 350, 210),
        arrow(570, 210, 630, 210),
        arrow(850, 210, 910, 210),
        arrow(1130, 210, 1190, 210),
        arrow(1018, 275, 740, 430, "时域输入"),
        arrow(1300, 275, 1010, 430, "谱域输入"),
        box(520, 430, 280, 150, "Time Feature", ["张量形状：1 x 4096", "输入 RNN1D / BiLSTM"], fill=GREEN_LIGHT),
        box(940, 430, 280, 150, "STFT Feature", ["张量形状：2 x 64 x 64", "输入 TinyCNN / ResNet"], fill=ORANGE_LIGHT),
        arrow(800, 505, 940, 505),
        text(870, 548, "同一标签 y", size=20, color=MUTED),
    ]
    write("fig02_preprocessing_pipeline.svg", svg(WIDE_W, WIDE_H, body))


def figure_03() -> None:
    body = [
        section_label(750, 58, "STFT 双通道特征构造"),
        box(80, 165, 360, 170, "固定长度波形 x[n]", ["长度 N = 4096", "归一化后进行分帧加窗"], fill=GRAY),
        wave_path(120, 270, 275, 38),
        arrow(440, 250, 565, 250, "STFT"),
        box(565, 165, 260, 170, "复时频矩阵 Zxx", ["nperseg = 128", "noverlap = 64", "包含幅度与相位"], fill=BLUE_LIGHT),
        arrow(825, 230, 960, 165, "abs"),
        arrow(825, 275, 960, 420, "angle"),
        box(960, 100, 330, 220, "幅度通道 |Zxx|", ["反映能量分布", "强调谐波与频带结构"], fill="#ffffff"),
        heatmap(1018, 190, phase=False),
        box(960, 390, 330, 220, "相位通道 ∠Zxx", ["反映相位变化", "缩放后参与训练"], fill="#ffffff"),
        heatmap(1018, 480, phase=True),
        arrow(1125, 320, 735, 635),
        arrow(1125, 610, 735, 675),
        box(545, 610, 360, 105, "双通道谱图张量", ["stack([magnitude, phase])，尺寸为 2 x 64 x 64"], fill=GREEN_LIGHT, body_size=20),
    ]
    write("fig03_stft_two_channel_feature.svg", svg(WIDE_W, MEDIUM_H, body))


def figure_04() -> None:
    body = [
        section_label(750, 58, "模型体系对比"),
        box(90, 170, 285, 340, "TinyCNN", ["输入：2 x 64 x 64", "少量卷积与池化", "参数少、训练快", "嵌入式候选"], fill="#ffffff"),
        box(430, 170, 285, 340, "ResNet18 谱域模型", ["首层改为 2 通道", "残差连接提取纹理", "输出高层谱域特征", "谱域强基线"], fill=BLUE_LIGHT),
        box(785, 170, 285, 340, "RNN1D 时域模型", ["输入：1 x 4096", "LSTM 建模序列动态", "关注包络与瞬态", "时域对照模型"], fill="#ffffff"),
        box(1125, 170, 285, 340, "FusionRNNResNet", ["BiLSTM 时域分支", "ResNet18 谱域分支", "特征拼接与分类", "本文重点模型"], fill=BLUE_LIGHT),
        text(232, 585, "轻量谱域基线", size=22, color=BLUE),
        text(572, 585, "深层谱域基线", size=22, color=BLUE),
        text(927, 585, "时域单模态对照", size=22, color=BLUE),
        text(1267, 585, "时频多模态融合", size=22, color=BLUE),
    ]
    write("fig04_model_family.svg", svg(WIDE_W, WIDE_H, body))


def figure_05() -> None:
    body = [
        section_label(750, 58, "FusionRNNResNet 网络结构"),
        box(70, 145, 250, 110, "时域输入", ["归一化波形 1 x 4096"], fill=GRAY),
        box(70, 475, 250, 110, "谱域输入", ["STFT 特征 2 x 64 x 64"], fill=GRAY),
        arrow(320, 200, 445, 200),
        arrow(320, 530, 445, 530),
        box(445, 130, 260, 145, "BiLSTM 分支", ["双向序列建模", "Dropout", "时间维均值池化"], fill=GREEN_LIGHT),
        box(445, 460, 260, 145, "ResNet18 分支", ["2 通道首层卷积", "残差特征提取", "输出 512 维向量"], fill=ORANGE_LIGHT),
        arrow(705, 200, 865, 300, "dt"),
        arrow(705, 530, 865, 430, "df"),
        box(865, 300, 250, 135, "特征融合", ["torch.cat([t, f])", "拼接为联合表示"], fill=BLUE_LIGHT),
        arrow(1115, 368, 1230, 368),
        box(1230, 300, 220, 135, "分类器", ["MLP + Dropout", "输出 9 类 logits"], fill="#ffffff"),
        text(750, 700, "融合思想：时域分支刻画动态变化，谱域分支刻画时频纹理，二者在特征层互补。", size=23, color=MUTED),
    ]
    write("fig05_fusion_rnn_resnet.svg", svg(WIDE_W, WIDE_H, body))


def figure_06() -> None:
    body = [
        section_label(750, 58, "AWGN 跨条件评估流程"),
        box(90, 150, 270, 145, "训练完成模型", ["TinyCNN / ResNet18", "RNN1D / Fusion"], fill=GRAY),
        box(430, 150, 270, 145, "干净测试样本", [".mat 波形", "固定长度处理"], fill="#ffffff"),
        box(770, 150, 270, 145, "AWGN 注入", ["按目标 SNR 控制", "模拟噪声条件迁移"], fill=BLUE_LIGHT),
        box(1110, 150, 270, 145, "模型推理", ["批量预测", "记录类别概率"], fill="#ffffff"),
        arrow(360, 222, 430, 222),
        arrow(700, 222, 770, 222),
        arrow(1040, 222, 1110, 222),
        box(310, 445, 310, 150, "SNR 扫描", ["例如 -10 dB 至 20 dB", "分区间统计性能"], fill=ORANGE_LIGHT),
        box(785, 445, 360, 150, "结果分析", ["Accuracy-SNR 曲线", "混淆矩阵 / F1", "单分支与融合模型对比"], fill=GREEN_LIGHT),
        arrow(620, 520, 785, 520),
        arrow(1245, 295, 965, 445),
    ]
    write("fig06_cross_condition_eval.svg", svg(WIDE_W, WIDE_H, body))


def figure_07() -> None:
    body = [
        section_label(750, 58, "树莓派端部署架构"),
        box(80, 160, 270, 140, "采集层", ["文件回放", "水听器 / ADC", "数据缓冲"], fill=GRAY),
        box(430, 160, 270, 140, "预处理层", ["4096 点窗口", "归一化", "STFT"], fill="#ffffff"),
        box(780, 160, 270, 140, "推理层", ["ONNX Runtime", "TinyCNN / Fusion", "Top-k 概率"], fill=BLUE_LIGHT),
        box(1130, 160, 270, 140, "应用层", ["UI 展示", "CSV 日志", "异常提示"], fill="#ffffff"),
        arrow(350, 230, 430, 230),
        arrow(700, 230, 780, 230),
        arrow(1050, 230, 1130, 230),
        box(230, 455, 300, 135, "PC 训练端", ["PyTorch 训练", "权重保存", "torch.onnx.export"], fill=ORANGE_LIGHT),
        box(720, 455, 300, 135, "模型文件", [".onnx", "类别映射表", "预处理参数"], fill=GREEN_LIGHT),
        box(1110, 455, 300, 135, "运行维护", ["开机自启动", "日志轮转", "温度与延迟监控"], fill=GRAY),
        arrow(530, 522, 720, 522),
        arrow(1020, 522, 1110, 522),
    ]
    write("fig07_raspberry_pi_deployment.svg", svg(WIDE_W, WIDE_H, body))


def figure_08() -> None:
    body = [
        section_label(750, 58, "人机界面原型"),
        f'<rect x="110" y="105" width="1280" height="585" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2.4"/>',
        f'<rect x="110" y="105" width="1280" height="58" rx="12" fill="{BLUE_LIGHT}" stroke="{LINE}" stroke-width="2.4"/>',
        text(750, 144, "水声信号识别系统", size=26, weight=700, color=INK),
        f'<rect x="155" y="205" width="520" height="170" rx="8" fill="{GRAY}" stroke="{LINE}" stroke-width="1.8"/>',
        text(415, 238, "实时波形显示", size=23, weight=700),
        wave_path(200, 305, 420, 36),
        f'<rect x="155" y="420" width="520" height="210" rx="8" fill="{GRAY}" stroke="{LINE}" stroke-width="1.8"/>',
        text(415, 455, "STFT 时频图", size=23, weight=700),
        heatmap(300, 490),
        f'<rect x="735" y="205" width="285" height="170" rx="8" fill="#ffffff" stroke="{LINE}" stroke-width="1.8"/>',
        text(878, 240, "识别结果", size=23, weight=700),
        text(878, 292, "目标类别：Class 3", size=24, color=BLUE),
        text(878, 334, "置信度：0.92", size=24, color=BLUE),
        f'<rect x="1080" y="205" width="265" height="170" rx="8" fill="#ffffff" stroke="{LINE}" stroke-width="1.8"/>',
        text(1212, 240, "运行控制", size=23, weight=700),
        text(1212, 292, "单文件 / 伪实时", size=22, color=MUTED),
        text(1212, 334, "开始  暂停  保存", size=22, color=MUTED),
        f'<rect x="735" y="420" width="610" height="210" rx="8" fill="{BLUE_LIGHT}" stroke="{LINE}" stroke-width="1.8"/>',
        text(1040, 455, "结果日志", size=23, weight=700),
        lines(790, 505, ["时间戳        文件名        Top-1        置信度", "16:45:02     sample_01     Class 3     0.92", "16:45:06     sample_02     Class 5     0.87"], size=21, anchor="start", gap=36),
    ]
    write("fig08_ui_wireframe.svg", svg(WIDE_W, WIDE_H, body))


def plot_xy(
    x: float,
    y: float,
    *,
    left: int,
    top: int,
    width: int,
    height: int,
    x_min: float = -10,
    x_max: float = 10,
    y_min: float = 40,
    y_max: float = 100,
) -> tuple[float, float]:
    px = left + (x - x_min) / (x_max - x_min) * width
    py = top + (y_max - y) / (y_max - y_min) * height
    return px, py


def marker(cx: float, cy: float, color: str, kind: str) -> str:
    if kind == "square":
        return f'<rect x="{cx - 5:.1f}" y="{cy - 5:.1f}" width="10" height="10" fill="#ffffff" stroke="{color}" stroke-width="2"/>'
    if kind == "triangle":
        return f'<path d="M{cx:.1f},{cy - 6:.1f} L{cx - 6:.1f},{cy + 5:.1f} L{cx + 6:.1f},{cy + 5:.1f} Z" fill="#ffffff" stroke="{color}" stroke-width="2"/>'
    if kind == "diamond":
        return f'<path d="M{cx:.1f},{cy - 6:.1f} L{cx + 6:.1f},{cy:.1f} L{cx:.1f},{cy + 6:.1f} L{cx - 6:.1f},{cy:.1f} Z" fill="#ffffff" stroke="{color}" stroke-width="2"/>'
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5.2" fill="#ffffff" stroke="{color}" stroke-width="2"/>'


def curve(
    xs: list[int],
    ys: list[float],
    *,
    color: str,
    kind: str,
    left: int,
    top: int,
    width: int,
    height: int,
) -> str:
    points = [plot_xy(x, y, left=left, top=top, width=width, height=height) for x, y in zip(xs, ys)]
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    symbols = "\n".join(marker(x, y, color, kind) for x, y in points)
    return f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="3"/>\n{symbols}'


def figure_09() -> None:
    left, top, width, height = 150, 90, 1030, 520
    xs = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
    series = [
        ("时域 RNN", [45, 50, 58, 65, 70, 75, 80, 82, 83, 85, 84], "#d33f3f", "circle"),
        ("STFT+ResNet", [67, 71, 76, 77, 79, 80, 80, 80, 84, 82, 84], "#2f6db3", "diamond"),
        ("STFT+CNN", [62, 68, 73, 77, 78, 78.5, 79.5, 79, 78.7, 78.3, 79], "#3a9b67", "triangle"),
        ("特征融合", [66, 72, 76, 80, 82.5, 85, 86.5, 87, 88.5, 88.7, 88.9], "#7a5ac8", "square"),
        ("RNN+ResNet 融合", [84.5, 86, 89, 91, 93.5, 94.5, 94.7, 96.5, 97.1, 96.6, 96.6], "#d96b1c", "circle"),
    ]

    body: list[str] = []
    for yt in [40, 50, 60, 70, 80, 90, 100]:
        _, py = plot_xy(-10, yt, left=left, top=top, width=width, height=height)
        body.append(f'<line x1="{left}" y1="{py:.1f}" x2="{left + width}" y2="{py:.1f}" stroke="#d9d9d9" stroke-width="1.2" stroke-dasharray="6 6"/>')
        body.append(text(left - 24, int(py + 7), str(yt), size=22, anchor="end", color=INK))
    for xt in xs:
        px, _ = plot_xy(xt, 40, left=left, top=top, width=width, height=height)
        body.append(f'<line x1="{px:.1f}" y1="{top}" x2="{px:.1f}" y2="{top + height}" stroke="#e5e5e5" stroke-width="1.1" stroke-dasharray="5 7"/>')
        body.append(text(int(px), top + height + 38, str(xt), size=22, color=INK))

    body.extend(
        [
            f'<rect x="{left}" y="{top}" width="{width}" height="{height}" fill="none" stroke="{INK}" stroke-width="2.2"/>',
            f'<line x1="{left}" y1="{top + height}" x2="{left + width}" y2="{top + height}" stroke="{INK}" stroke-width="2.4"/>',
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + height}" stroke="{INK}" stroke-width="2.4"/>',
            text(left + width // 2, top + height + 82, "信噪比 (dB)", size=27, color=INK),
            f'<text x="52" y="{top + height // 2}" text-anchor="middle" font-size="27" fill="{INK}" transform="rotate(-90 52 {top + height // 2})">识别率 (%)</text>',
        ]
    )

    for _, ys, color, kind in series:
        body.append(curve(xs, ys, color=color, kind=kind, left=left, top=top, width=width, height=height))

    legend_x, legend_y = 1215, 150
    body.append(f'<rect x="{legend_x - 20}" y="{legend_y - 40}" width="245" height="235" fill="#ffffff" stroke="{LINE}" stroke-width="1.5"/>')
    for i, (name, _, color, kind) in enumerate(series):
        y = legend_y + i * 42
        body.append(f'<line x1="{legend_x}" y1="{y}" x2="{legend_x + 48}" y2="{y}" stroke="{color}" stroke-width="3"/>')
        body.append(marker(legend_x + 24, y, color, kind))
        body.append(text(legend_x + 62, y + 8, name, size=21, anchor="start", color=INK))

    write("fig09_snr_accuracy_academic.svg", svg(WIDE_W, 780, body))


def figure_10() -> None:
    body = [
        section_label(750, 58, "制式识别多分类流程"),
        box(70, 180, 210, 135, "输入信号", ["接收片段 x", "固定长度窗口"], fill=GRAY),
        box(340, 180, 210, 135, "预处理", ["截取 / 补零", "波形标准化"], fill="#ffffff"),
        box(610, 180, 210, 135, "特征构建", ["时域波形", "STFT 谱图"], fill=BLUE_LIGHT),
        box(880, 180, 230, 135, "深度模型", ["学习判别特征", "fθ(x)"], fill="#ffffff"),
        box(1170, 180, 240, 135, "分类输出", ["P(y|x)", "类别标签 ĉ"], fill=GRAY),
        arrow(280, 248, 340, 248),
        arrow(550, 248, 610, 248),
        arrow(820, 248, 880, 248),
        arrow(1110, 248, 1170, 248),
        f'<rect x="110" y="405" width="1280" height="210" rx="10" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="10 8"/>',
        text(750, 440, "监督学习训练阶段", size=25, weight=700, color=BLUE),
        box(180, 480, 250, 95, "训练样本", ["{(x_i, y_i)}"], fill="#ffffff", title_size=23, body_size=22),
        box(520, 480, 250, 95, "损失函数", ["交叉熵损失"], fill=ORANGE_LIGHT, title_size=23, body_size=22),
        box(860, 480, 250, 95, "参数优化", ["反向传播更新 θ"], fill=GREEN_LIGHT, title_size=23, body_size=22),
        box(1180, 480, 150, 95, "模型保存", ["最优权重"], fill="#ffffff", title_size=23, body_size=21),
        arrow(430, 528, 520, 528),
        arrow(770, 528, 860, 528),
        arrow(1110, 528, 1180, 528),
        f'<line x1="985" y1="480" x2="985" y2="315" stroke="{BLUE}" stroke-width="2" stroke-dasharray="8 7" marker-end="url(#arrow)"/>',
        text(1008, 397, "训练得到", size=19, anchor="start", color=BLUE),
        text(750, 684, "判决规则：ĉ = arg max P(y = c_k | x)，其中 C = {c1, c2, ..., cK}", size=25, color=INK),
    ]
    write("fig10_modulation_multiclass_flow.svg", svg(WIDE_W, WIDE_H, body))


def figure_11() -> None:
    body = [
        section_label(750, 56, "深度学习模型结构概述"),
        f'<rect x="70" y="105" width="1360" height="70" rx="10" fill="{BLUE_LIGHT}" stroke="{BLUE}" stroke-width="1.8"/>',
        text(750, 150, "深度学习通过多层神经网络从波形或谱图中自动学习判别性特征，减少对人工特征设计的依赖", size=24, color=INK),
        box(95, 245, 250, 125, "一维时域波形", ["4096 点序列", "幅度 / 相位变化规律"], fill=GRAY, title_size=24, body_size=20),
        box(95, 460, 250, 125, "STFT 双通道谱图", ["幅值谱 + 相位谱", "局部时频纹理"], fill=BLUE_LIGHT, title_size=24, body_size=20),
        box(455, 245, 280, 125, "LSTM 时域分支", ["门控机制保留长时信息", "建模序列依赖关系"], fill="#ffffff", title_size=24, body_size=20),
        box(455, 460, 280, 125, "CNN / ResNet 谱图分支", ["局部连接与权值共享", "残差连接稳定深层训练"], fill="#ffffff", title_size=24, body_size=20),
        box(860, 335, 260, 145, "多分支特征融合", ["拼接时域与谱域表示", "增强低信噪比鲁棒性"], fill=GREEN_LIGHT, title_size=24, body_size=20),
        box(1235, 335, 190, 145, "制式分类", ["Softmax 输出", "9 类调制标签"], fill=ORANGE_LIGHT, title_size=24, body_size=20),
        arrow(345, 308, 455, 308, "序列建模"),
        arrow(345, 522, 455, 522, "局部纹理"),
        arrow(735, 308, 860, 382),
        arrow(735, 522, 860, 432),
        arrow(1120, 407, 1235, 407),
        f'<line x1="220" y1="370" x2="220" y2="460" stroke="{LINE}" stroke-width="1.6" stroke-dasharray="8 7"/>',
        f'<line x1="595" y1="370" x2="595" y2="460" stroke="{LINE}" stroke-width="1.6" stroke-dasharray="8 7"/>',
        text(750, 672, "图示关系：CNN/ResNet 侧重谱图局部稳健特征，LSTM 侧重长时依赖，多分支融合用于提升抗噪识别能力", size=23, color=INK),
    ]
    write("fig11_deep_learning_structure_summary.svg", svg(WIDE_W, WIDE_H, body))


def main() -> None:
    figure_01()
    figure_02()
    figure_03()
    figure_04()
    figure_05()
    figure_06()
    figure_07()
    figure_08()
    figure_09()
    figure_10()
    figure_11()


if __name__ == "__main__":
    main()
