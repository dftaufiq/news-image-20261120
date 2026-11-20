# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/dftaufiq/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/dftaufiq/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026: a newspaper front page with 35 stories across 7 regions — 3 illustrated lead stories, 10 illustrated features, a numbered world map and 22 more briefs — every one of them dated to Friday 20 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## About the image

`main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory. The image itself is drawn from scratch by `generate_image.py` (build-time only, needs Pillow) — no photographs or copied artwork: every panel, chart and the dotted world map are drawn in code. Every story on the page was checked against reporting of 20 November 2026, with sources named beside each story:

- Kyiv: Russian missiles hit three bridges over the Dnipro in an overnight barrage of 110+ missiles and 400 drones
- Odisha: Cyclone Akvan comes ashore near Gopalpur; 300,000+ evacuated, no deaths reported
- Markets: the AI sell-off sinks Asia — Taiex −6.2% for its worst week since 1991, Nikkei −5.1%, SoftBank −14.5%
- Brussels: the UK and EU seal a "reset" deal — food trade, 100,000 youth visas a year, linked carbon markets
- Antalya: COP31 reaches its last day with no deal as the draft drops fossil fuels
- Plus a Russian missile landing in Poland, BepiColombo reaching Mercury, Italy's general strike, Japan's inflation, Riyadh, Gaza, Hormuz, Phillips' 118 — and 22 more briefs

The DATE CHECK box at the foot of the page names the big stories deliberately left out because they happened on Thursday 19 November (the ICJ's Myanmar ruling, the Shenzhen summit, Anthropic's Nasdaq debut, the GTA VI launch, California's Nvidia subpoena) — so the page shows Friday's news and nothing else.

To redraw the image from its source data: `python3 generate_image.py`

---

<sub>Entered on [make.fun](https://make.fun/?ref=bqc0tvks&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
