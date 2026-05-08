from src.fetcher import get_lyrics, get_album_art
from src.analyzer import analyze_lyrics, export_to_csv
from src.visualizer import plot_mood_arc

song_title = input("Song title: ")
artist_name = input("Artist name: ")

print(f"\nFetching lyrics for '{song_title}' by {artist_name}...\n")

raw_lyrics = get_lyrics(song_title, artist_name)
art_path= get_album_art(song_title, artist_name)

if raw_lyrics is None:
    print("Couldn't find that song. Check the spelling and try again.")
else:
    print("Lyrics fetched. Analyzing mood...\n")
    
    song = analyze_lyrics(song_title, artist_name, raw_lyrics)
    
    print(f"Analysis complete — {len(song.lines)} lines analyzed.\n")
    
    for line in song.lines:
        print(f"[{line.section}] {line.text[:50]} | compound: {line.compound}")
    
    export_to_csv(song)
    plot_mood_arc(song, art_path)