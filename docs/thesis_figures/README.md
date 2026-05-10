# 论文配图素材：水声信号识别与树莓派部署

本目录提供一组可直接插入本科毕业论文的 SVG 矢量图，主题覆盖数据预处理、STFT 特征、模型结构、跨噪声评估、树莓派部署与 UI 方案。

图片按 Word 论文正文排版重新设计：白色背景、窄幅画布、细线框、少量浅灰/浅蓝填充、字号偏大，插入 A4 论文正文后仍能保持可读性。图内不再使用大面积渐变、阴影或幻灯片式标题，图题建议统一放在 Word 图片下方。

## 图片清单与建议位置

| 文件 | 建议图题 | 建议章节 |
| --- | --- | --- |
| `fig01_research_framework.svg` | 水声目标识别研究总体技术路线 | 第 1 章 / 第 4 章 |
| `fig02_preprocessing_pipeline.svg` | MAT 波形样本预处理流程 | 第 3 章 |
| `fig03_stft_two_channel_feature.svg` | STFT 双通道时频特征构造示意图 | 第 2 章 / 第 3 章 |
| `fig04_model_family.svg` | 单模态与多模态模型对比框架 | 第 4 章 |
| `fig05_fusion_rnn_resnet.svg` | FusionRNNResNet 时频融合网络结构 | 第 4 章 |
| `fig06_cross_condition_eval.svg` | AWGN 跨条件噪声鲁棒评估流程 | 第 5 章 |
| `fig07_raspberry_pi_deployment.svg` | 树莓派端水声识别系统部署架构 | 第 6 章 |
| `fig08_ui_wireframe.svg` | 水声识别系统人机界面原型 | 第 6 章 |
| `fig09_snr_accuracy_academic.svg` | 不同信噪比下各模型识别率对比 | 第 5 章 |
| `fig10_modulation_multiclass_flow.svg` | 水声信号制式识别多分类流程 | 第 2 章 |
| `fig11_deep_learning_structure_summary.svg` / `.pdf` | 深度学习模型结构与作用概述 | 第 2 章 |

## LaTeX 插入示例

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.92\textwidth]{docs/thesis_figures/fig01_research_framework.svg}
  \caption{水声目标识别研究总体技术路线}
  \label{fig:overall-framework}
\end{figure}
```

## Word / WPS 使用建议

1. 推荐使用“插入 -> 图片 -> 此设备”直接插入 SVG 文件，保持矢量清晰度。
2. 图片宽度建议设置为正文宽度的 85%--95%，居中排列；如果图中文字较多，可设为 100% 正文宽度。
3. 图题放在图片下方，不要把图题写进图片内部。示例：`图 3-1 MAT 波形样本预处理流程`。
4. Word 中可设置“环绕文字”为“上下型”或“嵌入型”，避免图片与正文错位。
5. 若学校模板不支持 SVG，可先用浏览器、Inkscape 或 draw.io 打开 SVG，再导出为 300 dpi PNG 后插入。
6. 所有图均为方法介绍类示意图，不依赖具体实验数值；后续若补充真实准确率、SNR 曲线，可另行增加结果图。

## 曲线图标题与坐标轴建议

针对 `fig09_snr_accuracy_academic.svg` 这类实验曲线图，建议采用第一幅示例图的论文格式：

- 图内不放顶部大标题，避免与 Word 题注重复。
- Word 图片下方题注写作：`图 5-x 不同信噪比下各模型识别率对比`。
- 横轴：`信噪比 (dB)`。
- 纵轴：`识别率 (%)`。
- 纵轴刻度使用百分数，例如 `40, 50, ..., 100`，不要使用 `0.4, 0.5, ..., 1.0`。

## 版式参数

- 画布宽度：约 150 mm，贴近 A4 论文正文可用宽度。
- 背景：纯白，适合黑白打印和学校查重系统导出 PDF。
- 字体：优先使用宋体类字体；标题节点加粗。
- 色彩：黑灰线条为主，浅蓝/浅灰仅用于区分模块。
- 图题：不嵌入图片，统一由 Word 的“题注”功能或手动图题完成。

## 重新生成图片

如需统一修改配色、字号或图中文字，可编辑 `generate_figures.py` 后执行：

```bash
python3 docs/thesis_figures/generate_figures.py
```
