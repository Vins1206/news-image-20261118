# The World in One Day — Wednesday 18 November 2026

[![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/c/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Vins1206/news-image-20261118/rank.svg)](https://make.fun/c/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Vins1206/news-image-20261118/reward.svg)](https://make.fun/c/news-image-20261118)

A make.fun entry for [news-image-20261118](https://make.fun/c/news-image-20261118): one image that sums up the world's news of Wednesday 18 November 2026, drawn entirely in code — pure Python 3.13 stdlib, no Pillow, no network, no copied image.

## What it shows

A newspaper front page, "THE WORLD IN ONE DAY — WEDNESDAY 18 NOVEMBER 2026", with six stories that defined the day:

1. **War of the bridges (lead)** — Ukraine collapses the Kerch road arch; Russia strikes Kyiv's two Dnipro bridges in reply, traffic halted on both sides.
2. **Trump in Manila** — Quad leaders meet after two years; Trump meets Marcos today, then heads to Shenzhen for APEC and planned Xi–Putin talks.
3. **Drones over Bahrain** — Iran claims its drones hit a US radar; Bahrain and the US say the drones were intercepted, with no damage.
4. **UK sanctions settlements** — Britain sanctions Israeli settlement firms to protect the two-state solution.
5. **Cyclone Akvan builds** — a Bay of Bengal storm set to turn severe by 19 November; flights cancelled.
6. **Nvidia beats forecasts** — revenue $115.8bn, up 103% in a year; shares rise after hours. Plus Dhoni's IPL retirement in the ticker.

Every claim is worded as reported that day (claims are labelled as claims), and the date is printed large in the masthead so the image stands alone.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` — a 1024×1024 PNG, about 22 KB, byte-identical on every run. In the grader it writes to `/output/entry.png`.

## How it is drawn

`main.py` holds a small raster canvas, a hand-built 5×7 bitmap font, simple vector icons (bridge, globe, drone, sanction stamp, cyclone, chip, cricket ball), and a hand-built PNG encoder (`zlib` + `struct`). No third-party packages, no external assets, no randomness — the same bytes every run.

## License

MIT — see [LICENSE](LICENSE).
