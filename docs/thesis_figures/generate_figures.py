from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable


OUT_DIR = Path(__file__).resolve().parent


def text(
    x: int,
    y: int,
    content: str,
    *,
    size: int = 24,
    weight: int | str = 500,
    anchor: str = "middle",
    color: str = "#18324a",
    cls: str = "",
) -> str:
    klass = f' class="{cls}"' if cls else ""
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}"{klass}>{escape(content)}</text>'
    )


def multiline_text(
    x: int,
    y: int,
    lines: Iterable[str],
    *,
    size: int = 18,
    anchor: str = "middle",
    color: str = "#27445e",
    line_gap: int = 26,
) -> str:
    items = []
    for i, line in enumerate(lines):
        items.append(
            f'<text x="{x}" y="{y + i * line_gap}" text-anchor="{anchor}" '
            f'font-size="{size}" fill="{color}">{escape(line)}</text>'
        )
    return "\n".join(items)


def box(
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
    lines: Iterable[str] = (),
    *,
    fill: str = "#ffffff",
    stroke: str = "#2d6cdf",
    title_color: str = "#14395b",
) -> str:
    body = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="2.5" filter="url(#shadow)"/>',
        text(x + w // 2, y + 36, title, size=22, weight=700, color=title_color),
    ]
    if lines:
        body.append(multiline_text(x + w // 2, y + 70, lines, size=17, line_gap=24))
    return "\n".join(body)


def arrow(x1: int, y1: int, x2: int, y2: int, label: str = "") -> str:
    body = [
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#37658c" '
        f'stroke-width="3" marker-end="url(#arrow)"/>'
    ]
    if label:
        body.append(text((x1 + x2) // 2, (y1 + y2) // 2 - 10, label, size=15, color="#48657a"))
    return "\n".join(body)


def pill(x: int, y: int, w: int, h: int, label: str, *, fill: str = "#e9f4ff") -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h // 2}" fill="{fill}" '
        f'stroke="#7fb2e5" stroke-width="1.6"/>'
        + text(x + w // 2, y + h // 2 + 7, label, size=17, color="#1f4e78")
    )


def svg(width: int, height: int, title_: str, subtitle: str, body: Iterable[str]) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#eef7ff"/>
      <stop offset="0.55" stop-color="#f8fbff"/>
      <stop offset="1" stop-color="#eef3ff"/>
    </linearGradient>
    <filter id="shadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#5a7390" flood-opacity="0.16"/>
    </filter>
    <marker id="arrow" markerWidth="13" markerHeight="13" refX="10" refY="6" orient="auto">
      <path d="M2,2 L11,6 L2,10 Z" fill="#37658c"/>
    </marker>
    <style>
      text {{ font-family: "Microsoft YaHei", "Noto Sans CJK SC", "PingFang SC", Arial, sans-serif; }}
      .small {{ letter-spacing: 0.2px; }}
    </style>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#bg)"/>
  {text(width // 2, 54, title_, size=30, weight=800, color="#112f4a")}
  {text(width // 2, 88, subtitle, size=18, color="#5b7288")}
  {"".join(body)}
</svg>
'''


def write(name: str, content: str) -> None:
    (OUT_DIR / name).write_text(content, encoding="utf-8")


def figure_01() -> None:
    nodes = [
        box(55, 170, 200, 155, "数据层", ["11k8m / .mat", "4096 点固定长度", "9 类标签映射"], fill="#ffffff"),
        box(300, 170, 200, 155, "特征层", ["时域归一化", "STFT 幅度", "STFT 相位"], fill="#f9fdff"),
        box(545, 170, 200, 155, "模型层", ["TinyCNN", "ResNet18", "RNN1D / Fusion"], fill="#ffffff"),
        box(790, 170, 200, 155, "评估层", ["验证 / 测试", "AWGN 注入", "跨 SNR 曲线"], fill="#f9fdff"),
        box(1035, 170, 200, 155, "部署层", ["ONNX 导出", "树莓派推理", "UI 展示"], fill="#ffffff"),
    ]
    arrows = [arrow(255, 248, 300, 248), arrow(500, 248, 545, 248), arrow(745, 248, 790, 248), arrow(990, 248, 1035, 248)]
    bottom = [
        box(155, 430, 300, 135, "论文主线", ["算法对比", "时频融合", "噪声鲁棒性"], fill="#eef7ff", stroke="#77a9dc"),
        box(495, 430, 300, 135, "工程主线", ["端侧轻量化", "模型格式迁移", "采集-推理-展示闭环"], fill="#fff7ed", stroke="#f0a04b"),
        box(835, 430, 300, 135, "预期成果", ["可复现实验流程", "论文图表素材", "嵌入式样机路线"], fill="#f0fff5", stroke="#52b879"),
    ]
    write(
        "fig01_research_framework.svg",
        svg(1280, 720, "水声目标识别研究总体技术路线", "从离线波形数据到融合识别模型，再到树莓派边缘端部署", nodes + arrows + bottom),
    )


def figure_02() -> None:
    body = [
        box(70, 145, 190, 120, "数据输入", ["11k8m/11k8m", "类别文件夹", ".mat 波形"], fill="#ffffff"),
        box(315, 145, 190, 120, "样本读取", ["scipy.io.loadmat", "一维波形展开", "label_map 编码"], fill="#f9fdff"),
        box(560, 145, 190, 120, "长度统一", ["截断过长样本", "零填充短样本", "SIGNAL_LENGTH=4096"], fill="#ffffff"),
        box(805, 145, 190, 120, "时域归一化", ["零均值", "单位方差", "稳定训练"], fill="#f9fdff"),
        box(1050, 145, 190, 120, "可选增强", ["AWGN", "SNR 区间采样", "增强鲁棒性"], fill="#ffffff"),
        arrow(260, 205, 315, 205),
        arrow(505, 205, 560, 205),
        arrow(750, 205, 805, 205),
        arrow(995, 205, 1050, 205),
        arrow(900, 265, 760, 400, "时域分支"),
        arrow(1135, 265, 995, 400, "谱域分支"),
        box(510, 410, 260, 130, "Time Feature", ["1 x 4096", "RNN1D / BiLSTM", "动态包络信息"], fill="#eef7ff", stroke="#77a9dc"),
        box(890, 410, 260, 130, "STFT Feature", ["2 x 64 x 64", "幅度 + 相位", "CNN / ResNet 输入"], fill="#fff7ed", stroke="#f0a04b"),
        arrow(770, 475, 855, 475),
        box(625, 590, 410, 80, "DataLoader 批处理：统一输入张量、标签与训练 / 评估流程", [], fill="#f0fff5", stroke="#52b879"),
    ]
    write(
        "fig02_preprocessing_pipeline.svg",
        svg(1280, 720, "MAT 波形样本预处理流程", "固定长度、归一化、STFT 与 AWGN 增强构成统一数据入口", body),
    )


def heatmap(x0: int, y0: int, *, phase: bool = False) -> str:
    colors = ["#dff1ff", "#a6d8ff", "#5aa9e6", "#2d6cdf"] if not phase else ["#fff1dd", "#ffd08a", "#f59e42", "#d96c1b"]
    rects = []
    for r in range(8):
        for c in range(8):
            idx = (r * 3 + c * 2 + (3 if phase else 0)) % len(colors)
            rects.append(f'<rect x="{x0 + c * 24}" y="{y0 + r * 18}" width="22" height="16" rx="3" fill="{colors[idx]}"/>')
    return "\n".join(rects)


def figure_03() -> None:
    waveform = [
        '<path d="M92,257 C130,210 165,300 205,250 S280,205 320,256 S395,310 435,250 S510,205 550,257" fill="none" stroke="#2d6cdf" stroke-width="4"/>',
        box(70, 180, 500, 160, "固定长度波形 x[n]", ["截断 / 零填充到 4096 点", "归一化后作为 STFT 输入"], fill="#ffffff"),
    ]
    body = waveform + [
        arrow(570, 260, 670, 260, "分帧加窗"),
        box(680, 180, 230, 160, "STFT", ["nperseg=128", "noverlap=64", "复矩阵 Zxx"], fill="#f9fdff"),
        arrow(910, 260, 1005, 210, "幅度"),
        arrow(910, 260, 1005, 345, "相位"),
        box(1000, 135, 220, 160, "|Zxx|", ["谱能量纹理", "谐波 / 频带结构"], fill="#eef7ff", stroke="#77a9dc"),
        heatmap(1015, 315, phase=False),
        text(1125, 305, "Magnitude", size=16, color="#1f4e78"),
        box(1000, 370, 220, 160, "∠Zxx", ["相位变化信息", "缩放到稳定范围"], fill="#fff7ed", stroke="#f0a04b"),
        heatmap(1015, 550, phase=True),
        text(1125, 540, "Phase", size=16, color="#9a4b10"),
        arrow(1110, 295, 740, 570),
        arrow(1110, 530, 740, 610),
        box(550, 555, 300, 95, "双通道张量", ["stack([magnitude, phase])", "输入尺寸：2 x 64 x 64"], fill="#f0fff5", stroke="#52b879"),
    ]
    write(
        "fig03_stft_two_channel_feature.svg",
        svg(1280, 720, "STFT 幅度-相位双通道特征构造", "将非平稳水声波形映射为适合卷积网络处理的二维时频表示", body),
    )


def figure_04() -> None:
    body = [
        box(60, 150, 250, 410, "TinyCNN", ["输入：2 x 64 x 64", "少量卷积层", "训练快、参数少", "适合嵌入式候选"], fill="#ffffff"),
        box(365, 150, 250, 410, "ResNet18 谱域", ["首层改为 2 通道", "残差结构提取纹理", "输出 512 维特征", "谱域强基线"], fill="#f9fdff"),
        box(670, 150, 250, 410, "RNN1D 时域", ["输入：1 x 4096", "序列动态建模", "关注包络与瞬态", "单模态对照"], fill="#ffffff"),
        box(975, 150, 250, 410, "FusionRNNResNet", ["BiLSTM 时域分支", "ResNet18 谱域分支", "concat 特征融合", "重点研究模型"], fill="#f9fdff"),
        pill(95, 600, 180, 46, "轻量谱域基线"),
        pill(400, 600, 180, 46, "深层谱域模型"),
        pill(705, 600, 180, 46, "时域序列模型"),
        pill(1010, 600, 180, 46, "时频融合模型"),
    ]
    write(
        "fig04_model_family.svg",
        svg(1280, 720, "本文对比模型体系", "通过单模态基线与多模态融合模型分析不同特征归纳偏置的贡献", body),
    )


def figure_05() -> None:
    body = [
        box(60, 155, 230, 110, "归一化波形", ["1 x 4096"], fill="#ffffff"),
        box(60, 455, 230, 110, "STFT 特征", ["2 x 64 x 64"], fill="#ffffff"),
        arrow(290, 210, 410, 210),
        arrow(290, 510, 410, 510),
        box(410, 145, 260, 130, "时域分支", ["BiLSTM 多层堆叠", "Dropout", "时间维均值池化"], fill="#eef7ff", stroke="#77a9dc"),
        box(410, 445, 260, 130, "谱域分支", ["ResNet18 Backbone", "去除最终 FC", "512 维谱域特征"], fill="#fff7ed", stroke="#f0a04b"),
        arrow(670, 210, 810, 335),
        arrow(670, 510, 810, 385),
        box(800, 300, 210, 120, "特征拼接", ["torch.cat([t, f])", "时域 + 谱域"], fill="#f0fff5", stroke="#52b879"),
        arrow(1010, 360, 1110, 360),
        box(1110, 290, 130, 140, "分类器", ["MLP", "Dropout", "9 类 logits"], fill="#ffffff"),
        text(535, 325, "时域动态：包络、瞬态、长时相关", size=17, color="#2f5f8f"),
        text(535, 625, "谱域纹理：谐波、频带、时频局部模式", size=17, color="#a05a1a"),
        text(905, 470, "互补信息在特征层融合", size=18, weight=700, color="#2f6b43"),
    ]
    write(
        "fig05_fusion_rnn_resnet.svg",
        svg(1280, 720, "FusionRNNResNet 时频融合网络结构", "双向 LSTM 捕获时域动态，ResNet18 捕获谱域纹理，融合后完成分类", body),
    )


def figure_06() -> None:
    curve = [
        '<polyline points="930,528 985,500 1040,455 1095,390 1150,330 1205,285" fill="none" stroke="#2d6cdf" stroke-width="4"/>',
        '<line x1="915" y1="545" x2="1215" y2="545" stroke="#607d96" stroke-width="2"/>',
        '<line x1="915" y1="545" x2="915" y2="260" stroke="#607d96" stroke-width="2"/>',
        text(1065, 585, "SNR / dB", size=15, color="#48657a"),
        text(875, 400, "Acc", size=15, color="#48657a"),
    ]
    body = [
        box(60, 155, 220, 115, "训练完成模型", ["TinyCNN / ResNet", "RNN1D / Fusion"], fill="#ffffff"),
        box(360, 155, 220, 115, "独立测试集", [".mat 波形", "不参与训练"], fill="#f9fdff"),
        box(660, 155, 220, 115, "AWGN 注入", ["按目标 SNR", "生成噪声样本"], fill="#ffffff"),
        arrow(280, 212, 360, 212),
        arrow(580, 212, 660, 212),
        arrow(770, 270, 770, 365, "扫描区间"),
        box(640, 370, 260, 120, "跨条件推理", ["SNR_min 到 SNR_max", "逐区间统计准确率"], fill="#eef7ff", stroke="#77a9dc"),
        arrow(900, 430, 970, 430),
        box(960, 315, 250, 120, "指标汇总", ["Accuracy", "Macro-F1", "混淆矩阵 / 每类召回"], fill="#f0fff5", stroke="#52b879"),
        box(60, 390, 430, 120, "分析重点", ["低 SNR 退化速度", "融合模型与单分支差异", "噪声增强是否提升泛化"], fill="#fff7ed", stroke="#f0a04b"),
    ] + curve
    write(
        "fig06_cross_condition_eval.svg",
        svg(1280, 720, "AWGN 跨条件噪声鲁棒评估流程", "在测试阶段控制信噪比，观察模型识别准确率随噪声强度变化的趋势", body),
    )


def figure_07() -> None:
    body = [
        box(60, 150, 245, 135, "PC 训练端", ["PyTorch 训练", "保存 best checkpoint", "torch.onnx.export"], fill="#ffffff"),
        arrow(305, 218, 425, 218, "ONNX 文件"),
        box(425, 150, 245, 135, "模型迁移", ["算子兼容检查", "输入尺寸固定", "可选量化"], fill="#f9fdff"),
        arrow(670, 218, 790, 218, "部署"),
        box(790, 150, 395, 135, "树莓派推理端", ["ONNX Runtime / OpenCV DNN", "CPU 推理", "日志与异常恢复"], fill="#ffffff"),
        box(120, 410, 210, 120, "采集层", ["文件回放", "水听器 / ADC", "缓冲区"], fill="#eef7ff", stroke="#77a9dc"),
        box(390, 410, 210, 120, "预处理层", ["4096 点切片", "归一化", "STFT"], fill="#fff7ed", stroke="#f0a04b"),
        box(660, 410, 210, 120, "推理层", ["ONNX 输入张量", "Top-k 概率", "延迟统计"], fill="#f0fff5", stroke="#52b879"),
        box(930, 410, 210, 120, "应用层", ["UI 展示", "CSV 记录", "告警提示"], fill="#ffffff"),
        arrow(330, 470, 390, 470),
        arrow(600, 470, 660, 470),
        arrow(870, 470, 930, 470),
        pill(190, 610, 220, 48, "端侧低时延"),
        pill(530, 610, 220, 48, "资源受限可运行"),
        pill(870, 610, 220, 48, "采集-推理-展示闭环"),
    ]
    write(
        "fig07_raspberry_pi_deployment.svg",
        svg(1280, 720, "树莓派端水声识别系统部署架构", "训练端负责模型生成，边缘端负责采集、预处理、推理与结果展示", body),
    )


def figure_08() -> None:
    bars = []
    labels = [("类别 A", 0.86, "#2d6cdf"), ("类别 B", 0.41, "#77a9dc"), ("类别 C", 0.23, "#f0a04b"), ("类别 D", 0.12, "#c7d3df")]
    y = 205
    for label, value, color in labels:
        bars.append(text(875, y, label, size=16, anchor="start", color="#27445e"))
        bars.append(f'<rect x="940" y="{y - 16}" width="210" height="18" rx="9" fill="#e8eef5"/>')
        bars.append(f'<rect x="940" y="{y - 16}" width="{int(210 * value)}" height="18" rx="9" fill="{color}"/>')
        bars.append(text(1165, y, f"{int(value * 100)}%", size=15, anchor="start", color="#27445e"))
        y += 48
    body = [
        '<rect x="70" y="120" width="1140" height="520" rx="26" fill="#ffffff" stroke="#9ab8d5" stroke-width="2.5" filter="url(#shadow)"/>',
        '<rect x="70" y="120" width="1140" height="54" rx="26" fill="#2d6cdf"/>',
        text(640, 155, "水声目标识别演示系统", size=22, weight=800, color="#ffffff"),
        '<rect x="105" y="205" width="470" height="150" rx="16" fill="#f4f9ff" stroke="#b7d4ef"/>',
        text(340, 230, "实时波形", size=18, weight=700),
        '<path d="M130,305 C165,270 195,340 230,300 S300,260 335,305 S405,350 445,300 S510,260 550,305" fill="none" stroke="#2d6cdf" stroke-width="4"/>',
        '<rect x="105" y="390" width="470" height="190" rx="16" fill="#fff8ef" stroke="#f0c28c"/>',
        text(340, 418, "STFT 时频图", size=18, weight=700),
        heatmap(185, 445, phase=False),
        heatmap(385, 445, phase=True),
        '<rect x="620" y="205" width="560" height="185" rx="16" fill="#f7fbff" stroke="#b7d4ef"/>',
        text(900, 235, "识别结果与置信度", size=18, weight=700),
        '<rect x="620" y="425" width="260" height="120" rx="16" fill="#f0fff5" stroke="#a8dcb8"/>',
        text(750, 455, "运行状态", size=18, weight=700),
        multiline_text(750, 488, ["模式：离线单文件", "延迟：38 ms", "设备：Raspberry Pi"], size=15),
        '<rect x="920" y="425" width="260" height="120" rx="16" fill="#f7fbff" stroke="#b7d4ef"/>',
        text(1050, 455, "记录与导出", size=18, weight=700),
        multiline_text(1050, 488, ["CSV 日志", "Top-k 概率", "时间戳 / 文件名"], size=15),
        '<rect x="620" y="565" width="560" height="42" rx="21" fill="#eaf3ff" stroke="#b7d4ef"/>',
        text(900, 592, "开始采集    单文件识别    导出结果    参数设置", size=16, color="#1f4e78"),
    ] + bars
    write(
        "fig08_ui_wireframe.svg",
        svg(1280, 720, "水声识别系统人机界面原型", "界面同时显示波形、时频图、分类置信度、运行状态与日志导出入口", body),
    )


def main() -> None:
    figure_01()
    figure_02()
    figure_03()
    figure_04()
    figure_05()
    figure_06()
    figure_07()
    figure_08()


if __name__ == "__main__":
    main()
