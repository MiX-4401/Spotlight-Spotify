import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
from json import dumps

client_id:     str = "00c64d2147594bf5a3f151afee1a0eb2"
client_secret: str = "fb9ec2fe81cd43c3a39446df48169fda"

repsonse_type: str = "code"
redirect_url: str = "https://localhost:8888/callback"
scope: str = "playlist-read-private playlist-read-collaborative user-library-read"

app: sp.Spotify = sp.Spotify(
    auth_manager=SpotifyOAuth(scope="playlist-read-private", client_id=client_id, client_secret=client_secret ,redirect_uri=redirect_url)
)

user_playlists: dict = {}
playlists:      dict = {}

user_playlists = app.current_user_playlists()

# Get basic playlist information
for pla in user_playlists["items"]:
    playlist_type: str = pla["type"]

    if playlist_type != "playlist": continue

    playlist_name:         str  = pla["name"]
    playlist_url: str  = pla["external_urls"]["spotify"]
    playlist_id:  str  = playlist_url.split("/")[-1]
    
    playlists[playlist_name]: dict = {"name": playlist_name, "type": playlist_type, "url": playlist_url, "id": playlist_id, "tracks":  {}}

# Get track information
for pla in playlists:

    track_information: dict = app.playlist_tracks(playlist_id=playlists[pla]["id"])

    tracks: dict = {}

    for track in track_information["items"]:
        track_name:     str  = track["track"]["name"]
        track_artists:  list = [art["name"] for art in track["track"]["artists"]]
        # track_url:      str  = track["track"]["external_urls"]["spotify"]
        track_url = ""
        track_id:       str  = track["track"]["id"]

        tracks[track_name]: dict = {"name": track_name, "artists": track_artists, "url": track_url, "id": track_id}

    playlists[pla]["tracks"] = tracks

# Store in file
with open("playlists.json", "w") as f:
    for pla in playlists:
        f.write(dumps(playlists))



