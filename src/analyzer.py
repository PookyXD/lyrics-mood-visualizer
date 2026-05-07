import re
import csv
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from src.models import LyricLine, Song

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

def analyze_lyrics(song_title, artist_name, raw_lyrics):
    sia = SentimentIntensityAnalyzer()

    cleaned = clean_lyrics(raw_lyrics)
    sections = extract_sections(cleaned)

    song = Song(song_title, artist_name)

    for line, section in sections:
        scores = sia.polarity_scores(line)

        lyric_line = LyricLine(line, section)
        lyric_line.positive = scores["pos"]
        lyric_line.negative = scores["neg"]
        lyric_line.neutral = scores["neu"]
        lyric_line.compound = scores["compound"]

        song.add_line(lyric_line)

    return song

def export_to_csv(song):
    os.makedirs("output", exist_ok=True)

    filename = f"output/{song.title}_{song.artist}.csv".replace(" ", "_")

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["line", "section", "positive", "negative", "neutral", "compound"])

        for lyric_line in song.lines:
            writer.writerow([
                lyric_line.text,
                lyric_line.section,
                lyric_line.positive,
                lyric_line.negative,
                lyric_line.neutral,
                lyric_line.compound
            ])
        
    print(f"\nCSV exported to {filename}")
    return filename
