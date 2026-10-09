"""Text -> SVG path rendering with real shaping (HarfBuzz).

GitHub serves README images through a sandboxed proxy that blocks web fonts,
so every glyph is converted to vector outlines. Arabic is shaped (joining,
ligatures, harakat) and laid out right-to-left exactly as the font intends.
"""
from __future__ import annotations

import functools
import os

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")

FAMILIES = {"ar": "readex", "sans": "readex", "mono": "jb"}


@functools.lru_cache(maxsize=None)
def _load(name: str):
    path = os.path.join(FONT_DIR, f"{name}.ttf")
    with open(path, "rb") as fh:
        data = fh.read()
    face = hb.Face(data)
    font = hb.Font(face)
    tt = TTFont(path)
    return font, tt, tt.getGlyphSet(), tt["head"].unitsPerEm


def _font_name(family: str, weight: int) -> str:
    base = FAMILIES[family]
    avail = {"readex": [300, 400, 500, 700], "jb": [400, 500, 700]}[base]
    w = min(avail, key=lambda a: abs(a - weight))
    return f"{base}{w}"


def shape(text: str, family: str = "sans", weight: int = 400, size: float = 16,
          tracking: float = 0.0):
    """Return (list of (glyph_name, x_offset_px, y_offset_px), advance_px)."""
    name = _font_name(family, weight)
    font, tt, gs, upem = _load(name)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    rtl = buf.direction == "rtl"
    hb.shape(font, buf, {"kern": True, "liga": True})
    scale = size / upem
    order = tt.getGlyphOrder()
    out, x = [], 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        g = order[info.codepoint]
        out.append((g, (x + pos.x_offset) * scale, pos.y_offset * scale))
        x += pos.x_advance
        if not rtl and tracking:
            x += tracking / scale
    adv = x * scale
    if rtl and tracking:
        pass  # tracking breaks Arabic joining — never apply it
    return name, out, adv


def _n(v: float) -> str:
    r = round(v, 1)
    return str(int(r)) if r == int(r) else f"{r}"


def text_path(text: str, x: float, y: float, *, family: str = "sans", weight: int = 400,
              size: float = 16, anchor: str = "start", tracking: float = 0.0,
              fill: str | None = None, cls: str | None = None, extra: str = "") -> str:
    """Render text as a single <path>. y is the baseline. anchor: start|middle|end."""
    if not text:
        return ""
    name, glyphs, adv = shape(text, family, weight, size, tracking)
    _, _, gs, upem = _load(name)
    scale = size / upem
    if anchor == "middle":
        x0 = x - adv / 2
    elif anchor == "end":
        x0 = x - adv
    else:
        x0 = x
    pen = SVGPathPen(gs, ntos=_n)
    for g, gx, gy in glyphs:
        t = TransformPen(pen, (scale, 0, 0, -scale, x0 + gx, y - gy))
        gs[g].draw(t)
    d = pen.getCommands()
    attrs = []
    if cls:
        attrs.append(f'class="{cls}"')
    if fill:
        attrs.append(f'fill="{fill}"')
    if extra:
        attrs.append(extra)
    return f'<path {" ".join(attrs)} d="{d}"/>'


def width(text: str, family: str = "sans", weight: int = 400, size: float = 16,
          tracking: float = 0.0) -> float:
    if not text:
        return 0.0
    return shape(text, family, weight, size, tracking)[2]
