import spotipy as sp
from spotipy import SpotifyOAuth
from json import dumps

# get    - is a method   subroutine
# return - is a function subroutine

class App:
    def __init__(self, client_id:str, client_secret:str):
        
        self.client_id:     str = client_id
        self.client_secret: str = client_secret
        self.redirect_url:  str = "https://localhost:8888/callback"
        self.scope:         str = "playlist-read-private playlist-read-collaborative user-library-read"
        
        self.ctx:          sp.Spotify   = None
        self.auth_manager: SpotifyOAuth = None

        self.playlists:              list = [] # [ {Name, id, url} ]
        self.max_playlist_name_size: int  = 0


    def load_spotify(self):
        """Spotify boilerplate"""

        # Load the spotify auth manager
        self.auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_url,
            scope=self.scope
        )
        
        # Load the spotify context
        self.ctx = sp.Spotify(
            auth_manager=self.auth_manager
        )

        self.get_user_playlists_basic()


    def get_user_playlists_basic(self):
        """Gets a list of playlist names binding to the user account"""

        data: dict = self.ctx.current_user_playlists()

        playlists: list = []
        for i in data["items"]:
            playlist_type: str = i["type"]

            # Accept only if it is a playlist
            if playlist_type != "playlist": continue

            playlist_name: str = i["name"]
            # playlist_url:  str = i["external_urls"]["url"]
            playlist_url:  str = ""
            playlist_id:   str = i["id"]
        
            playlists.append({"name": playlist_name, "url": playlist_url, "id": playlist_id})

        self.playlists = playlists


    def return_user_playlist_tracks(self, playlist_id:str):
        """Return the tracks included in a playlist"""

        tracks: list = []
        for track in self.ctx.playlist_tracks(playlist_id=playlist_id)["items"]:
            track_name:    str  = track["track"]["name"]
            track_artists: list = [artist["name"] for artist in track["track"]["artists"]]
            
            tracks.append({"name": track_name, "artists": track_artists})
        
        return tracks

    def return_user_playlists_names(self):
        """Returns a list of names of the user's playlists"""

        return [i["name"] for i in self.playlists]

    def display_user_playlists(self):
        max_char_count: int  = App.return_max_playlist_name_size(playlists=self.playlists)

        print("==================================")
        print(" Here is a list of your playlists")
        print("_" * 200)
        print("INDEX" + " " * 5 + "NAME" + " " * (max_char_count - 9) + "ID" + " " * 21 + "URL")
        print("_" * 200)
        for i,pla in enumerate(self.playlists):
            name: str = pla["name"]
            _id:  str = pla["id"]
            url:  str = pla["url"]
            print("[{}] ".format(i) + "{}".format(name) + " " * (App.return_whitespace_difference(highest=max_char_count, name=name) + 1) + "{}".format(_id) + " " * 21 + "{}".format(url))
        print("=" * 200)


    @staticmethod
    def return_max_playlist_name_size(playlists:list):
        """Returns the maximum char count of the names based on the playlists"""

        highest: int = 0
        for pla in playlists:
            highest = len(pla["name"]) if len(pla["name"]) > highest else highest
        
        return highest

    @staticmethod
    def return_whitespace_difference(highest:int, name:str):
        return highest - len(name)

    @staticmethod
    def convert_str_list_to_int_list(array:list):
        """Returns a list of converted string list to integer list"""
        
        new_array: list = []
        for e in array:
            try:
                new_array.append(int(e))
            except ValueError as e:
                pass

        return new_array
    
    @staticmethod
    def save_to_file(playlist_name:str, content:str):
        """I/O (Output) Write to file"""

        with open(rf"{playlist_name}.txt", "w") as f:
            f.write(dumps(content))
        


    def run(self):
        self.load_spotify()
        self.display_user_playlists()

        # Get user input
        indexes: list = input("Choose which playlists to jot (ie: '0 6 9 3 21 16'): ").split(" ")
        indexes = App.convert_str_list_to_int_list(array=indexes)

        # Get tracks
        for i in indexes:

            # Get the tracks
            playlist_name: str  = self.playlists[i]["name"]
            tracks:        list = self.return_user_playlist_tracks(playlist_id=self.playlists[i]["id"])
            
            content: dict = {
                "playlist_name":    playlist_name,
                "number_of_tracks": len(tracks),
                "tracks":           tracks
            }

            App.save_to_file(playlist_name=playlist_name, content=content)



if __name__ == "__main__":
    app: App = App(
        client_id=input("ClientID: "),
        client_secret=input("ClientSecret: ")
    )
    app.run()

