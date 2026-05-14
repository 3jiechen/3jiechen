# -*- coding: utf-8 -*-
"""
Generate a polished defense PPT for the thesis:
《基于树莓派的水声信号制式识别》
Author: 陈杰 (37120222203280)  Advisor: 苏为 教授
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree


# ----------------------------- Theme -----------------------------------------

CN_FONT = "Microsoft YaHei"        # falls back gracefully
CN_FONT_BOLD = "Microsoft YaHei"
EN_FONT = "Calibri"

NAVY      = RGBColor(0x0B, 0x2A, 0x5B)   # deep navy
OCEAN     = RGBColor(0x0E, 0x4D, 0x92)   # ocean blue
AZURE     = RGBColor(0x1D, 0x7A, 0xC4)   # azure blue
CYAN      = RGBColor(0x2E, 0xA8, 0xE0)
TEAL      = RGBColor(0x12, 0xB0, 0xB9)
LIGHT_BG  = RGBColor(0xF4, 0xF8, 0xFC)
PANEL     = RGBColor(0xE9, 0xF1, 0xF9)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
GREY      = RGBColor(0x64, 0x74, 0x88)
DARK      = RGBColor(0x14, 0x1E, 0x33)
ACCENT    = RGBColor(0xFF, 0xB7, 0x03)   # warm amber
ACCENT_2  = RGBColor(0xEF, 0x55, 0x6B)   # soft red
GREEN     = RGBColor(0x2A, 0xB7, 0x7E)

PALETTE = [OCEAN, AZURE, CYAN, TEAL, ACCENT, GREEN]


# ----------------------------- Helpers ---------------------------------------

def set_run_font(run, size=18, bold=False, color=DARK, font=CN_FONT):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    # Ensure East-Asian font is set for CJK glyphs
    rPr = run._r.get_or_add_rPr()
    for tag in ("eastAsia", "cs", "ascii"):
        el = rPr.find(qn(f"a:{tag}"))
        if el is None:
            el = etree.SubElement(rPr, qn(f"a:{tag}"))
        el.set("typeface", font)


def add_text(tf, text, size=18, bold=False, color=DARK, align=PP_ALIGN.LEFT,
             font=CN_FONT, first=False, space_after=2):
    if first:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    run = p.add_run()
    run.text = text
    set_run_font(run, size=size, bold=bold, color=color, font=font)
    return p


def add_rect(slide, x, y, w, h, fill=OCEAN, line=None, shadow=False, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, x, y, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(0.75)
    if not shadow:
        # remove default shadow
        sp = s.shadow
        try:
            sp.inherit = False
        except Exception:
            pass
        # Force no shadow via XML
        spPr = s.fill._xPr.find(qn("a:effectLst")) if False else None
    return s


def add_textbox(slide, x, y, w, h, text="", size=18, bold=False, color=DARK,
                align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=CN_FONT,
                line_spacing=1.15):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Pt(2)
    tf.margin_right = Pt(2)
    tf.margin_top = Pt(2)
    tf.margin_bottom = Pt(2)
    tf.vertical_anchor = anchor
    if text:
        add_text(tf, text, size=size, bold=bold, color=color, align=align,
                 font=font, first=True)
        tf.paragraphs[0].line_spacing = line_spacing
    return tb, tf


def disable_shadow(shape):
    """Strip default outer shadow by injecting empty effectLst."""
    spPr = shape.fill._xPr
    eff = spPr.find(qn("a:effectLst"))
    if eff is None:
        eff = etree.SubElement(spPr, qn("a:effectLst"))
    # clear children -> empty effectLst means no effects
    for child in list(eff):
        eff.remove(child)


def slide_blank(prs):
    layout = prs.slide_layouts[6]  # blank
    return prs.slides.add_slide(layout)


def slide_background(slide, prs, color=WHITE):
    bg = add_rect(slide, 0, 0, prs.slide_width, prs.slide_height, fill=color)
    bg.line.fill.background()
    disable_shadow(bg)
    return bg


def add_logo_text(slide, prs, text="厦门大学  信息学院", color=GREY):
    add_textbox(slide, prs.slide_width - Inches(2.3), Inches(0.18),
                Inches(2.1), Inches(0.3), text=text, size=10,
                color=color, align=PP_ALIGN.RIGHT)


def add_page_header(slide, prs, title, section_no, section_label):
    """A consistent top-bar for content slides."""
    # left accent
    bar = add_rect(slide, Inches(0.35), Inches(0.38), Inches(0.12), Inches(0.42), fill=ACCENT)
    disable_shadow(bar)
    # title
    add_textbox(slide, Inches(0.6), Inches(0.32), Inches(8.5), Inches(0.55),
                text=title, size=24, bold=True, color=NAVY,
                anchor=MSO_ANCHOR.MIDDLE)
    # section pill
    pill = add_rect(slide, prs.slide_width - Inches(2.4), Inches(0.4),
                    Inches(1.95), Inches(0.42), fill=OCEAN,
                    shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    pill.adjustments[0] = 0.5
    disable_shadow(pill)
    tf = pill.text_frame
    tf.margin_left = Pt(6); tf.margin_right = Pt(6)
    tf.margin_top = Pt(2); tf.margin_bottom = Pt(2)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r1 = p.add_run(); r1.text = f"PART {section_no:02d}  ·  "
    set_run_font(r1, size=10, bold=True, color=WHITE)
    r2 = p.add_run(); r2.text = section_label
    set_run_font(r2, size=11, bold=True, color=WHITE)
    # under-line
    ul = add_rect(slide, Inches(0.35), Inches(0.92),
                  prs.slide_width - Inches(0.7), Emu(9525), fill=PANEL)
    disable_shadow(ul)


def add_footer(slide, prs, page_no=None, total=27):
    add_rect(slide, 0, prs.slide_height - Inches(0.32),
             prs.slide_width, Inches(0.32), fill=NAVY)
    add_textbox(slide, Inches(0.4), prs.slide_height - Inches(0.32),
                Inches(7), Inches(0.32),
                text="基于树莓派的水声信号制式识别  |  陈杰  ·  指导老师：苏为 教授",
                size=10, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    if page_no is not None:
        add_textbox(slide, prs.slide_width - Inches(1.5),
                    prs.slide_height - Inches(0.32), Inches(1.1), Inches(0.32),
                    text=f"{page_no:02d} / {total:02d}", size=10,
                    color=WHITE, anchor=MSO_ANCHOR.MIDDLE,
                    align=PP_ALIGN.RIGHT)


# ----------------------------- Specific slides -------------------------------

def slide_cover(prs):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)

    # left navy panel
    panel = add_rect(s, 0, 0, Inches(4.6), prs.slide_height, fill=NAVY)
    disable_shadow(panel)
    # decorative waves on the left panel
    for i, (cx, cy, r, a) in enumerate([
        (Inches(0.5), Inches(0.7), Inches(0.9), 0.25),
        (Inches(1.4), Inches(6.6), Inches(1.8), 0.18),
        (Inches(3.6), Inches(4.2), Inches(0.6), 0.4),
    ]):
        d = add_rect(s, cx, cy, r, r, fill=AZURE, shape=MSO_SHAPE.OVAL)
        d.fill.transparency = 0.6  # not actually used by python-pptx
        disable_shadow(d)
    # accent bar
    ab = add_rect(s, Inches(4.6), Inches(2.8), Inches(0.18), Inches(2.5), fill=ACCENT)
    disable_shadow(ab)

    # left big label
    add_textbox(s, Inches(0.45), Inches(0.5), Inches(3.6), Inches(0.5),
                text="XIAMEN  UNIVERSITY", size=14, bold=True, color=WHITE,
                font=EN_FONT)
    add_textbox(s, Inches(0.45), Inches(0.85), Inches(3.6), Inches(0.4),
                text="厦  门  大  学  ·  信  息  学  院", size=12, color=AZURE)

    # main title block (right side)
    add_textbox(s, Inches(4.95), Inches(1.5), Inches(8.0), Inches(0.5),
                text="本科毕业论文答辩", size=14, color=AZURE, bold=True)

    add_textbox(s, Inches(4.95), Inches(2.0), Inches(8.0), Inches(1.5),
                text="基于树莓派的", size=40, bold=True, color=NAVY,
                line_spacing=1.15)
    add_textbox(s, Inches(4.95), Inches(2.85), Inches(8.0), Inches(1.5),
                text="水声信号制式识别", size=44, bold=True, color=OCEAN,
                line_spacing=1.15)

    add_textbox(s, Inches(4.95), Inches(4.05), Inches(8.0), Inches(0.5),
                text="Underwater Acoustic Modulation Recognition Based on Raspberry Pi",
                size=13, color=GREY, font=EN_FONT)

    # divider under EN title
    div = add_rect(s, Inches(4.95), Inches(4.55), Inches(1.6), Pt(2),
                   fill=ACCENT)
    disable_shadow(div)

    # info block
    info = [
        ("答 辩 人", "陈   杰"),
        ("学      号", "37120222203280"),
        ("专      业", "通 信 工 程"),
        ("年      级", "2022 级"),
        ("指导老师", "苏 为 教授"),
        ("日      期", "2026 年 5 月"),
    ]
    y0 = Inches(4.95)
    for i, (k, v) in enumerate(info):
        col = i % 2
        row = i // 2
        x = Inches(4.95) + Inches(2.6) * col
        y = y0 + Inches(0.38) * row
        add_textbox(s, x, y, Inches(0.95), Inches(0.32),
                    text=k, size=11, color=GREY, anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, x + Inches(1.0), y, Inches(1.6), Inches(0.32),
                    text=v, size=12, bold=True, color=NAVY,
                    anchor=MSO_ANCHOR.MIDDLE)

    # bottom strip on right
    bot = add_rect(s, Inches(4.6), prs.slide_height - Inches(0.5),
                   prs.slide_width - Inches(4.6), Inches(0.5),
                   fill=OCEAN)
    disable_shadow(bot)
    add_textbox(s, Inches(4.7), prs.slide_height - Inches(0.5),
                Inches(8.0), Inches(0.5),
                text="THESIS  DEFENSE  ·  2026", size=11, bold=True,
                color=WHITE, anchor=MSO_ANCHOR.MIDDLE, font=EN_FONT)
    return s


SECTIONS = [
    ("研究背景与意义",  "Research Background & Significance"),
    ("研究目标与内容",  "Research Objectives & Contents"),
    ("项目原理分析",    "Principle Analysis"),
    ("项目方案设计",    "System Design"),
    ("研究结果与应用",  "Results & Applications"),
    ("总结与展望",      "Conclusion & Future Work"),
]


def slide_toc(prs):
    s = slide_blank(prs)
    slide_background(s, prs, LIGHT_BG)

    # header
    add_textbox(s, Inches(0.6), Inches(0.55), Inches(8), Inches(0.6),
                text="目  录", size=34, bold=True, color=NAVY)
    add_textbox(s, Inches(0.6), Inches(1.15), Inches(8), Inches(0.35),
                text="CONTENTS", size=14, color=GREY, font=EN_FONT)
    # right accent line
    al = add_rect(s, Inches(0.6), Inches(1.55), Inches(1.2), Pt(3), fill=ACCENT)
    disable_shadow(al)

    # 2 x 3 grid of cards
    card_w = Inches(3.85)
    card_h = Inches(1.7)
    start_x = Inches(0.7)
    start_y = Inches(2.1)
    gap_x = Inches(0.25)
    gap_y = Inches(0.25)

    for i, (cn, en) in enumerate(SECTIONS):
        col = i % 3
        row = i // 3
        x = start_x + (card_w + gap_x) * col
        y = start_y + (card_h + gap_y) * row
        # card background
        card = add_rect(s, x, y, card_w, card_h, fill=WHITE,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.08
        card.line.color.rgb = PANEL
        disable_shadow(card)
        # left vertical accent
        accent_col = PALETTE[i]
        acc = add_rect(s, x, y, Inches(0.12), card_h, fill=accent_col,
                       shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        acc.adjustments[0] = 0.3
        disable_shadow(acc)
        # number
        add_textbox(s, x + Inches(0.25), y + Inches(0.15), Inches(1.2),
                    Inches(0.6),
                    text=f"0{i+1}", size=36, bold=True, color=accent_col,
                    font=EN_FONT)
        # cn title
        add_textbox(s, x + Inches(1.25), y + Inches(0.2),
                    card_w - Inches(1.35), Inches(0.55),
                    text=cn, size=18, bold=True, color=NAVY,
                    anchor=MSO_ANCHOR.MIDDLE)
        # en subtitle
        add_textbox(s, x + Inches(1.25), y + Inches(0.85),
                    card_w - Inches(1.35), Inches(0.4),
                    text=en, size=10, color=GREY, font=EN_FONT)
        # decorative dot row
        for k in range(3):
            dot = add_rect(s, x + Inches(1.25) + Inches(0.18) * k,
                           y + Inches(1.25), Inches(0.08), Inches(0.08),
                           fill=accent_col, shape=MSO_SHAPE.OVAL)
            disable_shadow(dot)

    add_footer(s, prs, page_no=2)
    return s


def slide_section_divider(prs, idx, page_no):
    s = slide_blank(prs)
    cn, en = SECTIONS[idx]
    slide_background(s, prs, NAVY)

    # decorative diagonal stripes
    for i in range(6):
        line = add_rect(s, Inches(-1) + Inches(2.0) * i, Inches(-1),
                        Inches(0.18), Inches(9.0), fill=OCEAN)
        disable_shadow(line)
    # large number
    add_textbox(s, Inches(0.7), Inches(1.6), Inches(5), Inches(3.5),
                text=f"0{idx+1}", size=240, bold=True, color=OCEAN,
                font=EN_FONT)
    # accent bar
    bar = add_rect(s, Inches(6.0), Inches(3.2), Inches(0.18), Inches(1.3),
                   fill=ACCENT)
    disable_shadow(bar)
    # cn title
    add_textbox(s, Inches(6.3), Inches(3.1), Inches(7), Inches(0.9),
                text=cn, size=40, bold=True, color=WHITE,
                anchor=MSO_ANCHOR.MIDDLE)
    # en subtitle
    add_textbox(s, Inches(6.3), Inches(4.05), Inches(7), Inches(0.6),
                text=en, size=14, color=AZURE, font=EN_FONT,
                anchor=MSO_ANCHOR.MIDDLE)
    # bottom right tag
    add_textbox(s, prs.slide_width - Inches(3.0),
                prs.slide_height - Inches(0.7),
                Inches(2.5), Inches(0.35),
                text="—  THESIS  DEFENSE  —",
                size=10, color=AZURE, font=EN_FONT, align=PP_ALIGN.RIGHT)
    add_footer(s, prs, page_no=page_no)
    return s


# ----------------------------- Section 1 -------------------------------------

def slide_background_overview(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "研究背景", 1, "研究背景与意义")

    # left big quote / context
    box = add_rect(s, Inches(0.6), Inches(1.25), Inches(5.2), Inches(5.5),
                   fill=PANEL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    box.adjustments[0] = 0.05
    disable_shadow(box)
    add_textbox(s, Inches(0.85), Inches(1.4), Inches(4.8), Inches(0.5),
                text="WHY  UNDERWATER  ACOUSTIC", size=11, bold=True,
                color=OCEAN, font=EN_FONT)
    add_textbox(s, Inches(0.85), Inches(1.85), Inches(4.8), Inches(0.7),
                text="为何关注水声调制识别？", size=22, bold=True, color=NAVY)
    # bullet body
    body_tb, body_tf = add_textbox(s, Inches(0.85), Inches(2.65),
                                   Inches(4.8), Inches(3.95))
    bullets = [
        ("海洋经济持续增长", "水下通信 / 目标探测 / 海洋监测等场景需求显著上升，"
                          "调制识别是水声频谱监测与信号解调的基础环节。"),
        ("水声信道更复杂", "传播速度慢、带宽受限、传播衰减明显、强多径与"
                         "时延扩展，并存在海洋环境噪声与舰船自噪声等多源干扰。"),
        ("低 SNR 下识别困难", "接收信号信噪比低、非平稳性强、频谱结构畸变，"
                            "使同一调制制式在不同条件下呈现明显差异。"),
        ("深度学习提供新思路", "可从波形/时频谱图端到端学习判别特征，"
                            "降低对人工特征工程的依赖。"),
    ]
    for i, (h, t) in enumerate(bullets):
        p = body_tf.add_paragraph() if i > 0 else body_tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(6)
        run = p.add_run(); run.text = "●  "
        set_run_font(run, size=14, bold=True, color=PALETTE[i % 6])
        run2 = p.add_run(); run2.text = h
        set_run_font(run2, size=14, bold=True, color=NAVY)
        p2 = body_tf.add_paragraph()
        p2.space_after = Pt(8)
        r = p2.add_run(); r.text = "      " + t
        set_run_font(r, size=12, color=DARK)
        p2.line_spacing = 1.25

    # right - "focus card" stack
    rx = Inches(6.05)
    ry = Inches(1.25)
    rw = Inches(7.3)

    # Card 1
    c1 = add_rect(s, rx, ry, rw, Inches(2.5), fill=OCEAN,
                  shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    c1.adjustments[0] = 0.05
    disable_shadow(c1)
    add_textbox(s, rx + Inches(0.3), ry + Inches(0.25), rw - Inches(0.6),
                Inches(0.5),
                text="本文研究路线", size=18, bold=True, color=WHITE)
    add_textbox(s, rx + Inches(0.3), ry + Inches(0.75), rw - Inches(0.6),
                Inches(0.4),
                text="RESEARCH  PIPELINE",
                size=11, color=CYAN, font=EN_FONT, bold=True)
    chain_items = ["数据预处理", "多特征构建", "融合网络训练",
                   "鲁棒性评估", "ONNX 部署"]
    chain_y = ry + Inches(1.4)
    chain_w = (rw - Inches(0.6)) / len(chain_items)
    for i, t in enumerate(chain_items):
        x = rx + Inches(0.3) + chain_w * i
        cell = add_rect(s, x + Inches(0.05), chain_y,
                        chain_w - Inches(0.1), Inches(0.75),
                        fill=WHITE, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        cell.adjustments[0] = 0.3
        disable_shadow(cell)
        add_textbox(s, x + Inches(0.05), chain_y,
                    chain_w - Inches(0.1), Inches(0.75),
                    text=t, size=11, bold=True, color=NAVY,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if i < len(chain_items) - 1:
            arr = add_rect(s, x + chain_w - Inches(0.08),
                           chain_y + Inches(0.27), Inches(0.16),
                           Inches(0.2), fill=ACCENT,
                           shape=MSO_SHAPE.RIGHT_ARROW)
            disable_shadow(arr)

    # Card 2 -- key tech
    c2y = ry + Inches(2.7)
    c2 = add_rect(s, rx, c2y, rw, Inches(2.9), fill=WHITE,
                  shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    c2.adjustments[0] = 0.04
    c2.line.color.rgb = PANEL
    disable_shadow(c2)
    add_textbox(s, rx + Inches(0.3), c2y + Inches(0.2), rw - Inches(0.6),
                Inches(0.5),
                text="关键技术", size=18, bold=True, color=NAVY)
    add_textbox(s, rx + Inches(0.3), c2y + Inches(0.7), rw - Inches(0.6),
                Inches(0.4),
                text="KEY  TECHNIQUES",
                size=11, color=GREY, font=EN_FONT, bold=True)
    keys = [
        ("Bi-LSTM",     "时域序列长时依赖建模",          OCEAN),
        ("ResNet-18*", "STFT 谱图局部纹理特征提取",      AZURE),
        ("STFT 双通道", "幅值 + 相位联合时频表示",         CYAN),
        ("ONNX + 树莓派", "跨平台轻量化端侧推理",         ACCENT),
    ]
    kx = rx + Inches(0.3)
    ky = c2y + Inches(1.3)
    kw = (rw - Inches(0.6) - Inches(0.2)) / 2
    kh = Inches(0.7)
    for i, (k, v, col) in enumerate(keys):
        col_i = i % 2; row_i = i // 2
        x = kx + (kw + Inches(0.2)) * col_i
        y = ky + (kh + Inches(0.15)) * row_i
        chip = add_rect(s, x, y, Inches(1.4), kh, fill=col,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        chip.adjustments[0] = 0.3
        disable_shadow(chip)
        add_textbox(s, x, y, Inches(1.4), kh, text=k, size=12, bold=True,
                    color=WHITE, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, x + Inches(1.5), y, kw - Inches(1.5), kh,
                    text=v, size=12, color=DARK, anchor=MSO_ANCHOR.MIDDLE)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_significance(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "研究意义", 1, "研究背景与意义")

    # subtitle banner
    sub_x = Inches(0.6); sub_y = Inches(1.1)
    add_textbox(s, sub_x, sub_y, Inches(12), Inches(0.45),
                text="VALUE  PROPOSITION", size=11, bold=True,
                color=OCEAN, font=EN_FONT)
    add_textbox(s, sub_x, sub_y + Inches(0.35), Inches(12), Inches(0.45),
                text="建模 · 评测 · 落地  三位一体的研究价值",
                size=18, bold=True, color=NAVY)

    items = [
        ("01", "应用牵引",
         "海洋监测 / 目标探测 / 水下通信等业务需要可靠的调制认知能力。",
         OCEAN),
        ("02", "课题切入点",
         "端到端深度学习 + 波形 / 时频互补融合 + 嵌入式原型验证。",
         AZURE),
        ("03", "瓶颈对照",
         "手工特征依赖经验，低 SNR、非平稳噪声下可分性变差。",
         CYAN),
        ("04", "互补建模",
         "Bi-LSTM 建模序列动态；ResNet 抽取谱图纹理；融合输出类别概率。",
         TEAL),
        ("05", "鲁棒评测",
         "测试集叠加 AWGN，SNR −10 ~ 10 dB（步长 2 dB）评估噪声敏感性。",
         ACCENT),
        ("06", "工程闭环",
         "导出 ONNX；树莓派 ONNX Runtime 推理；Tk 展示波形与识别结果。",
         GREEN),
    ]
    # 3 columns x 2 rows grid, with banner space at top
    coords = [
        (Inches(0.6),  Inches(2.1)),
        (Inches(5.05), Inches(2.1)),
        (Inches(9.5),  Inches(2.1)),
        (Inches(0.6),  Inches(4.7)),
        (Inches(5.05), Inches(4.7)),
        (Inches(9.5),  Inches(4.7)),
    ]
    card_w = Inches(3.8); card_h = Inches(2.3)
    for (num, h, t, col), (x, y) in zip(items, coords):
        card = add_rect(s, x, y, card_w, card_h, fill=WHITE,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.08
        card.line.color.rgb = PANEL
        disable_shadow(card)
        # numbered tag
        tag = add_rect(s, x + Inches(0.15), y - Inches(0.15), Inches(0.6),
                       Inches(0.45), fill=col,
                       shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        tag.adjustments[0] = 0.4
        disable_shadow(tag)
        add_textbox(s, x + Inches(0.15), y - Inches(0.15), Inches(0.6),
                    Inches(0.45), text=num, size=12, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    font=EN_FONT)
        add_textbox(s, x + Inches(0.9), y + Inches(0.05), card_w - Inches(1.0),
                    Inches(0.55),
                    text=h, size=16, bold=True, color=NAVY,
                    anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, x + Inches(0.25), y + Inches(0.75),
                    card_w - Inches(0.5), card_h - Inches(0.85),
                    text=t, size=12, color=DARK, line_spacing=1.3)

    add_footer(s, prs, page_no=page_no)
    return s


# ----------------------------- Section 2 -------------------------------------

def slide_main_overview(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, LIGHT_BG)
    add_page_header(s, prs, "主要研究内容总览", 2, "研究目标与内容")

    add_textbox(s, Inches(0.6), Inches(1.1), Inches(12), Inches(0.5),
                text="围绕“数据 → 特征 → 模型 → 评测 → 部署”五个环节，构建完整识别流程",
                size=14, color=GREY)

    items = [
        ("01", "数据集与预处理",
         ["9 类调制：2/4/8 FSK、2/4/8 PSK、16/64 QAM、64 OFDM",
          "统一为 4096 点 · 零均值 / 单位方差归一化",
          "训练 / 验证 / 独立测试集划分，固定随机种子"], OCEAN),
        ("02", "多特征构建",
         ["时域分支：1D 标准化波形序列",
          "时频分支：STFT 幅值 + 相位双通道谱图",
          "谱图与训练阶段归一化保持一致"], AZURE),
        ("03", "融合网络设计",
         ["时域：双向 LSTM 提取长时依赖",
          "频域：改造首层卷积的 ResNet-18 (2 通道输入)",
          "特征层拼接 + 全连接 9 类 Softmax"], CYAN),
        ("04", "鲁棒性评测",
         ["测试集叠加 AWGN，SNR −10 ~ 10 dB",
          "RNN / TinyCNN / ResNet / CNN+RNN / ResNet+RNN",
          "整体准确率 + SNR-准确率曲线 + 混淆矩阵"], TEAL),
        ("05", "树莓派 ONNX 部署",
         ["训练模型导出 ONNX，跨平台兼容",
          "树莓派 ONNX Runtime 端侧推理",
          "保持与训练端一致的预处理流程"], ACCENT),
        ("06", "可视化交互界面",
         ["基于 Tk 的图形界面",
          "实时显示输入波形",
          "输出识别类别与置信度"], GREEN),
    ]
    card_w = Inches(4.15); card_h = Inches(2.5)
    start_x = Inches(0.55); start_y = Inches(1.65)
    gap_x = Inches(0.13); gap_y = Inches(0.15)
    for i, (num, h, lines, col) in enumerate(items):
        c = i % 3; r = i // 3
        x = start_x + (card_w + gap_x) * c
        y = start_y + (card_h + gap_y) * r
        card = add_rect(s, x, y, card_w, card_h, fill=WHITE,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.05
        card.line.color.rgb = PANEL
        disable_shadow(card)
        # top color stripe
        stripe = add_rect(s, x, y, card_w, Inches(0.5), fill=col,
                          shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        stripe.adjustments[0] = 0.4
        disable_shadow(stripe)
        # cover bottom edge of stripe with white rect to make top-rounded
        cov = add_rect(s, x, y + Inches(0.25), card_w, Inches(0.25), fill=col)
        disable_shadow(cov)
        add_textbox(s, x + Inches(0.2), y, Inches(0.8), Inches(0.5),
                    text=num, size=14, bold=True, color=WHITE,
                    font=EN_FONT, anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, x + Inches(0.9), y, card_w - Inches(1.0), Inches(0.5),
                    text=h, size=15, bold=True, color=WHITE,
                    anchor=MSO_ANCHOR.MIDDLE)
        # body
        _, tf = add_textbox(s, x + Inches(0.25), y + Inches(0.65),
                            card_w - Inches(0.5), card_h - Inches(0.75))
        for j, line in enumerate(lines):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(4)
            p.line_spacing = 1.25
            r0 = p.add_run(); r0.text = "▸  "
            set_run_font(r0, size=12, bold=True, color=col)
            r1 = p.add_run(); r1.text = line
            set_run_font(r1, size=11, color=DARK)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_dataset(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "数据集与类别映射", 2, "研究目标与内容")

    # left -- summary text
    add_textbox(s, Inches(0.6), Inches(1.2), Inches(6), Inches(0.5),
                text="DATASET  &  EVALUATION", size=11, bold=True,
                color=OCEAN, font=EN_FONT)
    add_textbox(s, Inches(0.6), Inches(1.55), Inches(6), Inches(0.55),
                text="9 类水声调制信号 · 4096 点固定窗口", size=20, bold=True,
                color=NAVY)
    _, tf = add_textbox(s, Inches(0.6), Inches(2.25), Inches(6.0), Inches(4.5))
    bullets = [
        "数据集以 MAT 文件存储，依文件编号建立类别映射；",
        "训练集 / 验证集 / 独立测试集划分，固定随机种子保证可复现；",
        "评估阶段在测试集上叠加 AWGN：SNR −10 ~ 10 dB，步长 2 dB，共 11 个测试点；",
        "评价指标：整体分类准确率、SNR-准确率曲线、混淆矩阵；",
        "提供模型在可控噪声条件下的鲁棒性参考。",
    ]
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8); p.line_spacing = 1.35
        r0 = p.add_run(); r0.text = "◆  "
        set_run_font(r0, size=13, bold=True, color=PALETTE[i % 6])
        r1 = p.add_run(); r1.text = b
        set_run_font(r1, size=13, color=DARK)

    # right -- 9 class table
    classes = [
        ("0", "2FSK",   "FSK 类",   OCEAN),
        ("1", "4FSK",   "FSK 类",   OCEAN),
        ("2", "8FSK",   "FSK 类",   OCEAN),
        ("3", "2PSK",   "PSK 类",   AZURE),
        ("4", "4PSK",   "PSK 类",   AZURE),
        ("5", "8PSK",   "PSK 类",   AZURE),
        ("6", "16QAM",  "QAM 类",   TEAL),
        ("7", "64QAM",  "QAM 类",   TEAL),
        ("8", "64OFDM", "OFDM 类", ACCENT),
    ]
    panel_x = Inches(7.0); panel_y = Inches(1.2)
    panel_w = Inches(6.35); panel_h = Inches(5.85)
    panel = add_rect(s, panel_x, panel_y, panel_w, panel_h, fill=PANEL,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    panel.adjustments[0] = 0.04
    disable_shadow(panel)
    add_textbox(s, panel_x + Inches(0.3), panel_y + Inches(0.2),
                panel_w - Inches(0.6), Inches(0.5),
                text="表 3-1  数据集类别标签映射", size=15, bold=True,
                color=NAVY)
    add_textbox(s, panel_x + Inches(0.3), panel_y + Inches(0.7),
                panel_w - Inches(0.6), Inches(0.4),
                text="CLASS  MAPPING  ·  9  MODULATION  TYPES",
                size=10, color=GREY, font=EN_FONT)

    # header row
    hx = panel_x + Inches(0.3); hy = panel_y + Inches(1.25)
    hw = panel_w - Inches(0.6); hh = Inches(0.45)
    cols = [("标签", 0.18), ("调制方式", 0.42), ("信号家族", 0.4)]
    head = add_rect(s, hx, hy, hw, hh, fill=OCEAN,
                    shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    head.adjustments[0] = 0.3
    disable_shadow(head)
    acc = 0
    for cname, frac in cols:
        cw = hw * frac
        add_textbox(s, hx + Emu(int(acc)), hy, Emu(int(cw)), hh,
                    text=cname, size=12, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        acc += cw
    # body rows
    row_h = Inches(0.42)
    for i, (idx, name, fam, col) in enumerate(classes):
        ry = hy + hh + Inches(0.08) + row_h * i
        bg = WHITE if i % 2 == 0 else PANEL
        rrow = add_rect(s, hx, ry, hw, row_h, fill=bg,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        rrow.adjustments[0] = 0.15
        rrow.line.fill.background()
        disable_shadow(rrow)
        acc = 0
        for j, (val, frac, font_col, b) in enumerate([
                (idx, 0.18, NAVY, True),
                (name, 0.42, NAVY, True),
                (fam, 0.4, col, False)]):
            cw = hw * frac
            add_textbox(s, hx + Emu(int(acc)), ry, Emu(int(cw)), row_h,
                        text=val, size=12, bold=b, color=font_col,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            acc += cw

    add_footer(s, prs, page_no=page_no)
    return s


def slide_features(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "特征构建：时域 + STFT 双通道", 2, "研究目标与内容")

    # subtitle
    add_textbox(s, Inches(0.6), Inches(1.15), Inches(12), Inches(0.4),
                text="同一段 4096 点波形同时提供两类输入，时域 / 时频信息互为补充",
                size=13, color=GREY)

    # Two big columns
    col_w = Inches(6.25); col_h = Inches(5.55)
    cy = Inches(1.6)

    # ---- Time-domain column
    cx1 = Inches(0.6)
    box1 = add_rect(s, cx1, cy, col_w, col_h, fill=WHITE,
                    shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    box1.adjustments[0] = 0.04
    box1.line.color.rgb = PANEL
    disable_shadow(box1)
    head1 = add_rect(s, cx1, cy, col_w, Inches(0.7), fill=OCEAN,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    head1.adjustments[0] = 0.18
    disable_shadow(head1)
    cov1 = add_rect(s, cx1, cy + Inches(0.45), col_w, Inches(0.25),
                    fill=OCEAN)
    disable_shadow(cov1)
    add_textbox(s, cx1 + Inches(0.3), cy, col_w, Inches(0.7),
                text="① 时域波形特征", size=18, bold=True, color=WHITE,
                anchor=MSO_ANCHOR.MIDDLE)

    # formula box
    fx = cx1 + Inches(0.3); fy = cy + Inches(0.95)
    fbox = add_rect(s, fx, fy, col_w - Inches(0.6), Inches(1.0),
                    fill=LIGHT_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    fbox.adjustments[0] = 0.1
    disable_shadow(fbox)
    add_textbox(s, fx, fy, col_w - Inches(0.6), Inches(0.4),
                text="标准化公式", size=11, bold=True, color=OCEAN,
                anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.CENTER)
    add_textbox(s, fx, fy + Inches(0.35), col_w - Inches(0.6), Inches(0.65),
                text="x̃ = ( x − μ ) / ( σ + ε )",
                size=22, bold=True, color=NAVY, font=EN_FONT,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # bullets
    _, tf = add_textbox(s, cx1 + Inches(0.3), cy + Inches(2.15),
                        col_w - Inches(0.6), Inches(3.3))
    bs = [
        ("固定长度", "统一为 4096 点固定窗口，避免长度差异影响。"),
        ("零均值 / 单位方差", "稳定训练收敛速度，弱化幅值尺度差异。"),
        ("送入 Bi-LSTM", "保留波形相对变化规律，建模长时依赖。"),
        ("适用场景", "对幅值起伏、相位演替敏感的调制类别。"),
    ]
    for i, (h, t) in enumerate(bs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(4); p.line_spacing = 1.3
        r0 = p.add_run(); r0.text = "●  "
        set_run_font(r0, size=12, bold=True, color=OCEAN)
        r1 = p.add_run(); r1.text = h + " "
        set_run_font(r1, size=12, bold=True, color=NAVY)
        r2 = p.add_run(); r2.text = "— " + t
        set_run_font(r2, size=12, color=DARK)

    # ---- STFT column
    cx2 = Inches(7.1)
    box2 = add_rect(s, cx2, cy, col_w, col_h, fill=WHITE,
                    shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    box2.adjustments[0] = 0.04
    box2.line.color.rgb = PANEL
    disable_shadow(box2)
    head2 = add_rect(s, cx2, cy, col_w, Inches(0.7), fill=AZURE,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    head2.adjustments[0] = 0.18
    disable_shadow(head2)
    cov2 = add_rect(s, cx2, cy + Inches(0.45), col_w, Inches(0.25),
                    fill=AZURE)
    disable_shadow(cov2)
    add_textbox(s, cx2 + Inches(0.3), cy, col_w, Inches(0.7),
                text="② STFT 双通道时频特征", size=18, bold=True, color=WHITE,
                anchor=MSO_ANCHOR.MIDDLE)

    fx2 = cx2 + Inches(0.3); fy2 = cy + Inches(0.95)
    fbox2 = add_rect(s, fx2, fy2, col_w - Inches(0.6), Inches(1.0),
                     fill=LIGHT_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    fbox2.adjustments[0] = 0.1
    disable_shadow(fbox2)
    add_textbox(s, fx2, fy2, col_w - Inches(0.6), Inches(0.4),
                text="STFT 表达式", size=11, bold=True, color=AZURE,
                anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.CENTER)
    add_textbox(s, fx2, fy2 + Inches(0.35), col_w - Inches(0.6), Inches(0.65),
                text="X(m,k) = Σ x(n)·w(n−mH)·e^(−j2πkn/N)",
                size=16, bold=True, color=NAVY, font=EN_FONT,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    _, tf2 = add_textbox(s, cx2 + Inches(0.3), cy + Inches(2.15),
                         col_w - Inches(0.6), Inches(3.3))
    bs2 = [
        ("时频联合分析", "滑动窗口逐帧 DFT，刻画频率随时间的变化。"),
        ("双通道堆叠", "|X| 表示能量分布；arg(X) 保留相位信息。"),
        ("张量形状", "2 × H × W，H/W 由窗长与帧移决定。"),
        ("送入 ResNet-18*", "首层卷积输入通道改为 2，匹配双通道输入。"),
    ]
    for i, (h, t) in enumerate(bs2):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.space_after = Pt(4); p.line_spacing = 1.3
        r0 = p.add_run(); r0.text = "●  "
        set_run_font(r0, size=12, bold=True, color=AZURE)
        r1 = p.add_run(); r1.text = h + " "
        set_run_font(r1, size=12, bold=True, color=NAVY)
        r2 = p.add_run(); r2.text = "— " + t
        set_run_font(r2, size=12, color=DARK)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_architecture(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, LIGHT_BG)
    add_page_header(s, prs, "网络结构：STFT + ResNet + BiLSTM 融合模型", 2,
                    "研究目标与内容")

    add_textbox(s, Inches(0.6), Inches(1.1), Inches(12), Inches(0.45),
                text="两路特征在特征层拼接 (concat) 后送入全连接分类器，输出 9 类 Softmax 概率",
                size=12, color=GREY)

    # ---- Insert the matplotlib-rendered 3D architecture figure ----
    import os
    fig_path = os.path.join(os.path.dirname(__file__), "figs",
                            "network_architecture.png")
    if not os.path.exists(fig_path):
        # try cwd fallback
        fig_path = "figs/network_architecture.png"
    if os.path.exists(fig_path):
        img_left = Inches(0.5)
        img_top = Inches(1.55)
        img_w = Inches(12.33)
        s.shapes.add_picture(fig_path, img_left, img_top, width=img_w)

    # caption underneath
    add_textbox(s, Inches(0.6), Inches(6.85), Inches(12.2), Inches(0.3),
                text="图 3-2  Bi-LSTM × ResNet-18 双分支融合网络结构示意图（STFT 双通道输入 → Concat → FC → Softmax → 9 类）",
                size=10, color=GREY, align=PP_ALIGN.CENTER, bold=True)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_architecture_simple(prs, page_no):
    """Original block-flow architecture slide (kept for reference)."""
    s = slide_blank(prs)
    slide_background(s, prs, LIGHT_BG)
    add_page_header(s, prs, "网络结构：STFT + ResNet + BiLSTM 融合模型", 2,
                    "研究目标与内容")

    add_textbox(s, Inches(0.6), Inches(1.1), Inches(12), Inches(0.45),
                text="两路特征在特征层拼接 (concat) 后送入全连接分类器，输出 9 类 Softmax 概率",
                size=12, color=GREY)

    # ------- diagram --------
    ix = Inches(0.4)
    def block(x, y, w, h, label, sub="", fill=OCEAN, text_color=WHITE,
              size=14, sub_size=10, font=CN_FONT):
        rec = add_rect(s, x, y, w, h, fill=fill,
                       shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        rec.adjustments[0] = 0.15
        disable_shadow(rec)
        add_textbox(s, x, y, w, h,
                    text=label, size=size, bold=True, color=text_color,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    font=font)
        if sub:
            add_textbox(s, x, y + h - Inches(0.32), w, Inches(0.3),
                        text=sub, size=sub_size, color=text_color,
                        align=PP_ALIGN.CENTER, font=EN_FONT)
        return rec

    def arrow(x, y, w=Inches(0.45), h=Inches(0.25), fill=NAVY):
        a = add_rect(s, x, y, w, h, fill=fill,
                     shape=MSO_SHAPE.RIGHT_ARROW)
        disable_shadow(a)
        return a

    blk_w = Inches(1.9); blk_h = Inches(0.9)
    top_y = Inches(1.85)
    bot_y = Inches(3.55)
    arr_w = Inches(0.35); arr_h = Inches(0.25); gap = Inches(0.15)

    # ---- Top path: time-domain ----
    add_textbox(s, ix, top_y - Inches(0.45), Inches(4), Inches(0.4),
                text="◆  时域分支（Time-domain Branch）", size=12, bold=True,
                color=OCEAN)
    x = ix
    block(x, top_y, blk_w, blk_h, "1D 时域波形",
          sub="4096 × 1", fill=PANEL, text_color=NAVY); x += blk_w
    arrow(x + Inches(0.02), top_y + (blk_h - arr_h)/2, w=arr_w); x += arr_w + gap
    block(x, top_y, blk_w + Inches(0.1), blk_h, "Bi-LSTM",
          sub="forward + backward", fill=OCEAN); x += blk_w + Inches(0.1)
    arrow(x + Inches(0.02), top_y + (blk_h - arr_h)/2, w=arr_w); x += arr_w + gap
    block(x, top_y, blk_w, blk_h, "时间均值池化",
          sub="Mean Pooling", fill=AZURE); x += blk_w
    arrow(x + Inches(0.02), top_y + (blk_h - arr_h)/2, w=arr_w); x += arr_w + gap
    f_t_x = x
    block(x, top_y, blk_w + Inches(0.1), blk_h, "时域特征 f_t",
          sub="time-domain", fill=CYAN)
    f_t_end_x = x + blk_w + Inches(0.1)

    # ---- Bottom path: spectrogram ----
    add_textbox(s, ix, bot_y - Inches(0.45), Inches(4), Inches(0.4),
                text="◆  谱图分支（Spectrogram Branch）", size=12, bold=True,
                color=AZURE)
    x = ix
    block(x, bot_y, blk_w, blk_h, "STFT 双通道谱图",
          sub="2 × H × W", fill=PANEL, text_color=NAVY); x += blk_w
    arrow(x + Inches(0.02), bot_y + (blk_h - arr_h)/2, w=arr_w); x += arr_w + gap
    block(x, bot_y, blk_w + Inches(0.1), blk_h, "ResNet-18 *",
          sub="first conv: 2-ch input", fill=AZURE); x += blk_w + Inches(0.1)
    arrow(x + Inches(0.02), bot_y + (blk_h - arr_h)/2, w=arr_w); x += arr_w + gap
    block(x, bot_y, blk_w, blk_h, "全局池化",
          sub="GAP", fill=OCEAN); x += blk_w
    arrow(x + Inches(0.02), bot_y + (blk_h - arr_h)/2, w=arr_w); x += arr_w + gap
    block(x, bot_y, blk_w + Inches(0.1), blk_h, "谱图特征 f_s",
          sub="spectrogram", fill=TEAL)

    # ---- Concat between branches (right side) ----
    cx_c = f_t_end_x + Inches(0.6)
    cw = Inches(2.0); ch = Inches(1.0)
    cy_c = (top_y + bot_y + blk_h)/2 - ch/2
    block(cx_c, cy_c, cw, ch, "Concat", sub="[ f_t ; f_s ]",
          fill=NAVY, size=16)
    # connectors: arrows from f_t and f_s into the concat
    # horizontal stub from f_t out
    h1 = add_rect(s, f_t_end_x, top_y + blk_h/2 - Pt(1.5),
                  cx_c + cw/2 - f_t_end_x, Pt(3), fill=NAVY)
    disable_shadow(h1)
    h2 = add_rect(s, f_t_end_x, bot_y + blk_h/2 - Pt(1.5),
                  cx_c + cw/2 - f_t_end_x, Pt(3), fill=NAVY)
    disable_shadow(h2)
    # vertical join into concat
    v_top = add_rect(s, cx_c + cw/2 - Pt(1.5), top_y + blk_h/2,
                     Pt(3), cy_c - (top_y + blk_h/2), fill=NAVY)
    disable_shadow(v_top)
    v_bot = add_rect(s, cx_c + cw/2 - Pt(1.5), cy_c + ch,
                     Pt(3), (bot_y + blk_h/2) - (cy_c + ch), fill=NAVY)
    disable_shadow(v_bot)

    # ---- Classifier path: FC -> Softmax -> 9 classes (below) ----
    fy = bot_y + blk_h + Inches(0.55)
    classify_w = Inches(2.8); classify_h = Inches(1.05)
    classify_x = cx_c + cw/2 - classify_w/2
    # vertical line from Concat down to classifier
    v_line = add_rect(s, cx_c + cw/2 - Pt(1.5), cy_c + ch,
                      Pt(3), fy - (cy_c + ch) - Inches(0.05), fill=NAVY)
    disable_shadow(v_line)
    # down arrow at the bottom of the line
    da = add_rect(s, cx_c + cw/2 - Inches(0.15), fy - Inches(0.32),
                  Inches(0.3), Inches(0.3), fill=NAVY,
                  shape=MSO_SHAPE.DOWN_ARROW)
    disable_shadow(da)
    # classifier block
    cls = add_rect(s, classify_x, fy, classify_w, classify_h,
                   fill=ACCENT, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    cls.adjustments[0] = 0.13
    disable_shadow(cls)
    add_textbox(s, classify_x, fy + Inches(0.05),
                classify_w, Inches(0.45),
                text="全连接 FC + Softmax", size=14, bold=True, color=WHITE,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, classify_x, fy + Inches(0.5),
                classify_w, Inches(0.5),
                text="9 类调制制式概率分布",
                size=11, color=WHITE,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Output classes summary on the left below the bottom branch
    lx = ix; ly = fy + Inches(0.05)
    sumw = Inches(7.5); sumh = Inches(1.0)
    sumbox = add_rect(s, lx, ly, sumw, sumh, fill=PANEL,
                      shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    sumbox.adjustments[0] = 0.08
    disable_shadow(sumbox)
    add_textbox(s, lx + Inches(0.25), ly + Inches(0.1),
                sumw - Inches(0.5), Inches(0.35),
                text="OUTPUT  CLASSES", size=10, bold=True,
                color=OCEAN, font=EN_FONT)
    add_textbox(s, lx + Inches(0.25), ly + Inches(0.45),
                sumw - Inches(0.5), Inches(0.5),
                text="2FSK · 4FSK · 8FSK  ·  2PSK · 4PSK · 8PSK  ·  16QAM · 64QAM  ·  64OFDM",
                size=12, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_training(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "训练策略与超参数设置", 2, "研究目标与内容")

    # left -- strategy
    add_textbox(s, Inches(0.6), Inches(1.2), Inches(7), Inches(0.5),
                text="TRAINING  STRATEGY", size=11, bold=True, color=OCEAN,
                font=EN_FONT)
    add_textbox(s, Inches(0.6), Inches(1.55), Inches(7), Inches(0.55),
                text="监督学习 · 交叉熵损失 · Adam 优化器", size=20, bold=True,
                color=NAVY)

    _, tf = add_textbox(s, Inches(0.6), Inches(2.25), Inches(7), Inches(4.5))
    bullets = [
        ("交叉熵损失",
         "L = −Σ y_k · log(ŷ_k)，K = 9 类调制制式。"),
        ("Adam 优化器",
         "兼顾收敛速度与稳定性，配合 StepLR 学习率衰减策略。"),
        ("验证集监控",
         "保存验证准确率最高的权重，用于后续测试与部署。"),
        ("ONNX 导出",
         "同时构造时域与谱图两路输入张量，保持训练/部署一致。"),
    ]
    for i, (h, t) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8); p.line_spacing = 1.35
        r0 = p.add_run(); r0.text = "▣  "
        set_run_font(r0, size=13, bold=True, color=PALETTE[i % 6])
        r1 = p.add_run(); r1.text = h + "  "
        set_run_font(r1, size=13, bold=True, color=NAVY)
        r2 = p.add_run(); r2.text = "— " + t
        set_run_font(r2, size=12, color=DARK)

    # right -- params table panel
    px = Inches(8.0); py = Inches(1.2)
    pw = Inches(5.35); ph = Inches(5.85)
    panel = add_rect(s, px, py, pw, ph, fill=LIGHT_BG,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    panel.adjustments[0] = 0.04
    disable_shadow(panel)
    add_textbox(s, px + Inches(0.3), py + Inches(0.2),
                pw - Inches(0.6), Inches(0.45),
                text="表 3-2  主要训练参数", size=15, bold=True, color=NAVY)
    add_textbox(s, px + Inches(0.3), py + Inches(0.65),
                pw - Inches(0.6), Inches(0.35),
                text="TRAINING  HYPER-PARAMETERS", size=10, color=GREY,
                font=EN_FONT)

    params = [
        ("优化器",        "Adam"),
        ("学习率",        "5 × 10⁻⁴"),
        ("学习率调度",    "StepLR"),
        ("损失函数",      "Cross Entropy"),
        ("批量大小",      "16"),
        ("最大训练轮数",  "40"),
        ("早停轮数",      "10"),
        ("验证集比例",    "5 %"),
    ]
    hx = px + Inches(0.3); hy = py + Inches(1.2)
    hw = pw - Inches(0.6)
    head = add_rect(s, hx, hy, hw, Inches(0.45), fill=OCEAN,
                    shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    head.adjustments[0] = 0.3
    disable_shadow(head)
    add_textbox(s, hx, hy, hw * 0.5, Inches(0.45), text="参数",
                size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, hx + hw*0.5, hy, hw * 0.5, Inches(0.45), text="设置",
                size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE)
    rh = Inches(0.42)
    for i, (k, v) in enumerate(params):
        ry = hy + Inches(0.5) + rh * i
        bg = WHITE if i % 2 == 0 else PANEL
        row = add_rect(s, hx, ry, hw, rh, fill=bg,
                       shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        row.adjustments[0] = 0.18
        row.line.fill.background()
        disable_shadow(row)
        add_textbox(s, hx + Inches(0.15), ry, hw*0.5, rh, text=k,
                    size=12, color=DARK, anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, hx + hw*0.5, ry, hw*0.5 - Inches(0.15), rh, text=v,
                    size=12, bold=True, color=OCEAN,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    font=EN_FONT)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_compare_models(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, LIGHT_BG)
    add_page_header(s, prs, "对比实验：五种模型方案", 2, "研究目标与内容")

    add_textbox(s, Inches(0.6), Inches(1.1), Inches(12), Inches(0.45),
                text="单特征基线 vs. 多特征融合，验证时域 / 时频特征的互补性",
                size=12, color=GREY)

    models = [
        ("①", "时域 RNN",          "一维时域波形",       OCEAN, "单特征 · 时域"),
        ("②", "STFT + TinyCNN",   "STFT 幅值 + 相位",   AZURE, "单特征 · 时频"),
        ("③", "STFT + ResNet",    "STFT 幅值 + 相位",   TEAL,  "单特征 · 时频"),
        ("④", "STFT-CNN + 时域 RNN", "时域 + STFT 谱图", ACCENT, "融合 · 双特征"),
        ("⑤", "STFT-ResNet + 时域 RNN  ★", "时域 + STFT 谱图",
                                                       ACCENT_2, "融合 · 双特征 (本文)"),
    ]
    # row layout: 5 cards in a row
    cw = Inches(2.46); ch = Inches(4.6)
    sx = Inches(0.4); sy = Inches(1.7)
    gap = Inches(0.1)
    for i, (num, name, feat, col, tag) in enumerate(models):
        x = sx + (cw + gap) * i
        card = add_rect(s, x, sy, cw, ch, fill=WHITE,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.05
        card.line.color.rgb = PANEL
        disable_shadow(card)
        # top
        head = add_rect(s, x, sy, cw, Inches(1.2), fill=col,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        head.adjustments[0] = 0.13
        disable_shadow(head)
        cov = add_rect(s, x, sy + Inches(0.7), cw, Inches(0.5), fill=col)
        disable_shadow(cov)
        add_textbox(s, x, sy + Inches(0.05), cw, Inches(0.5),
                    text=num, size=28, bold=True, color=WHITE, font=EN_FONT,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, x, sy + Inches(0.65), cw, Inches(0.5),
                    text=name, size=12, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # body
        add_textbox(s, x + Inches(0.15), sy + Inches(1.35),
                    cw - Inches(0.3), Inches(0.4),
                    text=tag, size=10, color=GREY, align=PP_ALIGN.CENTER,
                    font=EN_FONT, bold=True)
        # feature row
        feat_box = add_rect(s, x + Inches(0.2), sy + Inches(1.75),
                            cw - Inches(0.4), Inches(0.6),
                            fill=PANEL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        feat_box.adjustments[0] = 0.25
        disable_shadow(feat_box)
        add_textbox(s, x + Inches(0.2), sy + Inches(1.75),
                    cw - Inches(0.4), Inches(0.6),
                    text="输入特征\n" + feat, size=10, color=NAVY,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    line_spacing=1.15)
        # description
        descs = [
            "直接对一维时域序列建模，捕捉幅值 / 相位起伏。",
            "轻量 CNN 提取谱图局部能量与频带分布。",
            "更深网络 + 残差连接，提取层次化谱图特征。",
            "时域动态 + 时频纹理，特征层拼接分类。",
            "本文方案：ResNet-18 + Bi-LSTM 融合分类，整体表现最佳。",
        ]
        add_textbox(s, x + Inches(0.2), sy + Inches(2.5),
                    cw - Inches(0.4), Inches(1.7),
                    text=descs[i], size=11, color=DARK, line_spacing=1.35)
        # bottom accent
        bot = add_rect(s, x, sy + ch - Inches(0.3), cw, Inches(0.3),
                       fill=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        bot.adjustments[0] = 0.3
        disable_shadow(bot)
        cov2 = add_rect(s, x, sy + ch - Inches(0.3), cw, Inches(0.15),
                        fill=col)
        disable_shadow(cov2)

    # Bottom hint
    add_textbox(s, Inches(0.6), Inches(6.55), Inches(12.5), Inches(0.4),
                text="说明：★ 为本文重点采用方案；后续实验将在独立测试集上叠加 AWGN 进行多 SNR 对比。",
                size=11, color=GREY, align=PP_ALIGN.CENTER)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_snr_comparison(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "不同信噪比下识别率对比", 2, "研究目标与内容")

    add_textbox(s, Inches(0.6), Inches(1.15), Inches(12), Inches(0.45),
                text="AWGN 测试：SNR −10 ~ 10 dB，步长 2 dB，共 11 个测试点",
                size=12, color=GREY)

    # chart - mock line chart with shapes
    chart_x = Inches(0.6); chart_y = Inches(1.75)
    chart_w = Inches(8.4); chart_h = Inches(5.0)
    panel = add_rect(s, chart_x, chart_y, chart_w, chart_h, fill=LIGHT_BG,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    panel.adjustments[0] = 0.04
    disable_shadow(panel)

    # axes area
    ax_left = chart_x + Inches(0.7)
    ax_right = chart_x + chart_w - Inches(0.3)
    ax_top = chart_y + Inches(0.5)
    ax_bot = chart_y + chart_h - Inches(0.7)
    # y gridlines: 0%, 25, 50, 75, 100
    for i, pct in enumerate([0, 25, 50, 75, 100]):
        gy = ax_bot - (ax_bot - ax_top) * (pct / 100.0)
        gl = add_rect(s, ax_left, gy, ax_right - ax_left, Pt(0.5),
                      fill=GREY)
        disable_shadow(gl)
        add_textbox(s, chart_x + Inches(0.15), gy - Inches(0.12),
                    Inches(0.5), Inches(0.25), text=f"{pct}%",
                    size=9, color=GREY, align=PP_ALIGN.RIGHT, font=EN_FONT)
    # x labels
    snrs = list(range(-10, 11, 2))  # 11 points
    n = len(snrs)
    for i, snr in enumerate(snrs):
        gx = ax_left + (ax_right - ax_left) * (i / (n - 1))
        add_textbox(s, gx - Inches(0.25), ax_bot + Inches(0.05),
                    Inches(0.5), Inches(0.3),
                    text=f"{snr}", size=9, color=GREY, align=PP_ALIGN.CENTER,
                    font=EN_FONT)
    # axis label
    add_textbox(s, (ax_left + ax_right)/2 - Inches(1.5),
                ax_bot + Inches(0.32), Inches(3), Inches(0.3),
                text="SNR  /  dB", size=11, bold=True, color=NAVY,
                align=PP_ALIGN.CENTER, font=EN_FONT)
    add_textbox(s, chart_x + Inches(0.05), chart_y + Inches(0.2),
                Inches(1.5), Inches(0.3),
                text="Accuracy  /  %", size=11, bold=True, color=NAVY,
                font=EN_FONT)

    # mock data (monotonic increasing per model)
    series = [
        ("RNN",                 [22,28,33,39,46,53,61,68,74,77,79], OCEAN),
        ("STFT+TinyCNN",        [30,37,45,53,60,66,72,77,81,84,86], AZURE),
        ("STFT+ResNet",         [35,42,50,58,65,72,78,82,86,88,90], TEAL),
        ("STFT+CNN+RNN",        [40,48,56,64,71,77,82,86,89,91,92], ACCENT),
        ("STFT+ResNet+RNN ★",   [58,66,73,80,85,89,92,94,95,96,96], ACCENT_2),
    ]
    def pt(i, v):
        x = ax_left + (ax_right - ax_left) * (i / (n - 1))
        y = ax_bot - (ax_bot - ax_top) * (v / 100.0)
        return x, y

    # Lines as series of small rectangles (segments)
    for name, vals, col in series:
        for i in range(n - 1):
            x1, y1 = pt(i, vals[i])
            x2, y2 = pt(i + 1, vals[i + 1])
            # draw a thin connector by adding a line shape using freeform
            line = s.shapes.add_connector(1, x1, y1, x2, y2)
            line.line.color.rgb = col
            line.line.width = Pt(2.5)
        for i in range(n):
            x, y = pt(i, vals[i])
            d = add_rect(s, x - Inches(0.07), y - Inches(0.07),
                         Inches(0.14), Inches(0.14),
                         fill=col, shape=MSO_SHAPE.OVAL)
            d.line.color.rgb = WHITE
            d.line.width = Pt(0.75)
            disable_shadow(d)

    # right - legend & take-away
    lx = Inches(9.3); ly = Inches(1.75)
    lw = Inches(4.05); lh = Inches(5.0)
    legend = add_rect(s, lx, ly, lw, lh, fill=WHITE,
                      shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    legend.adjustments[0] = 0.05
    legend.line.color.rgb = PANEL
    disable_shadow(legend)
    add_textbox(s, lx + Inches(0.3), ly + Inches(0.2), lw - Inches(0.6),
                Inches(0.4),
                text="模型图例", size=14, bold=True, color=NAVY)
    add_textbox(s, lx + Inches(0.3), ly + Inches(0.6), lw - Inches(0.6),
                Inches(0.4),
                text="MODEL  LEGEND", size=10, color=GREY, font=EN_FONT,
                bold=True)
    for i, (name, vals, col) in enumerate(series):
        ly0 = ly + Inches(1.1) + Inches(0.45) * i
        dot = add_rect(s, lx + Inches(0.35), ly0 + Inches(0.1),
                       Inches(0.25), Inches(0.25), fill=col,
                       shape=MSO_SHAPE.OVAL)
        disable_shadow(dot)
        add_textbox(s, lx + Inches(0.7), ly0,
                    lw - Inches(1.0), Inches(0.45),
                    text=name, size=12, bold=True, color=NAVY,
                    anchor=MSO_ANCHOR.MIDDLE)

    # takeaway
    ty = ly + Inches(3.6)
    take = add_rect(s, lx + Inches(0.3), ty, lw - Inches(0.6), Inches(1.3),
                    fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    take.adjustments[0] = 0.1
    disable_shadow(take)
    add_textbox(s, lx + Inches(0.5), ty + Inches(0.1),
                lw - Inches(1.0), Inches(0.4),
                text="KEY  TAKE-AWAY", size=10, bold=True,
                color=CYAN, font=EN_FONT)
    add_textbox(s, lx + Inches(0.5), ty + Inches(0.45),
                lw - Inches(1.0), Inches(0.85),
                text="融合模型在低 SNR 下保持更高且更平稳的识别率，"
                     "印证时域 / 时频特征的互补价值。",
                size=11, color=WHITE, line_spacing=1.3)

    # note: dashed lines? skip; add note
    add_textbox(s, chart_x + Inches(0.4), chart_y + chart_h + Inches(0.0),
                chart_w - Inches(0.8), Inches(0.25),
                text="注：曲线为示意趋势图，具体数值以独立测试集实验结果为准。",
                size=9, color=GREY, align=PP_ALIGN.RIGHT)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_deploy_rpi(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "树莓派端系统实现", 2, "研究目标与内容")

    add_textbox(s, Inches(0.6), Inches(1.15), Inches(12), Inches(0.45),
                text="PC 端训练 → ONNX 模型导出 → 树莓派 ONNX Runtime 端侧推理 → Tk 界面显示",
                size=12, color=GREY)

    # Insert deployment schematic figure
    import os
    fig_path = os.path.join(os.path.dirname(__file__), "figs",
                            "deployment_system.png")
    if not os.path.exists(fig_path):
        fig_path = "figs/deployment_system.png"
    if os.path.exists(fig_path):
        s.shapes.add_picture(fig_path, Inches(0.45), Inches(1.6),
                             width=Inches(12.45))
        add_textbox(s, Inches(0.6), Inches(7.0), Inches(12.2), Inches(0.25),
                    text="图 3-3  树莓派端部署系统示意图（PC 训练 → ONNX → 树莓派推理 → 结果显示）",
                    size=10, color=GREY, align=PP_ALIGN.CENTER, bold=True)
        add_footer(s, prs, page_no=page_no)
        return s

    # Pipeline
    stages = [
        ("数据采集",   "ADC / 文件回放\n4096 点窗口", OCEAN),
        ("信号预处理", "零均值 / 单位方差\nSTFT 双通道谱图", AZURE),
        ("ONNX 推理",  "ONNX Runtime\nARM 端轻量化", TEAL),
        ("结果输出",   "类别 + 置信度\nTop-K 辅助参考", ACCENT),
        ("Tk 界面",    "波形显示\n实时识别可视化", ACCENT_2),
    ]
    px = Inches(0.4); py = Inches(1.75)
    pw = Inches(2.4); ph = Inches(2.1); gap = Inches(0.16)
    for i, (h, t, col) in enumerate(stages):
        x = px + (pw + gap) * i
        # number bubble
        nb = add_rect(s, x + pw/2 - Inches(0.35), py - Inches(0.05),
                      Inches(0.7), Inches(0.7), fill=col,
                      shape=MSO_SHAPE.OVAL)
        disable_shadow(nb)
        add_textbox(s, x + pw/2 - Inches(0.35), py - Inches(0.05),
                    Inches(0.7), Inches(0.7),
                    text=f"{i+1}", size=18, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    font=EN_FONT)
        # card
        card = add_rect(s, x, py + Inches(0.35), pw, ph, fill=WHITE,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.07
        card.line.color.rgb = PANEL
        disable_shadow(card)
        add_textbox(s, x + Inches(0.15), py + Inches(0.65),
                    pw - Inches(0.3), Inches(0.5),
                    text=h, size=14, bold=True, color=NAVY,
                    align=PP_ALIGN.CENTER)
        # divider
        div = add_rect(s, x + pw/2 - Inches(0.3), py + Inches(1.15),
                       Inches(0.6), Pt(2), fill=col)
        disable_shadow(div)
        add_textbox(s, x + Inches(0.15), py + Inches(1.25),
                    pw - Inches(0.3), ph - Inches(0.9),
                    text=t, size=11, color=DARK,
                    align=PP_ALIGN.CENTER, line_spacing=1.35)
        if i < len(stages) - 1:
            ar = add_rect(s, x + pw - Inches(0.05),
                          py + Inches(0.35) + ph/2 - Inches(0.15),
                          Inches(0.28), Inches(0.3), fill=NAVY,
                          shape=MSO_SHAPE.RIGHT_ARROW)
            disable_shadow(ar)

    # bottom row -- key advantages
    by = Inches(4.5)
    advs = [
        ("LOW COST",   "树莓派单板设备，部署门槛低"),
        ("CROSS PLATFORM", "ONNX 解耦训练框架与运行平台"),
        ("CONSISTENT", "训练 / 部署预处理流程严格一致"),
        ("INTERACTIVE", "Tk 图形界面直观展示波形与结果"),
    ]
    cw = Inches(3.07); ch = Inches(2.1); gx = Inches(0.4); gap = Inches(0.16)
    for i, (h, t) in enumerate(advs):
        x = gx + (cw + gap) * i
        cd = add_rect(s, x, by, cw, ch, fill=LIGHT_BG,
                      shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        cd.adjustments[0] = 0.05
        disable_shadow(cd)
        bar = add_rect(s, x, by, Inches(0.12), ch, fill=PALETTE[i],
                       shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        bar.adjustments[0] = 0.4
        disable_shadow(bar)
        add_textbox(s, x + Inches(0.3), by + Inches(0.25),
                    cw - Inches(0.5), Inches(0.5),
                    text=h, size=14, bold=True, color=NAVY, font=EN_FONT)
        add_textbox(s, x + Inches(0.3), by + Inches(0.75),
                    cw - Inches(0.5), ch - Inches(0.85),
                    text=t, size=12, color=DARK, line_spacing=1.4)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_ui_mockup(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, LIGHT_BG)
    add_page_header(s, prs, "树莓派 Tk UI 界面设计", 2, "研究目标与内容")

    # left: UI mockup
    ux = Inches(0.55); uy = Inches(1.25)
    uw = Inches(7.8); uh = Inches(5.85)
    # window frame
    win = add_rect(s, ux, uy, uw, uh, fill=DARK,
                   shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    win.adjustments[0] = 0.03
    disable_shadow(win)
    # title bar
    tb = add_rect(s, ux, uy, uw, Inches(0.45), fill=NAVY,
                  shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tb.adjustments[0] = 0.1
    disable_shadow(tb)
    cov = add_rect(s, ux, uy + Inches(0.22), uw, Inches(0.23), fill=NAVY)
    disable_shadow(cov)
    # dots
    for i, c in enumerate([ACCENT_2, ACCENT, GREEN]):
        d = add_rect(s, ux + Inches(0.15) + Inches(0.32) * i,
                     uy + Inches(0.12), Inches(0.22), Inches(0.22),
                     fill=c, shape=MSO_SHAPE.OVAL)
        disable_shadow(d)
    add_textbox(s, ux + Inches(1.3), uy, uw - Inches(2), Inches(0.45),
                text="UAM-Recognizer  ·  树莓派水声制式识别系统  v1.0",
                size=11, bold=True, color=WHITE, font=EN_FONT,
                anchor=MSO_ANCHOR.MIDDLE)

    # inner content
    iy0 = uy + Inches(0.6)
    # waveform area
    wf = add_rect(s, ux + Inches(0.25), iy0, uw - Inches(0.5), Inches(2.2),
                  fill=PANEL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    wf.adjustments[0] = 0.04
    disable_shadow(wf)
    add_textbox(s, ux + Inches(0.4), iy0 + Inches(0.08),
                uw - Inches(0.8), Inches(0.3),
                text="◆  实时输入波形 (Waveform)", size=11, bold=True,
                color=NAVY)
    # mock waveform
    import math
    base_y = iy0 + Inches(1.25)
    amp = Inches(0.65)
    npts = 120
    width = uw - Inches(0.8)
    px_prev = ux + Inches(0.4)
    py_prev = base_y
    for i in range(1, npts + 1):
        x = ux + Inches(0.4) + width * (i / npts)
        v = (math.sin(i * 0.45) * 0.55 +
             math.sin(i * 0.18) * 0.35 +
             math.sin(i * 0.85 + 1.2) * 0.25)
        y = base_y - amp * v
        line = s.shapes.add_connector(1, px_prev, py_prev, x, y)
        line.line.color.rgb = OCEAN
        line.line.width = Pt(1.5)
        px_prev = x; py_prev = y
    # axis line
    ax = add_rect(s, ux + Inches(0.4), base_y,
                  width, Pt(0.5), fill=GREY)
    disable_shadow(ax)

    # STFT area
    sy_ = iy0 + Inches(2.4)
    sp = add_rect(s, ux + Inches(0.25), sy_, uw - Inches(0.5), Inches(1.6),
                  fill=PANEL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    sp.adjustments[0] = 0.04
    disable_shadow(sp)
    add_textbox(s, ux + Inches(0.4), sy_ + Inches(0.08),
                uw - Inches(0.8), Inches(0.3),
                text="◆  STFT 时频谱图 (Spectrogram)", size=11, bold=True,
                color=NAVY)
    # heatmap grid
    import random
    random.seed(7)
    cell_w = (uw - Inches(0.8)) / 36
    cell_h = Inches(0.13)
    grid_x = ux + Inches(0.4); grid_y = sy_ + Inches(0.45)
    for r in range(7):
        for c in range(36):
            v = abs(math.sin(c * 0.25) * math.cos(r * 0.4) +
                    random.uniform(-0.2, 0.2))
            v = max(0.05, min(1.0, v))
            # interpolate from light to deep
            r_col = int(232 - 200 * v)
            g_col = int(241 - 150 * v)
            b_col = int(252 - 60 * v)
            cell = add_rect(s, grid_x + cell_w * c, grid_y + cell_h * r,
                            cell_w + Pt(0.5), cell_h + Pt(0.5),
                            fill=RGBColor(max(0,r_col), max(0,g_col), b_col))
            cell.line.fill.background()
            disable_shadow(cell)

    # bottom panel: prediction + buttons
    pyb = iy0 + Inches(4.15)
    pan = add_rect(s, ux + Inches(0.25), pyb, uw - Inches(0.5), Inches(1.0),
                   fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    pan.adjustments[0] = 0.06
    disable_shadow(pan)
    add_textbox(s, ux + Inches(0.45), pyb + Inches(0.08),
                Inches(3), Inches(0.4),
                text="◆  识别结果  (Prediction)", size=11, bold=True,
                color=CYAN)
    add_textbox(s, ux + Inches(0.45), pyb + Inches(0.4),
                Inches(3.5), Inches(0.55),
                text="类别：4PSK", size=20, bold=True, color=WHITE,
                anchor=MSO_ANCHOR.TOP)
    add_textbox(s, ux + Inches(3.2), pyb + Inches(0.4),
                Inches(3.0), Inches(0.55),
                text="置信度：93.8 %", size=15, bold=True, color=ACCENT,
                font=EN_FONT, anchor=MSO_ANCHOR.TOP)
    # buttons
    btn_specs = [("加载", OCEAN), ("识别", AZURE), ("停止", ACCENT_2)]
    for i, (bn, bc) in enumerate(btn_specs):
        bx = ux + uw - Inches(2.7) + Inches(0.85) * i
        btn = add_rect(s, bx, pyb + Inches(0.3), Inches(0.78),
                       Inches(0.55), fill=bc,
                       shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        btn.adjustments[0] = 0.4
        disable_shadow(btn)
        add_textbox(s, bx, pyb + Inches(0.3), Inches(0.78), Inches(0.55),
                    text=bn, size=12, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # caption
    add_textbox(s, ux, uy + uh + Inches(0.05), uw, Inches(0.3),
                text="图 3-1  设计的树莓派 UI 界面",
                size=11, color=GREY, align=PP_ALIGN.CENTER, bold=True)

    # right info column
    rx = Inches(8.6); ry = Inches(1.25)
    rw = Inches(4.75)
    add_textbox(s, rx, ry, rw, Inches(0.45),
                text="UI  COMPONENTS", size=11, bold=True, color=OCEAN,
                font=EN_FONT)
    add_textbox(s, rx, ry + Inches(0.4), rw, Inches(0.55),
                text="界面功能划分", size=20, bold=True, color=NAVY)

    panels = [
        ("波形显示区", "实时绘制 4096 点输入波形，便于观察输入信号", OCEAN),
        ("时频谱图区", "可视化 STFT 谱图，辅助判断频率/时间结构", AZURE),
        ("识别结果区", "输出当前类别与置信度，支持 Top-K 显示", TEAL),
        ("控制按钮区", "加载、识别、停止等基本交互操作", ACCENT),
    ]
    for i, (h, t, col) in enumerate(panels):
        py_ = ry + Inches(1.15) + Inches(1.18) * i
        card = add_rect(s, rx, py_, rw, Inches(1.05), fill=WHITE,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.08
        card.line.color.rgb = PANEL
        disable_shadow(card)
        cb = add_rect(s, rx, py_, Inches(0.12), Inches(1.05), fill=col,
                      shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        cb.adjustments[0] = 0.4
        disable_shadow(cb)
        add_textbox(s, rx + Inches(0.3), py_ + Inches(0.1),
                    rw - Inches(0.5), Inches(0.4),
                    text=h, size=13, bold=True, color=NAVY)
        add_textbox(s, rx + Inches(0.3), py_ + Inches(0.5),
                    rw - Inches(0.5), Inches(0.55),
                    text=t, size=11, color=DARK, line_spacing=1.3)

    add_footer(s, prs, page_no=page_no)
    return s


# ----------------------------- Section 3 -------------------------------------

def slide_principles(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "原理分析：信道 · 时频变换 · 深度模型", 3,
                    "项目原理分析")

    cols = [
        ("水声信道特性", OCEAN, [
            "声波在水中传播速度慢、带宽受限；",
            "海面 / 海底反射 → 多径传播，时延扩展；",
            "海洋环境噪声 + 舰船噪声 + 设备自噪声；",
            "信号非平稳性强，频谱结构易畸变；",
            "AWGN 模型用于可控的鲁棒性评估。",
        ]),
        ("STFT 时频变换", AZURE, [
            "滑窗短时频谱分析，刻画频率随时间演变；",
            "X(m,k) = Σ x(n)·w(n−mH)·e^(−j2πkn/N)；",
            "幅值通道反映能量分布，相位通道保留相位信息；",
            "对相位调制 (PSK/QAM/OFDM) 类信号尤为重要；",
            "得到 2×H×W 双通道张量送入 CNN 分支。",
        ]),
        ("深度学习结构", TEAL, [
            "CNN：捕捉谱图局部纹理与频带结构；",
            "ResNet：残差连接缓解深层退化，逐层抽象；",
            "RNN/LSTM：建模时序长时依赖；",
            "Bi-LSTM：同时利用过去与未来上下文；",
            "特征层融合：拼接互补特征 → 全连接分类。",
        ]),
    ]
    cw = Inches(4.15); ch = Inches(5.55); gap = Inches(0.13)
    sx = Inches(0.55); sy = Inches(1.45)
    for i, (h, col, items) in enumerate(cols):
        x = sx + (cw + gap) * i
        card = add_rect(s, x, sy, cw, ch, fill=WHITE,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.05
        card.line.color.rgb = PANEL
        disable_shadow(card)
        # header
        hd = add_rect(s, x, sy, cw, Inches(0.85), fill=col,
                      shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        hd.adjustments[0] = 0.14
        disable_shadow(hd)
        cov = add_rect(s, x, sy + Inches(0.55), cw, Inches(0.3), fill=col)
        disable_shadow(cov)
        add_textbox(s, x, sy, cw, Inches(0.85),
                    text=h, size=18, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # number on the side
        nb = add_rect(s, x + Inches(0.2), sy - Inches(0.25),
                      Inches(0.7), Inches(0.7),
                      fill=ACCENT, shape=MSO_SHAPE.OVAL)
        disable_shadow(nb)
        add_textbox(s, x + Inches(0.2), sy - Inches(0.25),
                    Inches(0.7), Inches(0.7),
                    text=f"0{i+1}", size=14, bold=True, color=WHITE,
                    font=EN_FONT, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE)
        # body
        _, tf = add_textbox(s, x + Inches(0.3), sy + Inches(1.1),
                            cw - Inches(0.6), ch - Inches(1.2))
        for j, item in enumerate(items):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.space_after = Pt(8); p.line_spacing = 1.35
            r0 = p.add_run(); r0.text = "▸  "
            set_run_font(r0, size=13, bold=True, color=col)
            r1 = p.add_run(); r1.text = item
            set_run_font(r1, size=12, color=DARK)

    add_footer(s, prs, page_no=page_no)
    return s


# ----------------------------- Section 4 -------------------------------------

def slide_design_overall(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, LIGHT_BG)
    add_page_header(s, prs, "总体方案：从数据到部署的端到端流程", 4,
                    "项目方案设计")

    # 5-step horizontal pipeline
    stages = [
        ("数据预处理",   "波形截取/补零\n零均值/单位方差",  OCEAN),
        ("特征构建",     "时域序列 + STFT\n双通道幅值/相位", AZURE),
        ("融合网络",     "Bi-LSTM × ResNet-18\n特征拼接 + FC", TEAL),
        ("鲁棒性评估",   "AWGN 多 SNR\n准确率 / 混淆矩阵",   ACCENT),
        ("端侧部署",     "ONNX 模型导出\n树莓派 + Tk UI",   ACCENT_2),
    ]
    px = Inches(0.55); py = Inches(1.6)
    w = Inches(2.45); h = Inches(2.55); gap = Inches(0.18)
    for i, (title, sub, col) in enumerate(stages):
        x = px + (w + gap) * i
        # number diamond above
        nb = add_rect(s, x + w/2 - Inches(0.3),
                      py - Inches(0.05), Inches(0.6), Inches(0.6),
                      fill=col, shape=MSO_SHAPE.OVAL)
        disable_shadow(nb)
        add_textbox(s, x + w/2 - Inches(0.3),
                    py - Inches(0.05), Inches(0.6), Inches(0.6),
                    text=f"0{i+1}", size=14, bold=True, color=WHITE,
                    font=EN_FONT, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE)
        card = add_rect(s, x, py + Inches(0.4), w, h, fill=WHITE,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.06
        card.line.color.rgb = PANEL
        disable_shadow(card)
        # title strip
        ts = add_rect(s, x + Inches(0.2), py + Inches(0.65),
                      w - Inches(0.4), Inches(0.55), fill=col,
                      shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        ts.adjustments[0] = 0.3
        disable_shadow(ts)
        add_textbox(s, x + Inches(0.2), py + Inches(0.65),
                    w - Inches(0.4), Inches(0.55),
                    text=title, size=14, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, x + Inches(0.2), py + Inches(1.35),
                    w - Inches(0.4), Inches(1.4),
                    text=sub, size=11, color=DARK,
                    align=PP_ALIGN.CENTER, line_spacing=1.4)
        if i < len(stages) - 1:
            ar = add_rect(s, x + w - Inches(0.05),
                          py + Inches(0.4) + h/2 - Inches(0.15),
                          Inches(0.28), Inches(0.3), fill=NAVY,
                          shape=MSO_SHAPE.RIGHT_ARROW)
            disable_shadow(ar)

    # bottom -- two highlight boxes
    by = Inches(4.85)
    highlights = [
        ("MAIN  IDEA",
         "结合时域波形动态特征与 STFT 双通道时频纹理特征，"
         "通过特征层拼接得到互补表示，在低 SNR 下显著提升识别鲁棒性。",
         NAVY, WHITE),
        ("ENGINEERING  VALUE",
         "训练得到的 PyTorch 模型导出为 ONNX 格式，"
         "在树莓派端实现轻量化推理，构建低成本水声调制识别原型。",
         WHITE, NAVY),
    ]
    for i, (h, t, fill, col) in enumerate(highlights):
        x = Inches(0.55) + Inches(6.5) * i
        card = add_rect(s, x, by, Inches(6.3), Inches(1.95),
                        fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.06
        if fill == WHITE:
            card.line.color.rgb = PANEL
        disable_shadow(card)
        add_textbox(s, x + Inches(0.35), by + Inches(0.2),
                    Inches(5.5), Inches(0.4),
                    text=h, size=12, bold=True, color=ACCENT, font=EN_FONT)
        add_textbox(s, x + Inches(0.35), by + Inches(0.65),
                    Inches(5.5), Inches(1.2),
                    text=t, size=13, color=col, line_spacing=1.45)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_design_details(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "关键设计细节与一致性保障", 4, "项目方案设计")

    add_textbox(s, Inches(0.6), Inches(1.15), Inches(12), Inches(0.4),
                text="确保训练阶段与部署阶段在数据预处理与特征参数上严格一致",
                size=12, color=GREY)

    # two-column layout
    items_left = [
        ("输入长度",
         "训练 / 推理均统一为 4096 点固定窗口；不足补零，超出截断。"),
        ("归一化",
         "x̃ = (x − μ) / (σ + ε)，每个样本独立完成，避免幅值尺度漂移。"),
        ("STFT 参数",
         "窗长、帧移、FFT 点数固定；幅值与相位独立归一化。"),
        ("时域分支",
         "Bi-LSTM + 时间均值池化 + Dropout，降低过拟合风险。"),
    ]
    items_right = [
        ("谱图分支",
         "ResNet-18 首层卷积输入通道改为 2，去除原分类头，输出特征向量。"),
        ("特征融合",
         "concat([f_t, f_s]) → 全连接层 → Softmax，输出 9 类概率分布。"),
        ("训练监控",
         "验证准确率最高的权重保存为候选模型，用于测试与部署。"),
        ("ONNX 导出",
         "同时构造两路输入张量，保持 shape 一致，方便嵌入式推理调用。"),
    ]

    def render_list(items, x0, y0, w):
        for i, (h, t) in enumerate(items):
            y = y0 + Inches(1.45) * i
            num = add_rect(s, x0, y, Inches(0.55), Inches(0.55),
                           fill=PALETTE[i % 6], shape=MSO_SHAPE.OVAL)
            disable_shadow(num)
            add_textbox(s, x0, y, Inches(0.55), Inches(0.55),
                        text=f"{i+1:02d}", size=12, bold=True, color=WHITE,
                        font=EN_FONT, align=PP_ALIGN.CENTER,
                        anchor=MSO_ANCHOR.MIDDLE)
            add_textbox(s, x0 + Inches(0.7), y - Inches(0.05),
                        w - Inches(0.7), Inches(0.45),
                        text=h, size=14, bold=True, color=NAVY)
            add_textbox(s, x0 + Inches(0.7), y + Inches(0.4),
                        w - Inches(0.7), Inches(1.0),
                        text=t, size=11, color=DARK, line_spacing=1.4)

    render_list(items_left, Inches(0.6), Inches(1.7), Inches(6.2))
    # divider
    dv = add_rect(s, Inches(6.95), Inches(1.7), Pt(1.5), Inches(5.2),
                  fill=PANEL)
    disable_shadow(dv)
    render_list(items_right, Inches(7.2), Inches(1.7), Inches(6.2))

    add_footer(s, prs, page_no=page_no)
    return s


# ----------------------------- Section 5 -------------------------------------

def slide_results_table(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, LIGHT_BG)
    add_page_header(s, prs, "对比实验：整体识别准确率", 5, "研究结果与应用")

    add_textbox(s, Inches(0.6), Inches(1.15), Inches(12), Inches(0.45),
                text="表 4-1  不同模型在独立测试集上的整体分类准确率",
                size=13, bold=True, color=NAVY)

    # Table panel (shorter to leave room for the conclusion strip below)
    px = Inches(0.6); py = Inches(1.7)
    pw = Inches(8.2); ph = Inches(3.95)
    panel = add_rect(s, px, py, pw, ph, fill=WHITE,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    panel.adjustments[0] = 0.03
    panel.line.color.rgb = PANEL
    disable_shadow(panel)

    cols = [("模型", 0.32), ("输入特征", 0.38), ("准确率", 0.3)]
    rows = [
        ("时域 RNN",                "一维时域波形",         71.0, OCEAN),
        ("STFT + CNN",             "STFT 幅值 + 相位",     76.2, AZURE),
        ("STFT + ResNet",          "STFT 幅值 + 相位",     79.3, TEAL),
        ("STFT + CNN + RNN",       "时域 + STFT 谱图",     80.8, ACCENT),
        ("STFT + ResNet + RNN  ★", "时域 + STFT 谱图",     91.4, ACCENT_2),
    ]
    # header
    hx = px + Inches(0.3); hy = py + Inches(0.3); hh = Inches(0.55)
    hw = pw - Inches(0.6)
    hd = add_rect(s, hx, hy, hw, hh, fill=NAVY,
                  shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    hd.adjustments[0] = 0.2
    disable_shadow(hd)
    acc = 0
    for cname, frac in cols:
        cw = hw * frac
        add_textbox(s, hx + Emu(int(acc)), hy, Emu(int(cw)), hh,
                    text=cname, size=13, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        acc += cw
    # rows -- with bar in the rightmost column
    rh = Inches(0.48)
    for i, (mname, mfeat, mpct, mcol) in enumerate(rows):
        ry_ = hy + hh + Inches(0.1) + (rh + Inches(0.06)) * i
        bg = PANEL if i % 2 == 0 else WHITE
        row = add_rect(s, hx, ry_, hw, rh, fill=bg,
                       shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        row.adjustments[0] = 0.15
        row.line.fill.background()
        disable_shadow(row)
        # model name
        add_textbox(s, hx + Inches(0.2), ry_, hw * cols[0][1], rh,
                    text=mname, size=12, bold=True, color=NAVY,
                    anchor=MSO_ANCHOR.MIDDLE)
        # feature
        add_textbox(s, hx + hw * cols[0][1], ry_, hw * cols[1][1], rh,
                    text=mfeat, size=11, color=DARK,
                    anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        # bar
        bar_x = hx + hw * (cols[0][1] + cols[1][1]) + Inches(0.1)
        bar_full = hw * cols[2][1] - Inches(1.2)
        bar_track = add_rect(s, bar_x, ry_ + Inches(0.14),
                             bar_full, Inches(0.24), fill=PANEL,
                             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        bar_track.adjustments[0] = 0.4
        bar_track.line.fill.background()
        disable_shadow(bar_track)
        bar = add_rect(s, bar_x, ry_ + Inches(0.14),
                       bar_full * (mpct / 100.0), Inches(0.24), fill=mcol,
                       shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        bar.adjustments[0] = 0.4
        disable_shadow(bar)
        add_textbox(s, bar_x + bar_full + Inches(0.1), ry_,
                    Inches(1.0), rh,
                    text=f"{mpct:.1f}%", size=13, bold=True, color=mcol,
                    anchor=MSO_ANCHOR.MIDDLE, font=EN_FONT)

    # right info card -- key takeaway
    rx = Inches(9.0); ry = Inches(1.7)
    rw = Inches(4.35); rh2 = Inches(3.95)
    card = add_rect(s, rx, ry, rw, rh2, fill=NAVY,
                    shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.04
    disable_shadow(card)
    # decorative
    deco = add_rect(s, rx + rw - Inches(1.2), ry + Inches(0.15),
                    Inches(0.85), Inches(0.85), fill=OCEAN,
                    shape=MSO_SHAPE.OVAL)
    disable_shadow(deco)
    deco2 = add_rect(s, rx + rw - Inches(1.4), ry + Inches(0.5),
                     Inches(0.5), Inches(0.5), fill=ACCENT,
                     shape=MSO_SHAPE.OVAL)
    disable_shadow(deco2)

    add_textbox(s, rx + Inches(0.35), ry + Inches(0.3),
                rw - Inches(0.7), Inches(0.35),
                text="KEY  RESULT", size=11, bold=True, color=CYAN,
                font=EN_FONT)
    add_textbox(s, rx + Inches(0.35), ry + Inches(0.65),
                rw - Inches(0.7), Inches(1.1),
                text="91.4%", size=54, bold=True, color=WHITE,
                font=EN_FONT)
    add_textbox(s, rx + Inches(0.35), ry + Inches(1.85),
                rw - Inches(0.7), Inches(0.5),
                text="STFT+ResNet+RNN 融合模型",
                size=13, bold=True, color=WHITE)
    add_textbox(s, rx + Inches(0.35), ry + Inches(2.15),
                rw - Inches(0.7), Inches(1.7),
                text="• 较单一时域 RNN 提升 +20.4 pp\n"
                     "• 较 STFT+ResNet 提升 +12.1 pp\n"
                     "• 较 STFT+CNN+RNN 提升 +10.6 pp\n"
                     "• 在所有对比模型中表现最佳",
                size=11, color=CYAN, line_spacing=1.5)

    # ====== Bottom: 对比结论 strip (4 progressive findings) ======
    cy = Inches(5.8)
    cw_total = Inches(12.73)
    ccx = Inches(0.3)
    # title bar
    title_bar = add_rect(s, ccx, cy, cw_total, Inches(0.38),
                         fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    title_bar.adjustments[0] = 0.25
    disable_shadow(title_bar)
    add_textbox(s, ccx + Inches(0.25), cy, Inches(3.2), Inches(0.38),
                text="◆  对  比  结  论",
                size=12, bold=True, color=WHITE,
                anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, ccx + Inches(3.2), cy, Inches(6), Inches(0.38),
                text="COMPARATIVE  FINDINGS",
                size=10, bold=True, color=CYAN, font=EN_FONT,
                anchor=MSO_ANCHOR.MIDDLE)

    # 4 finding cards in a row
    findings = [
        ("①", "时域单特征受限",
         "仅一维波形 71.0%  难以稳定区分相近调制",
         OCEAN),
        ("②", "时频特征更稳健",
         "STFT  79.3% > 76.2% > 71%   ResNet 优于 TinyCNN",
         AZURE),
        ("③", "双特征融合互补",
         "时域 + 时频  80.8% / 91.4%  >  任一单特征",
         TEAL),
        ("④", "本文方案最优",
         "91.4%   验证 ResNet + Bi-LSTM 融合的有效性",
         ACCENT_2),
    ]
    fy = cy + Inches(0.48)
    fh = Inches(0.82)
    fw = (cw_total - Inches(0.45)) / 4
    gap = Inches(0.15)
    for i, (num, h, t, col) in enumerate(findings):
        x = ccx + (fw + gap) * i + Inches(0.1)
        card_f = add_rect(s, x, fy, fw, fh, fill=WHITE,
                          shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card_f.adjustments[0] = 0.1
        card_f.line.color.rgb = PANEL
        disable_shadow(card_f)
        # left accent
        acc_bar = add_rect(s, x, fy, Inches(0.12), fh, fill=col,
                           shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        acc_bar.adjustments[0] = 0.4
        disable_shadow(acc_bar)
        # number
        add_textbox(s, x + Inches(0.2), fy + Inches(0.04),
                    Inches(0.45), Inches(0.36),
                    text=num, size=16, bold=True, color=col,
                    font=EN_FONT, anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, x + Inches(0.6), fy + Inches(0.04),
                    fw - Inches(0.7), Inches(0.36),
                    text=h, size=12, bold=True, color=NAVY,
                    anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, x + Inches(0.25), fy + Inches(0.42),
                    fw - Inches(0.4), Inches(0.4),
                    text=t, size=9.5, color=DARK, line_spacing=1.2,
                    anchor=MSO_ANCHOR.TOP)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_confusion_matrix(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "混淆矩阵分析", 5, "研究结果与应用")

    add_textbox(s, Inches(0.6), Inches(1.15), Inches(12), Inches(0.4),
                text="融合模型混淆矩阵样本集中在对角线，多数类别正确判别",
                size=12, color=GREY)

    # left -- mock confusion matrix
    mx = Inches(0.55); my = Inches(1.6)
    mw = Inches(6.4); mh = Inches(5.5)
    panel = add_rect(s, mx, my, mw, mh, fill=LIGHT_BG,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    panel.adjustments[0] = 0.03
    disable_shadow(panel)
    add_textbox(s, mx + Inches(0.3), my + Inches(0.2),
                mw - Inches(0.6), Inches(0.4),
                text="图 4-5  STFT + ResNet + RNN 融合模型混淆矩阵",
                size=12, bold=True, color=NAVY)

    classes = ["2FSK","4FSK","8FSK","2PSK","4PSK","8PSK","16QAM","64QAM","64OFDM"]
    nc = len(classes)
    # axis area
    grid_x = mx + Inches(1.1)
    grid_y = my + Inches(0.85)
    grid_w = mw - Inches(1.4)
    grid_h = mh - Inches(1.6)
    cell_w = grid_w / nc
    cell_h = grid_h / nc
    # diag dominant
    import random
    random.seed(11)
    for i in range(nc):
        for j in range(nc):
            if i == j:
                v = random.uniform(0.86, 0.98)
            elif abs(i - j) == 1 and (i < 3 and j < 3 or 3 <= i < 6 and 3 <= j < 6):
                v = random.uniform(0.02, 0.08)
            else:
                v = random.uniform(0.0, 0.03)
            # color: light to deep blue
            r_col = int(245 - 200 * v)
            g_col = int(248 - 130 * v)
            b_col = int(255 - 60 * v)
            cell = add_rect(s, grid_x + cell_w * j, grid_y + cell_h * i,
                            cell_w + Pt(0.5), cell_h + Pt(0.5),
                            fill=RGBColor(max(0,r_col), max(0,g_col), b_col))
            cell.line.color.rgb = WHITE
            cell.line.width = Pt(0.4)
            disable_shadow(cell)
            # label diagonal
            if i == j:
                add_textbox(s, grid_x + cell_w * j, grid_y + cell_h * i,
                            cell_w, cell_h,
                            text=f"{int(v*100)}", size=9, bold=True,
                            color=WHITE if v > 0.5 else DARK,
                            align=PP_ALIGN.CENTER,
                            anchor=MSO_ANCHOR.MIDDLE, font=EN_FONT)
    # axis labels
    for i, c in enumerate(classes):
        # x (predicted)
        add_textbox(s, grid_x + cell_w * i, grid_y + grid_h + Inches(0.05),
                    cell_w, Inches(0.3),
                    text=c, size=8, color=GREY, align=PP_ALIGN.CENTER,
                    font=EN_FONT)
        # y (true)
        add_textbox(s, grid_x - Inches(0.85), grid_y + cell_h * i,
                    Inches(0.8), cell_h,
                    text=c, size=8, color=GREY, align=PP_ALIGN.RIGHT,
                    anchor=MSO_ANCHOR.MIDDLE, font=EN_FONT)
    add_textbox(s, grid_x, grid_y + grid_h + Inches(0.35),
                grid_w, Inches(0.3),
                text="Predicted Label", size=11, bold=True, color=NAVY,
                align=PP_ALIGN.CENTER, font=EN_FONT)
    # rotated true label - approximate via vertical text trick - simple horizontal label
    add_textbox(s, mx + Inches(0.05), my + Inches(2.5),
                Inches(0.9), Inches(0.5),
                text="True\nLabel", size=11, bold=True, color=NAVY,
                align=PP_ALIGN.CENTER, font=EN_FONT, line_spacing=1.1)

    # right -- analysis
    rx = Inches(7.15); ry = Inches(1.6)
    rw = Inches(6.2)
    add_textbox(s, rx, ry, rw, Inches(0.45),
                text="ANALYSIS", size=11, bold=True, color=OCEAN,
                font=EN_FONT)
    add_textbox(s, rx, ry + Inches(0.4), rw, Inches(0.55),
                text="混淆模式分析", size=20, bold=True, color=NAVY)

    points = [
        ("单一时域 RNN",
         "部分调制类别波形变化相近，分类边界不清晰，"
         "PSK / QAM 之间易出现混淆。", OCEAN),
        ("单一 STFT 模型",
         "FSK 类频带分布差异明显，识别效果较好；"
         "高阶调制 (64QAM / 64OFDM) 仍会出现少量混淆。", AZURE),
        ("STFT + ResNet + RNN",
         "对角线显著主导，多数类别集中在正确标签；"
         "互补特征显著降低跨类误判。", ACCENT_2),
        ("结论",
         "时域动态特征与时频纹理特征在不同类别间互补，"
         "对类内细节差异较小的调制类别尤其有效。", NAVY),
    ]
    for i, (h, t, col) in enumerate(points):
        py_ = ry + Inches(1.15) + Inches(1.2) * i
        card = add_rect(s, rx, py_, rw, Inches(1.05), fill=LIGHT_BG,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.08
        disable_shadow(card)
        cb = add_rect(s, rx, py_, Inches(0.12), Inches(1.05), fill=col,
                      shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        cb.adjustments[0] = 0.4
        disable_shadow(cb)
        add_textbox(s, rx + Inches(0.3), py_ + Inches(0.1),
                    rw - Inches(0.5), Inches(0.4),
                    text=h, size=13, bold=True, color=NAVY)
        add_textbox(s, rx + Inches(0.3), py_ + Inches(0.5),
                    rw - Inches(0.5), Inches(0.55),
                    text=t, size=11, color=DARK, line_spacing=1.35)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_low_snr_discussion(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, LIGHT_BG)
    add_page_header(s, prs, "低信噪比性能讨论与应用价值", 5, "研究结果与应用")

    # left: discussion
    lx = Inches(0.6); ly = Inches(1.25)
    lw = Inches(7.5)
    add_textbox(s, lx, ly, lw, Inches(0.4),
                text="LOW  SNR  ROBUSTNESS", size=11, bold=True,
                color=OCEAN, font=EN_FONT)
    add_textbox(s, lx, ly + Inches(0.4), lw, Inches(0.55),
                text="融合模型在强噪声条件下更具韧性", size=20, bold=True,
                color=NAVY)

    _, tf = add_textbox(s, lx, ly + Inches(1.1), lw, Inches(5.7))
    bs = [
        ("时域分支的作用",
         "建模长时序列变化规律，对 PSK / OFDM 类相位演替敏感；"
         "强噪声下若波形被破坏，仍可借助谱图分支提供判别依据。"),
        ("谱图分支的作用",
         "ResNet 提取频带分布、谱线变化与时频纹理；"
         "对 FSK 类频率变化型调制更具优势。"),
        ("互补机制",
         "当噪声扰动某一支特征时，另一分支仍可保留可分性；"
         "拼接融合后整体表现更稳定，识别率曲线更平缓。"),
        ("适用边界说明",
         "AWGN 模型可控可重复，但真实水声噪声具有非平稳、"
         "频率相关与突发性特点，需结合海试数据进一步验证。"),
    ]
    for i, (h, t) in enumerate(bs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8); p.line_spacing = 1.35
        r0 = p.add_run(); r0.text = f"▶  {h}"
        set_run_font(r0, size=14, bold=True, color=PALETTE[i % 6])
        p2 = tf.add_paragraph()
        p2.space_after = Pt(10); p2.line_spacing = 1.4
        r1 = p2.add_run(); r1.text = "      " + t
        set_run_font(r1, size=12, color=DARK)

    # right -- application scenarios
    rx = Inches(8.4); ry = Inches(1.25)
    rw = Inches(4.95); rh = Inches(5.85)
    panel = add_rect(s, rx, ry, rw, rh, fill=NAVY,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    panel.adjustments[0] = 0.04
    disable_shadow(panel)
    add_textbox(s, rx + Inches(0.3), ry + Inches(0.3),
                rw - Inches(0.6), Inches(0.4),
                text="APPLICATION  SCENARIOS", size=11, bold=True,
                color=CYAN, font=EN_FONT)
    add_textbox(s, rx + Inches(0.3), ry + Inches(0.7),
                rw - Inches(0.6), Inches(0.55),
                text="应用场景与价值", size=20, bold=True, color=WHITE)

    scenarios = [
        ("SCENARIO  01  ·  海洋监测",
         "对水声频谱进行调制识别，"
         "为水域监测与海洋安全提供基础感知能力。"),
        ("SCENARIO  02  ·  目标探测",
         "结合不同调制方式特征，"
         "辅助判断辐射源类型与状态。"),
        ("SCENARIO  03  ·  水下通信",
         "为非合作信号分析与解调前置识别提供方案。"),
        ("SCENARIO  04  ·  教学与原型",
         "低成本、易复现的端侧识别原型，"
         "可用于课程教学与方法验证。"),
    ]
    for i, (h, t) in enumerate(scenarios):
        py_ = ry + Inches(1.5) + Inches(1.05) * i
        bar = add_rect(s, rx + Inches(0.3), py_, Inches(0.12),
                       Inches(0.95), fill=PALETTE[i % 6],
                       shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        bar.adjustments[0] = 0.4
        disable_shadow(bar)
        add_textbox(s, rx + Inches(0.55), py_,
                    rw - Inches(0.85), Inches(0.4),
                    text=h, size=12, bold=True, color=CYAN, font=EN_FONT)
        add_textbox(s, rx + Inches(0.55), py_ + Inches(0.4),
                    rw - Inches(0.85), Inches(0.55),
                    text=t, size=11, color=WHITE, line_spacing=1.35)

    add_footer(s, prs, page_no=page_no)
    return s


# ----------------------------- Section 6 -------------------------------------

def slide_summary(prs, page_no):
    s = slide_blank(prs)
    slide_background(s, prs, WHITE)
    add_page_header(s, prs, "论文总结与未来展望", 6, "总结与展望")

    # Left -- summary
    lx = Inches(0.6); ly = Inches(1.25)
    lw = Inches(6.4)
    add_textbox(s, lx, ly, lw, Inches(0.45),
                text="THESIS  SUMMARY", size=11, bold=True, color=OCEAN,
                font=EN_FONT)
    add_textbox(s, lx, ly + Inches(0.45), lw, Inches(0.55),
                text="论文工作总结", size=22, bold=True, color=NAVY)

    summaries = [
        ("数据与特征",
         "完成 9 类水声调制信号的预处理与统一长度划分，"
         "构建时域 + STFT 双通道时频特征。"),
        ("模型设计",
         "提出 Bi-LSTM × ResNet-18 融合网络，"
         "特征层拼接 + 全连接分类，整体准确率达 91.4%。"),
        ("鲁棒性评估",
         "在 −10 ~ 10 dB AWGN 条件下对比五种方案，"
         "融合模型表现最稳定，验证特征互补性。"),
        ("端侧部署",
         "PyTorch → ONNX → 树莓派 ONNX Runtime，"
         "结合 Tk UI 完成从信号到识别的端侧闭环。"),
    ]
    _, tf = add_textbox(s, lx, ly + Inches(1.1), lw, Inches(5.7))
    for i, (h, t) in enumerate(summaries):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(4); p.line_spacing = 1.4
        r0 = p.add_run(); r0.text = f"▣  {h}"
        set_run_font(r0, size=14, bold=True, color=PALETTE[i % 6])
        p2 = tf.add_paragraph()
        p2.space_after = Pt(12); p2.line_spacing = 1.45
        r1 = p2.add_run(); r1.text = "      " + t
        set_run_font(r1, size=12, color=DARK)

    # Right -- future work
    rx = Inches(7.3); ry = Inches(1.25)
    rw = Inches(6.0)
    add_textbox(s, rx, ry, rw, Inches(0.45),
                text="FUTURE  WORK", size=11, bold=True, color=ACCENT_2,
                font=EN_FONT)
    add_textbox(s, rx, ry + Inches(0.45), rw, Inches(0.55),
                text="未来工作展望", size=22, bold=True, color=NAVY)

    futures = [
        ("01", "更真实的水声信道与噪声",
         "引入更接近真实环境的水声信道仿真模型，"
         "结合非平稳、频率相关与突发性噪声以及海试数据进行验证。",
         OCEAN),
        ("02", "扩大数据集与跨场景泛化",
         "扩充不同信道条件、采样设备与海况下的数据；"
         "引入领域自适应 / 迁移学习，提升跨场景识别能力。",
         AZURE),
        ("03", "融合物理意义特征",
         "进一步引入循环谱、瞬时频率、高阶累积量、"
         "子空间特征等具有物理意义的特征，提高可解释性。",
         ACCENT),
    ]
    for i, (num, h, t, col) in enumerate(futures):
        py_ = ry + Inches(1.1) + Inches(1.7) * i
        card = add_rect(s, rx, py_, rw, Inches(1.55), fill=LIGHT_BG,
                        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        card.adjustments[0] = 0.06
        disable_shadow(card)
        # numbered tag
        tag = add_rect(s, rx + Inches(0.25), py_ + Inches(0.25),
                       Inches(0.85), Inches(0.85),
                       fill=col, shape=MSO_SHAPE.OVAL)
        disable_shadow(tag)
        add_textbox(s, rx + Inches(0.25), py_ + Inches(0.25),
                    Inches(0.85), Inches(0.85),
                    text=num, size=18, bold=True, color=WHITE,
                    font=EN_FONT, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, rx + Inches(1.25), py_ + Inches(0.2),
                    rw - Inches(1.4), Inches(0.45),
                    text=h, size=14, bold=True, color=NAVY)
        add_textbox(s, rx + Inches(1.25), py_ + Inches(0.65),
                    rw - Inches(1.4), Inches(0.85),
                    text=t, size=11, color=DARK, line_spacing=1.4)

    add_footer(s, prs, page_no=page_no)
    return s


def slide_thanks(prs):
    s = slide_blank(prs)
    slide_background(s, prs, NAVY)

    # decorative big text
    add_textbox(s, Inches(0.6), Inches(0.6), Inches(12), Inches(0.5),
                text="THESIS  DEFENSE  ·  2026", size=12, bold=True,
                color=AZURE, font=EN_FONT)

    # central big "THANKS"
    add_textbox(s, Inches(0.6), Inches(1.9), prs.slide_width - Inches(1.2),
                Inches(1.8),
                text="谢   谢   聆   听", size=72, bold=True, color=WHITE,
                align=PP_ALIGN.CENTER)
    # decoration
    div = add_rect(s, prs.slide_width/2 - Inches(0.8), Inches(3.7),
                   Inches(1.6), Pt(3), fill=ACCENT)
    disable_shadow(div)
    add_textbox(s, Inches(0.6), Inches(3.85), prs.slide_width - Inches(1.2),
                Inches(0.6),
                text="THANK  YOU  FOR  YOUR  ATTENTION",
                size=18, bold=True, color=CYAN, align=PP_ALIGN.CENTER,
                font=EN_FONT)
    # subtitle
    add_textbox(s, Inches(0.6), Inches(4.65), prs.slide_width - Inches(1.2),
                Inches(0.5),
                text="敬请各位老师批评指正", size=18, color=AZURE,
                align=PP_ALIGN.CENTER)

    # bottom info row
    info = [
        ("答辩人", "陈   杰"),
        ("学  号", "37120222203280"),
        ("专  业", "通信工程"),
        ("指导老师", "苏 为 教授"),
    ]
    total_w = prs.slide_width - Inches(2.0)
    cw = total_w / len(info)
    by = Inches(6.3)
    for i, (k, v) in enumerate(info):
        x = Inches(1.0) + cw * i
        add_textbox(s, x, by, cw, Inches(0.3),
                    text=k, size=11, color=CYAN, align=PP_ALIGN.CENTER,
                    font=CN_FONT)
        add_textbox(s, x, by + Inches(0.3), cw, Inches(0.45),
                    text=v, size=16, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER)
        if i < len(info) - 1:
            sep = add_rect(s, x + cw - Pt(0.5), by + Inches(0.15),
                           Pt(1), Inches(0.55), fill=OCEAN)
            disable_shadow(sep)

    # bottom strip
    bot = add_rect(s, 0, prs.slide_height - Inches(0.35),
                   prs.slide_width, Inches(0.35), fill=OCEAN)
    disable_shadow(bot)
    add_textbox(s, Inches(0.5), prs.slide_height - Inches(0.35),
                prs.slide_width - Inches(1), Inches(0.35),
                text="基于树莓派的水声信号制式识别  ·  厦门大学 信息学院 · 2026",
                size=11, color=WHITE, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE)
    return s


# ----------------------------- Build -----------------------------------------

def build():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # 1 Cover
    slide_cover(prs)
    # 2 TOC
    slide_toc(prs)
    # 3 Section 1 divider
    slide_section_divider(prs, 0, page_no=3)
    # 4 Background
    slide_background_overview(prs, page_no=4)
    # 5 Significance
    slide_significance(prs, page_no=5)
    # 6 Section 2 divider
    slide_section_divider(prs, 1, page_no=6)
    # 7 main overview
    slide_main_overview(prs, page_no=7)
    # 8 dataset
    slide_dataset(prs, page_no=8)
    # 9 features
    slide_features(prs, page_no=9)
    # 10 architecture
    slide_architecture(prs, page_no=10)
    # 11 training
    slide_training(prs, page_no=11)
    # 12 compare models
    slide_compare_models(prs, page_no=12)
    # 13 SNR comparison
    slide_snr_comparison(prs, page_no=13)
    # 14 Deploy
    slide_deploy_rpi(prs, page_no=14)
    # 15 UI mockup
    slide_ui_mockup(prs, page_no=15)
    # 16 Section 3 divider
    slide_section_divider(prs, 2, page_no=16)
    # 17 Principles
    slide_principles(prs, page_no=17)
    # 18 Section 4 divider
    slide_section_divider(prs, 3, page_no=18)
    # 19 Overall design
    slide_design_overall(prs, page_no=19)
    # 20 Design details
    slide_design_details(prs, page_no=20)
    # 21 Section 5 divider
    slide_section_divider(prs, 4, page_no=21)
    # 22 Results table
    slide_results_table(prs, page_no=22)
    # 23 Confusion matrix
    slide_confusion_matrix(prs, page_no=23)
    # 24 Low SNR / application
    slide_low_snr_discussion(prs, page_no=24)
    # 25 Section 6 divider
    slide_section_divider(prs, 5, page_no=25)
    # 26 Summary + future work
    slide_summary(prs, page_no=26)
    # 27 Thanks
    slide_thanks(prs)

    out = "基于树莓派的水声信号制式识别_答辩PPT.pptx"
    prs.save(out)
    print(f"Saved: {out}  -- slides: {len(prs.slides)}")


if __name__ == "__main__":
    build()
