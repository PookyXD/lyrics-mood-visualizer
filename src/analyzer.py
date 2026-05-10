import re
import csv
import os
from transformers import pipeline
from src.models import LyricLine, Song

print("Loading text-classification model...")
sentiment_pipeline = pipeline(
    "text-classification",
    model="models/emotions",
    top_k=1,
)
print("Model ready.")



EMOTION_SCORES = {
    "joy":      1.0,
    "surprise": 0.5,
    "neutral":  0.0,
    "fear":    -0.4,
    "sadness": -0.7,
    "disgust": -0.8,
    "anger":   -1.0,
}


def clean_lyrics(raw_lyrics):
    lines = raw_lyrics.split("\n")

    cleaned = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        cleaned.append(line)

    return cleaned


def extract_sections(cleaned_lines):
    sections = []
    current_section = "Intro"

    for line in cleaned_lines:
        if re.match(r'^\[.+\]$', line):
            current_section = line.strip("[]")
            continue
        sections.append((line, current_section))

    return sections


def score_to_compound(label, score):
    base = EMOTION_SCORES.get(label.lower(), 0.0)
    return round(base * score, 4)

def analyze_lyrics(song_title, artist_name, raw_lyrics):
    cleaned  = clean_lyrics(raw_lyrics)
    sections = extract_sections(cleaned)

    song = Song(song_title, artist_name)

    lines_text = [line for line, _ in sections]
    labels_sec = [sec  for _, sec  in sections]

    # run all lines through model in one batch
    results = sentiment_pipeline(
        lines_text,
        truncation=True,
        max_length=128,
        batch_size=16,
    )

    for i, result in enumerate(results):
        label    = result[0]["label"]
        score    = result[0]["score"]
        compound = score_to_compound(label, score)

        lyric_line = LyricLine(lines_text[i], labels_sec[i])
        lyric_line.emotion = label.lower()
        lyric_line.compound  = compound
        lyric_line.positive = score if label in ["joy", "surprise"] else 0.0
        lyric_line.negative = score if label in ["anger", "sadness", "disgust", "fear"] else 0.0
        lyric_line.neutral  = score if label == "neutral" else 0.0

        song.add_line(lyric_line)

    return song


def export_to_csv(song):
    os.makedirs("output", exist_ok=True)

    filename = f"output/{song.title}_{song.artist}.csv".replace(" ", "_")

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["line", "section", "positive",
                         "negative", "neutral", "compound"])

        for lyric_line in song.lines:
            writer.writerow([
                lyric_line.text,
                lyric_line.section,
                lyric_line.positive,
                lyric_line.negative,
                lyric_line.neutral,
                lyric_line.compound,
            ])

    print(f"\nCSV exported to {filename}")
    return filename