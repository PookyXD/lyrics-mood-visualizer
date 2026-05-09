from src.fetcher import get_lyrics, get_album_art
from src.analyzer import analyze_lyrics, export_to_csv
from src.visualizer import plot_mood_arc
from src.cli import (
    console, print_header, print_divider,
    fetch_spinner, analyze_spinner, visual_spinner,
    print_table, print_summary
)

print_header()
print_divider()

song_title  = input("Song title:  ")
artist_name = input("Artist name: ")

print_divider()

with fetch_spinner():
    raw_lyrics, real_title, real_artist = get_lyrics(song_title, artist_name)
    art_path = get_album_art(song_title, artist_name)

if raw_lyrics is None:
    console.print(f"\n[red3]Couldn't find that song. Check spelling and try again.[/]")
else:
    with analyze_spinner():
        song = analyze_lyrics(real_title, real_artist, raw_lyrics)

    print_divider()
    print_table(song)
    print_divider()

    with visual_spinner():
        export_to_csv(song)
        plot_mood_arc(song, art_path)
    
    print_divider()
    print_summary(song)
    print_divider()

    print_divider()