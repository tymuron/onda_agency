#!/usr/bin/env python3
"""Self-host the 4 Google font families as Latin-subset woff2.
Instances the variable fonts (drops unused weight ranges; keeps Fraunces opsz
so font-optical-sizing:auto still works), Latin-subsets, outputs 5 woff2 into
frontend/assets/fonts/. Re-run if the type system changes:  python3 scripts/build_fonts.py
Removes the render-blocking cross-origin fonts.googleapis.com round-trip and
fixes the latent DM Sans 600 faux-bold (variable weight range now covers it)."""
import os, urllib.request
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.subset import Subsetter, Options

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "frontend", "assets", "fonts")
TMP = "/tmp/onda-fontsrc"
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)

B = "https://raw.githubusercontent.com/google/fonts/main/ofl"
UNI = (list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) +
       [0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2026, 0x2022, 0x00B7, 0x20AC])

FONTS = [
    ("fraunces-var.woff2",            B + "/fraunces/Fraunces%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf",        {"SOFT": 0, "WONK": 0, "opsz": 144, "wght": (300, 400)}),
    ("fraunces-italic-var.woff2",     B + "/fraunces/Fraunces-Italic%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf", {"SOFT": 0, "WONK": 0, "opsz": 144, "wght": (300, 400)}),
    ("dmsans-var.woff2",              B + "/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",                            {"opsz": 14, "wght": (400, 700)}),
    ("jetbrains-mono-var.woff2",      B + "/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",                     {"wght": (400, 500)}),
    ("instrument-serif-italic.woff2", B + "/instrumentserif/InstrumentSerif-Italic.ttf",                   None),
]

def fetch(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return dst
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r, open(dst, "wb") as f:
        f.write(r.read())
    return dst

for out, url, axes in FONTS:
    src = fetch(url, os.path.join(TMP, out.replace(".woff2", ".ttf")))
    f = TTFont(src)
    if axes:
        instantiateVariableFont(f, axes, inplace=True)
    # fontTools subset chokes when gvar lacks an entry for a retained glyph
    # (blank glyphs like space/nbsp have no variation) -> pre-fill empty entries.
    if "gvar" in f:
        gv = f["gvar"]
        v = dict(gv.variations)
        for g in f.getGlyphOrder():
            v.setdefault(g, [])
        gv.variations = v
    opt = Options()
    opt.flavor = "woff2"
    opt.layout_features = ["*"]   # keep kerning / ligatures / contextual alts
    opt.name_IDs = ["*"]
    ss = Subsetter(options=opt)
    ss.populate(unicodes=UNI)
    ss.subset(f)
    f.flavor = "woff2"
    dst = os.path.join(OUT, out)
    f.save(dst)
    print("%-32s %4d KB" % (out, os.path.getsize(dst) // 1024))
print("-> " + OUT)
