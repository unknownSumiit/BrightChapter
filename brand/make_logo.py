"""Bright Chapter Realty logo kit. Text is converted to outlines so it looks the same everywhere.
Fonts: Lora (OFL), Inter (OFL)."""
import os, re
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
TEAL, CHERRY, CREAM, INK, BUTTER = "#1b4d5c", "#c7832a", "#ffffff", "#1b2328", "#ffd28a"

lora = instantiateVariableFont(TTFont("/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"), {"wght": 700})
inter = TTFont("/usr/share/fonts/opentype/inter/Inter-Bold.otf")


class Font:
    def __init__(self, tt):
        self.gs, self.cmap, self.hmtx, self.upm = tt.getGlyphSet(), tt.getBestCmap(), tt["hmtx"], tt["head"].unitsPerEm

    def text(self, s, x, y, size, tracking=0.0):
        sc, pen, cx = size / self.upm, SVGPathPen(self.gs), x
        for ch in s:
            name = self.cmap[ord(ch)]
            self.gs[name].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y)))
            cx += self.hmtx[name][0] * sc + tracking * size
        return pen.getCommands(), cx - x - tracking * size


LORA, INTER = Font(lora), Font(inter)


def mark(card=CREAM, edge=TEAL, line=CHERRY, faint=TEAL, heart=CHERRY):
    """A house roof with a rising sun behind it: a bright new chapter."""
    rays = "".join(f'<path d="M{48 + 30*c:.1f} {52 - 30*s_:.1f} L{48 + 38*c:.1f} {52 - 38*s_:.1f}" stroke="{heart}" stroke-width="4.5" stroke-linecap="round"/>'
                   for c, s_ in [(-0.94, 0.34), (-0.64, 0.77), (0, 1), (0.64, 0.77), (0.94, 0.34)])
    return f'''
  {rays}
  <path d="M26 52 A22 22 0 0 1 70 52 Z" fill="{heart}"/>
  <path d="M10 66 L48 38 L86 66" fill="none" stroke="{edge}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M22 60 V88 H74 V60" fill="{card}" stroke="{edge}" stroke-width="6" stroke-linejoin="round"/>
  <rect x="41" y="70" width="14" height="18" rx="2" fill="{edge}"/>'''


def lockup(word=INK, small=CHERRY, card=CREAM, edge=TEAL):
    top_d, top_w = LORA.text("Bright Chapter", 106, 58, 40)
    main_d, main_w = INTER.text("REALTY", 109, 86, 17, tracking=0.5)
    W = int(106 + max(top_w, main_w) + 8)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 100" width="{W * 3}" height="300">'
            f'<g transform="translate(4 2)">{mark(card=card, edge=edge)}</g>'
            f'<path d="{top_d}" fill="{word}"/><path d="{main_d}" fill="{small}"/></svg>'), W


def icon(bg=CREAM, rx=22):
    back = f'<rect width="100" height="100" rx="{rx}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{back}<g transform="translate(1 3) scale(.98)">{mark()}</g></svg>'


logo, W = lockup()
open(os.path.join(OUT, "bright-chapter-realty-logo.svg"), "w").write(logo)
open(os.path.join(OUT, "bright-chapter-realty-logo-white.svg"), "w").write(lockup(word="#ffffff", small=BUTTER, card="#1a222c", edge="#7fc4d6")[0])
open(os.path.join(OUT, "bright-chapter-realty-icon.svg"), "w").write(icon())
open(os.path.join(OUT, "bright-chapter-realty-icon-square.svg"), "w").write(icon(rx=0))
print("width", W)
