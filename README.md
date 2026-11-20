# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/dftaufiq/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/dftaufiq/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026: a newspaper front page led by the ICJ's genocide ruling on Myanmar and the Trump–Xi–Putin peace declaration, with 16 verified stories across every region.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## About the image

`main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory. The image itself is drawn from scratch by `generate_image.py` (build-time only, needs Pillow) — no photographs or copied artwork. Every story on the page was checked against reporting of 20 November 2026 from Reuters, BBC, UN News, Euronews and the India Meteorological Department:

- The Hague: the ICJ holds Myanmar responsible for genocide against the Rohingya, 9–6 — the first such ruling against a state
- Shenzhen: the first US–China–Russia summit ends in a four-point joint peace declaration
- Odisha: Cyclone Akvan makes landfall near Gopalpur; 300,000+ evacuated
- Kyiv: Russia's mass missile strike; Ukraine hits the Kerch Bridge a third time in four days
- Markets: S&P 500 −2.0% for a fifth day, Nikkei −4.8%, while Anthropic's Nasdaq debut closes 17% up
- Plus Riyadh, Brussels, COP31 in Antalya, Gaza, Hormuz, the IMF, Meta, Türkiye and more

To redraw the image from its source data: `python3 generate_image.py`

---

<sub>Entered on [make.fun](https://make.fun/?ref=bqc0tvks&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
