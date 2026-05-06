# 论文配图素材：水声信号识别与树莓派部署

本目录提供一组可直接插入本科毕业论文的 SVG 矢量图，主题覆盖数据预处理、STFT 特征、模型结构、跨噪声评估、树莓派部署与 UI 方案。SVG 可直接插入 Word/WPS/LaTeX，也可以用浏览器、Inkscape、draw.io 或在线工具导出为 PNG。

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

1. 直接插入 SVG 文件，保持矢量清晰度。
2. 若学校模板不支持 SVG，可先用浏览器或 Inkscape 导出 300 dpi PNG。
3. 图题建议统一写成“图 3-1 xxx”，正文中用“如图 3-1 所示”引用。
4. 所有图均为方法介绍类示意图，不依赖具体实验数值；后续若补充真实准确率、SNR 曲线，可另行增加结果图。

## 重新生成图片

如需统一修改配色、字号或图中文字，可编辑 `generate_figures.py` 后执行：

```bash
python3 docs/thesis_figures/generate_figures.py
```
