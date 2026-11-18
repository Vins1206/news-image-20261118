#!/usr/bin/env python3
"""news-image-20261118 -- one image summing up world news, Wed 18 Nov 2026.

Pure Python 3.13 stdlib. Draws a 1024x1024 newspaper front page with a
hand-built 5x7 bitmap font and a hand-built PNG encoder (zlib + struct),
then writes it deterministically to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png outside the grader).

Stories (all reported 18 Nov 2026, checked against public news that day):
  1. War of the bridges: Ukraine collapses the Kerch road arch; Russia
     strikes Kyiv's two Dnipro bridges.
  2. Manila: Trump meets Marcos today after the first Quad leaders'
     meeting in two years; next stop Shenzhen for APEC and planned
     Trump-Xi-Putin talks on Thursday.
  3. Bahrain: Iran claims its drones hit a US radar; Bahrain and the
     US say the drones were intercepted, with no damage.
  4. London: Britain sanctions Israeli settlement firms to protect
     the two-state solution.
  5. Cyclone Akvan builds in the Bay of Bengal, set to turn severe
     by 19 November.
  6. Nvidia beats forecasts: $115.8bn revenue, up 103%; shares rise.
  Footer ticker: Dhoni retires from the IPL (CSK mentor), India win
  a 10th SAFF title 2-1 over Pakistan, Israel elects Matan Kahana
  as Knesset speaker.
"""
import os
import struct
import zlib

W, H = 1024, 1024

# --- palette ---------------------------------------------------------------
NAVY = (15, 42, 68)
NAVY2 = (23, 62, 96)
GOLD = (242, 183, 5)
PAPER = (247, 243, 232)
WHITE = (255, 255, 255)
INK = (18, 24, 32)
GREY = (90, 100, 112)
RED = (178, 34, 34)
TEAL = (0, 122, 110)
ORANGE = (214, 96, 0)
PURPLE = (98, 62, 150)
BLUE = (24, 90, 178)
GREEN = (28, 128, 60)
LIGHT = (232, 238, 244)

# --- 5x7 bitmap font --------------------------------------------------------
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.rect(x0 - t // 2, y0 - t // 2, t, t, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill:
                    if d2 <= r * r:
                        self.set(xx, yy, c)
                else:
                    if abs(d2 - r * r) <= r * 2:
                        self.set(xx, yy, c)

    def disc(self, cx, cy, r, c):
        self.circle(cx, cy, r, c, fill=True)

    def ring(self, cx, cy, r, c, t=3):
        for k in range(t):
            self.circle(cx, cy, r - k, c, fill=False)

    def text(self, x, y, s, c, msg):
        msg = msg.upper()
        cx = x
        for ch in msg:
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * s, y + row * s, s, s, c)
            cx += 6 * s
        return cx

    def text_w(self, s, msg):
        return len(msg) * 6 * s - s

    def centred(self, y, s, c, msg, x0=0, x1=None):
        x1 = self.w if x1 is None else x1
        w = self.text_w(s, msg)
        self.text(x0 + (x1 - x0 - w) // 2, y, s, c, msg)

    def wrap(self, x, y, maxw, s, c, msg, lh=None):
        lh = lh or (9 * s)
        words = msg.upper().split(" ")
        lines, cur = [], ""
        for wd in words:
            trial = (cur + " " + wd).strip()
            if self.text_w(s, trial) <= maxw or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, s, c, ln)
        return y + len(lines) * lh


def png_bytes(cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def draw_bridge(cv, x, y, w, h, deck_c, arch_c, gap=True):
    """A bridge deck with an arch; gap=True drops the middle span."""
    mid = x + w // 2
    cv.hline(x, y + h - 18, w, deck_c, 6)
    # arch: sampled half-ellipse
    pts = []
    for i in range(41):
        t = i / 40.0
        px = x + int(t * w)
        py = y + h - 18 - int(52 * (1 - (2 * t - 1) ** 2))
        pts.append((px, py))
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        if gap and mid - 36 < ax < mid + 36:
            continue
        cv.line(ax, ay, bx, by, arch_c, 5)
    # pillars
    cv.rect(x + 18, y + h - 18, 10, 18, deck_c)
    cv.rect(x + w - 28, y + h - 18, 10, 18, deck_c)
    if gap:
        # fallen span below the deck
        cv.line(mid - 24, y + h - 14, mid + 10, y + h + 2, deck_c, 5)
        cv.line(mid + 10, y + h + 2, mid + 30, y + h - 10, deck_c, 5)
    # one wave line under the bridge (kept clear of any label)
    for xx in range(x, x + w, 26):
        cv.hline(xx, y + h + 14, 16, (120, 170, 205), 3)


def draw_globe(cv, cx, cy, r):
    cv.disc(cx, cy, r, (38, 110, 160))
    cv.ring(cx, cy, r, NAVY, 4)
    cv.circle(cx, cy, r, NAVY, fill=False)
    # meridians / latitude
    for k in range(1, 4):
        cv.vline(cx - r + k * r // 2, cy - r + 8, 2 * r - 16, (140, 190, 225), 2)
    cv.hline(cx - r, cy, 2 * r, (140, 190, 225), 2)
    cv.hline(cx - r + 10, cy - r // 2, 2 * r - 20, (140, 190, 225), 2)
    cv.hline(cx - r + 10, cy + r // 2, 2 * r - 20, (140, 190, 225), 2)
    # land blobs
    cv.disc(cx - r // 3, cy - r // 4, r // 4, GREEN)
    cv.disc(cx + r // 3, cy + r // 5, r // 5, GREEN)


def draw_drone(cv, cx, cy):
    cv.rect(cx - 13, cy - 7, 26, 14, INK)
    cv.disc(cx - 24, cy - 13, 8, GREY)
    cv.disc(cx + 24, cy - 13, 8, GREY)
    cv.disc(cx - 24, cy + 13, 8, GREY)
    cv.disc(cx + 24, cy + 13, 8, GREY)
    cv.line(cx - 13, cy - 5, cx - 24, cy - 13, INK, 3)
    cv.line(cx + 13, cy - 5, cx + 24, cy - 13, INK, 3)
    cv.line(cx - 13, cy + 5, cx - 24, cy + 13, INK, 3)
    cv.line(cx + 13, cy + 5, cx + 24, cy + 13, INK, 3)
    cv.disc(cx, cy, 4, RED)
    # intercepted: red slash ring
    cv.ring(cx, cy, 37, RED, 4)
    cv.line(cx - 26, cy + 26, cx + 26, cy - 26, RED, 4)


def draw_stamp(cv, x, y, s=3):
    cv.rect(x, y, 84, 56, WHITE)
    cv.rect(x, y, 84, 56, RED)
    cv.rect(x + 4, y + 4, 76, 48, WHITE)
    cv.text(x + 10, y + 9, 2, RED, "BAN")
    cv.text(x + 10, y + 27, 2, RED, "FIRMS")
    cv.line(x + 8, y + 46, x + 76, y + 10, RED, 3)


def draw_storm(cv, cx, cy):
    for r, c in ((36, BLUE), (28, (90, 150, 210)), (20, (160, 200, 240)), (12, WHITE)):
        cv.ring(cx, cy, r, c, 5)
    cv.disc(cx, cy, 7, BLUE)
    # rain
    for dx, dy in ((-42, 26), (-30, 38), (36, 30), (44, 40), (0, 44)):
        cv.line(cx + dx, cy + dy, cx + dx - 5, cy + dy + 10, BLUE, 3)


def draw_chip(cv, x, y):
    cv.rect(x, y, 64, 64, INK)
    cv.rect(x + 8, y + 8, 48, 48, GREEN)
    cv.rect(x + 20, y + 20, 24, 24, GOLD)
    for k in range(4):
        cv.hline(x - 10, y + 11 + k * 13, 10, GOLD, 3)
        cv.hline(x + 64, y + 11 + k * 13, 10, GOLD, 3)
        cv.vline(x + 11 + k * 13, y - 10, 10, GOLD, 3)
        cv.vline(x + 11 + k * 13, y + 64, 10, GOLD, 3)
    # rising arrow
    cv.line(x + 78, y + 52, x + 78, y + 14, GREEN, 4)
    cv.line(x + 78, y + 14, x + 68, y + 26, GREEN, 4)
    cv.line(x + 78, y + 14, x + 88, y + 26, GREEN, 4)


def card(cv, x, y, w, h, accent, kicker, title, body, icon):
    cv.rect(x, y, w, h, WHITE)
    cv.rect(x, y, w, 8, accent)
    cv.rect(x, y, 3, h, accent)
    cv.text(x + 16, y + 20, 2, accent, kicker)
    cv.wrap(x + 16, y + 46, w - 32, 3, INK, title, lh=26)
    cv.wrap(x + 16, y + 46 + 52, w - 32, 2, GREY, body, lh=17)
    icon(x + w - 108, y + h - 96)


def main():
    cv = Canvas(W, H, PAPER)

    # ---- masthead ---------------------------------------------------------
    cv.rect(0, 0, W, 132, NAVY)
    cv.rect(0, 126, W, 6, GOLD)
    cv.centred(16, 6, GOLD, "THE WORLD IN ONE DAY", 0, W)
    cv.centred(58, 4, WHITE, "WEDNESDAY 18 NOVEMBER 2026", 0, W)
    cv.centred(96, 2, (180, 200, 220), "SIX STORIES THAT DEFINED THE DAY  -  READ IT IN ONE LOOK", 0, W)

    # ---- lead: war of the bridges ----------------------------------------
    lx, ly, lw, lh = 24, 148, 976, 238
    cv.rect(lx, ly, lw, lh, WHITE)
    cv.rect(lx, ly, lw, 8, RED)
    cv.text(lx + 20, ly + 22, 2, RED, "LEAD  -  UKRAINE / RUSSIA")
    cv.wrap(lx + 20, ly + 48, 560, 5, INK, "WAR OF THE BRIDGES", lh=44)
    cv.wrap(lx + 20, ly + 100, 560, 3, INK,
            "UKRAINE COLLAPSES THE KERCH ROAD ARCH.", lh=26)
    cv.wrap(lx + 20, ly + 152, 560, 2, GREY,
            "RUSSIA HITS KYIV'S TWO DNIPRO BRIDGES IN REPLY. TRAFFIC HALTED ON BOTH SIDES.",
            lh=17)
    draw_bridge(cv, lx + 620, ly + 30, 320, 110, NAVY, RED, gap=True)
    cv.text(lx + 620, ly + 196, 2, GREY, "KERCH  -  KYIV, OVERNIGHT")

    # ---- six-story grid ----------------------------------------------------
    gx, gy = 24, 402
    cw, ch, gap = 318, 272, 11
    cards = [
        (TEAL, "MANILA  -  ASIA",
         "TRUMP IN MANILA",
         "QUAD MEETS AFTER TWO YEARS. MARCOS TALKS TODAY, THEN SHENZHEN.",
         lambda x, y: draw_globe(cv, x + 46, y + 40, 34)),
        (ORANGE, "GULF  -  BAHRAIN",
         "DRONES OVER BAHRAIN",
         "IRAN CLAIMS A US RADAR HIT. US AND BAHRAIN SAY DRONES INTERCEPTED.",
         lambda x, y: draw_drone(cv, x + 46, y + 40)),
        (PURPLE, "LONDON",
         "UK SANCTIONS SETTLEMENTS",
         "BRITAIN SANCTIONS ISRAELI SETTLEMENT FIRMS TO PROTECT TWO STATES.",
         lambda x, y: draw_stamp(cv, x + 8, y + 10)),
        (BLUE, "WEATHER  -  BAY OF BENGAL",
         "CYCLONE AKVAN BUILDS",
         "BAY OF BENGAL STORM SET TO TURN SEVERE BY 19 NOV. FLIGHTS CANCELLED.",
         lambda x, y: draw_storm(cv, x + 46, y + 40)),
        (GREEN, "MARKETS  -  AI",
         "NVIDIA BEATS FORECASTS",
         "REVENUE $115.8BN, UP 103% IN A YEAR. SHARES RISE AFTER HOURS.",
         lambda x, y: draw_chip(cv, x + 10, y + 4)),
        (RED, "ALSO TODAY",
         "DHONI BOWS OUT",
         "DHONI RETIRES FROM THE IPL, BECOMES CSK MENTOR. INDIA WIN SAFF 2-1.",
         lambda x, y: (cv.disc(x + 46, y + 40, 28, RED),
                       cv.disc(x + 46, y + 40, 28, RED),
                       cv.line(x + 26, y + 22, x + 34, y + 58, WHITE, 3),
                       cv.line(x + 58, y + 22, x + 66, y + 58, WHITE, 3))),
    ]
    for i, (accent, kicker, title, body, icon) in enumerate(cards):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + gap)
        card(cv, cx, cy, cw, ch, accent, kicker, title, body, icon)

    # ---- footer ticker ------------------------------------------------------
    fy = 962
    cv.rect(0, fy, W, 62, NAVY)
    cv.rect(0, fy, W, 4, GOLD)
    cv.text(24, fy + 16, 2, GOLD, "ALSO:")
    cv.text(24 + 78, fy + 16, 2, WHITE,
            "ISRAEL ELECTS KAHANA SPEAKER  -  CANADA-CHINA EXTEND TRADE DEALS.")
    cv.text(24, fy + 38, 2, (180, 200, 220),
            "REPORTED 18 NOV 2026  -  MANILA  -  KYIV  -  BAHRAIN  -  LONDON  -  BAY OF BENGAL")

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(png_bytes(cv))
    print(f"wrote {path} {W}x{H}")


if __name__ == "__main__":
    main()
