import spotipy as sp
from spotipy import SpotifyOAuth
from json import loads

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

        self.playlists: dict = {}
        self.max_playlist_name_size: int = 0


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
        """Return a list of playlist names binding to the user account"""

        data: dict = self.ctx.current_user_playlists()

        playlists: dict = {}
        for pla in data["items"]:
            playlist_type: str = pla["type"]

            # Accept only if it is a playlist
            if playlist_type != "playlist": continue

            playlist_name: str = pla["name"]
            # playlist_url:  str = pla["external_urls"]["url"]
            playlist_url:  str = ""
            playlist_id:   str = pla["id"]
        
            playlists[playlist_name] = {"name": playlist_name, "url": playlist_url, "id": playlist_id}
        
        return playlists

    def get_user_playlist_tracks(playlist_name:str):
        pass

    def return_user_playlists_names(self):
        """Returns a list of names of the user's playlists"""

        return [pla["name"] for pla in self.playlists]

    def display_user_playlists(self):
        playlists:      dict = self.return_user_playlists_names()
        max_char_count: int  = App.return_max_playlist_name_size(playlists=playlists)

        print("==================================")
        print(" Here is a list of your playlists")
        print("_" * 200)
        print("INDEX" + " " * 5 + "NAME" + " " * (max_char_count - 9) + "ID" + " " * 21 + "URL")
        print("_" * 200)
        for i,pla in enumerate(playlists):
            print("[{}] ".format(i) + "{}".format(playlists[pla]["name"]) + " " * (App.return_whitespace_difference(highest=max_char_count, name=playlists[pla]["name"]) + 1) + "{}".format(playlists[pla]["id"]) + " " * 21 + "{}".format(playlists[pla]["url"]))
        print("=" * 200)


    @staticmethod
    def return_max_playlist_name_size(playlists:dict):
        """Returns the maximum char count of the names based on the playlists"""

        highest: int = 0
        for pla in playlists:
            highest = len(playlists[pla]["name"]) if len(playlists[pla]["name"]) > highest else highest
        
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
            except valueError as e:
                pass

        return new_array
        
    def run(self):
        self.load_spotify()
        self.display_user_playlists()

        # Get user input
        indexes: list = input("Choose which playlists to jot (ie: '0 6 9 3 21 16'): ").split(" ")
        indexes = App.convert_str_list_to_int_list(array=indexes)

        pass


if __name__ == "__main__":
    app: App = App(
        client_id="00c64d2147594bf5a3f151afee1a0eb2",
        client_secret="fb9ec2fe81cd43c3a39446df48169fda"
    )
    app.run()

