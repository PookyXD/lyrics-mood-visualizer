import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

def get_lyrics(song_title, artist_name):
    token = os.getenv("GENIUS_TOKEN")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    search_url = "https://api.genius.com/search"
    params = {"q": f"{song_title} {artist_name}"}
    
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
    
    hits = data["response"]["hits"]
    
    if not hits:
        return None
    
    song_url = hits[0]["result"]["url"]
    
    return scrape_lyrics(song_url, headers)

def scrape_lyrics(url, headers):
    from bs4 import BeautifulSoup
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    containers = soup.find_all("div", attrs={"data-lyrics-container": "true"})
    
    if not containers:
        return None
    
    lyrics = ""
    for container in containers:
        for br in container.find_all("br"):
            br.replace_with("\n")
        lyrics += container.get_text() + "\n"
    
    lyrics = re.sub(r'^\d+\s*Contributor[s]?.*?Lyrics', '', lyrics, flags=re.DOTALL)
    lyrics = re.sub(r'\d+\s*Embed$', '', lyrics.strip())

    return lyrics.strip()

def get_album_art(song_title, artist_name):
    token = os.getenv("GENIUS_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}

    search_url = "https://api.genius.com/search"
    params = {"q": f"{song_title} {artist_name}"}
    
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
    
    hits = data["response"]["hits"]
    
    if not hits:
        return None
    
    image_url = hits[0]["result"]["song_art_image_url"]
    
    image_response = requests.get(image_url)
    
    if image_response.status_code == 200:
        os.makedirs("assets", exist_ok=True)
        art_path = "assets/album_art.jpg"
        with open(art_path, "wb") as f:
            f.write(image_response.content)
        return art_path
    
    return None