import spotipy 
from spotipy.oauth2 import SpotifyOAuth

from bs4 import BeautifulSoup
import requests
client_id1="c67a13e3a6324e5b8b26f581e183febd"
client_secret1="0060be8a15e848b3906f6a9a471588be"

date = input("Input date in format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in song_names_spans]



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id1,
        client_secret=client_secret1,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")






playlist = sp.user_playlist_create(user=sp.current_user()['id'],
                                             name=f'{date} Billboard 999',
                                             public=False,
                                             collaborative=False,
                                             description=f'{date} Billboard 9999')



sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris,position=None)