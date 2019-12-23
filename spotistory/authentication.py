import json
import toml
from flask import Flask, request, redirect, render_template
import requests
from urllib.parse import quote

# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.

app = Flask(__name__)


class authentication:

    def __init__(self, config, config_file):
        self.config = config
        self.config_file = config_file

        #  Client Keys
        self.CLIENT_ID = config["spotify"]["client_id"]
        self.CLIENT_SECRET = config["spotify"]["client_secret"]

        # Spotify URLS
        self.SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
        self.SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
        self.SPOTIFY_API_BASE_URL = "https://api.spotify.com"
        self.API_VERSION = "v1"
        self.SPOTIFY_API_URL = "{}/{}".format(self.SPOTIFY_API_BASE_URL, self.API_VERSION)

        # Server-side Parameters
        self.CLIENT_SIDE_URL = "http://127.0.0.1"
        self.PORT = 8080
        self.REDIRECT_URI = "{}:{}/callback/q".format(self.CLIENT_SIDE_URL, self.PORT)
        self.SCOPE = 'user-library-read user-read-recently-played playlist-modify-public playlist-modify-private'
        self.STATE = ""
        self.SHOW_DIALOG_bool = True
        self.SHOW_DIALOG_str = str(self.SHOW_DIALOG_bool).lower()

        self.auth_query_parameters = {
            "response_type": "code",
            "redirect_uri": self.REDIRECT_URI,
            "scope": self.SCOPE,
            "client_id": self.CLIENT_ID
        }
        self.application = None

    @app.route("/")
    def index(self):
        # Auth Step 1: Authorization
        url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in self.auth_query_parameters.items()])
        auth_url = "{}/?{}".format(self.SPOTIFY_AUTH_URL, url_args)
        return redirect(auth_url)

    @app.route("/callback/q")
    def callback(self):
        # Auth Step 4: Requests refresh and access tokens
        auth_token = request.args['code']
        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_token),
            "redirect_uri": self.REDIRECT_URI,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
        }
        post_request = requests.post(self.SPOTIFY_TOKEN_URL, data=code_payload)

        # Auth Step 5: Tokens are Returned to Application
        response_data = json.loads(post_request.text)
        self.config["spotify"]["access_token"] = response_data["access_token"]
        self.config["spotify"]["refresh_token"] = response_data["refresh_token"]
        self.config["spotify"]["expires_in"] = response_data["expires_in"]

        # Auth Step 6: Use the access token to access Spotify API
        authorization_header = {"Authorization": "Bearer {}".format(self.config["spotify"]["access_token"])}

        # Get profile data
        user_profile_api_endpoint = "{}/me".format(self.SPOTIFY_API_URL)
        profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
        profile_data = json.loads(profile_response.text)

        # Get user playlist data
        playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
        playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
        playlist_data = json.loads(playlists_response.text)

        # Combine profile and playlist data to display
        display_arr = [profile_data] + playlist_data["items"]
        return render_template("index.html", sorted_array=display_arr)

    def launch(self):
        app.run(debug=True, port=self.PORT)

    def synchronize(self):
        with open(self.config_file, 'w') as myfile:
            toml.dump(config, myfile)
