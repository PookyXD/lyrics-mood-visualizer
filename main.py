from src.fetcher import get_lyrics

song = input("Song title: ")
artist = input("Artist name: ")

print(f"\nFetching lyrics for '{song}' by {artist}...\n")

lyrics = get_lyrics(song, artist)

if lyrics is None:
    print("Couldn't find that song. Check the spelling and try again.")
else:
    print(lyrics)