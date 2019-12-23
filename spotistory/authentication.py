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

        # Spotify URL API
        self.spotify_api_base_url = "{}/{}".format(self.config["spotify"]["api_base_url"], self.config["spotify"]["api_version"])

        # Server-side Parameters
        self.config["spotify"]["redirect_uri"] = "{}:{}/callback/q".format(self.config["server"]["url"], self.config["server"]["port"])
        self.scope = 'user-library-read user-read-recently-played playlist-modify-public playlist-modify-private'

        self.auth_query_parameters = {
            "response_type": "code",
            "redirect_uri": self.config["spotify"]["redirect_uri"],
            "scope": self.scope,
            "client_id": self.config["spotify"]["client_id"]
        }
        self.application = None
        self.is_synchronized = False

    @app.route("/")
    def index(self):
        # Auth Step 1: Authorization
        url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in self.auth_query_parameters.items()])
        auth_url = "{}/?{}".format(self.config["spotify"]["auth_url"], url_args)
        return redirect(auth_url)

    @app.route("/callback/q")
    def callback(self):
        # Auth Step 4: Requests refresh and access tokens
        auth_token = request.args['code']
        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_token),
            "redirect_uri": self.config["spotify"]["redirect_uri"],
            'client_id': self.config["spotify"]["client_id"],
            'client_secret': self.config["spotify"]["client_secret"],
        }
        post_request = requests.post(self.config["spotify"]["token_url"], data=code_payload)

        # Auth Step 5: Tokens are Returned to Application
        response_data = json.loads(post_request.text)
        self.config["spotify"]["access_token"] = response_data["access_token"]
        self.config["spotify"]["refresh_token"] = response_data["refresh_token"]

        # Auth Step 6: Use the access token to access Spotify API
        authorization_header = {"Authorization": "Bearer {}".format(self.config["spotify"]["access_token"])}

        return render_template("index.html")

    def launch(self):
        app.run(debug=True, port=self.config["server"]["port"])
    
    def is_synchronized(self):
        return self.is_synchronized
    
    def stop_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @app.route("/synchro")
    def synchronize(self):
        with open(self.config_file, 'w') as myfile:
            toml.dump(self.config, myfile)
        self.is_synchronized = True
        return render_template("index.html")
