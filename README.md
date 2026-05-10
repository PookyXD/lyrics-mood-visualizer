# ✦ Lyrics Mood Visualizer

> Turn any song into a constellation of emotions.

![Python](https://img.shields.io/badge/Python-3.10+-gold?style=flat-square&logo=python)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-gold?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-gold?style=flat-square)
![Rich](https://img.shields.io/badge/Rich-CLI-gold?style=flat-square)

---

## What is this?

Lyrics Mood Visualizer fetches any song's lyrics automatically, runs every line through a state-of-the-art emotion detection model, and generates a unique **constellation map** — where each star represents a lyric line, sized by emotional intensity, connected across the song's emotional journey.

Every song produces a completely different constellation.

---

## Features

- **Automatic lyrics fetching** via Genius API — no copy pasting
- **Real emotion detection** using `j-hartmann/emotion-english-distilroberta-base` — detects joy, sadness, anger, fear, disgust, surprise and neutral per line
- **Constellation visualization** — each lyric line is a star, sized by emotional intensity, connected in sequence
- **Emotional Score** — a single -1.0 to +1.0 score summarizing the song's overall emotional weight
- **Most emotional line** — the peak moment of the song quoted at the bottom
- **CSV export** — full mood data exported per song for your own analysis
- **Beautiful CLI** — rich terminal output with spinners, color coded emotion table, and summary panel
- **Fully configurable** — `config.py` and `cli_config.py` let you tweak every visual and terminal detail without touching the core code

---

## How it works

Song title + artist
↓
Genius API → fetches lyrics automatically
↓
Hartmann Transformer → scores every line by emotion
↓
Constellation generator → maps emotion to stars
↓
PNG poster + CSV export

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/PookyXD/lyrics-mood-visualizer.git
cd lyrics-mood-visualizer
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# source venv/bin/activate    # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the emotion model

Download these files from:
**https://huggingface.co/j-hartmann/emotion-english-distilroberta-base/tree/main**

- `config.json`
- `tokenizer_config.json`
- `vocab.json`
- `merges.txt`
- `special_tokens_map.json`
- `pytorch_model.bin`

Place them all in `models/emotions/`

### 5. Get your Genius API key

- Go to **genius.com/api-clients**
- Create a new app
- Copy your Client Access Token

### 6. Create your `.env` file

GENIUS_TOKEN=your_token_here

### 7. Run it

```bash
python main.py
```

---

## Project Structure

lyrics-mood-visualizer/
├── main.py              ← entry point
├── config.py            ← visual configuration
├── cli_config.py        ← terminal configuration
├── requirements.txt
├── .env                 ← your Genius API key (never shared)
├── src/
│   ├── fetcher.py       ← Genius API + lyrics scraping
│   ├── analyzer.py      ← emotion detection pipeline
│   ├── visualizer.py    ← constellation generator
│   ├── models.py        ← Song and LyricLine classes
│   └── cli.py           ← rich terminal interface
├── models/
│   └── emotions/        ← local transformer model
├── assets/
│   └── frame.png        ← optional album art frame
└── output/              ← generated PNGs and CSVs

---

## Configuration

All visual settings live in `config.py` — star colors, sizes, background, canvas dimensions, DPI. All terminal settings live in `cli_config.py` — colors, spinner style, table styling, panel layout. Change anything there without touching core code.

---

## Built with

- [Genius API](https://genius.com/api-clients) — lyrics
- [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/) — lyrics scraping
- [Hartmann Emotion Model](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) — emotion detection
- [Matplotlib](https://matplotlib.org/) — constellation visualization
- [Pillow](https://pillow.readthedocs.io/) — image composition
- [Rich](https://rich.readthedocs.io/) — terminal interface

---

*Built as a portfolio project — Summer 2026*